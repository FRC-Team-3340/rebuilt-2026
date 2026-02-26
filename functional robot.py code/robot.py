import wpilib
import phoenix5
from wpilib import Joystick
import rev

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Drivetrain
        self.talon1 = phoenix5.WPI_TalonSRX(1)
        self.talon2 = phoenix5.WPI_TalonSRX(2)
        self.talon3 = phoenix5.WPI_TalonSRX(3)
        self.talon4 = phoenix5.WPI_TalonSRX(4)

        # Intake + Shooter
        self.talon5 = phoenix5.WPI_TalonSRX(5)  # intake
        self.talon6 = phoenix5.WPI_TalonSRX(6)  # shooter

        # Sparks (wrist, feeder, whatever you want)
        self.spark1 = rev.SparkMax(7, rev.SparkLowLevel.MotorType.kBrushless)
        self.spark2 = rev.SparkMax(8, rev.SparkLowLevel.MotorType.kBrushless)

        self.joystick = Joystick(0)

        # Timer for delayed intake
        self.intake_timer = wpilib.Timer()
        self.intake_delay_active = False

    def teleopPeriodic(self):
        lx = self.joystick.getRawAxis(0)
        ly = self.joystick.getRawAxis(1)
        lt = self.joystick.getRawAxis(2)
        rt = self.joystick.getRawAxis(3)
        rx = self.joystick.getRawAxis(4)
        ry = self.joystick.getRawAxis(5)
        lb = self.joystick.getRawAxis(6)
        rb = self.joystick.getRawAxis(7)

        def db(x, d=0.15):
            return x if abs(x) > d else 0

        def scale(x):
            return x * 0.1

        # Drivetrain power
        left_power = scale(db(ly))
        right_power = scale(db(ry))

        # Shooter + intake
        shooter_power = 0
        intake_power = 0

        # SHOOTER TRIGGER
        if rt > 0.2:
            shooter_power = 0.9

            # Start the 1 second delay ONCE
            if not self.intake_delay_active:
                self.intake_delay_active = True
                self.intake_timer.reset()
                self.intake_timer.start()

        # After 1 second, start intake
        if self.intake_delay_active and self.intake_timer.hasElapsed(0.5):
            intake_power = 0.9

        # If shooter is released, stop everything
        if rt <= 0.2:
            shooter_power = 0
            intake_power = 0
            self.intake_delay_active = False
            self.intake_timer.stop()

        # DRIVETRAIN
        self.talon1.set(phoenix5.ControlMode.PercentOutput, right_power)
        self.talon2.set(phoenix5.ControlMode.PercentOutput, right_power)
        self.talon3.set(phoenix5.ControlMode.PercentOutput, -left_power)
        self.talon4.set(phoenix5.ControlMode.PercentOutput, -left_power)

        # INTAKE + SHOOTER
        self.talon5.setInverted(True)
        
        if lt > 0.2:
            intake_power =  -0.7
            shooter_power = 0.7
        self.talon5.set(phoenix5.ControlMode.PercentOutput, intake_power)
        self.talon6.set(phoenix5.ControlMode.PercentOutput, shooter_power)

        # SPARKS
        if lb >=0.2:
            self.spark1.set(lb)
            self.spark2.set(-lb)

        if rb >=0.2:
            self.spark1.set(-lb)
            self.spark2.set(lb)

        print(f"AXES: 0={lx:.2f} 1={ly:.2f} 2={lt:.2f} 3={rt:.2f} 4={rx:.2f} 5={ry:.2f}")

        print()


if __name__ == "__main__":
    wpilib.run(MyRobot)
