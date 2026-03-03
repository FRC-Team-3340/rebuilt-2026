import wpilib as wpi
from wpilib import Joystick, SmartDashboard, XboxController
from modules.components.drive import Drive
#from modules.components.climber import Climber
import phoenix5
from phoenix5 import WPI_TalonSRX as SRX
from wpilib import Joystick
import rev

import modules.components.motors as m
class MyRobot(wpi.TimedRobot):
    def robotInit(self):
        self.drive = Drive()
        #self.climber = Climber()
        #self.arm = Arm()
        self.controller = Joystick(0)

        self.cs = wpi.cameraserver.CameraServer()
        self.cs.launch()

        
        # self.mySwitch = LimitSwitch(0)

    # def robotPeriodic(self):

    def testPeriodic(self):
        pass
       # self.arm.initializeArm()
    
    # Assigning buttons on selected controller to
    def teleopPeriodic(self):
        '''forward = (-self.controller.getRawButton(1) + self.controller.getRawButton(2)
                   )/(.5+(abs(self.controller.getRawAxis(0)) > 0.1))
        self.robotDrive.arcadeDrive(
             -self.controller.getLeftY(), -self.controller.getRightX()
        )

         try:
            self.robot_drive.arcadeDrive( 
                xSpeed=forward, zRotation=self.controller.getRawAxis(0))
        except Exception:
            raise Exception'''

        # if self.mySwitch.get() == False:
        self.drive.tankDrive(self.controller.getRawAxis(0),
                                 self.controller.getRawAxis(5))

        
            # self.drive.arcadeDrive(self.controller.getRawAxis(1), self.controller.getRawAxis(4))
#CHECK BINDINGS
        #self.climber.climb(self.controller.getPOV())
        # self.arm.manualArmControl(self.controller.getPOV())
        
        roller_direction = -self.controller.getRawAxis(2) + self.controller.getRawAxis(3)
       # self.arm.activateRollers(roller_direction)

        # if self.controller.getRawButton(1):
        #     self.arm.extendArm()
        # if self.controller.getRawButton(4):
        #     self.arm.retractArm()

    
