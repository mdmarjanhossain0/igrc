from django.db import models
from mysite.settings import DEFAULT_AUTO_FIELD
from account.models import Account, Audit

from django.core.validators import MinValueValidator, MaxValueValidator
# from django_ckeditor_5.fields import CKEditor5Field

from django.db.models.signals import post_save
from django.dispatch import receiver

from grc_config.models import (
	BaseModel,
	StatusDB
)
import os
import uuid

class Framework(BaseModel):
	id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=255, null=False,blank=False)
	description=models.TextField(null=False,blank=False)
	reference_link=models.CharField(max_length=255, null=True,blank=True)
	guidance = models.TextField(null=True, blank=True)
	feature_evidence = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class Task(BaseModel):
	framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
	id=models.AutoField(primary_key=True,)
	serial = models.CharField(max_length=32, null=True, blank=True)
	title=models.CharField(max_length=255, null=False,blank=False)
	description=models.TextField(null=True,blank=True)
	type = models.CharField(max_length=32)
	duration = models.IntegerField(null=True, blank=True)
	start = models.DateField(null=True, blank=True)
	end = models.DateField(null=True, blank=True)
	assignee = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
	files = models.ManyToManyField('TemplateFile', blank=True)
	deliverable = models.TextField(null=True, blank=True)
 
	context = models.TextField(null=True, blank=True)
	feedback = models.TextField(null=True, blank=True)

	# subclauses = models.ManyToManyField('SubClause', blank=True, related_name='subclauses')
	# subcontrols = models.ManyToManyField('SubControl', blank=True, related_name='subcontrols')

	def __str__(self):
		return self.title
	
def upload_to_template(instance, filename):
    return instance.get_upload_path(filename)

class TemplateFile(BaseModel):
	title=models.CharField(max_length=255, null=False,blank=False)
	description = models.TextField(null=True, blank=True)
	file=models.FileField(upload_to=upload_to_template, null=True, blank=True)

	def get_upload_path(self, filename):
			# Get the first associated task's framework name
			task = self.task_set.first()
			if task and task.framework:
					framework_name = task.framework.name
			else:
					framework_name = 'default'
			return os.path.join('templates', framework_name, filename)

	def save(self, *args, **kwargs):
			# Override the save method to set the upload path dynamically
			if self.file:
					self.file.upload_to = upload_to_template
			super().save(*args, **kwargs)

class Clause(BaseModel):
	CORE = "core"
	CONTROL = "control"
	TYPES =  (
		(CORE, CORE),
		(CONTROL, CONTROL)
	)
	framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

	title=models.CharField(max_length=255, null=False,blank=False)
	description=models.TextField(null=True,blank=True)
	ref_id = models.CharField(max_length=8, null=False)
	type = models.CharField(max_length=32, choices=TYPES, default=CORE)

	class Meta:
		unique_together = ('framework', 'ref_id')
	
	def __str__(self):
		return self.title

class SubClause(BaseModel):
	framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

	title=models.CharField(max_length=255, null=False,blank=False)
	description=models.TextField(null=True,blank=True)
	clause = models.ForeignKey(Clause, on_delete=models.CASCADE)
	ref_id = models.CharField(max_length=8, null=False)

	class Meta:
		unique_together = ('clause', 'ref_id')
	
	def __str__(self):
		return self.title

class Policy(BaseModel):
	framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

	title=models.CharField(max_length=255, null=False,blank=False)
	description=models.TextField(null=True,blank=True)
	content=models.TextField(null=False,blank=False)
	ref_id = models.CharField(max_length=8, null=False)

