import json
from django.core.management.base import BaseCommand
from app.models import Control, SubControl, Framework  # Update with your app name

class Command(BaseCommand):
    help = 'Import controls and subcontrols from a JSON file.'


    def add_arguments(self, parser):
        parser.add_argument(
            'framework_id',
            type=int,
            help="ID of the framework to associate the clauses and sub-clauses with."
        )

    def handle(self, *args, **kwargs):
        file_path = 'iso_27001_control.json'  # Replace with the actual path to your JSON file
        framework_id = kwargs['framework_id']

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("JSON file not found at the specified path."))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON file format."))
            return

        # Example Framework for foreign key, change based on your logic
        framework = Framework.objects.first()
        if not framework:
            self.stdout.write(self.style.ERROR("No framework found. Add a framework before importing."))
            return

        for control_data in data:
            # Create the Control instance
            control, created = Control.objects.update_or_create(
                ref_id=control_data["ref_code"],
                framework=framework,
                defaults={
                    "title": control_data["name"],
                    "description": control_data["description"],
                    "system_level": control_data["system_level"],
                    "category": control_data["category"],
                    "control_type": control_data["control_type"],
                    "operational_capability": control_data["operational_capability"],
                    "zreferences": control_data["references"],
                    "level": None,  # Add logic to set the level if applicable
                }
            )

            # Check if there are subcontrols
            subcontrols = control_data.get("subcontrols", [])
            if not subcontrols:
                # If subcontrols are empty, add the Control data as a SubControl
                SubControl.objects.update_or_create(
                    control=control,
                    ref_id=control.ref_id,
                    defaults={
                        "title": control.title,
                        "description": control.description,
                        "framework": control.framework,
                    }
                )
            else:
                # Otherwise, add provided subcontrols
                for subcontrol_data in subcontrols:
                    SubControl.objects.update_or_create(
                        control=control,
                        ref_id=subcontrol_data["ref_code"],
                        defaults={
                            "title": subcontrol_data["name"],
                            "description": subcontrol_data["description"],
                            "framework": control.framework,
                        }
                    )

        self.stdout.write(self.style.SUCCESS("Controls and SubControls imported successfully!"))
