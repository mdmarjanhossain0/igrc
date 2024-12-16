import json
from django.core.management.base import BaseCommand, CommandError
from app.models import Clause, SubClause, Framework

# Static file path
STATIC_JSON_PATH = "iso_27001.json"

class Command(BaseCommand):
    help = "Import clauses and sub-clauses into the database for a given framework."

    def add_arguments(self, parser):
        parser.add_argument(
            'framework_id',
            type=int,
            help="ID of the framework to associate the clauses and sub-clauses with."
        )

    def handle(self, *args, **kwargs):
        framework_id = kwargs['framework_id']

        # Validate the framework
        try:
            framework = Framework.objects.get(id=framework_id)
        except Framework.DoesNotExist:
            raise CommandError(f"Framework with ID {framework_id} does not exist.")

        # Load the JSON data from the static file path
        try:
            with open(STATIC_JSON_PATH, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            raise CommandError(f"Static JSON file not found at: {STATIC_JSON_PATH}")
        except json.JSONDecodeError:
            raise CommandError("Error decoding JSON file. Ensure the file is valid.")

        # Process and save clauses and sub-clauses
        for clause_data in data["clauses"]:
            clause, created = Clause.objects.update_or_create(
                framework=framework,
                ref_id=str(clause_data['id']),
                defaults={
                    'title': clause_data['title'],
                    'description': clause_data.get('description', ''),
                    'type': clause_data.get('type', Clause.CORE),
                }
            )

            self.stdout.write(
                f"{'Created' if created else 'Updated'} Clause: {clause.title} (ID: {clause.id})"
            )

            # Process sub-clauses for this clause
            for sub_clause_data in clause_data.get('sub_clauses', []):
                sub_clause, sub_created = SubClause.objects.update_or_create(
                    clause=clause,
                    framework=framework,
                    ref_id=sub_clause_data['id'],
                    defaults={
                        'title': sub_clause_data['description'],
                        'description': sub_clause_data.get('description', ''),
                    }
                )
                # self.stdout.write(
                #     f"  {'Created' if sub_created else 'Updated'} Sub-Clause: {sub_clause.title} (ID: {sub_clause.id})"
                # )

        self.stdout.write(self.style.SUCCESS("Import completed successfully."))
