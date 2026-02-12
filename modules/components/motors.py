from phoenix5 import NeutralMode, WPI_TalonSRX, WPI_VictorSPX, IMotorController
from rev import SparkMax, SparkLowLevel


def createSparkMax(can_id: int, motor_type: SparkLowLevel.MotorType) -> SparkMax:
    motor = SparkMax(can_id, motor_type)

    return motor

def createVictorSPX(can_id: int, neutral_mode: NeutralMode) -> WPI_VictorSPX:
    motor = WPI_VictorSPX(can_id)
    motor.setNeutralMode(neutral_mode)

    return motor

def createTalonSRX(can_id: int, neutral_mode: NeutralMode) -> WPI_TalonSRX:
    motor = WPI_TalonSRX(can_id)
    motor.setNeutralMode(neutral_mode)

    return motor
    
def createSparkMaxEncoder(controller: SparkMax):
    return controller.getEncoder()

                    