class Control(BaseModel):
	status_choices=[
		("not started","not started"),
		("completed","completed")
	]
	EASY = "Easy"
	MODARATE = "Moderate"
	HARD = "Hard"
	DIFFICULTIES = [
		(EASY, EASY),
		(MODARATE, MODARATE),
		(HARD, HARD),
	]
	framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
	
	title=models.CharField(max_length=255, null=False,blank=False)
	description=models.TextField(null=True,blank=True)
	sub_clause = models.ForeignKey(SubClause, on_delete=models.CASCADE, null=True, blank=True)
	visible = models.BooleanField(default=True)
	system_level = models.BooleanField(default=True)
	category = models.CharField(max_length=32, null=True, blank=True)
	sub_category = models.CharField(max_length=32, null=True, blank=True)
	guidance = models.TextField(null=True, blank=True)
	zreferences = models.CharField(max_length=255, null=True, blank=True)
	mapping = models.TextField(null=True, blank=True)
	level = models.IntegerField(null=True, blank=True)
	operational_capability = models.CharField(max_length=255, choices=DIFFICULTIES, null=True, blank=True)
	control_type = models.CharField(max_length=255, null=True, blank=True)


	ref_id=models.CharField(max_length=32, null=False, blank=False)
	dtc = models.CharField(max_length=32, choices=DIFFICULTIES, default=EASY)
	dtc = models.CharField(max_length=32, choices=DIFFICULTIES, default=EASY)

	def __str__(self):
		return self.title
	
class SubControl(BaseModel):
	EASY = "Easy"
	MODARATE = "Moderate"
	HARD = "Hard"
	DIFFICULTIES = [
		(EASY, EASY),
		(MODARATE, MODARATE),
		(HARD, HARD),
	]
	framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
	control = models.ForeignKey(Control, related_name="subcontrols",on_delete=models.CASCADE)
	
	title=models.CharField(max_length=255, null=False,blank=False)
	description=models.TextField(null=True,blank=True)

	ref_id=models.CharField(max_length=32, null=False, blank=False)
	dtc = models.CharField(max_length=32, choices=DIFFICULTIES, default=EASY)
	dtc = models.CharField(max_length=32, choices=DIFFICULTIES, default=EASY)

	def __str__(self):
		return self.title


class Tenant(BaseModel):
	id=models.AutoField(primary_key=True)
	title=models.CharField(max_length=255, null=False,blank=False)
	description=models.TextField(null=False,blank=False)
	contact_email=models.EmailField(null=False,blank=False)
	owner=models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False, related_name="tenant_owner")


	def __str__(self):
		return self.title

class Project(BaseModel):
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
	framework = models.ForeignKey(Framework, on_delete=models.SET_NULL, null=True, blank=True)

	framework_name = models.CharField(max_length=255, null=True,blank=True)
	framework_description=models.TextField(null=True,blank=True)


	owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False)
	status = models.ForeignKey(StatusDB, on_delete=models.SET_NULL, null=True, blank=True)
	title = models.CharField(max_length=255, null=False, blank=False)
	description=models.TextField(null=True,blank=True)
	is_auditable = models.BooleanField(default=False)

	can_read_scratchpad=models.BooleanField(default=True)
	can_write_scratchpad=models.BooleanField(default=True)
	can_read_comments=models.BooleanField(default=True)
	can_write_comments=models.BooleanField(default=True)
	
	def save(self, *args, **kwargs):
		if not self.framework_name and self.framework:
			self.framework_name = self.framework.name
		if not self.framework_description and self.framework:
			self.framework_description = self.framework.description
		


		super(Project, self).save(*args, **kwargs)

class ProjectScratchpad(BaseModel):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	content = models.TextField(null=True, blank=True)


class ProjectMember(BaseModel):
	ROLE_CHOICES = [
		('viewer', 'Viewer'),
		('Editor', 'Editor'),
		('Admin', 'Admin'),
		('Manager','Manager'),
		('external_auditor', 'Auditor(External)'),
		('internal_auditor', 'Auditor(Internal)'),
	]
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	member = models.ForeignKey(Account, blank=False, on_delete=models.CASCADE)
	role=models.CharField(max_length=255, choices=ROLE_CHOICES ,default="viewer")
	
	all_clause = models.BooleanField(default=True)
	clauses = models.ManyToManyField('ProjectClause', blank=True)
	all_policy = models.BooleanField(default=True)
	policies = models.ManyToManyField('TenantPolicy', blank=True)
	all_control = models.BooleanField(default=True)
	controls = models.ManyToManyField("ProjectControl", blank=True)
	all_sub_control = models.BooleanField(default=True)
	sub_controls = models.ManyToManyField("ProjectSubControl", blank=True)
	all_task = models.BooleanField(default=True)
	tasks=models.ManyToManyField("ProjectTask", blank=True)
	def __str__(self):
		return self.member.username

