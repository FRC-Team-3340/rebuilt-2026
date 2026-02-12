import wpilib
from modules.config.config import ConfigLoader
from modules.components.hardware.motor_controllers import TalonMotor, SparkMaxMotor
from modules.input.joystick_handler import JoystickHandler
from modules.components.vision.limelight_manager import LimelightManager


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
        print("[robot] Connecting to motors...")
        try:
            # get ids from config
            left_id = motors_cfg.get("left_id", 3)
            right_id = motors_cfg.get("right_id", 2)
            
            # Create motor controllers
            self.left_motor = TalonMotor(left_id)
            self.right_motor = SparkMaxMotor(right_id)
            print("[robot] Motors connected!")
            
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
        # reads controller triggers (0.0 to 1.0)
        right_trigger = self.joystick.get_axis("right_trigger")
        left_trigger = self.joystick.get_axis("left_trigger")
        x,y = self.joystick.get_stick()

        
        # sets motor speeds (divided by 10 to make it gentler, idk if that would work though)
        self.right_motor.set(right_trigger * 2)
        #self.left_motor.set(left_trigger / 10)
        self.left_motor.set(y)

        if y < 0.1: # remove stick drift
            self.left_motor.set(0)

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
            print("[vision] No data")

    def disabledInit(self):
        """This runs once when the robot is disabled."""
        print("[robot] Disabled - Stopping camera")
        self.limelight.stop()


if __name__ == "__main__":
    wpilib.run(MyRobot)