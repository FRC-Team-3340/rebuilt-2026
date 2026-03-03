import wpilib
import wpilib.interfaces
#_ = wpilib.interfaces.MotorController 

#from modules.config.config import ConfigLoader
#from modules.input.joystick_handler import JoystickHandler
#from modules.components.vision.limelight_manager import LimelightManager
###from modules.components.drive import Drive
from wpilib.drive import DifferentialDrive
from phoenix5 import WPI_TalonSRX
from phoenix5 import NeutralMode

class Drive:
    def __init__(self):
        # initialize motors
        self.left_motor = WPI_TalonSRX(3)
        self.right_motor = WPI_TalonSRX(1)

        # set neutral mode to brake for better control
        self.left_motor.setNeutralMode(NeutralMode.Brake)
        self.right_motor.setNeutralMode(NeutralMode.Brake)

        self.left_motor.setInverted(True)
        self.right_motor.setInverted(False)
        
        # create drive object
        self.drive = DifferentialDrive(self.left_motor, self.right_motor)
        self.drive.setMaxOutput(0.6)
        self.drive.setDeadband(0.05)

    def apply_tank(self, left_speed, right_speed):
        self.drive.tankDrive(left_speed, right_speed)

    def stop_robot(self):
        self.drive.stopMotor()

        
class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drive = Drive()
    def teleopPeriodic(self):
        self.drive.apply_tank(0.4, 0.4)
    def autonomousInit(self):
        pass
    def autonomousPeriodic(self):
        pass
    def disabledInit(self):
       pass


if __name__ == "__main__":
    wpilib.run(MyRobot)