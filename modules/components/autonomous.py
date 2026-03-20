import wpilib
import phoenix5
from ntcore import NetworkTableInstance
from modules.components.vision.limelight_manager import LimelightManager
#What this auto does: Drives forward off starting line, Searches for AprilTag, Aligns using Limelight Vision Camera tx, Drives to target using ta distance, Fires shooter
#NEED TO ADD THIS TO MAIN ROBOTPY BEFORE USE: 
# """from auto_apriltag import AprilTagAuto
# self.auto = AprilTagAuto(
#     self.talon1,
#     self.talon2,
#     self.talon3,
#     self.talon4,
#     self.talon5,
#     self.talon6
# )

# def autonomousInit(self):
#     self.auto.autoInit()

# def autonomousPeriodic(self):
#     self.auto.periodic()

# """


class AprilTagAuto:

    def __init__(self, talon1, talon2, talon3, talon4, intake, shooter):

        # drivetrain motors
        self.talon1 = talon1
        self.talon2 = talon2
        self.talon3 = talon3
        self.talon4 = talon4

        # mechanisms
        self.intake = intake
        self.shooter = shooter

        # limelight network tables
        self.limelight = LimelightManager()
        self.limelight.start()
        # self.nt = NetworkTableInstance.getDefault()
        # self.limelight = self.nt.getTable("limelight")

        # auto state machine
        self.state = 0

        # timer
        self.timer = wpilib.Timer()

    def autoInit(self):

        self.state = 0
        self.timer.reset()
        self.timer.start()
        

    def stopDrive(self):

        self.talon1.set(0)
        self.talon2.set(0)
        self.talon3.set(0)
        self.talon4.set(0)

    def drive(self, left, right):

        self.talon1.set(right)
        self.talon2.set(right)
        self.talon3.set(-left)
        self.talon4.set(-left)

    def periodic(self):

        # Limelight values
        # tv = self.limelight.getNumber("tv", 0)   # target valid
        # tx = self.limelight.getNumber("tx", 0)   # horizontal offset
        # ta = self.limelight.getNumber("ta", 0)   # target area (distance)
        self.limelight.update()
        data = self.limelight.get_latest()

        if data is not None:
            print(f"[vision] Camera sees: {data}")

        # STATE 0: Leave starting zone
        # -----------------------------
        if self.state == 0:

            self.drive(0.25, 0.25)

            if self.timer.hasElapsed(2.0):
                self.stopDrive()
                self.state = 1


        # STATE 1: Search for AprilTag
        # -----------------------------
        elif self.state == 1:

            if data and data.target_valid:
                self.state = 2
            else:
                # rotate slowly to search
                self.drive(0.2, -0.2)


        # STATE 2: Align to tag
        # -----------------------------
        elif self.state == 2:

            kP = 0.03
            turn = tx * kP

            left = -turn
            right = turn

            self.drive(left, right)

            if abs(tx) < 1.5:
                self.stopDrive()
                self.state = 3


        # STATE 3: Drive to target
        # -----------------------------
        elif self.state == 3:

            if ta < 5:
                self.drive(0.25, 0.25)
            else:
                self.stopDrive()
                self.state = 4
                self.timer.reset()
                self.timer.start()

  
        # STATE 4: Shoot game piece
        # -----------------------------
        elif self.state == 4:

            self.shooter.set(0.3)
            self.intake.set(0.3)

            if self.timer.hasElapsed(2.0):

                self.shooter.set(0)
                self.intake.set(0)
                self.state = 5


        # STATE 5: Finished
        # -----------------------------
        elif self.state == 5:
            self.limelight.stop()
            self.stopDrive()