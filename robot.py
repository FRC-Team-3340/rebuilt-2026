import wpilib
import phoenix5
from wpilib import Joystick, SmartDashboard
import rev
from modules.components.autonomous import AprilTagAuto

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):

        self.GEAR_RATIO = 48.0 # change
        self.SPOOL_CIRCUMFERENCE = 2.6 # changed
        self.TARGET_HEIGHT = 11.0 # change to actual height

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

        self.talon5.setInverted(True)


        # Sparks, Climbers
        self.spark1 = rev.SparkMax(7, rev.SparkLowLevel.MotorType.kBrushless)
        self.spark2 = rev.SparkMax(8, rev.SparkLowLevel.MotorType.kBrushless)

        #Gets joystick 0 in driver station
        self.joystick = Joystick(0)
    
        # Timer for delayed intake
        self.intake_timer = wpilib.Timer()
        self.intake_delay_active = False
        
        # 1. Create the configuration object
        climber_config = rev.SparkMaxConfig()

        # 2. Configure the Soft Limits
        (climber_config.softLimit
            .forwardSoftLimitEnabled(True)
            .reverseSoftLimitEnabled(True)
            .forwardSoftLimit(self.TARGET_HEIGHT) # Set to 150 rotations (or 8.0 if using inches)
            .reverseSoftLimit(0.0))
        
        climber_config.encoder.positionConversionFactor(self.SPOOL_CIRCUMFERENCE / self.GEAR_RATIO) # Set the position conversion factor to convert rotations to inches 

        # Math: (1 Rotation / Gear Ratio) * Circumference = Inches per motor rotation
        self.position_factor = self.SPOOL_CIRCUMFERENCE / self.GEAR_RATIO

        self.spark1.configure(climber_config, 
                              rev.ResetMode.kResetSafeParameters, 
                              rev.PersistMode.kPersistParameters)
        
        self.spark2.configure(climber_config, 
                              rev.ResetMode.kResetSafeParameters, 
                              rev.PersistMode.kPersistParameters)
        
        self.climber1_encoder = self.spark1.getEncoder()
        self.climber2_encoder = self.spark2.getEncoder()
        
        self.climber1_encoder.setPosition(0)
        self.climber2_encoder.setPosition(0)

        # init auto
        self.auto = AprilTagAuto(
            self.talon1,
            self.talon2,
            self.talon3,
            self.talon4,
            self.talon5,
            self.talon6
        )

        SmartDashboard.putNumber("Shooter Speed", 0.8)
        SmartDashboard.putNumber("Intake Speed", 0.9)
        SmartDashboard.putNumber("Reverse Intake Speed", 0.65)
        SmartDashboard.putNumber("Reverse Intake Shooter Speed", -0.65)
    
    def teleopPeriodic(self):
        intake_speed = SmartDashboard.getNumber("Intake Speed", 0.9)
        shooter_speed = SmartDashboard.getNumber("Shooter Speed", 0.8)
        reverse_intake_speed = SmartDashboard.getNumber("Reverse Intake Speed", 0.65)
        reverse_intake_shooter_speed = SmartDashboard.getNumber("Reverse Intake Shooter Speed", -0.65)

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
            shooter_power = shooter_speed

            # Start the 1 second delay
            if not self.intake_delay_active:
                self.intake_delay_active = True
                self.intake_timer.reset()
                self.intake_timer.start()
                

        # After 1 second, start intake
        if self.intake_delay_active and self.intake_timer.hasElapsed(1):
            intake_power = intake_speed

        # If shooter is released, stop
        if righttrigger <= 0.2:
            shooter_power = 0
            intake_power = 0
            self.intake_delay_active = False
            self.intake_timer.stop()

        # INTAKE + SHOOTER
        
        if lefttrigger > 0.2:
            intake_power =  reverse_intake_speed
            shooter_power = reverse_intake_shooter_speed
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
            
            if self.climber1_encoder.getPosition() >= self.TARGET_HEIGHT: # do we need only one? One acting as the leader and the other following?
                self.spark1.set(0)
            else:
                self.spark1.set(-0.5)

            if self.climber2_encoder.getPosition() >= self.TARGET_HEIGHT: # do we need only one? One acting as the leader and the other following?
                self.spark2.set(0)
            else:
                self.spark2.set(0.5)
        
        elif b_button:
            self.spark1.setIdleMode(rev.SparkMax.IdleMode.kCoast)
            self.spark2.setIdleMode(rev.SparkMax.IdleMode.kCoast)
            
            if self.climber1_encoder.getPosition() >= self.TARGET_ROTATIONS: # do we need only one? One acting as the leader and the other following?
                self.spark1.set(0)
            else:
                self.spark1.set(0.5)

            if self.climber2_encoder.getPosition() >= self.TARGET_ROTATIONS: # do we need only one? One acting as the leader and the other following?
                self.spark2.set(0)
            else:
                self.spark2.set(-0.5)

        
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
