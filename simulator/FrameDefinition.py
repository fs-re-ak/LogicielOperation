import json
import uuid
from datetime import datetime
from time import time
class Frame(object):
    
    Type = None
    CreatedAt = None

    def __init__(self, count=None, status=None, device_id=None, **metrics):

        self.timestamp = time()

        if count is not None:
            self.count = count

        if status is not None:
            self.status = status

        if device_id is not None:
            self.device_id = device_id

        if metrics:
            self.metrics = metrics
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

