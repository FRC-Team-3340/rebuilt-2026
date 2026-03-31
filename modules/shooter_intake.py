import phoenix5
import rev
import wpilib
from wpilib import SmartDashboard
import modules.constants as constants


class ShooterIntake:
    def __init__(self):
        self._indexer  = phoenix5.WPI_TalonSRX(constants.INDEXER_ID)
        self._shuffler = phoenix5.WPI_TalonSRX(constants.SHUFFLER_ID)
        self._shooter  = phoenix5.WPI_TalonSRX(constants.SHOOTER_ID)

        self._intake = rev.SparkMax(constants.INTAKE_ID, rev.SparkMax.MotorType.kBrushless)
        
        self._indexer.setInverted(True)

        # Dashboard tunables
        SmartDashboard.putNumber("Shooter Speed",        constants.SHOOTER_SPEED)
        SmartDashboard.putNumber("Intake Speed",         constants.INTAKE_SPEED)
        SmartDashboard.putNumber("Reverse Intake Speed", constants.REVERSE_INTAKE_SPEED)
        SmartDashboard.putNumber("Reverse Shooter Speed",constants.REVERSE_INTAKE_SHOOTER_SPEED)
        SmartDashboard.putNumber("Indexer Speed",        constants.INDEXER_SPEED)
        SmartDashboard.putNumber("Shuffler Speed",       constants.SHUFFLER_SPEED)

        self._spinup_timer  = wpilib.Timer()
        self._spinup_active = False


    # ---------------------------------------------------------
    # SHOOT
    # ---------------------------------------------------------
    def shoot(self):
        shooter_speed = SmartDashboard.getNumber("Shooter Speed",      constants.SHOOTER_SPEED)
        intake_speed  = SmartDashboard.getNumber("Intake Speed",       constants.INTAKE_SPEED)
        indexer_speed = SmartDashboard.getNumber("Indexer Speed",      constants.INDEXER_SPEED)

        # Start spinup timer on first call
        if not self._spinup_active:
            self._spinup_active = True
            self._spinup_timer.reset()
            self._spinup_timer.start()

        # Shooter + shuffler always spin up immediately
        self._set_shooter(shooter_speed)

        # Feed balls only after the flywheel has reached speed
        if self._spinup_timer.hasElapsed(constants.SHOOTER_SPINUP_DELAY):
            self._set_intake(-intake_speed)
            self._set_indexer(indexer_speed)


    # ---------------------------------------------------------
    # INTAKE
    # ---------------------------------------------------------
    def intake(self):
        intake_speed = SmartDashboard.getNumber("Intake Speed", constants.INTAKE_SPEED)
        indexer_speed = SmartDashboard.getNumber("Indexer Speed", constants.INDEXER_SPEED)
        shuffler_speed = SmartDashboard.getNumber("Shuffler Speed", constants.SHUFFLER_SPEED)

        self._set_shuffler(shuffler_speed)
        self._set_intake(-intake_speed)
        self._set_indexer(-indexer_speed)
        self._set_shooter(0.35)

    # ---------------------------------------------------------
    # EJECT
    # ---------------------------------------------------------
    def eject(self):
        intake_speed = SmartDashboard.getNumber("Intake Speed", constants.INTAKE_SPEED)
        indexer_speed = SmartDashboard.getNumber("Indexer Speed", constants.INDEXER_SPEED)
        shuffler_speed = SmartDashboard.getNumber("Shuffler Speed", constants.SHUFFLER_SPEED)

        self._set_intake(intake_speed)
        self._set_indexer(indexer_speed)
        self._set_shuffler(-shuffler_speed)


    # ---------------------------------------------------------
    # IDLE
    # ---------------------------------------------------------
    def idle(self):
        self._reset_spinup()
        self._set_shooter(0)
        self._set_intake(0)
        self._set_indexer(0)
        self._set_shuffler(0)


    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------
    def _reset_spinup(self):
        if self._spinup_active:
            self._spinup_active = False
            self._spinup_timer.stop()
            self._spinup_timer.reset()  # FIX: reset so next shoot() starts fresh

    def _set_shooter(self, power: float):
        # FIX: use consistent ControlMode.PercentOutput for both TalonSRX motors
        self._shooter.set( phoenix5.ControlMode.PercentOutput, power)
        self._shuffler.set(phoenix5.ControlMode.PercentOutput, -power)

    def _set_intake(self, power: float):
        self._intake.set(power)

    def _set_indexer(self, power: float):
        self._indexer.set(phoenix5.ControlMode.PercentOutput, power)

    def _set_shuffler(self, power: float):
        self._shuffler.set(phoenix5.ControlMode.PercentOutput, power)