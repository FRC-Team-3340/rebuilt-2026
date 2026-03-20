from wpilib.drive import DifferentialDrive
from phoenix5 import WPI_TalonSRX
from phoenix5 import NeutralMode
import json
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.kinematics import DifferentialDriveKinematics, ChassisSpeeds

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


    # methods for pathplanner
    def getPose(self):
        # Read the botPose_wpiblue (or botPose_wpired) NetworkTables entry from the Limelight. This gives [x, y, z, roll, pitch, yaw, latency]
        botPose = self.limelight_table.getEntry("botPose_wpiblue").getDoubleArray([0]*7)
        
        if botPose and len(botPose) >= 6:
            return Pose2d(
                Translation2d(botPose[0], botPose[1]),
                Rotation2d.fromDegrees(botPose[5])
            )
    
    # Fall back to odometry pose if Limelight has no target
    return self.odometry.getPose()
    def resetPose(self, pose: Pose2d):
        self.pose_estimator.resetPosition(
        self.getGyroRotation(),
        self.getModulePositions(),  # or wheel positions for tank drive
        pose
    )

    def getRobotRelativeSpeeds(self) -> ChassisSpeeds:
        current_pose = self.getPose()
        dt = self.timer.get() - self.last_time
        
        dx = (current_pose.X() - self.last_pose.X()) / dt
        dy = (current_pose.Y() - self.last_pose.Y()) / dt
        dtheta = (current_pose.rotation().radians() - self.last_pose.rotation().radians()) / dt
        
        self.last_pose = current_pose
        self.last_time = self.timer.get()
        
        # Convert field-relative to robot-relative
        return ChassisSpeeds.fromFieldRelativeSpeeds(dx, dy, dtheta, current_pose.rotation())

    def driveRobotRelative(self, speeds: ChassisSpeeds):
        wheel_speeds = self.kinematics.toWheelSpeeds(speeds)
        
        # Convert m/s to [-1, 1] percent output based on your max speed
        max_speed = 3.0  # tune this to your robot's actual max m/s
        left_percent = wheel_speeds.left / max_speed
        right_percent = wheel_speeds.right / max_speed
        
        self.left_motor.set(ControlMode.PercentOutput, left_percent)
        self.right_motor.set(ControlMode.PercentOutput, right_percent)
        
        self.last_commanded_speeds = speeds  # store for getRobotRelativeSpeeds