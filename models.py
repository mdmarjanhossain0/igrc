from django.db import models


class AuditorFeedback(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    response = models.CharField(max_length=255, blank=True, null=True)
    is_complete = models.IntegerField(blank=True, null=True)
    auditor_complete = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    subcontrol = models.ForeignKey('ProjectSubcontrols', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditor_feedback'


class ConfigStore(models.Model):
    zkey = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'config_store'


class ControlComments(models.Model):
    message = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    control = models.ForeignKey('ProjectControls', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'control_comments'


class ControlTags(models.Model):
    control = models.ForeignKey('ProjectControls', models.DO_NOTHING, blank=True, null=True)
    tag = models.ForeignKey('Tags', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'control_tags'


class Controls(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    ref_code = models.CharField(max_length=255, blank=True, null=True)
    abs_ref_code = models.CharField(max_length=255, blank=True, null=True)
    visible = models.IntegerField(blank=True, null=True)
    system_level = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    subcategory = models.CharField(max_length=255, blank=True, null=True)
    guidance = models.CharField(max_length=255, blank=True, null=True)
    zreferences = models.CharField(max_length=255, blank=True, null=True)
    mapping = models.JSONField(blank=True, null=True)
    vendor_recommendations = models.JSONField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    operational_capability = models.CharField(max_length=255, blank=True, null=True)
    control_type = models.CharField(max_length=255, blank=True, null=True)
    dti = models.CharField(max_length=255, blank=True, null=True)
    dtc = models.CharField(max_length=255, blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)
    framework = models.ForeignKey('Frameworks', models.DO_NOTHING, blank=True, null=True)
    tenant = models.ForeignKey('Tenants', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'controls'


class Evidence(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    collected_on = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    tenant = models.ForeignKey('Tenants', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evidence'
        unique_together = (('name', 'tenant'),)


class EvidenceAssociation(models.Model):
    control = models.ForeignKey('ProjectSubcontrols', models.DO_NOTHING, blank=True, null=True)
    evidence = models.ForeignKey(Evidence, models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evidence_association'


class Findings(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    mitigation = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    risk = models.IntegerField(blank=True, null=True)
    task = models.ForeignKey('Tasks', models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'findings'


class Frameworks(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    reference_link = models.CharField(max_length=255, blank=True, null=True)
    guidance = models.CharField(max_length=255, blank=True, null=True)
    feature_evidence = models.IntegerField(blank=True, null=True)
    tenant = models.ForeignKey('Tenants', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frameworks'


class Integrations(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'integrations'


class Jobs(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    result = models.JSONField(blank=True, null=True)
    bg_id = models.IntegerField()
    tenant = models.ForeignKey('Tenants', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jobs'


class LockerAssociation(models.Model):
    locker = models.ForeignKey('Lockers', models.DO_NOTHING, blank=True, null=True)
    integration = models.ForeignKey(Integrations, models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locker_association'


class Lockers(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    value = models.JSONField(blank=True, null=True)
    tenant = models.ForeignKey('Tenants', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lockers'


class Logs(models.Model):
    namespace = models.CharField(max_length=255)
    log_type = models.CharField(max_length=255)
    action = models.CharField(max_length=255, blank=True, null=True)
    message = models.CharField(max_length=255)
    succeeded = models.IntegerField(blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'


class Policies(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    ref_code = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    template = models.CharField(max_length=255, blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    visible = models.IntegerField(blank=True, null=True)
    tenant = models.ForeignKey('Tenants', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'policies'


class PolicyAssociations(models.Model):
    policy = models.ForeignKey(Policies, models.DO_NOTHING, blank=True, null=True)
    control = models.ForeignKey(Controls, models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'policy_associations'


class PolicyLabels(models.Model):
    zkey = models.CharField(unique=True, max_length=255)
    value = models.CharField(max_length=255)
    owner = models.ForeignKey('Users', models.DO_NOTHING)
    tenant = models.ForeignKey('Tenants', models.DO_NOTHING)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'policy_labels'


class PolicyTags(models.Model):
    policy = models.ForeignKey('ProjectPolicies', models.DO_NOTHING, blank=True, null=True)
    tag = models.ForeignKey('Tags', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'policy_tags'


class ProjectComments(models.Model):
    message = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_comments'


class ProjectControls(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    auditor_notes = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING, blank=True, null=True)
    control = models.ForeignKey(Controls, models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_controls'


class ProjectMembers(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING, blank=True, null=True)
    access_level = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_members'


class ProjectPolicies(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    public_viewable = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING, blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    reviewer = models.ForeignKey('Users', models.DO_NOTHING, related_name='projectpolicies_reviewer_set', blank=True, null=True)
    policy = models.ForeignKey(Policies, models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_policies'


class ProjectPolicyAssociations(models.Model):
    policy = models.ForeignKey(ProjectPolicies, models.DO_NOTHING, blank=True, null=True)
    control = models.ForeignKey(ProjectControls, models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_policy_associations'


class ProjectSubcontrols(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    implemented = models.IntegerField(blank=True, null=True)
    is_applicable = models.IntegerField(blank=True, null=True)
    context = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    auditor_notes = models.CharField(max_length=255, blank=True, null=True)
    review_status = models.CharField(max_length=255, blank=True, null=True)
    auditor_feedback = models.CharField(max_length=255, blank=True, null=True)
    process_maturity = models.IntegerField(blank=True, null=True)
    operator = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING, related_name='projectsubcontrols_owner_set', blank=True, null=True)
    subcontrol = models.ForeignKey('Subcontrols', models.DO_NOTHING)
    project_control = models.ForeignKey(ProjectControls, models.DO_NOTHING)
    project = models.ForeignKey('Projects', models.DO_NOTHING)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_subcontrols'


class ProjectTags(models.Model):
    project = models.ForeignKey('Projects', models.DO_NOTHING, blank=True, null=True)
    tag = models.ForeignKey('Tags', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_tags'


class Projects(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    can_auditor_read_scratchpad = models.IntegerField(blank=True, null=True)
    can_auditor_write_scratchpad = models.IntegerField(blank=True, null=True)
    can_auditor_read_comments = models.IntegerField(blank=True, null=True)
    can_auditor_write_comments = models.IntegerField(blank=True, null=True)
    target_level = models.IntegerField(blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    tenant = models.ForeignKey('Tenants', models.DO_NOTHING, blank=True, null=True)
    framework = models.ForeignKey(Frameworks, models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects'


class QuestionnaireGuests(models.Model):
    questionnaire = models.ForeignKey('Questionnaires', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questionnaire_guests'


class QuestionnaireTemplates(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    description = models.CharField(unique=True, max_length=255, blank=True, null=True)
    form = models.JSONField(blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING)
    tenant = models.ForeignKey('Tenants', models.DO_NOTHING)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questionnaire_templates'


class Questionnaires(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    enabled = models.IntegerField(blank=True, null=True)
    feedback = models.CharField(max_length=255, blank=True, null=True)
    submitted = models.IntegerField(blank=True, null=True)
    published = models.IntegerField(blank=True, null=True)
    form = models.JSONField(blank=True, null=True)
    submission = models.JSONField(blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING)
    tenant = models.ForeignKey('Tenants', models.DO_NOTHING)
    due_before = models.DateTimeField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questionnaires'


class Roles(models.Model):
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class SubcontrolComments(models.Model):
    message = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    subcontrol = models.ForeignKey(ProjectSubcontrols, models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subcontrol_comments'


class Subcontrols(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    ref_code = models.CharField(max_length=255, blank=True, null=True)
    mitigation = models.CharField(max_length=255, blank=True, null=True)
    guidance = models.CharField(max_length=255, blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)
    tasks = models.JSONField(blank=True, null=True)
    implementation_group = models.IntegerField(blank=True, null=True)
    control = models.ForeignKey(Controls, models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subcontrols'


class Tags(models.Model):
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING)
    tenant = models.ForeignKey('Tenants', models.DO_NOTHING)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'


class TaskResults(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    task = models.ForeignKey('Tasks', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task_results'
        unique_together = (('version', 'task'),)


class Tasks(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    queue = models.CharField(max_length=255, blank=True, null=True)
    disabled = models.IntegerField(blank=True, null=True)
    last_run = models.DateTimeField(blank=True, null=True)
    not_before = models.DateTimeField(blank=True, null=True)
    cron = models.CharField(max_length=255, blank=True, null=True)
    integration = models.ForeignKey(Integrations, models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tasks'


class Tenants(models.Model):
    uuid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(unique=True, max_length=64)
    logo_ref = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)
    license = models.CharField(max_length=255, blank=True, null=True)
    approved_domains = models.CharField(max_length=255, blank=True, null=True)
    magic_link_login = models.IntegerField(blank=True, null=True)
    storage_cap = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING)
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tenants'


class UserRoles(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    role = models.ForeignKey(Roles, models.DO_NOTHING, blank=True, null=True)
    tenant = models.ForeignKey(Tenants, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_roles'


class Users(models.Model):
    is_active = models.IntegerField()
    email = models.CharField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=100, blank=True, null=True)
    email_confirmed_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    last_password_change = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    super = models.IntegerField()
    built_in = models.IntegerField(blank=True, null=True)
    tenant_limit = models.IntegerField(blank=True, null=True)
    can_user_create_tenant = models.IntegerField()
    date_added = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