@receiver(post_save, sender=ProjectMember)
def assign_all_related_fields(sender, instance, created, **kwargs):
	if created:
		if instance.all_clause:
			instance.clauses.set(ProjectClause.objects.filter(project=instance.project))
		if instance.all_policy:
			instance.policies.set(TenantPolicy.objects.filter(project=instance.project))
		if instance.all_control:
			instance.controls.set(ProjectControl.objects.filter(project=instance.project))
		if instance.all_sub_control:
			instance.sub_controls.set(ProjectSubControl.objects.filter(project=instance.project))
		if instance.all_task:
			instance.tasks.set(ProjectTask.objects.filter(project=instance.project))

class ProjectTask(BaseModel):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
	serial = models.CharField(max_length=32, null=True, blank=True)
	files = models.ManyToManyField('TemplateFile', blank=True)
	user_files = models.ManyToManyField('TemplateFile', blank=True, related_name="user_files")
	completion = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	deliverable = models.TextField(null=True, blank=True)

	title=models.CharField(max_length=255, null=True,blank=True)
	description=models.TextField(null=True, blank=True)
	status = models.ForeignKey(StatusDB, on_delete=models.SET_NULL, null=True, blank=True)
	type = models.CharField(max_length=32)
	
	# assigned_member = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True, blank=True)
	is_completed = models.BooleanField(default=False)
	is_audited = models.BooleanField(default=False)
	evidence_required = models.BooleanField(default=True)
	evidence_provided =models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

	deadline = models.DateTimeField(null=True, blank=True)
	completed_at = models.DateTimeField(null=True, blank=True)
	duration = models.IntegerField(null=True, blank=True)
	start = models.DateField(null=True, blank=True)
	end = models.DateField(null=True, blank=True)
	assignee = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
	
	ref_id = models.CharField(max_length=8, null=False, blank=True)
	# clause = models.ManyToManyField(Clause, blank=True)
	subclauses = models.ManyToManyField('ProjectSubClause', blank=True, related_name='project_subclauses')
	subcontrols = models.ManyToManyField('ProjectSubControl', blank=True, related_name='project_subcontrols')

	context = models.TextField(null=True, blank=True)
	feedback = models.TextField(null=True, blank=True)
 
class ProjectClause(BaseModel):
	CORE = "core"
	CONTROL = "control"
	TYPES =  (
		(CORE, CORE),
		(CONTROL, CONTROL)
	)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
	clause = models.ForeignKey(Clause, on_delete=models.SET_NULL, null=True, blank=True)

	title=models.CharField(max_length=255, null=False,blank=True)
	description=models.TextField(null=True,blank=True)
	completion = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

	ref_id = models.CharField(max_length=8, null=False, blank=True)
	type = models.CharField(max_length=32, choices=TYPES, default=CORE)

	class Meta:
		unique_together = ('project', 'ref_id')
	
	def __str__(self):
		return self.title
	
	def save(self, *args, **kwargs):
		if not self.ref_id:
			if  not self.clause:
				self.ref_id = self.clause.ref_id
		super(ProjectClause, self).save(*args, **kwargs)
	
class ProjectSubClause(BaseModel):
	project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
	sub_clause = models.ForeignKey(SubClause, on_delete=models.SET_NULL, null=True, blank=True)
	project_clause = models.ForeignKey(ProjectClause, on_delete=models.SET_NULL, null=True, blank=True)

	title=models.CharField(max_length=255, null=True,blank=True)
	description=models.TextField(null=True,blank=True)
	completion = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	context = models.TextField(null=True, blank=True)

	ref_id = models.CharField(max_length=8, null=False, blank=True)

	class Meta:
		unique_together = ('project', 'project_clause', 'ref_id')
	
	def __str__(self):
		return self.title
	
	def save(self, *args, **kwargs):
		if not self.ref_id:
			if self.sub_clause:
				self.ref_id = self.sub_clause.ref_id 
		super(ProjectSubClause, self).save(*args, **kwargs)


