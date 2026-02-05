import wpilib
import phoenix5


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):

        self.motor = phoenix5.WPI_TalonSRX(2)

    def teleopPeriodic(self):

        motor_speed = 0.5
        self.motor.set(phoenix5.ControlMode.PercentOutput, motor_speed)
