import wpilib
import phoenix5
from wpilib import Joystick
import rev    
import limelight
import limelightresults
import json
import time

"""
just in case this code fails..
"""

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        print("[motor-connect] Connecting motors..")
        try:
            self.talon1 = phoenix5.WPI_TalonSRX(3)
            self.sparkmax1 = rev.SparkMax(2, rev.SparkLowLevel.MotorType.kBrushless)
            self.joystick = Joystick(0)
        except RuntimeError or KeyboardInterrupt:
            print("[motor-connect] An error has occurred while connecting motors")
        finally:
            print("[motor-connect] Successfully connected ")

    def teleopPeriodic(self):
        right_trigger = self.joystick.getRawAxis(3)  # Right trigger for motor speed
        left_trigger = self.joystick.getRawAxis(2)
        self.sparkmax1.set(right_trigger / 10)
        self.talon1.set(phoenix5.ControlMode.PercentOutput, left_trigger / 10)
        print(right_trigger, left_trigger)
    

    def testInit(self):
        """This function is called once each time the robot enters test mode.""" 

        print("[limelight-connect] Connecting limelight..")
        try:
            self.discovered_limelights = limelight.discover_limelights()
            print("[limelight-connect] Discovered: ", self.discovered_limelights)
            if self.discovered_limelights:
                limelight_address = self.discovered_limelights[0] 
                self.ll = limelight.Limelight(limelight_address)
            
                # print the current pipeline settings
                print(self.ll.get_pipeline_atindex(0))

                # update the current pipeline and flush to disk
                pipeline_update = {
                'area_max': 98.7,
                'area_min': 1.98778
                }
                self.ll.update_pipeline(json.dumps(pipeline_update),flush=1)

                print(self.ll.get_pipeline_atindex(0))

                # switch to pipeline 1
                self.ll.pipeline_switch(1)

                # update custom user data
                self.ll.update_python_inputs([4.2,0.1,9.87])
        except RuntimeError or KeyboardInterrupt:
            print("[limelight-connect] An error has occurred while connecting limelight")
        finally:
            print("[limelight-connect] Successfully connected limelight")

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        try:
            self.ll.enable_websocket()

            while self.isTest():
                result = self.ll.get_latest_results()
                parsed_result = limelightresults.parse_results(result)
                if parsed_result is not None:
                    print("valid targets: ", parsed_result.validity)
                    
                    for tag in parsed_result.fiducialResults:
                        print("Target ID: ", tag.fiducial_id)
                time.sleep(0.5)  # Set this to 0 for max fps --> currently set for half of the fps (~20)


        except RuntimeError or KeyboardInterrupt:
            print("[limelight] An error occurred during limelight processing")
        finally:
            self.ll.disable_websocket()
            print("[limelight] Disabling websocket")
    def teleopInit(self):
        """This function is called once each time the robot enters teleoperated mode."""
    
    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""



if __name__ == "__main__":
    wpilib.run(MyRobot)
