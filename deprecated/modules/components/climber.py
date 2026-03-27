import rev

class Climber:
    def __init__(self, can_id_1, can_id_2):
        # Initialize motors
        self.spark1 = rev.SparkMax(can_id_1, rev.SparkLowLevel.MotorType.kBrushless)
        self.spark2 = rev.SparkMax(can_id_2, rev.SparkLowLevel.MotorType.kBrushless)
        
        # Set to Brake Mode so the robot doesn't slide down as easily
        self.spark1.IdleMode(rev.SparkMax.IdleMode.kBrake)
        self.spark2.IdleMode(rev.SparkMax.IdleMode.kBrake)

        # Speed constant (1/5 = 0.2)
        self.climb_speed = 0.2

    def update(self, left_button, right_button):
        """
        Call this in teleopPeriodic. 
        left_button: boolean (True/False)
        right_button: boolean (True/False)
        """
        if left_button:
            # Move Down
            self.spark1.set(self.climb_speed)
            self.spark2.set(-self.climb_speed)

        elif right_button:
            # Move Up
            self.spark1.set(-self.climb_speed)
            self.spark2.set(self.climb_speed)

        else:
            # Stop motors
            self.spark1.set(0)
            self.spark2.set(0)