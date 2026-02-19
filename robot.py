import wpilib
from modules.config.config import ConfigLoader
from modules.components.hardware.motor_controllers import TalonMotor, SparkMaxMotor
from modules.input.joystick_handler import JoystickHandler
from modules.components.vision.limelight_manager import LimelightManager
from modules.components.drive import Drive

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """This runs once when the robot turns on."""

        print("="*50)
        print("ROBOT STARTING UP")
        print("="*50)
        
        # load settings from config
        self.config = ConfigLoader.load_config()
        motors_cfg = self.config.get("motors", {})
        
        # set up motors
        print("[robot] Setting up drive...")
        try:
            self.drive = Drive()
            
        except Exception as e:
            print(f"[robot] ERROR connecting to motors: {e}")
            raise  # stop if motors don't work
        
        # set up controller
        self.joystick = JoystickHandler(0)
        
        # set up vision
        self.limelight = LimelightManager()
        self.limelight.start()
        
        print("[robot] Initialization complete!")

    def teleopPeriodic(self):
        # drive logic
        left_y, right_y = self.joystick.get_tank_inputs()
        self.drive.apply_tank(left_y, right_y)

    def testPeriodic(self):
        # currently using to test limelight vision as i dont want to merge with teleop or auto just yet

        # upd camera data
        self.limelight.update()
        
        # fetch latest data
        data = self.limelight.get_latest()
        
        # print data if existing
        if data is not None:
            print(f"[vision] Camera sees: {data}")
        else:
            print("[vision] Can't see anything boohoo")

    def disabledInit(self):
        """This runs once when the robot is disabled."""
        print("[robot] Disabled - Stopping camera")
        self.limelight.stop()


if __name__ == "__main__":
    wpilib.run(MyRobot)