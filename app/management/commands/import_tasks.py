from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from app.models import Task, Framework, Account

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

        raw_tasks = [
            {"title": "Management Support", "type": "S", "duration": 31, "start": "2024-08-01", "end": "2024-09-12"},
            {"title": "Purchase ISO/IEC 27001:2022", "type": "T", "duration": 1, "start": "2024-08-01", "end": "2024-08-01"},
            {"title": "Understand business vision and objectives", "type": "T", "duration": 1, "start": "2024-09-13", "end": "2024-09-13"},
            {"title": "Outline business case", "type": "T", "duration": 9, "start": "2024-08-02", "end": "2024-08-14"},
            {"title": "Present business case", "type": "T", "duration": 1, "start": "2024-08-15", "end": "2024-08-15"},
            {"title": "Develop project charter", "type": "T", "duration": 10, "start": "2024-08-16", "end": "2024-08-29"},
            {"title": "Obtain approval for project charter", "type": "T", "duration": 2, "start": "2024-08-30", "end": "2024-09-02"},
            {"title": "Assign overall responsibility for the ISMS", "type": "T", "duration": 1, "start": "2024-09-03", "end": "2024-09-03"},
            {"title": "Communicate roles, responsibilities and authorities for the ISMS", "type": "T", "duration": 1, "start": "2024-09-04", "end": "2024-09-04"},
            {"title": "Establish information security governance process", "type": "T", "duration": 5, "start": "2024-09-05", "end": "2024-09-11"},
            {"title": "Establish requirements management process", "type": "T", "duration": 5, "start": "2024-09-12", "end": "2024-09-18"},
            {"title": "Establish customer relationship management process", "type": "T", "duration": 5, "start": "2024-09-19", "end": "2024-09-25"},
            {"title": "Determine external issues", "type": "T", "duration": 5, "start": "2024-09-26", "end": "2024-10-02"},
            {"title": "Determine internal issues", "type": "T", "duration": 5, "start": "2024-10-03", "end": "2024-10-09"},
            {"title": "Identify external interested parties", "type": "T", "duration": 3, "start": "2024-10-10", "end": "2024-10-14"},
            {"title": "Identify internal interested parties", "type": "T", "duration": 3, "start": "2024-10-15", "end": "2024-10-17"},
            {"title": "Identify requirements of interested parties", "type": "T", "duration": 2, "start": "2024-10-18", "end": "2024-10-21"},
            {"title": "Determine preliminary scope", "type": "T", "duration": 5, "start": "2024-10-22", "end": "2024-10-28"},
            {"title": "Determine refined scope", "type": "T", "duration": 1, "start": "2024-10-29", "end": "2024-10-29"},
            {"title": "Determine final scope", "type": "T", "duration": 1, "start": "2024-10-30", "end": "2024-10-30"},
            {"title": "Document final scope", "type": "T", "duration": 1, "start": "2024-10-31", "end": "2024-10-31"},
            {"title": "Approve final scope", "type": "T", "duration": 1, "start": "2024-11-01", "end": "2024-11-01"},
            {"title": "Develop Risk Treatment Plan", "type": "S", "duration": 31, "start": "2025-05-14", "end": "2025-06-25"},
            {"title": "Establish resource management process", "type": "T", "duration": 5, "start": "2025-05-14", "end": "2025-05-20"},
            {"title": "Select risk treatment options", "type": "T", "duration": 5, "start": "2025-05-21", "end": "2025-05-27"},
            {"title": "Determine controls", "type": "T", "duration": 5, "start": "2025-05-28", "end": "2025-06-03"},
            {"title": "Produce Statement of Applicability (SoA)", "type": "T", "duration": 1, "start": "2025-06-04", "end": "2025-06-04"},
            {"title": "Formulate risk treatment plan", "type": "T", "duration": 10, "start": "2025-06-05", "end": "2025-06-18"},
            {"title": "Obtain approval for risk treatment plan", "type": "T", "duration": 5, "start": "2025-06-19", "end": "2025-06-25"}
        ]

        for task in raw_tasks:
            task['start'] = datetime.strptime(task['start'], '%Y-%m-%d').date()
            task['end'] = datetime.strptime(task['end'], '%Y-%m-%d').date()
            Task.objects.create(
                framework=framework,
                title=task['title'],
                type=task['type'],
                duration=task['duration'],
                start=task['start'],
                end=task['end'],
                assignee=assignee
            )

        self.stdout.write(self.style.SUCCESS(f'Tasks have been successfully created for framework ID {framework_id}.'))
