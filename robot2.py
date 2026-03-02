#Import necessary packages

import wpilib
import phoenix5s
from wpilib import Joystick
import rev

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
        self.talon5 = phoenix5.WPI_TalonSRX(5)  # intake motor
        self.talon6 = phoenix5.WPI_TalonSRX(6)  # shooter motor

        # Sparks, Climbers
        self.spark1 = rev.SparkMax(7, rev.SparkLowLevel.MotorType.kBrushless)
        self.spark2 = rev.SparkMax(8, rev.SparkLowLevel.MotorType.kBrushless)

        #Gets joystick 0 in driver station
        self.joystick = Joystick(0)

        # Timer for delayed shooter
        self.intake_timer = wpilib.Timer()
        self.intake_delay_active = False

        #inverts talon5 on opposite drive train
        self.talon5.setInverted(True)

    #Code that runs when enabled
    def teleopPeriodic(self):

        #Gets the remote axis

        #Get raw axis are from joysticks and triggers
        lx = self.joystick.getRawAxis(0)
        ly = self.joystick.getRawAxis(1)
        lt = self.joystick.getRawAxis(2)
        rt = self.joystick.getRawAxis(3)
        rx = self.joystick.getRawAxis(4)
        ry = self.joystick.getRawAxis(5)

        #Raw buttons are from left and right bumbers//to be changed to d pad
        lb = self.joystick.getRawButton(4)
        rb = self.joystick.getRawButton(5)

        def db(x, d=0.15):
            return x if abs(x) > d else 0

        # Sets the speed limit you can run the drive train
        def scale(x):
            return x * 0.1

        # Drivetrain power
        left_power = scale(db(ly))
        right_power = scale(db(ry))

        # Shooter + intake
        shooter_power = 0
        intake_power = 0

        # SHOOTER TRIGGER
        if rt > 0.2:
            shooter_power = 0.9

            # Start the 1 second delay on trigger press
            if not self.intake_delay_active:
                self.intake_delay_active = True
                self.intake_timer.reset()
                self.intake_timer.start()

        # After 1 second, start shooter
        if self.intake_delay_active and self.intake_timer.hasElapsed(0.5):
            #shooter running at 90% power
            intake_power = 0.9

        # DRIVETRAIN
        
        self.talon1.set(phoenix5.ControlMode.PercentOutput, right_power)
        self.talon2.set(phoenix5.ControlMode.PercentOutput, right_power)
        self.talon3.set(phoenix5.ControlMode.PercentOutput, -left_power)
        self.talon4.set(phoenix5.ControlMode.PercentOutput, -left_power)

       
        # If shooter is released, stop everything
        if rt <= 0.2:
            shooter_power = 0
            intake_power = 0
            self.intake_delay_active = False
            self.intake_timer.stop()
            self.intake_timer.reset()
        
        # INTAKE + SHOOTER
        elif lt > 0.2:
            intake_power =  -0.7
            shooter_power = 0.7
        self.talon5.set(phoenix5.ControlMode.PercentOutput, intake_power)
        self.talon6.set(phoenix5.ControlMode.PercentOutput, shooter_power)

        # sparks for climber
        if lb == True:
            self.spark1.set(0.2)
            self.spark2.set(-0.2)

        elif rb == True:
            self.spark1.set(-0.2)
            self.spark2.set(0.2)
        else:
            self.spark1.set(0)
            self.spark2.set(0)

        # debug for viewing the axis
        print(f"AXES: 0={lx:.2f} 1={ly:.2f} 2={lt:.2f} 3={rt:.2f} 4={rx:.2f} 5={ry:.2f} Buttons: 4={lb} 5={rb}")

if __name__ == "__main__":
    wpilib.run(MyRobot)
