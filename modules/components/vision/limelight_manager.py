import wpilib
import limelightresults

class LimelightManager:
    def __init__(self):
        self.limelight = None
        self.latest_result = None
        self.connected = False

    def connect(self):
        # DO NOT REMOVE THIS - It must be the very first thing

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
        if not self.connected or self.limelight is None:
            return Exception("Limelight not connected")
        try:
            raw_result = self.limelight.get_latest_results()
            print(f"[limelight] Raw results: {raw_result}")
            if raw_result:
                self.latest_result = limelightresults.parse_results(raw_result)
                print(f"[limelight] Parsed results: {self.latest_result}")
        except Exception as e:
            print(f"[limelight] Error parsing results: {e}")
    
    def get_latest(self):
        return self.latest_result
    
    def stop(self):
        self.connected = False
        self.limelight = None
