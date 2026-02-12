from pathplannerlib.auto import AutoBuilder, PathPlannerAuto
from pathplannerlib.controller import PPLTVController
from pathplannerlib.config import RobotConfig
from wpilib import DriverStation

class Drive(DifferentialDrive):
    def __init__(self):
        # Do all subsystem initialization here
        # ...

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

    def getAutonomousCommand():
        # This method loads the auto when it is called, however, it is recommended
        # to first load your paths/autos when code starts, then return the
        # pre-loaded auto/path
        return PathPlannerAuto('Example Auto')

    def shouldFlipPath():
        # Boolean supplier that controls when the path will be mirrored for the red alliance
        # This will flip the path being followed to the red side of the field.
        # THE ORIGIN WILL REMAIN ON THE BLUE SIDE
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed