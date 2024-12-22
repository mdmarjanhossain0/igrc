import json
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from app.models import Task, Framework, Account
STATIC_JSON_PATH = "task.json"

class Command(BaseCommand):
    help = 'Populate the database with predefined tasks'

    def add_arguments(self, parser):
        parser.add_argument('framework_id', type=int, help='ID of the Framework to associate tasks with')

    def handle(self, *args, **kwargs):
        framework_id = kwargs['framework_id']
        try:
            framework = Framework.objects.get(id=framework_id)
        except Framework.DoesNotExist:
            raise CommandError(f'Framework with ID {framework_id} does not exist')

        assignee = None  # Replace with Account object or keep None if no assignee

                # Load the JSON data from the static file path
        try:
            with open(STATIC_JSON_PATH, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            raise CommandError(f"Static JSON file not found at: {STATIC_JSON_PATH}")
        except json.JSONDecodeError:
            raise CommandError("Error decoding JSON file. Ensure the file is valid.")
        # counts = {}
        for task in data:
            # print(task['serial'])
            # if task['serial'] in counts:
            #     counts[task['serial']] = counts[task['serial']]  + 1
            #     print(task['serial'])
            # else:
            #     counts[task['serial']] = 1
            task['start'] = datetime.strptime(task['start'], '%Y-%m-%d').date()
            task['end'] = datetime.strptime(task['end'], '%Y-%m-%d').date()
            Task.objects.create(
                framework=framework,
                title=task['title'],
                type=task['type'],
                duration=task['duration'],
                start=task['start'],
                end=task['end'],
                serial = task['serial'],
                assignee=assignee
            )
        # print(counts)
        self.stdout.write(self.style.SUCCESS(f'Tasks have been successfully created for framework ID {framework_id}.'))
