# TODO: insert robot code here

import wpilib
import wpilib.drive
import phoenix6
import rev

from phoenix6 import hardware

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        print("""

        |
        |
        |        REBUILT -- 2026
        |            by yes
        |
        |

        """)

        self.motors = self.setup_talons([2])
        self.controller = wpilib.XboxController(0)
        self.stick = wpilib.Joystick(0)

        self.first_motor = wpilib.Talon(2)
        
        pass

    def setup_neos(self, can_ids: list):
        """
        Inits a NEO dictionary with given CAN IDs
        """

        neo_dict = {}

        for can_id in can_ids:
            motor = rev.SparkMax(can_id, rev.SparkLowLevel.MotorType.kBrushless)
            
            neo_dict[can_id] = motor
        
        print(f"[!] Succesfully init'ed NEOs on CAN IDs: {list(neo_dict.keys())}")
        return neo_dict
    
    def setup_talons(self, can_ids: list):
        """
        Inits a NEO dictionary with given CAN IDs
        """

        talon_dict = {}

        for can_id in can_ids:
            motor = hardware.TalonFX(can_id)
            
            talon_dict[can_id] = motor
        
        print(f"[!] Succesfully init'ed Talons on CAN IDs: {list(talon_dict.keys())}")
        return talon_dict

    def testPeriodic(self):
        """speed = -self.stick.getRawAxis(0)

        if abs(speed) < 0.1: # don't move if move is slight
            speed = 0
        
        self.first_motor.set(speed)
        pass
        speed = 0.5"""
        self.first_motor.set(0.5)

