#LEHANSA, dR. MICHAEL 2-27-2026 6PM


import wpilib
import wpilib.interfaces
_ = wpilib.interfaces.MotorController 

from modules.config.config import ConfigLoader
from modules.components.hardware.motor_controllers import TalonMotor, SparkMaxMotor
from modules.input.joystick_handler import JoystickHandler
from modules.components.vision.limelight_manager import LimelightManager
from modules.components.drive import Drive

class MyRobot(wpilib.TimedRobot):
    def robotPeriodic(self):
        pass

    def disabledPeriodic(self):
        pass
    def robotInit(self):
        self.timer = wpilib.Timer()
        self.stage = 0
        self.timer.start()
        """This runs once when the robot turns on."""
        
        print("="*50)
        print("ROBOT STARTING UP")
        print("="*50)
        
        # load settings from config
        self.config = ConfigLoader.load_config()
        self.firstDelay = False

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

        # intake shoot rotation logic
        try:
            self.intake_motor = TalonMotor(6)
            self.outtake_motor = TalonMotor(5)
        except Exception as e:
            print(f"[robot] ERROR connecting intake motor")

    
        print("[robot] Initialization complete!")

    def teleopPeriodic(self):
        # drive logic
        

        left_y, right_y = self.joystick.get_tank_inputs()
        self.drive.apply_tank(left_y, right_y)

        
        self.intake_axis = self.joystick.get_axis("right_trigger")
        self.outake_axis = self.joystick.get_axis("left_trigger")

        
        #outtake_axis = self.joystick.get_axis("left_trigger")
        try:
            if self.intake_axis > 0:
                self.timer.start()
                self.intake_motor.set(self.intake_axis)
                
                print(self.timer.get())

                match(self.stage):
                            case 0:
                                self.stage += 1
                            case 1:
                                #if self.timer.get() < 4:
                                if self.timer.get() > 5:
                                #self.outtake_motor.set(self.intake_axis/2)
                                    self.outtake_motor.set(0.25)                            
                               
                                else:
                                    #self.stage += 1
                                    self.stage = 1

             
            else:
                print("no")
                print(self.timer.get())


        except:
            print(f"[robot] Caught exception at motor intake {e}")
         
            


    def autonomousInit(self):
        #self.timer = None #wpilib.Timer()
        #self.timer.start()
        self.timer = wpilib.Timer()
        self.stage = 1
        self.timer.start()
    

    def autonomousPeriodic(self):
        # upd camera data
        self.limelight.update()
        data = self.limelight.get_latest()
        
        # print data if existing
        if data is not None:
            print(f"[vision] Camera sees: {data}")
        else:
            print("[vision] Can't see anything boohoo")

        match(self.stage):
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
                pass

    def disabledInit(self):
        print("[robot] Disabled - Stopping camera")
        # Only stop if we aren't in simulation, or if it was actually started
        self.limelight.stop()
        """This runs once when the robot is disabled.
        print("[robot] Disabled - Stopping camera")
        print(self.limelight)
        self.limelight.stop()
        def disabledInit(self):"""
       

if __name__ == "__main__":
    import robotpy
    robotpy.main()
"""if __name__ == "__main__":
    wpilib.run(MyRobot)"""







"""
            if self.intake_motor.get() == 1 and not self.firstDelay: # quarter of a full rotation
                self.outtake_motor.set(-self.intake_axis)
                self.firstDelay = True
            else:
                if self.firstDelay and self.outtake_motor.get() < 0.25: # imitate release
                    self.outtake_motor.set(0)
                    self.firstDelay = False
              
        except Exception as e:
            print(f"[robot] Caught exception at motor intake {e}")"""