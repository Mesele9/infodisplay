import json
from datetime import time

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.isoformat()  # Serialize time as ISO 8601 string
        return super().default(obj)