class TenantPolicy(BaseModel):
	tenant=models.ForeignKey(Tenant, on_delete=models.CASCADE)
	project = models.ManyToManyField(Project, blank=True)
	policy = models.ForeignKey(Policy, on_delete=models.SET_NULL, null=True, blank=True)
	title = models.CharField(max_length=255, blank=True)
	description = models.TextField(blank=True)
	content = models.TextField(blank=True)
	label = models.CharField(max_length=255, null=True, blank=True)
	ref_id=models.CharField(max_length=32, null=True, blank=True)


@receiver(post_save, sender=TenantPolicy)
def copy_policy_fields(sender, instance, created, **kwargs):
    if created and instance.policy:
        instance.title = instance.policy.title
        instance.description = instance.policy.description
        instance.content = instance.policy.content
        instance.ref_id = instance.policy.ref_id
        instance.save()

class ProjectControl(BaseModel):
	status_choices=[
		("not started","not started"),
		("completed","completed")
	]
	EASY = "Easy"
	MODARATE = "Moderate"
	HARD = "Hard"
	DIFFICULTIES = [
		(EASY, EASY),
		(MODARATE, MODARATE),
		(HARD, HARD),
	]
	# project = models.ForeignKey(Project, on_delete=models.CASCADE)
	project = models.ManyToManyField(Project, blank=True)
	control = models.ForeignKey(Control, on_delete=models.SET_NULL, null=True, blank=True)
	project_sub_clause = models.ForeignKey(ProjectSubClause, on_delete=models.CASCADE, null=True, blank=True)

	title=models.CharField(max_length=255, null=True,blank=True)
	description=models.TextField(null=True,blank=True)
	completion = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	status = models.CharField(max_length=255, default="not started", choices=status_choices)
	# refcode=models.CharField(max_length=32, null=False, blank=False)
	implementation_context=models.TextField(null=True, blank=True)
	category = models.TextField(null=True, blank=True)
	sub_category =  models.TextField(null=True, blank=True)
	implementation_difficulty = models.CharField(max_length=32, choices=DIFFICULTIES, default=EASY)
	collaboration_difficulty = models.CharField(max_length=32, choices=DIFFICULTIES, default=EASY)
	
	visible = models.BooleanField(default=True)
	guidance = models.TextField(null=True, blank=True)
	zreferences = models.CharField(max_length=255, null=True, blank=True)
	mapping = models.TextField(null=True, blank=True)
	level = models.IntegerField(null=True, blank=True)
	operational_capability = models.CharField(max_length=255, null=True, blank=True)
	control_type = models.CharField(max_length=255, null=True, blank=True)
	applicable = models.BooleanField(default=True)

	ref_id=models.CharField(max_length=32, null=False, blank=False)
	dtc = models.CharField(max_length=32, choices=DIFFICULTIES, default=EASY)
	dtc = models.CharField(max_length=32, choices=DIFFICULTIES, default=EASY)

	def average_completion(self):
		avg_completion=ProjectSubControl.objects.filter(project_control=self).aggregate(models.Avg('completion'))
		return avg_completion['completion__avg'] or self.completion

class ProjectSubControl(BaseModel):
	
	status_choices=[
		("not implemented","not implemented"),
		("partially implemented","partially implemented"),
		("fully implemented","fully implemented"),
	]
	EASY = "Easy"
	MODARATE = "Moderate"
	HARD = "Hard"
	DIFFICULTIES = [
		(EASY, EASY),
		(MODARATE, MODARATE),
		(HARD, HARD),
	]
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	sub_control = models.ForeignKey(SubControl, on_delete=models.SET_NULL, null=True, blank=True)
	project_control = models.ForeignKey(ProjectControl, on_delete=models.CASCADE)
	# project_sub_clause = models.ForeignKey(ProjectSubClause, on_delete=models.CASCADE)
	owner=models.ForeignKey(Account, on_delete=models.SET_NULL,null=True, blank=True, related_name="subcontrol_owner")
	operator=models.ForeignKey(Account, on_delete=models.SET_NULL,null=True, blank=True, related_name="subcontrol_operator")

	title=models.CharField(max_length=255, null=True,blank=True)
	description=models.TextField(null=True,blank=True)
	applicable = models.BooleanField(default=True)
	# refcode=models.CharField(max_length=32, null=False, blank=False)
	implementation_context=models.TextField(null=True, blank=True)
	mitigation = models.TextField(null=True, blank=True)

	completion = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	has_evidence= models.BooleanField(default=False)
	
	status= models.CharField(max_length=255, default="not implemented", choices=status_choices)
	ref_id=models.CharField(max_length=32, null=False, blank=False)
	dtc = models.CharField(max_length=32, choices=DIFFICULTIES, default=EASY)
	dtc = models.CharField(max_length=32, choices=DIFFICULTIES, default=EASY)
	
	#review
	#todo
	#category
	#subcategory

