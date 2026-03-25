import wpilib
import phoenix5
from wpilib import Joystick, SmartDashboard
import rev

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):

        self.GEAR_RATIO = 48.0
        self.SPOOL_CIRCUMFERENCE = 2.6
        self.TARGET_HEIGHT = 40       # max extension in inches
        self.MIN_HEIGHT    = 0.5      # small dead-band above zero so rope never goes slack

        # Drivetrain
        self.talon1 = phoenix5.WPI_TalonSRX(1)
        self.talon2 = phoenix5.WPI_TalonSRX(2)
        self.talon3 = phoenix5.WPI_TalonSRX(3)
        self.talon4 = phoenix5.WPI_TalonSRX(4)

        # Intake + Shooter
        self.talon5 = phoenix5.WPI_TalonSRX(5)
        self.talon6 = phoenix5.WPI_TalonSRX(6)
        self.talon5.setInverted(True)

        self.joystick = Joystick(0)

        # Timer for delayed intake
        self.intake_timer = wpilib.Timer()
        self.intake_delay_active = False

        SmartDashboard.putNumber("Shooter Speed", 0.8)
        SmartDashboard.putNumber("Intake Speed", 0.9)
        SmartDashboard.putNumber("Reverse Intake Speed", -0.65)
        SmartDashboard.putNumber("Reverse Intake Shooter Speed", 0.65)

        self.intake_speed = SmartDashboard.getNumber("Intake Speed", 0.9)
        self.shooter_speed = SmartDashboard.getNumber("Shooter Speed", 0.8)
        self.reverse_intake_speed = SmartDashboard.getNumber("Reverse Intake Speed", 0.65)
        self.reverse_intake_shooter_speed = SmartDashboard.getNumber("Reverse Intake Shooter Speed", -0.65)

    def teleopInit(self):
        pass

    def teleopPeriodic(self):

        leftyaxis    = self.joystick.getRawAxis(1)
        lefttrigger  = self.joystick.getRawAxis(2)
        righttrigger = self.joystick.getRawAxis(3)
        rightyaxis   = self.joystick.getRawAxis(5)

        a_button    = self.joystick.getRawButton(1)
        b_button    = self.joystick.getRawButton(2)
        x_button    = self.joystick.getRawButton(3)
        y_button    = self.joystick.getRawButton(4)

        def db(x, d=0.15):
            return x if abs(x) > d else 0

        def scale(x):
            return x * 0.95

        left_power  = scale(db(leftyaxis))
        right_power = scale(db(rightyaxis))

        # ---------------------------------------------------------------
        # Shooter + Intake
        # ---------------------------------------------------------------
        shooter_power = 0
        intake_power  = 0

        if righttrigger > 0.2:
            shooter_power = self.shooter_speed
            if not self.intake_delay_active:
                self.intake_delay_active = True
                self.intake_timer.reset()
                self.intake_timer.start()

        if self.intake_delay_active and self.intake_timer.hasElapsed(1):
            intake_power = self.intake_speed

        if righttrigger <= 0.2:
            shooter_power = 0
            intake_power  = 0
            self.intake_delay_active = False
            self.intake_timer.stop()

        if lefttrigger > 0.2:
            intake_power  = self.reverse_intake_speed
            shooter_power = self.reverse_intake_shooter_speed

        if lefttrigger < 0.2 and righttrigger < 0.2:
            intake_power  = 0
            shooter_power = 0

        if b_button:
            intake_power  =  0.65
            shooter_power = -0.65

        self.talon5.set(phoenix5.ControlMode.PercentOutput, intake_power)
        self.talon6.set(phoenix5.ControlMode.PercentOutput, shooter_power)

        

        # Publish positions so you can watch and tune limits safely

        # X button: lock climb in place with kBrake (one-way latch)

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
        intake_power  = 0
        shooter_power = 0

        self.talon1.set(phoenix5.ControlMode.PercentOutput, 0)
        self.talon2.set(phoenix5.ControlMode.PercentOutput, 0)
        self.talon3.set(phoenix5.ControlMode.PercentOutput, 0)
        self.talon4.set(phoenix5.ControlMode.PercentOutput, 0)

        shooter_power = self.shooter_speed

        if not self.intake_delay_active:
            self.intake_delay_active = True
            self.intake_timer.reset()
            self.intake_timer.start()

        if self.intake_delay_active and self.intake_timer.hasElapsed(1):
            intake_power = self.intake_speed

        self.talon5.set(phoenix5.ControlMode.PercentOutput, intake_power)
        self.talon6.set(phoenix5.ControlMode.PercentOutput, shooter_power)

    def disabledInit(self):
        self.talon5.set(phoenix5.ControlMode.PercentOutput, 0)
        self.talon6.set(phoenix5.ControlMode.PercentOutput, 0)

if __name__ == "__main__":
    wpilib.run(MyRobot)