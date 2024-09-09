import json
from loguru import logger

def save_dict(data: dict, file_path: str):
    """
    Save the data to a JSON file.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4))
    
def load_dict(file_path: str) -> dict:
    """
    Load the data from a JSON file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}
    except Exception as e:
        logger.error(f"Failed to load file={file_path} error={e}")
        return {}