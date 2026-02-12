# updated code

## changes

The main robot code has been split into small, easy-to-understand pieces:

## new structure

lets start using modular code please, as we start adding more and more code, this means that it'll be harder to read just one file and interpret everything without having a bunch of issues -- especially when it's a team and not a solo project

<small>__init__.py files are for helping the python interpreter find the files in each folder so please bear with that</small>

**Want to change how motors work?**
→ Edit `robot/modules/hardware/motor_controllers.py`

**Want to change controller mappings?**
→ Edit `robot/input/joystick_handler.py`

**Want to change what happens during teleop?**
→ Edit the `teleopPeriodic()` method in `robot.py`

**Want to change camera settings?**
→ Edit `robot/modules/vision/limelight_manager.py`

<small>and so on</small>
## classes

yes, start using classes, very important, makes code easy to read

### SimulatedMotor, TalonMotor, SparkMaxMotor
simple motor classes with three methods:
- `set(speed)` - Set motor speed from -1.0 to 1.0
- `stop()` - Stop the motor
- `get()` - Get current speed

### JoystickHandler
makes it easy to read controller inputs:
- `get_axis("right_trigger")` - Read right trigger (0.0 to 1.0)
- `get_axis("left_trigger")` - Read left trigger (0.0 to 1.0)

### LimelightManager
simple camera interface:
- `start()` - Connect to camera
- `update()` - Get fresh data (call this regularly!)
- `get_latest()` - See what camera sees
- `stop()` - Disconnect
