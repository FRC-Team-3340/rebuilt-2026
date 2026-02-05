import wpilib
import ctre

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
      
        self.motor = ctre.WPI_TalonSRX(2)
        
    

    def teleopPeriodic(self):
      
        motor_speed = 0.5  
        self.motor.set(ctre.ControlMode.PercentOutput, motor_speed)

