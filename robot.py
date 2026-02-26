import wpilib
import wpilib.interfaces
_ = wpilib.interfaces.MotorController 

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
        
        # set up motors
        print("[robot] Setting up drive...")

        try:
            self.drive = Drive()
            
        except Exception as e:
            print(f"[robot] ERROR connecting to motors: {e}")
            raise  # stop if motors don't work
        
        # set up controller
        try:
            self.joystick = JoystickHandler(0)
        except Exception as e:
            print(f"[robot] ERROR connecting Joystick: {e}")
        # set up vision
        self.limelight = LimelightManager()
        if not wpilib.RobotBase.isSimulation():
            self.limelight.start()
        else:
            print("[robot] Skipping Limelight socket start for Simulation/Test")
        print("[robot] Initialization complete!")

    def teleopPeriodic(self):
        # drive logic
        left_y, right_y = self.joystick.get_tank_inputs()
        self.drive.apply_tank(left_y, right_y)

    def autonomousInit(self):
        self.timer = None #wpilib.Timer()
        self.stage = 1
        #self.timer.start()

    def autonomousPeriodic(self):
        # upd camera data
        self.limelight.update()
        data = self.limelight.get_latest()
        
        # print data if existing
        if data is not None:
            print(f"[vision] Camera sees: {data}")
        else:
            print("[vision] Can't see anything boohoo")

        """match(self.stage):
            case 0:
                if self.timer.get() > 3:
                    self.stage += 1
            case 1:
                # if self.timer.get() < 4:
                    # self.arm.arm_motor.set(0.025)
                if self.timer.get() < 8:
                    # self.arm.arm_motor.set(0)
                    self.drive.arcadeDrive(xSpeed=-0.2, zRotation=0)
                else:
                    self.stage += 1
            case 2:
                if self.timer.get() < 11:
                    self.drive.arcadeDrive(xSpeed=0, zRotation=0)
                   # self.arm.activateRollers(direction=1)
                else:
                    self.stage +=1
            case 3:
               # self.arm.activateRollers(0)
                pass"""

    def disabledInit(self):
        """This runs once when the robot is disabled."""
        print("[robot] Disabled - Stopping camera")
        print(self.limelight)
        self.limelight.stop()


if __name__ == "__main__":
    wpilib.run(MyRobot)