import wpilib
from wpilib import Joystick
from cscore import CameraServer

import modules.constants as constants
from modules.drivetrain import Drivetrain
from modules.shooter_intake import ShooterIntake

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drivetrain = Drivetrain()
        self.shooter_intake = ShooterIntake()
        self.joystick = Joystick(constants.JOYSTICK_PORT)

        camera = CameraServer.startAutomaticCapture()
        camera.setResolution(constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT)
        camera.setFPS(constants.CAMERA_FPS)

    def teleopPeriodic(self):
        left_trig = self.joystick.getRawAxis(constants.AXIS_LEFT_TRIG)
        right_trig = self.joystick.getRawAxis(constants.AXIS_RIGHT_TRIG)
        left_y = self.joystick.getRawAxis(constants.AXIS_LEFT_Y)
        right_y = self.joystick.getRawAxis(constants.AXIS_RIGHT_Y)
        b_button = self.joystick.getRawButton(constants.BTN_B)

        self.drivetrain.tank_drive(left_y, right_y)

        if b_button:
            self.shooter_intake.eject()
        
        if left_trig > constants.TRIGGER_DEADBAND:
            self.shooter_intake.intake()
        
        if right_trig > constants.TRIGGER_DEADBAND:
            self.shooter_intake.shoot()

        if right_trig <= constants.TRIGGER_DEADBAND and left_trig <= constants.TRIGGER_DEADBAND and not b_button:
            self.shooter_intake.idle()

    # The shooter_intake.shoot function call handles the spinup delay internally. please do not change...

    def autonomousInit(self):
        self.shooter_intake.idle()

    def autonomousPeriodic(self):
        self.drivetrain.stop()
        self.shooter_intake.shoot()

    def disabledInit(self):
        self.drivetrain.stop()
        self.shooter_intake.idle()


if __name__ == "__main__":
    wpilib.run(MyRobot)