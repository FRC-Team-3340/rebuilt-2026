# All CAN IDs and changeable values live here.
# Change numbers here ONLY PLEASE.

# Drivetrain CAN IDs
DRIVETRAIN_RIGHT_1 = 1
DRIVETRAIN_RIGHT_2 = 2
DRIVETRAIN_LEFT_1  = 3
DRIVETRAIN_LEFT_2  = 4

# Shooter / Intake CAN IDs
INDEXER_ID      = 5
SHUFFLER_ID     = 7
SHOOTER_ID      = 6
INTAKE_ID       = 8    # SparkMax (brushless)

# Joystick
JOYSTICK_PORT = 0

# Axes
AXIS_LEFT_X      = 0
AXIS_LEFT_Y      = 1
AXIS_LEFT_TRIG   = 2
AXIS_RIGHT_TRIG  = 3
AXIS_RIGHT_X     = 4
AXIS_RIGHT_Y     = 5

# Buttons
BTN_A = 1
BTN_B = 2
BTN_X = 3
BTN_Y = 4
BTN_LEFT_BUMPER  = 5
BTN_RIGHT_BUMPER = 6

# Deadband / scaling
DRIVE_DEADBAND   = 0.15
DRIVE_SCALE      = 0.95
TRIGGER_DEADBAND = 0.2

# Shooter / Intake speeds (also written to SmartDashboard)
SHOOTER_SPEED                =  0.50
INTAKE_SPEED                 =  0.65
REVERSE_INTAKE_SPEED         =  -0.65  # FIX: was -0.65, but reverse() already negates this value
REVERSE_INTAKE_SHOOTER_SPEED =  0.65
REVERSE_INDEXER_SPEED        =  0.70  # FIX: was -0.70, but reverse() already negates this value
INDEXER_SPEED                =  0.70
SHUFFLER_SPEED               = 1

# Timing
SHOOTER_SPINUP_DELAY = 1.0   # seconds before intake/indexer engage after shooter starts

# Camera
CAMERA_WIDTH  = 320
CAMERA_HEIGHT = 240
CAMERA_FPS    = 30