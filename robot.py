import wpilib
import phoenix5
from wpilib import Joystick
import rev

from modules.components.autonomous import AprilTagAuto

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Drivetrain
        #left side
        self.talon1 = phoenix5.WPI_TalonSRX(1)
        self.talon2 = phoenix5.WPI_TalonSRX(2)
        #right side
        self.talon3 = phoenix5.WPI_TalonSRX(3)
        self.talon4 = phoenix5.WPI_TalonSRX(4)


        # Intake + Shooter
        self.talon5 = phoenix5.WPI_TalonSRX(5)  # intake
        self.talon6 = phoenix5.WPI_TalonSRX(6)  # shooter

        # Sparks, Climbers
        self.spark1 = rev.SparkMax(7, rev.SparkLowLevel.MotorType.kBrushless)
        self.spark2 = rev.SparkMax(8, rev.SparkLowLevel.MotorType.kBrushless)

        #Gets joystick 0 in driver station
        self.joystick = Joystick(0)
    
        # Timer for delayed intake
        self.intake_timer = wpilib.Timer()
        self.intake_delay_active = False

        # Climber settings
        self.climber1_timer = wpilib.Timer()
        self.climber2_timer = wpilib.Timer()
        self.climb_time = 5 # seconds for climber to go down
        self.climb1_difference = 0
        self.climb2_difference = 0

        self.climber1_encoder = self.spark1.getEncoder()
        self.climber2_encoder = self.spark2.getEncoder()
        
        self.climber1_encoder.setPosition(0)
        self.climber2_encoder.setPosition(0)
        
        self.spark1.enableSoftLimit(rev.SoftLimitDirection.kForward, True)
        self.spark1.enableSoftLimit(rev.SoftLimitDirection.kReverse, True)
        self.spark2.enableSoftLimit(rev.SoftLimitDirection.kForward, True)
        self.spark2.enableSoftLimit(rev.SoftLimitDirection.kReverse, True)
        
        self.spark1.setSoftLimit(rev.SoftLimitDirection.kForward, 150.0) # changed to 20 --> for inches
        self.spark1.setSoftLimit(rev.SoftLimitDirection.kReverse, 0)
        self.spark2.setSoftLimit(rev.SoftLimitDirection.kForward, 150.0) # changed to 20 --> for inches
        self.spark2.setSoftLimit(rev.SoftLimitDirection.kReverse, 0)


        self.GEAR_RATIO = 48.0 # change
        self.SPOOL_CIRCUMFERENCE = 2.6 # changed
        self.TARGET_HEIGHT = 28.0 # change to actual height

        # Math: (1 Rotation / Gear Ratio) * Circumference = Inches per motor rotation
        self.position_factor = self.SPOOL_CIRCUMFERENCE / self.GEAR_RATIO

        self.climber1_encoder.setPositionConversionFactor(self.position_factor)
        self.climber2_encoder.setPositionConversionFactor(self.position_factor)


        # init auto
        self.auto = AprilTagAuto(
            self.talon1,
            self.talon2,
            self.talon3,
            self.talon4,
            self.talon5,
            self.talon6
        )

        self.TARGET_ROTATIONS = (self.TARGET_HEIGHT / self.SPOOL_CIRCUMFERENCE) * self.GEAR_RATIO

        
    def motor_rotations_to_height(self, motor_rotations):
        return (motor_rotations / self.GEAR_RATIO) * self.SPOOL_CIRCUMFERENCE
    
    def teleopPeriodic(self):

        # gets raw axis for the joysticks and trigers
        leftxaxis = self.joystick.getRawAxis(0)
        leftyaxis = self.joystick.getRawAxis(1)
        lefttrigger = self.joystick.getRawAxis(2)
        righttrigger = self.joystick.getRawAxis(3)
        rightxaxis = self.joystick.getRawAxis(4)
        rightyaxis = self.joystick.getRawAxis(5)
        # gets raw axis for the buttons
        a_button = self.joystick.getRawButton(1)
        b_button = self.joystick.getRawButton(2)
        x_button = self.joystick.getRawButton(3)
        leftbutton = self.joystick.getRawButton(5)
        rightbutton = self.joystick.getRawButton(6)

        def db(x, d=0.15):
            return x if abs(x) > d else 0

        # sets the limit of the drive train
        def scale(x):
            return x * 0.5

        # Drivetrain power
        left_power = scale(db(leftyaxis))
        right_power = scale(db(rightyaxis))

        # Shooter + intake
        shooter_power = 0
        intake_power = 0

        # SHOOTER TRIGGER
        if righttrigger > 0.2:
            shooter_power = 0.8

            # Start the 1 second delay
            if not self.intake_delay_active:
                self.intake_delay_active = True
                self.intake_timer.reset()
                self.intake_timer.start()
                

        # After 1 second, start intake
        if self.intake_delay_active and self.intake_timer.hasElapsed(1):
            intake_power = 0.9

        # If shooter is released, stop
        if righttrigger <= 0.2:
            shooter_power = 0
            intake_power = 0
            self.intake_delay_active = False
            self.intake_timer.stop()

        # INTAKE + SHOOTER
        self.talon5.setInverted(True)
        
        if lefttrigger > 0.2:
            intake_power =  -0.5
            shooter_power = 0.5
        if lefttrigger < 0.2 and righttrigger < 0.2:
            intake_power =  0
            shooter_power = 0

        if a_button: # kicks the ball out of intake if it gets stuck
            intake_power =  0.65
            shooter_power = -0.65

        self.talon5.set(phoenix5.ControlMode.PercentOutput, intake_power)
        self.talon6.set(phoenix5.ControlMode.PercentOutput, shooter_power)
        print(leftbutton, rightbutton)
        
        
        # CLIMBER
        if x_button:
            self.spark1.setIdleMode(rev.SparkMax.IdleMode.kCoast)
            self.spark2.setIdleMode(rev.SparkMax.IdleMode.kCoast)
            
            if self.climber1_encoder.getPosition() >= self.TARGET_ROTATIONS: # do we need only one? One acting as the leader and the other following?
                self.spark1.set(0)
            else:
                self.spark1.set(-0.5)

            if self.climber2_encoder.getPosition() >= self.TARGET_ROTATIONS: # do we need only one? One acting as the leader and the other following?
                self.spark2.set(0)
            else:
                self.spark2.set(0.5)
        
        elif b_button:
            self.spark1.setIdleMode(rev.SparkMax.IdleMode.kCoast)
            self.spark2.setIdleMode(rev.SparkMax.IdleMode.kCoast)
            
            if self.climber1_encoder.getPosition() >= self.TARGET_ROTATIONS: # do we need only one? One acting as the leader and the other following?
                self.spark1.set(0)
            else:
                self.spark1.set(-0.5)

            if self.climber2_encoder.getPosition() >= self.TARGET_ROTATIONS: # do we need only one? One acting as the leader and the other following?
                self.spark2.set(0)
            else:
                self.spark2.set(0.5)

        
        else:
            self.spark1.setIdleMode(rev.SparkMax.IdleMode.kBrake)
            self.spark2.setIdleMode(rev.SparkMax.IdleMode.kBrake)
            self.spark1.set(0)
            self.spark2.set(0)
    

        # DRIVETRAIN
        self.talon1.set(phoenix5.ControlMode.PercentOutput, right_power)
        self.talon2.set(phoenix5.ControlMode.PercentOutput, right_power)
        self.talon3.set(phoenix5.ControlMode.PercentOutput, -left_power)
        self.talon4.set(phoenix5.ControlMode.PercentOutput, -left_power)

    def autonomousInit(self):
        """Drives forward at 50% for 2 seconds."""
        self.auto.init()
        self.auto_timer = wpilib.Timer()
        self.auto_timer.start()

        # Start driving forward
        self.talon1.set(phoenix5.ControlMode.PercentOutput, 0.5)
        self.talon2.set(phoenix5.ControlMode.PercentOutput, 0.5)
        self.talon3.set(phoenix5.ControlMode.PercentOutput, -0.5)
        self.talon4.set(phoenix5.ControlMode.PercentOutput, -0.5)

    def autonomousPeriodic(self):
        """Stop motors after 2 seconds."""
        if self.auto_timer.get() >= 2.0:
            self.talon1.set(phoenix5.ControlMode.PercentOutput, 0)
            self.talon2.set(phoenix5.ControlMode.PercentOutput, 0)
            self.talon3.set(phoenix5.ControlMode.PercentOutput, 0)
            self.talon4.set(phoenix5.ControlMode.PercentOutput, 0)
        
if __name__ == "__main__":
    wpilib.run(MyRobot)
