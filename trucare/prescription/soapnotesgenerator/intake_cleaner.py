
import json


# file = open('trucare/prescription/soapnotesgenerator/sample_intake.json', 'r')
# json_data = json.load(file)

# file.close()

# print(json_data)

class IntakeCleaner:

    def __init__(self, intake_data: dict):
        self.intake_data = intake_data

    def clean(self) -> dict:
        # Implement cleaning logic here
        cleaned_data = self.intake_data.copy()
        # Example: remove empty fields
        for key in list(cleaned_data.keys()):
            if cleaned_data[key] in (None, '', [], {}):
                del cleaned_data[key]
        return cleaned_data

# intake_cleaner = IntakeCleaner(json_data)
# cleaned_data = intake_cleaner.clean()
# print(cleaned_data)
