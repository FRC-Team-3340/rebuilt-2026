"""
Simple Limelight camera wrapper.
Call update() regularly to get fresh data from the camera.
Call get_latest() to "see" what the camera sees.
"""


class LimelightManager:
    def __init__(self):
        self.limelight = None
        self.latest_result = None
        self.connected = False
    
    def start(self):
        """Try to connect to the Limelight camera."""
        try:
            import limelight
            import limelightresults
            
            # Find any limelights on the network
            print("[limelight] Looking for cameras...")
            discovered = limelight.discover_limelights()
            
            if discovered:
                address = discovered[0]
                print(f"[limelight] Found camera at {address}")
                self.limelight = limelight.Limelight(address)
                self.connected = True
            else:
                print("[limelight] No cameras found")
                self.connected = False
                
        except Exception as e:
            print(f"[limelight] Could not connect: {e}")
            self.connected = False
    
    def update(self):
        """Get fresh data from the camera."""
        if not self.connected or self.limelight is None:
            return
        
        try:
            import limelightresults
            
            # Get the latest data from the camera
            raw_result = self.limelight.get_latest_results()
            
            # Parse it into something useful
            parsed = limelightresults.parse_results(raw_result)
            
            # Save it so get_latest() can return it
            self.latest_result = parsed
            
        except Exception as e:
            print(f"[limelight] Error getting data: {e}")
    
    def get_latest(self):
        """Get the most recent camera data.
        
        Returns:
            The latest parsed result, or None if no data yet
        """
        return self.latest_result
    
    def stop(self):
        """Disconnect from the camera."""
        print("[limelight] Disconnecting")
        self.limelight = None
        self.connected = False
