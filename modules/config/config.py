"""
Configuration loader for robot settings.
Reads settings from robot_config.toml file.
"""
import os
from pathlib import Path

# Try to import TOML library
try:
    import tomllib
except:
    try:
        import toml as tomllib
    except:
        tomllib = None


# Default settings if config file not found
DEFAULT_CONFIG = {
    "motors": {
        "left_id": 3,    # CAN ID for left motor
        "right_id": 2    # CAN ID for right motor
    },
    "limelight": {
        "pipeline": 0    # Which vision pipeline to use
    }
}


class ConfigLoader:
    """Loads robot configuration from TOML file."""
    
    @staticmethod
    def load_config(path=None):
        """Load config from file, or use defaults if file not found.
        
        Args:
            path: Path to config file (optional)
        
        Returns:
            Dictionary with all config settings
        """
        # Figure out where the config file is
        if path is None:
            config_folder = Path(__file__).parent
            path = config_folder / "robot_config.toml"
        
        # If we don't have a TOML library, just use defaults
        if tomllib is None:
            print("[config] No TOML library found, using defaults")
            return DEFAULT_CONFIG.copy()
        
        # Try to load the config file
        try:
            with open(path, "rb") as f:
                config = tomllib.load(f)
            print(f"[config] Loaded settings from {path}")
            
            # Merge with defaults (in case file is missing some settings)
            result = DEFAULT_CONFIG.copy()
            result.update(config)
            return result
            
        except FileNotFoundError:
            print(f"[config] File not found: {path}, using defaults")
            return DEFAULT_CONFIG.copy()
        except Exception as e:
            print(f"[config] Error loading file: {e}, using defaults")
            return DEFAULT_CONFIG.copy()
