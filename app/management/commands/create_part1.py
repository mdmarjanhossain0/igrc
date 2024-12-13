from django.core.management.base import BaseCommand
import random
from faker import Faker
from django.db import transaction
from app.models import (Account, AuditorFeedback, Clause, Comment, Control, Evidence, EvidenceFile,
    Framework, Note, Policy, Project, ProjectClause, ProjectControl, ProjectMember,
    ProjectSubControl, ProjectTask, StatusDB, SubClause, SubControl, Task, Tenant, TenantPolicy)

fake = Faker()

def generate_fake_data(
    num_frameworks=10,
    num_tasks_per_framework=10,
    num_clauses_per_framework=10,
    num_policies_per_framework=10,
    num_controls_per_framework=10,
    num_subcontrols_per_control=10,
    num_tenants=10,
    num_projects_per_tenant=10,
    num_project_members_per_project=10,
    num_tasks_per_project=10,
    num_clauses_per_project=10,
    num_controls_per_project=10,
    num_tenant_policies=10,
    num_comments_per_policy=10,
    num_notes_per_policy=10,
    num_auditor_feedbacks_per_policy=10,
    num_evidences_per_project=10,
    num_evidence_files_per_evidence=10
):
    with transaction.atomic():

        # Create Frameworks
        frameworks = []
        for _ in range(num_frameworks):
            framework = Framework.objects.create(
                name=fake.word().capitalize(),
                description=fake.text(),
                reference_link=fake.url() if random.choice([True, False]) else None
            )
            frameworks.append(framework)
        print("Framework data created.")

        # Create Tasks
        for framework in frameworks:
            for _ in range(num_tasks_per_framework):
                try:
                    task = Task.objects.create(
                        framework=framework,
                        title=fake.sentence(nb_words=4),
                        description=fake.text(),
                        type=fake.word(),
                    )
                except Exception as e:
                    print(f"Error creating task: {e}")

        print("Task data created.")

        # Create Clauses
        for framework in frameworks:
            for _ in range(num_clauses_per_framework):
                Clause.objects.create(
                    framework=framework,
                    title=fake.sentence(nb_words=4),
                    description=fake.text(),
                    ref_id=fake.bothify(text='??####'),
                    type=random.choice([Clause.CORE, Clause.CONTROL])  # Randomly select a valid choice

                )
        print("Clause data created.")
        
        # Create SubClauses
        for framework in frameworks:
            for _ in range(num_subclauses_per_framework):
                try:
                    sub_clause = SubClause.objects.create(
                        framework=framework,
                        task=Task.objects.order_by("?").first(),  # Assign a random Task instance
                        title=fake.sentence(nb_words=4),
                        description=fake.text(),
                        clause=Clause.objects.order_by("?").first(),  # Assign a random Clause instance
                        ref_id=fake.bothify(text='??####')
                    )
                except Exception as e:
                    print(f"Error creating sub_clause: {e}")
        
        print("SubClause data created.")

        # Create Policies
        for framework in frameworks:
            for _ in range(num_policies_per_framework):
                Policy.objects.create(
                    framework=framework,
                    title=fake.sentence(nb_words=4),
                    description=fake.text(),
                    content=fake.text()
                )
        print("Policy data created.")

        # Create Controls and SubControls
        for framework in frameworks:
            controls = []
            for _ in range(num_controls_per_framework):
                control = Control.objects.create(
                    framework=framework,
                    title=fake.sentence(nb_words=4),
                    description=fake.text(),
                    sub_clause=SubClause.objects.order_by("?").first(),  # Assign a random SubClause instance
                    ref_id=fake.bothify(text='??####')

                )
                controls.append(control)

            for control in controls:
                for _ in range(num_subcontrols_per_control):
                    SubControl.objects.create(
                        framework=control.framework,
                        control=control,
                        title=fake.sentence(nb_words=4),
                        description=fake.text(),
                        ref_id=fake.bothify(text='??####')
                    )
        print("Control and SubControl data created.")

        # Create Tenants and Projects
        tenants = []
        for _ in range(num_tenants):
            tenant = Tenant.objects.create(
                title=fake.company(),
                description=fake.text(),
                contact_email=fake.email(),
                owner=Account.objects.order_by("?").first()  # Random owner

            )
            tenants.append(tenant)

            for _ in range(num_projects_per_tenant):
                project = Project.objects.create(
                    tenant=tenant,
                    title=fake.company() + " Project",
                    description=fake.text(),
                    owner=tenant.owner,
                    status=StatusDB.objects.order_by("?").first(),
                    
                )
                # Add Project Members
                for _ in range(num_project_members_per_project):
                    ProjectMember.objects.create(
                        project=project,
                        member=Account.objects.order_by("?").first(),  # Random member
                        role=random.choice(["Viewer", "Editor", "Admin"])
                    )
        print("Tenant and Project data created.")

        # Create ProjectTasks
        for project in Project.objects.all():
            for _ in range(num_tasks_per_project):
                ProjectTask.objects.create(
                    project=project,
                    task=Task.objects.order_by("?").first(),
                    title=fake.sentence(nb_words=4),
                    description=fake.text(),
                    status=StatusDB.objects.order_by("?").first(),
                    is_completed=random.choice([True, False]),
                    deadline=fake.date_time_this_year(),
                    completed_at=fake.date_time_this_year() if random.choice([True, False]) else None
                )
        print("ProjectTask data created.")


        # Create ProjectClauses
        for project in Project.objects.all():
            for _ in range(num_clauses_per_project):
                ProjectClause.objects.create(
                    project=project,
                    clause=Clause.objects.order_by("?").first(),
                    title=fake.sentence(nb_words=4),
                    description=fake.text(),
                    completion=random.randint(0, 100)
                )
        print("ProjectClause data created.")

        # Create TenantPolicies
        for tenant in tenants:
            for _ in range(num_tenant_policies):
                TenantPolicy.objects.create(
                    title=fake.sentence(nb_words=4),
                    description=fake.text(),
                    content=fake.text(),
                    # project=Project.objects.filter(tenant=tenant).order_by("?")[:random.randint(1, num_projects_per_tenant)]
                )
        print("TenantPolicy data created.")


        # Create ProjectControls
        for project in Project.objects.all():
            for _ in range(num_controls_per_project):
                ProjectControl.objects.create(
                    project=project,
                    control=Control.objects.order_by("?").first(),
                    title=fake.sentence(nb_words=4),
                    description=fake.text(),
                    completion=random.randint(0, 100)
                )
        print("ProjectControl data created.")


        # Create ProjectSubControls
        for project in Project.objects.all():
            for _ in range(num_controls_per_project):
                project_control = ProjectControl.objects.filter(project=project).order_by("?").first()
                if project_control:
                    for _ in range(num_subcontrols_per_control):
                        ProjectSubControl.objects.create(
                            project=project,
                            sub_control=SubControl.objects.order_by("?").first(),
                            project_control=project_control,
                            title=fake.sentence(nb_words=4),
                            description=fake.text(),
                            completion=random.randint(0, 100)
                        )
        print("ProjectSubControl data created.")


        # Create Evidence and EvidenceFiles
        # for tenant in tenants:
        #     for _ in range(num_evidences_per_project):
        #         evidence = Evidence.objects.create(
        #             tenant=tenant,
        #             project=Project.objects.filter(tenant=tenant).order_by("?").first(),
        #             title=fake.sentence(nb_words=4),
        #             description=fake.text(),
        #             content=fake.text()
        #         )
        #         for _ in range(num_evidence_files_per_evidence):
        #             EvidenceFile.objects.create(file=fake.file_path())
        # print("Evidence and EvidenceFile data created.")

        from django.core.files.uploadedfile import SimpleUploadedFile

        for tenant in tenants:
            for _ in range(num_evidences_per_project):
                evidence = Evidence.objects.create(
                    tenant=tenant,
                    project=Project.objects.filter(tenant=tenant).order_by("?").first(),
                    title=fake.sentence(nb_words=4),
                    description=fake.text(),
                    content=fake.text()
                )
                for _ in range(num_evidence_files_per_evidence):
                    evidence_file = EvidenceFile.objects.create(
                        file=SimpleUploadedFile(
                            name=f"{fake.word()}.txt",
                            content=fake.text().encode('utf-8'),
                            content_type='text/plain'
                        )
                    )
            print("Evidence and EvidenceFile data created.")


        # Create Comments, Notes, and AuditorFeedback
        policies = TenantPolicy.objects.all()
        for policy in policies:
            # for _ in range(num_comments_per_policy):
            #     Comment.objects.create(
            #         policy=policy,
            #         content=fake.text(),
            #         created_by=Account.objects.order_by("?").first()
            #     )
            for _ in range(num_notes_per_policy):
                Note.objects.create(
                    policy=policy,
                    content=fake.text(),
                    created_by=Account.objects.order_by("?").first()
                )
            for _ in range(num_auditor_feedbacks_per_policy):
                AuditorFeedback.objects.create(
                    policy=policy,
                    content=fake.text(),
                    created_by=Account.objects.order_by("?").first()
                )
        print("Comment, Note, and AuditorFeedback data created.")

        print("All fake data generation completed.")

class Command(BaseCommand):
    help = 'Generate fake data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting fake data generation...")
        generate_fake_data()
        self.stdout.write("Fake data generation completed.")
