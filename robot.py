import wpilib
import phoenix5
from wpilib import Joystick, SmartDashboard
import rev

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):

        # Drivetrain
        self.talon1 = phoenix5.WPI_TalonSRX(1)
        self.talon2 = phoenix5.WPI_TalonSRX(2)
        self.talon3 = phoenix5.WPI_TalonSRX(3)
        self.talon4 = phoenix5.WPI_TalonSRX(4)

        # Intake + Shooter
        self.talon5 = phoenix5.WPI_TalonSRX(5)   # intake
        self.talon6 = phoenix5.WPI_TalonSRX(6)   # shooter
        self.talon5.setInverted(True)

        # NEW 3rd intake motor (SparkMax)
        self.sparkmax1 = rev.CANSparkMax(7, rev.CANSparkMax.MotorType.kBrushless)

        self.joystick = Joystick(0)

        # Timer for delayed intake
        self.intake_timer = wpilib.Timer()
        self.intake_delay_active = False

        # Dashboard tunables
        SmartDashboard.putNumber("Shooter Speed", 0.8)
        SmartDashboard.putNumber("Intake Speed", 0.9)
        SmartDashboard.putNumber("Reverse Intake Speed", -0.65)
        SmartDashboard.putNumber("Reverse Intake Shooter Speed", 0.65)

    def teleopPeriodic(self):

        leftyaxis    = self.joystick.getRawAxis(1)
        lefttrigger  = self.joystick.getRawAxis(2)
        righttrigger = self.joystick.getRawAxis(3)
        rightyaxis   = self.joystick.getRawAxis(5)

        a_button = self.joystick.getRawButton(1)
        b_button = self.joystick.getRawButton(2)

        # Deadband + scaling
        def db(x, d=0.15):
            return x if abs(x) > d else 0

        def scale(x):
            return x * 0.95

        left_power  = scale(db(leftyaxis))
        right_power = scale(db(rightyaxis))

        # Load speeds from dashboard
        intake_speed  = SmartDashboard.getNumber("Intake Speed", 0.9)
        shooter_speed = SmartDashboard.getNumber("Shooter Speed", 0.8)
        rev_intake    = SmartDashboard.getNumber("Reverse Intake Speed", -0.65)
        rev_shooter   = SmartDashboard.getNumber("Reverse Intake Shooter Speed", 0.65)

        # ---------------------------------------------------------------
        # Shooter + Intake Logic (clean + non-conflicting)
        # ---------------------------------------------------------------
        shooter_power = 0
        intake_power  = 0

        # --- SHOOTING (right trigger) ---
        if righttrigger > 0.2:
            shooter_power = shooter_speed

            if not self.intake_delay_active:
                self.intake_delay_active = True
                self.intake_timer.reset()
                self.intake_timer.start()

            if self.intake_timer.hasElapsed(1):
                intake_power = intake_speed

        # --- REVERSE (left trigger) ---
        elif lefttrigger > 0.2:
            shooter_power = rev_shooter
            intake_power  = rev_intake
            self.intake_delay_active = False
            self.intake_timer.stop()

        # --- MANUAL REVERSE (B button) ---
        elif b_button:
            shooter_power = -0.65
            intake_power  = 0.65
            self.intake_delay_active = False
            self.intake_timer.stop()

        # --- NOTHING PRESSED ---
        else:
            shooter_power = 0
            intake_power  = 0
            self.intake_delay_active = False
            self.intake_timer.stop()

        # Apply intake + shooter power
        self.talon5.set(phoenix5.ControlMode.PercentOutput, intake_power)
        self.sparkmax1.set(intake_power)  # NEW 3rd intake motor
        self.talon6.set(phoenix5.ControlMode.PercentOutput, shooter_power)

        # ---------------------------------------------------------------
        # Drivetrain
        # ---------------------------------------------------------------
        self.talon1.set(phoenix5.ControlMode.PercentOutput,  right_power)
        self.talon2.set(phoenix5.ControlMode.PercentOutput,  right_power)
        self.talon3.set(phoenix5.ControlMode.PercentOutput, -left_power)
        self.talon4.set(phoenix5.ControlMode.PercentOutput, -left_power)

    # ---------------------------------------------------------------
    # Autonomous
    # ---------------------------------------------------------------
    def autonomousInit(self):
        self.auto_timer = wpilib.Timer()
        self.auto_timer.start()
        self.intake_delay_active = False

    def autonomousPeriodic(self):
        shooter_power = SmartDashboard.getNumber("Shooter Speed", 0.8)
        intake_speed  = SmartDashboard.getNumber("Intake Speed", 0.9)

        # Stop drivetrain
        for t in [self.talon1, self.talon2, self.talon3, self.talon4]:
            t.set(phoenix5.ControlMode.PercentOutput, 0)

        # Shooter always on
        self.talon6.set(phoenix5.ControlMode.PercentOutput, shooter_power)

        # Intake after 1 second
        if not self.intake_delay_active:
            self.intake_delay_active = True
            self.intake_timer.reset()
            self.intake_timer.start()

        if self.intake_timer.hasElapsed(1):
            self.talon5.set(phoenix5.ControlMode.PercentOutput, intake_speed)
            self.sparkmax1.set(intake_speed)
        else:
            self.talon5.set(phoenix5.ControlMode.PercentOutput, 0)
            self.sparkmax1.set(0)

    def disabledInit(self):
        self.talon5.set(phoenix5.ControlMode.PercentOutput, 0)
        self.talon6.set(phoenix5.ControlMode.PercentOutput, 0)
        self.sparkmax1.set(0)

if __name__ == "__main__":
    wpilib.run(MyRobot)
