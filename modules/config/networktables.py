import time
from networktables import NetworkTables

# Team number (replace with your team number)
TEAM = 3340 

# To use with a robot, you need to tell the client the IP address of the server (the roboRIO)
# It is recommended to use the startDSClient() method to get the address from the Driver Station
# or use a static IP, e.g., 10.TE.AM.2

# Initialize NetworkTables client
# By default, it will connect to the robot IP address found by the Driver Station
# If the DS is not running, you can manually set the server IP
NetworkTables.initialize(server='10.33.40.2') # Replace XX and YY with your team number

# Get the 'SmartDashboard' table
sd = NetworkTables.getTable("SmartDashboard")

# Or get a specific table, e.g., for vision data
limelight = NetworkTables.getTable("limelight")

# Listen for changes (optional, but useful)
def valueChanged(table, key, value, isNew):
    print(f"Key '{key}' in table '{table}' changed to '{value}'")

# Add a listener to the 'Vision' table
# vision_table.addEntryListener(valueChanged) # This uses the NT3 API

# Modern NT4 API uses publishers and subscribers
# Create a subscriber for the 'targetX' number topic (specify a default value)
targetX_sub = limelight.getNumberTopic("targetX").subscribe(0)
# Create a publisher for a boolean topic
targetFound_pub = limelight.getBooleanTopic("targetFound").publish()


print("Connected to NetworkTables. Waiting for data...")

try:
    while True:
        # Get the current value of 'targetX'
        x_value = targetX_sub.get()
        
        # Publish a value back to the robot
        targetFound_pub.set(x_value != 0)

        print(f"Received targetX: {x_value}, Published targetFound: {x_value != 0}")
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    # Close NetworkTables connection
    NetworkTables.shutdown()
