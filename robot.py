import wpilib
from wpilib import Joystick, SmartDashboard
from cscore import CameraServer
from wpilib import shuffleboard
from wpilib.shuffleboard import Shuffleboard
import modules.constants as constants
from modules.drivetrain import Drivetrain
from modules.shooter_intake import ShooterIntake


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.left_y = 0.0
        self.right_y = 0.0

        self.drivetrain = Drivetrain()
        self.shooter_intake = ShooterIntake()
        self.joystick = Joystick(constants.JOYSTICK_PORT)

        camera = CameraServer.startAutomaticCapture()
        camera.setResolution(constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT)
        camera.setFPS(constants.CAMERA_FPS)

        self.auto_active = False

        # Anti-drift brake force and last directions
        self.BRAKE_FORCE = 0.12
        self.last_left_dir = 0.0   # -1, 0, or 1
        self.last_right_dir = 0.0  # -1, 0, or 1

        SmartDashboard.putNumber("Left Train", 0.0)
        SmartDashboard.putNumber("Right Train", 0.0)
        
        SmartDashboard.putBoolean("Shooting", False)
        SmartDashboard.putBoolean("Intaking", False)
        SmartDashboard.putBoolean("Ejecting", False)
        SmartDashboard.putBoolean("Precision Mode", False)
    

    def handle_status(self, shooting=False, intaking=False, ejecting=False):
        SmartDashboard.putBoolean("Shooting", shooting)
        SmartDashboard.putBoolean("Intaking", intaking)
        SmartDashboard.putBoolean("Ejecting", ejecting)


    def teleopPeriodic(self):
        # Read joystick axes/buttons
        left_y = self.joystick.getRawAxis(constants.AXIS_LEFT_Y)
        right_y = self.joystick.getRawAxis(constants.AXIS_RIGHT_Y)
        left_trig = self.joystick.getRawAxis(constants.AXIS_LEFT_TRIG)
        right_trig = self.joystick.getRawAxis(constants.AXIS_RIGHT_TRIG)
        b_button = self.joystick.getRawButton(constants.BTN_B)
        right_bumper = self.joystick.getRawButton(6)  # precision / aiming mode

        # --- PRECISION SCALING (RIGHT BUMPER) ---
        # When held, scale down drive power for aiming
        if right_bumper:
            SmartDashboard.putBoolean("Precision Mode", True)
            scale = 0.4  # tweak if you want slower/faster aiming
            left_y *= scale
            right_y *= scale
        else:
            SmartDashboard.putBoolean("Precision Mode", False)

        # --- 10% DEADBAND FOR STICK DRIFT ---
        if abs(left_y) < 0.10:
            left_y = 0.0
        if abs(right_y) < 0.10:
            right_y = 0.0

        # --- TRACK LAST DIRECTION (FORWARD/BACKWARD) ---
        # Only update when we're clearly moving (> 20%)
        if abs(left_y) > 0.20:
            self.last_left_dir = 1.0 if left_y > 0 else -1.0
        if abs(right_y) > 0.20:
            self.last_right_dir = 1.0 if right_y > 0 else -1.0

        # --- AUTO "BRAKE" SIMULATION ---
        # If we're in the slow zone (<= 20%) and sticks are centered after deadband,
        # apply a small opposite force to fight momentum.
        max_input = max(abs(left_y), abs(right_y))

        if max_input <= 0.20:
            # Only apply when driver is not actively commanding movement
            if left_y == 0.0 and self.last_left_dir != 0.0:
                left_y = -self.last_left_dir * self.BRAKE_FORCE
            if right_y == 0.0 and self.last_right_dir != 0.0:
                right_y = -self.last_right_dir * self.BRAKE_FORCE

        # Drive with final values
        SmartDashboard.putNumber("Left Train", left_y)
        SmartDashboard.putNumber("Right Train", right_y)
        self.drivetrain.tank_drive(left_y, right_y)

        # --- SHOOTER / INTAKE LOGIC (UNCHANGED) ---
        if b_button:
            self.shooter_intake.eject()
            self.handle_status(ejecting=True)
        elif left_trig > constants.TRIGGER_DEADBAND:
            self.shooter_intake.intake()
            self.handle_status(intaking=True)
        elif right_trig > constants.TRIGGER_DEADBAND:
            self.shooter_intake.shoot()
            self.handle_status(shooting=True)
        else:
            self.handle_status()
            self.shooter_intake.idle()


    def autonomousInit(self):
        self.shooter_intake.idle()
        self.auto_timer = wpilib.Timer()


    def autonomousPeriodic(self):
        if not self.auto_active:
            self.auto_active = True
            self.auto_timer.reset()
            self.auto_timer.start()

        if self.auto_timer.get() <= 1 and self.auto_active:
            # Slow auto drive
            self.drivetrain.tank_drive(-0.20, -0.20)
        else:
            self.drivetrain.stop()
            self.shooter_intake.shoot()


    def disabledInit(self):
        self.drivetrain.stop()
        self.shooter_intake.idle()
        self.auto_active = False


if __name__ == "__main__":
    wpilib.run(MyRobot)