class ContextTempFile(BaseModel):
	title = models.CharField(max_length=255, null=True, blank=True)
	file = models.FileField(upload_to='context-temp/', null=True, blank=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
	task = models.ForeignKey(ProjectTask, on_delete=models.SET_NULL, null=True, blank=True)	

class ContextFile(BaseModel):
	title = models.CharField(max_length=255, null=True, blank=True)
	file = models.FileField(upload_to='context/', null=True, blank=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
	task = models.ForeignKey(ProjectTask, on_delete=models.SET_NULL, null=True, blank=True)	

class EvidenceFile(BaseModel):
    def upload_to(instance, filename):
        unique_prefix = uuid.uuid4().hex
        return f'evidence/{unique_prefix}-{filename}'

    file = models.FileField(upload_to=upload_to, null=True, blank=True)


class Evidence(BaseModel):
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
	project = models.ManyToManyField(Project, blank=True)
	task = models.ManyToManyField(ProjectTask, blank=True)
	clause = models.ManyToManyField(ProjectClause, blank=True)
	policy = models.ManyToManyField(TenantPolicy, blank=True)
	control = models.ManyToManyField(ProjectControl, blank=True)
	sub_control = models.ManyToManyField(ProjectSubControl, blank=True)

	title = models.CharField(max_length=255, null=False, blank=False)
	description = models.TextField(max_length=255, null=True, blank=True)
	content = models.TextField(null=False, blank=False)
	files = models.ManyToManyField(EvidenceFile, blank=True)
	is_complete = models.BooleanField(default=False)
 

class Comment(BaseModel):
	task = models.ForeignKey(ProjectTask, on_delete=models.SET_NULL, null=True, blank=True)
	policy = models.ForeignKey(TenantPolicy, on_delete=models.SET_NULL, null=True, blank=True)
	control = models.ForeignKey(ProjectControl, on_delete=models.SET_NULL, null=True, blank=True)
	sub_control = models.ForeignKey(ProjectSubControl, on_delete=models.SET_NULL, null=True, blank=True)
	project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	audit = models.ForeignKey(Audit, on_delete=models.SET_NULL, null=True, blank=True)
	created_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False)

class Note(BaseModel):
	task = models.ForeignKey(ProjectTask, on_delete=models.SET_NULL, null=True, blank=True)
	policy = models.ForeignKey(TenantPolicy, on_delete=models.SET_NULL, null=True, blank=True)
	control = models.ForeignKey(ProjectControl, on_delete=models.SET_NULL, null=True, blank=True)
	sub_control = models.ForeignKey(ProjectSubControl, on_delete=models.SET_NULL, null=True, blank=True)
	project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	audit = models.ForeignKey(Audit, on_delete=models.SET_NULL, null=True, blank=True)
	created_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False)

class AuditorFeedback(BaseModel):
	status_choices=[
		("not started","not started"),
		("infosec: in progress","infosec: in progress"),
		("infosec: ready for auditor","infosec: ready for auditor"),
		("action required","action required"),
		("completed", "completed")
	]
	task = models.ForeignKey(ProjectTask, on_delete=models.SET_NULL, null=True, blank=True)
	policy = models.ForeignKey(TenantPolicy, on_delete=models.SET_NULL, null=True, blank=True)
	control = models.ForeignKey(ProjectControl, on_delete=models.SET_NULL, null=True, blank=True)
	sub_control = models.ForeignKey(ProjectSubControl, on_delete=models.SET_NULL, null=True, blank=True)
	content = models.TextField(null=True, blank=True)

	status=models.CharField(max_length=255, choices=status_choices)
	auditor_note=models.TextField(null=True, blank=True)
	title=models.CharField(max_length=255)
	auditor_feedback = models.TextField(null=True, blank=True)
	infosec_feedback = models.TextField(null=True, blank=True)

	infosec_completed=models.BooleanField(default=False)
	auditor_completed=models.BooleanField(default=False)

	created_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False)


