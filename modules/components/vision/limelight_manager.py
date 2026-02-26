import wpilib

class LimelightManager:
    def __init__(self):
        self.limelight = None
        self.latest_result = None
        self.connected = False

    def connect(self):
        # DO NOT REMOVE THIS - It must be the very first thing
        if wpilib.RobotBase.isSimulation():
            return

        # Move the import INSIDE the if-statement so it never loads during tests
        try:
            import limelight 
            self.limelight = limelight.Limelight("10.33.40.11")
            self.connected = True
        except Exception as e:
            print(f"[limelight] Connection failed: {e}")
            self.connected = False
    
    def start(self):
        if not self.connected:
            self.connect()
    
    def update(self):
        # If we are in simulation, exit immediately before importing limelightresults
        if wpilib.RobotBase.isSimulation() or not self.connected:
            return
        
        try:
            import limelightresults
            raw_result = self.limelight.get_latest_results()
            if raw_result:
                self.latest_result = limelightresults.parse_results(raw_result)
        except Exception as e:
            pass # Avoid spamming the console
    
    def get_latest(self):
        return self.latest_result
    
    def stop(self):
        self.connected = False
        self.limelight = None
