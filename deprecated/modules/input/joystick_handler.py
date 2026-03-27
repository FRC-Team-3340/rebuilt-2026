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
            "get_x": 0,
            "get_y": 1,
            "left_trigger": 2,
            "right_trigger": 3,
        }
        
        axis = axis_numbers.get(name)
        if axis is None:
            return 0.0
        
        try:
            return self.joystick.getRawAxis(axis)
        except Exception:
            return 0.0
    def get_stick(self):
        return -self.joystick.getX(), -self.joystick.getY()
    
    def get_tank_inputs(self):
        """
        Returns the Y axes for both sticks for Tank Drive.
        Typically: Left Stick Y = Axis 1, Right Stick Y = Axis 5
        """
        if self.joystick is None:
            return 0.0, 0.0
        
        # WPILib axes are often inverted (up is negative), 
        # so we negate them for intuitive driving.
        left_y = -self.joystick.getRawAxis(1)
        right_y = -self.joystick.getRawAxis(5)
        
        return left_y, right_y
    def get_button(self, name):
        name = name.upper()

        if self.joystick is None:
            raise Exception("No joystick connected")
        
        button_numbers = {
            "A": 1,
            "B": 2,
            "X": 3,
            "Y": 4,
            "LB": 5,
            "RB": 6
        }

        if name not in button_numbers:
            raise Exception(f"Unknown button name: {name}")

        button = button_numbers.get(name)
        if button is None:
            raise Exception(f"Unknown button name: {name}")
        
        return self.joystick.getRawButton(button)
    
    def get_dpad(self, val):
        if self.joystick is None:
            raise Exception("No joystick connected")
        
        dpad_angles = {
            "up": 0,
            "right": 90,
            "down": 180,
            "left": 270
        }

        if not val in dpad_angles:
            raise Exception(f"Unknown angle: {val}")
        
        return self.joystick.getPOV() == dpad_angles[val]
