from wpilib import MotorControllerGroup, DriverStation

from wpilib.drive import DifferentialDrive
import wpilib.drive
from phoenix5 import WPI_TalonSRX as SRX

# pathplanner
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.controller import PPLTVController
from pathplannerlib.config import RobotConfig

#from modules.components.hardware.motor_controllers import TalonMotor as m


class Drive(DifferentialDrive):
    ''' Drive class - inherits from Differential Drive. Represents the robot drive train.
    Class parameters to modify:
        MAX_POWER - Adjust maximum robot power (0-1, where 1 is full power)
        INVERT_LEFT - Inverts left drive train (assuming intake region is front)  
        INVERT_RIGHT - Inverts right drive train (assuming intake region is front)

    # The way the motors are inverted may affect robot direction.
    # By default, the left train is inverted. At least ONE drive train must be inverted.

    '''
    MAX_POWER = 0.6
    INVERT_LEFT = True  
    INVERT_RIGHT = not(INVERT_LEFT)

    def __init__(self):
        front_left = SRX(0)
        back_left = SRX(1)
        front_right = SRX(2)
        back_right = SRX(3)

        # Motors are created like this: Left[0, 1] Right[2,3]
        # Use Phoenix Tuner to change CAN IDs if needed.

        # wpilib.MotorControllerGroup is deprecated as of 2024 and will be removed next season.
        # See if you could use the follow command to replace MotorControllerGroup?
        # drive_train_motors[0].follow(drive_train_motors[1])


        # back_left.follow(front_left)
        # front_left.setInverted(Drive.INVERT_LEFT)
        
        # back_right.follow(front_right)
        # front_right.setInverted(Drive.INVERT_RIGHT)

        left_train = MotorControllerGroup(
            front_left, back_left)
        left_train.setInverted(Drive.INVERT_LEFT)

        right_train = MotorControllerGroup(
            front_right, back_right)
        right_train.setInverted(Drive.INVERT_RIGHT)

        

        # Since this class inherits DifferentialDrive, we all super().__init__ to
        # initialize parent class and create a reference for the robot.
        super().__init__(leftMotor=left_train, rightMotor=right_train)
        # super().__init__(leftMotor=front_left, rightMotor=front_right)

        self.setMaxOutput(maxOutput=Drive.MAX_POWER)

        # (Moved from auto_drive.py to drive.py)
        # Load the RobotConfig from the GUI settings. You should probably
        # store this in your Constants file
        config = RobotConfig.fromGUISettings()

        # Configure the AutoBuilder last
        AutoBuilder.configure(
            self.getPose, # Robot pose supplier
            self.resetPose, # Method to reset odometry (will be called if your auto has a starting pose)
            self.getRobotRelativeSpeeds, # ChassisSpeeds supplier. MUST BE ROBOT RELATIVE
            lambda speeds, feedforwards: self.driveRobotRelative(speeds), # Method that will drive the robot given ROBOT RELATIVE ChassisSpeeds. Also outputs individual module feedforwards
            PPLTVController(0.02), # PPLTVController is the built in path following controller for differential drive trains
            config, # The robot configuration
            self.shouldFlipPath, # Supplier to control path flipping based on alliance color
            self # Reference to this subsystem to set requirements
        )
    def shouldFlipPath():
        # Boolean supplier that controls when the path will be mirrored for the red alliance
        # This will flip the path being followed to the red side of the field.
        # THE ORIGIN WILL REMAIN ON THE BLUE SIDE
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed