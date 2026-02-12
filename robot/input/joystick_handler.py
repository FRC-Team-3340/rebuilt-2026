"""
Simple joystick/controller wrapper.
Makes it easier to read controller inputs by name instead of numbers.
"""


class JoystickHandler:
    """Wrapper for Xbox controller or other joystick."""
    
    def __init__(self, port=0):
        """Create a joystick handler.
        
        Args:
            port: Which USB port the controller is plugged into (usually 0)
        """
        try:
            from wpilib import Joystick
            self.joystick = Joystick(port)
            print(f"[input] Connected controller on port {port}")
        except Exception as e:
            print(f"[input] Could not connect controller: {e}")
            self.joystick = None
    
    def get_axis(self, name):
        """Get a controller axis value by name.
        
        Args:
            name: Either 'right_trigger' or 'left_trigger'
        
        Returns:
            A number from 0.0 to 1.0, or 0.0 if controller not connected
        """
        if self.joystick is None:
            return 0.0
        
        # Map friendly names to axis numbers
        axis_numbers = {
            "right_trigger": 3,
            "left_trigger": 2,
        }
        
        axis = axis_numbers.get(name)
        if axis is None:
            return 0.0
        
        try:
            return self.joystick.getRawAxis(axis)
        except Exception:
            return 0.0
