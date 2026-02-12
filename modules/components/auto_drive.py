#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2

from subsystems.candrivesubsystem import CANDriveSubsystem


class AutoDrive(commands2.Command):
    def __init__(
        self, driveSubsystem: CANDriveSubsystem, xSpeed: float, zRotation: float
    ) -> None:
        super().__init__()
        self.driveSubsystem = driveSubsystem
        self.xSpeed = xSpeed
        self.zRotation = zRotation
        self.addRequirements(self.driveSubsystem)

    def execute(self) -> None:
        self.driveSubsystem.driveArcade(self.xSpeed, self.zRotation)

    def end(self, interrupted: bool) -> None:
        self.driveSubsystem.driveArcade(0, 0)

    def isFinished(self) -> bool:
        return False