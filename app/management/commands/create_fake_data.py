import random
from django.core.management.base import BaseCommand
from faker import Faker
from app.models import (Account, AuditorFeedback, Clause, Comment, Control, Evidence, EvidenceFile,
  Framework, Note, Project, ProjectClause, ProjectControl, ProjectSubClause, ProjectSubControl,
  ProjectTask, SubClause, SubControl, Tenant, TenantPolicy)
from django.core.files.uploadedfile import SimpleUploadedFile

class Command(BaseCommand):
    help = 'Generate fake data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Generate fake accounts
        for _ in range(10):
            Account.objects.create(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password()
            )
        print("Fake accounts created.")

        # Generate fake frameworks
        for _ in range(5):
            Framework.objects.create(
                name=fake.sentence(),
                description=fake.text(),
                reference_link=fake.url()
            )
        print("Fake frameworks created.")

        # Generate fake projects
        for _ in range(5):
            Project.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                owner=Account.objects.order_by("?").first(),
                framework=Framework.objects.order_by("?").first()
            )
        print("Fake projects created.")

        # Generate fake controls
        for _ in range(10):
            Control.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                ref_id=fake.bothify(text='??####'),
                framework=Framework.objects.order_by("?").first()
            )
        print("Fake controls created.")

        # Generate fake subclauses
        for _ in range(10):
            SubClause.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                clause=Clause.objects.order_by("?").first(),
                ref_id=fake.bothify(text='??####'),
                framework=Framework.objects.order_by("?").first()
            )
        print("Fake subclauses created.")

        # Generate fake project subclauses
        for _ in range(10):
            ProjectSubClause.objects.create(
                project=Project.objects.order_by("?").first(),
                sub_clause=SubClause.objects.order_by("?").first(),
                project_clause=ProjectClause.objects.order_by("?").first(),
                ref_id=fake.bothify(text='??####')
            )
        print("Fake project subclauses created.")

        # Generate fake project controls
        for _ in range(10):
            project = Project.objects.order_by("?").first()
            control = Control.objects.order_by("?").first()
            project_sub_clause = ProjectSubClause.objects.order_by("?").first()
            ProjectControl.objects.create(
                project=project,
                control=control,
                ref_id=control.ref_id,
                project_sub_clause=project_sub_clause
            )
        print("Fake project controls created.")

        # Generate fake evidence and evidence files
        for _ in range(10):
            evidence = Evidence.objects.create(
                description=fake.text(),
                created_by=Account.objects.order_by("?").first(),
                tenant=Tenant.objects.order_by("?").first(),
                project=Project.objects.order_by("?").first(),
                task=ProjectTask.objects.order_by("?").first(),
                clause=ProjectClause.objects.order_by("?").first(),
                policy=TenantPolicy.objects.order_by("?").first(),
                control=ProjectControl.objects.order_by("?").first(),
                sub_control=ProjectSubControl.objects.order_by("?").first(),
                title=fake.sentence(),
                content=fake.text()
            )
            evidence_file = EvidenceFile.objects.create(
                evidence=evidence,
                file=SimpleUploadedFile(
                    name=f"{fake.word()}.txt",
                    content=fake.text().encode('utf-8'),
                    content_type='text/plain'
                )
            )
        print("Fake evidence and evidence files created.")

        # Generate fake comments, notes, and auditor feedback
        policies = TenantPolicy.objects.all()
        for policy in policies:
            for _ in range(3):  # Number of comments per policy
                Comment.objects.create(
                    policy=policy,
                    content=fake.text(),
                    created_by=Account.objects.order_by("?").first()
                )
            for _ in range(3):  # Number of notes per policy
                Note.objects.create(
                    policy=policy,
                    content=fake.text(),
                    created_by=Account.objects.order_by("?").first()
                )
            for _ in range(3):  # Number of auditor feedbacks per policy
                AuditorFeedback.objects.create(
                    policy=policy,
                    feedback=fake.text(),
                    created_by=Account.objects.order_by("?").first()
                )
        print("Fake comments, notes, and auditor feedback created.")
