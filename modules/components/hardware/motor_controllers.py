"""
Simple motor controller wrappers.
Each motor class has three basic methods:
  - set(value): Set motor speed (-1.0 to 1.0)
  - stop(): Stop the motor (same as set(0))
  - get(): Get the current motor speed
"""


class TalonMotor:
    """Wrapper for CTRE Talon SRX motor controller."""
    
    def __init__(self, can_id):
        """Create a Talon motor controller.
        
        Args:
            can_id: The CAN ID number (found in Phoenix Tuner)
        """
        try:
            import phoenix5
            self.talon = phoenix5.WPI_TalonSRX(can_id)
            print(f"[motor] Connected Talon on CAN ID {can_id}")
        except Exception as e:
            print(f"[motor] ERROR: Could not connect Talon: {e}")
            raise
    
    def set(self, speed):
        """Set the motor speed (between -1.0 and 1.0)"""
        self.talon.set(speed)
    
    def stop(self):
        """Stop the motor"""
        self.talon.set(0)
    
    def get(self):
        """Get the current motor speed"""
        return self.talon.get()


class SparkMaxMotor:
    """Wrapper for REV Robotics Spark Max motor controller."""
    
    def __init__(self, can_id):
        """Create a Spark Max motor controller.
        
        Args:
            can_id: The CAN ID number (found in REV Hardware Client)
        """
        try:
            import rev
            self.spark = rev.SparkMax(can_id, rev.SparkLowLevel.MotorType.kBrushless)
            print(f"[motor] Connected Spark Max on CAN ID {can_id}")
        except Exception as e:
            print(f"[motor] ERROR: Could not connect Spark Max: {e}")
            raise
    
    def set(self, speed):
        """Set the motor speed (between -1.0 and 1.0)"""
        self.spark.set(speed)
    
    def stop(self):
        """Stop the motor"""
        self.spark.set(0)
    
    def get(self):
        """Get the current motor speed"""
        return self.spark.get()
