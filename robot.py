# TODO: insert robot code here

import wpilib
import wpilib.drive
import phoenix6
import phoenix5 as p5
import rev


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

        self.motors = self.setup_neos([2])
        self.controller = wpilib.XboxController(0)
        self.stick = wpilib.Joystick(0)

        self.first_motor = self.motors[2]

    def setup_neos(self, can_ids: list):
        """
        Inits a NEO dictionary with given CAN IDs
        """

        neo_dict = {}

        for can_id in can_ids:
            motor = rev.SparkMax(
                can_id, rev.SparkLowLevel.MotorType.kBrushless)

            neo_dict[can_id] = motor

        print(
            f"[!] Succesfully init'ed NEOs on CAN IDs: {list(neo_dict.keys())}")

        return neo_dict

    def setup_talonsrx(self, can_ID: list):
        '''
        Creates dictionary of Talon SRX motor controllers with provided CAN IDs.

        '''

        talon_srxs = {}

        for id in can_ID:
            motor = p5.TalonSRX(id)

            talon_srxs[can_ID] = motor

        return neo_dict

    def testPeriodic(self):
        speed = -self.stick.getRawAxis(1)

        if abs(speed) < 0.1:  # don't move if move is slight
            speed = 0
            print('joystick speed too small')
        else:
            print('joystick speed good enough')
            self.first_motor.set(speed)
        pass
