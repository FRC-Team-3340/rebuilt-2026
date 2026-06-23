import phoenix5
from wpilib import SmartDashboard
import modules.constants as constants

def _deadband(value: float, threshold: float = constants.DRIVE_DEADBAND) -> float: 
    return value if abs(value) > threshold else 0.0


def _scale(value: float) -> float:
    return value * constants.DRIVE_SCALE


class Drivetrain:
    def __init__(self):
        self._right1 = phoenix5.WPI_TalonSRX(constants.DRIVETRAIN_RIGHT_1)
        self._right2 = phoenix5.WPI_TalonSRX(constants.DRIVETRAIN_RIGHT_2)
        self._left1  = phoenix5.WPI_TalonSRX(constants.DRIVETRAIN_LEFT_1)
        self._left2  = phoenix5.WPI_TalonSRX(constants.DRIVETRAIN_LEFT_2)

        # Left side is mechanically reversed
        self._left1.setInverted(True)
        self._left2.setInverted(True)

    def tank_drive(self, left_raw: float, right_raw: float) -> float:
        left  = _scale(_deadband(left_raw))
        right = _scale(_deadband(right_raw))

        

        self._set_left(left)
        self._set_right(right)

        return left, right

    def stop(self) -> None:
        self._set_left(0)
        self._set_right(0)

    # helpers

    def _set_left(self, power: float) -> None:
        self._left1.set(phoenix5.ControlMode.PercentOutput, power)
        self._left2.set(phoenix5.ControlMode.PercentOutput, power)

    def _set_right(self, power: float) -> None:
        self._right1.set(phoenix5.ControlMode.PercentOutput, power)
        self._right2.set(phoenix5.ControlMode.PercentOutput, power)