import wpilib
import phoenix5
from wpilib import Joystick
import rev    

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.talon1 = phoenix5.WPI_TalonSRX(3)
        self.sparkmax1 = rev.SparkMax(2, rev.SparkLowLevel.MotorType.kBrushless)
        self.joystick = Joystick(0)

    def teleopPeriodic(self):
        right_trigger = self.joystick.getRawAxis(3)  # Right trigger for motor speed
        left_trigger = self.joystick.getRawAxis(2)
        self.sparkmax1.set(right_trigger / 10)
        self.talon1.set(phoenix5.ControlMode.PercentOutput, left_trigger / 10)
        print(right_trigger, left_trigger)
    
    def testInit(self):
        """This function is called once each time the robot enters test mode."""

    def testPeriodic(self):
        """This function is called periodically during test mode."""

    def teleopInit(self):
        """This function is called once each time the robot enters teleoperated mode."""
    
    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""



if __name__ == "__main__":
    wpilib.run(MyRobot)