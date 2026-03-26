import wpilib

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize PWM port 0 on the roboRIO
        self.pwm0 = wpilib.PWM(0)

    def teleopPeriodic(self):
        # Set the pulse width in MICROSECONDS
        # 1000 = Full Reverse, 1500 = Neutral, 2000 = Full Forward
        self.pwm0.setPulseTime(2000) 

if __name__ == "__main__":
    wpilib.run(MyRobot)
