
import json


# file = open('trucare/prescription/soapnotesgenerator/sample_intake.json', 'r')
# json_data = json.load(file)

# file.close()

# print(json_data)



def flatten_data(data, prefix=""):
    parts = []

    if isinstance(data, dict):
        for key, value in data.items():
            if value in (None, "", [], {}):
                continue
            if '_id' in key or key == 'id':
                continue
            label = f"{prefix} {key}".strip()
            parts.extend(flatten_data(value, label))

    elif isinstance(data, list):
        for item in data:
            parts.extend(flatten_data(item, prefix))

    else:
        parts.append(f"{prefix}: {data}")

    return parts




class IntakeCleaner:

    def __init__(self, intake_data: dict):
        self.intake_data = intake_data

    def clean(self) -> dict:
        # Implement cleaning logic here
        cleaned_data = self.intake_data.copy()
        # Example: remove empty fields
        
        for i in cleaned_data.get("condition_answers", []):
            for key in list(i):
                if i[key] in (None, "", [], {}) or "_id" in key or key == "id":
                    del i[key]

        parts = flatten_data(cleaned_data)
        long_string = "\n".join(parts)
        return long_string


# intake_cleaner = IntakeCleaner(json_data)
# cleaned_data = intake_cleaner.clean()
# print(cleaned_data)