@receiver(post_save, sender=Project)
def created_project_receiver(sender, instance=None, created=False, **kwargs):
	if created:
		# instance.framework_name = instance.framework.name
		# instance.framework_description = instance.framework.description
		if instance.framework:
			for item in instance.framework.task_set.all():
				project_task=ProjectTask.objects.create(
					project=instance,
					task=item,
					serial=item.serial,
					title=item.title,
					description=item.description,
					type=item.type,
					start=item.start,
					end=item.end,
					assignee=item.assignee if item.assignee else instance.owner,
					context = item.context,
					feedback = item.feedback

				)
				project_task.files.set(item.files.all())
				# print(project_task)
				context_temps = ContextTempFile.objects.all()
				for context_temp in context_temps:
					# Create a new ContextFile instance
					context = ContextFile.objects.create(
						project=instance,
						task=project_task,
						title=context_temp.title,
						file = context_temp.file,
					)
					
			for item in instance.framework.clause_set.all():
				clause = ProjectClause.objects.create(
					project=instance,
					clause=item,
					title=item.title,
					description=item.description,
					ref_id=item.ref_id,
					type=item.type
				)
				sub_clauses = item.subclause_set.all()
				for sub_clause in sub_clauses:
					ProjectSubClause.objects.create(
						project=instance,
						project_clause=clause,
						sub_clause=sub_clause,
						title=sub_clause.title,
						description=sub_clause.description,
						ref_id=sub_clause.ref_id
					)
				
			# for item in instance.framework.policy_set.all():
				# tp = TenantPolicy(
				#     title=item.title,
				#     description=item.description,
				#     content=item.content
				# )
				# tp.save()
				
				# tp.project.set([item.pk])
				# tp.save()
				# pass


			for item in instance.framework.control_set.all():
				print(item)
				# project_sub_clauses = instance.projectsubclause_set.all()
				# for project_sub_clause in project_sub_clauses:
				project_sub_clauses = ProjectSubClause.objects.filter(sub_clause=item.sub_clause, project=instance)
				if project_sub_clauses:
					for psc in project_sub_clauses:
						project_control = ProjectControl.objects.create(
								control=item,
								ref_id=item.ref_id,
								project_sub_clause=psc,
								title=item.title,
								description=item.description,
								visible=item.visible,
								zreferences=item.zreferences,
								mapping=item.mapping,
								level=item.level,
								operational_capability=item.operational_capability,
								control_type=item.control_type,
								implementation_context=item.implementation_context,
								category=item.category,
								sub_category=item.sub_category,
								implementation_difficulty=item.implementation_difficulty,
								collaboration_difficulty=item.collaboration_difficulty,
								guidance=item.guidance,
								applicable=item.applicable
							)
						project_control.project.add(instance)
				else:
					project_control = ProjectControl.objects.create(
								# project=instance,
								control=item,
								ref_id=item.ref_id,
								title=item.title,
								description=item.description,
								visible=item.visible,
								zreferences=item.zreferences,
								mapping=item.mapping,
								level=item.level,
								operational_capability=item.operational_capability,
								control_type=item.control_type,
								implementation_context=item.implementation_context,
								category=item.category,
								sub_category=item.sub_category,
								implementation_difficulty=item.implementation_difficulty,
								collaboration_difficulty=item.collaboration_difficulty,
								guidance=item.guidance,
								applicable=item.applicable
							)
					project_control.project.add(instance)

			for item in instance.framework.subcontrol_set.all():
				for project_control in item.control.projectcontrol_set.all():
					ProjectSubControl.objects.create(
						project=instance,
						sub_control=item,
						project_control=project_control,
						title=item.title,
						description=item.description,
						ref_id=item.ref_id
					)
