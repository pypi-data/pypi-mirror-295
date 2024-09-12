from datetime import datetime
import json


class JSON:
    def stringify(data):
        # Remove callable objects from the data and serialize datetimes.
        def serialize(obj):
            if isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items() if not callable(v)}
            elif isinstance(obj, list):
                return [serialize(item) for item in obj if not callable(item)]
            elif isinstance(obj, datetime):
                return obj.isoformat()
            else:
                return obj

        cleaned_data = serialize(data)
        return json.dumps(cleaned_data)

    def parse(data):
        return json.loads(data)
