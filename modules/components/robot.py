import wpilib
import phoenix5
from wpilib import Joystick
import rev

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.talon1 = phoenix5.WPI_TalonSRX(3)
        self.talon2 = phoenix5.WPI_TalonSRX(4)
        self.sparkmax1 = rev.SparkMax(2, rev.SparkLowLevel.MotorType.kBrushless)
        self.joystick = Joystick(0)

    def teleopPeriodic(self):
        Left_X_Axis = self.joystick.getRawAxis(0)  # Left stick X-axis
        Left_Y_Axis = self.joystick.getRawAxis(1)  # Left stick Y-axis    
        left_trigger = self.joystick.getRawAxis(2) # Left trigger for motor speed
        right_trigger = self.joystick.getRawAxis(3)  # Right trigger for motor speed
        Right_x_Axis = self.joystick.getRawAxis(4)  # Right stick X-axis
        Right_y_Axis = self.joystick.getRawAxis(5)  # Right stick Y-axis

        # --- moving Forward and Backwards ---
      #  if Left_Y_Axis > 0.2 or Left_Y_Axis < -0.2: 
       #     self.talon1.set(phoenix5.ControlMode.PercentOutput, Left_Y_Axis /10)
       #     self.talon2.set(phoenix5.ControlMode.PercentOutput, Left_Y_Axis / 10)
       # if Right_x_Axis < 0.2 and Right_x_Axis > -0.2:
       #     self.talon1.set(phoenix5.ControlMode.PercentOutput, 1)
        #    self.talon2.set(phoenix5.ControlMode.PercentOutput, 1)
        '''
        if Left_X_Axis > 0.1: # code for intake
            self.talon_.set(phoenix5.ControlMode.PercentOutput, Left_X_Axis)
            self.talon_.set(phoenix5.ControlMode.PercentOutput, Left_X_Axis)
        if Left_Y_Axis > 0.1:
            self.talon_.set(phoenix5.ControlMode.PercentOutput, Left_Y_Axis)
            self.talon_.set(phoenix5.ControlMode.PercentOutput, Left_X_Axis)
        if left_trigger > 0.1:
            self.talon_.set(phoenix5.ControlMode.PercentOutput, left_trigger)
            
        if right_trigger > 0.1:
            self.talon_.set(phoenix5.ControlMode.PercentOutput, right_trigger)
        
        if Right_x_Axis > 0.1:
            self.talon_.set(phoenix5.ControlMode.PercentOutput, Right_x_Axis)
        
        if Right_y_Axis > 0.1:
            self.talon_.set(phoenix5.ControlMode.PercentOutput, Right_y_Axis)


        # Drive control
        #self.drive(Left_Y_Axis, Right_x_Axis)

        '''

        self.sparkmax1.set(right_trigger / 10)
        self.talon1.set(phoenix5.ControlMode.PercentOutput, left_trigger / 10)
        print(right_trigger, left_trigger)
    
    def testInit(self):
        """This function is called once each time the robot enters test mode."""

    def testPeriodic(self):
        """This function is called periodically during test mode."""

    def teleopInit(self):
        """This function is called once each time the robot enters teleoperated mode."""
    
    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""



if __name__ == "__main__":
    wpilib.run(MyRobot)
