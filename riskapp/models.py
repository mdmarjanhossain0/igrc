from django.db import models

from account.models import (
    Account,
    Audit
)

from app.models import (
    BaseModel,
    Project,
    ProjectClause,
    ProjectControl,
    ProjectSubControl
)


class RiskRegister(BaseModel):
    subject = models.CharField(max_length=100, null=False, blank=False)
    risk_mapping = models.CharField(max_length=100, null=False, blank=False)
    thread_mapping = models.CharField(max_length=100, null=False, blank=False)
    category = models.CharField(max_length=100, null=False, blank=False)
    risk_source = models.CharField(max_length=100, null=False, blank=False)
    location = models.CharField(max_length=100, null=False, blank=False)
    risk_scoring_method = models.CharField(max_length=100, null=False, blank=False)
    external_reference_id = models.CharField(max_length=100, null=False, blank=False)
    courrent_likelihood = models.CharField(max_length=100, null=False, blank=False)
    control_regulation = models.CharField(max_length=100, null=False, blank=False)
    current_impact = models.CharField(max_length=100, null=False, blank=False)
    control_number = models.CharField(max_length=100, null=False, blank=False)
    affected_assets = models.CharField(max_length=100, null=False, blank=False)
    risk_assessment = models.TextField(null=True, blank=True)
    additional_notes = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="owner")
    owner_manager = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="owner_maager")
    supporting_document = models.FileField(upload_to="risk_register/document")
    tags = models.CharField(max_length=255)


class RiskMitigation(BaseModel):
    submittion_date = models.DateTimeField()
    planned_mitigation_date = models.DateTimeField()
    planning_strategy = models.CharField(max_length=255)
    mitigation_effort = models.CharField(max_length=255, null=True, blank=True)
    mitigation_cost = models.CharField(max_length=255, null=True, blank=True)
    mitigation_owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="mitigation_owner")
    migitation_team = models.ManyToManyField(Account, blank=True)
    mitigation_percent = models.IntegerField(default=0)
    current_solution = models.CharField(max_length=255, null=True, blank=True)
    security_requirements = models.TextField(null=True, blank=True)
    security_recommendations = models.TextField(null=True, blank=True)
    supporting_documentation = models.TextField(null=True, blank=True)