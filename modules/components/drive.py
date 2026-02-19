from wpilib.drive import DifferentialDrive
from modules.components.hardware.motor_controllers import TalonMotor
from modules.config.config import ConfigLoader

class Drive(DifferentialDrive):
    """
    Drive class for True Tank Drive.
    Uses Leader/Follower mode to replace the deprecated MotorControllerGroup.
    """
    
    MAX_POWER = 0.6
    INVERT_LEFT = True  
    INVERT_RIGHT = not(INVERT_LEFT)
    DEADBAND = 0.05  # Ignore inputs smaller than 5%

    def __init__(self):
        self.config = ConfigLoader.load_config()
        drive_cfg = self.config.get("drive", {})
        
        left_ids = drive_cfg.get("left", [0, 1])
        right_ids = drive_cfg.get("right", [2, 3])

        print(f"[drive] Initializing Tank Drive: Left{left_ids}, Right{right_ids}")

        # The first ID in the list is the Leader
        self.left_leader = TalonMotor(left_ids[0]).talon
        for can_id in left_ids[1:]:
            follower = TalonMotor(can_id).talon
            follower.follow(self.left_leader)
        
        self.right_leader = TalonMotor(right_ids[0]).talon
        for can_id in right_ids[1:]:
            follower = TalonMotor(can_id).talon
            follower.follow(self.right_leader)

        self.left_leader.setInverted(Drive.INVERT_LEFT)
        self.right_leader.setInverted(Drive.INVERT_RIGHT)

        super().__init__(self.left_leader, self.right_leader)
        
        self.setMaxOutput(Drive.MAX_POWER)
        self.setDeadband(self.DEADBAND)

    def apply_tank(self, left_y, right_y):
        """
        Applies Tank Drive logic. 
        Left stick controls left motors, right stick controls right motors.
        """
        # DifferentialDrive.tankDrive includes its own squaredInputs option 
        # (default True) which makes fine movements easier.
        self.tankDrive(left_y, right_y, squaredInputs=True)

    def stop_robot(self):
        """Emergency stop for the drivetrain."""
        self.stopMotor()