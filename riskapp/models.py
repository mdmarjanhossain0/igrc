from django.db import models
from django.core.validators import MaxValueValidator
from account.models import (
    Account,
    Audit
)

from app.models import (
    BaseModel,
    Project,
    ProjectClause,
    ProjectControl,
    ProjectSubControl,
    
    Tenant,
    Framework,
)

from grc_config.models import (
    BaseModel,
    StatusDB,
    RiskSource,
    LikelyHood,
    Impact,
    PlanningStrategy,
    MitigationEffort,
    NextStep,
    DataClassifiation,
    ReviewStatus,
    ReviewStatus
)

class RiskMapping(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

class ThreatMapping(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

class RiskCategory(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class RiskScroingMethod(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

class ControlRegister(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)



class Team(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(Account, blank=True)

class RiskRegister(BaseModel):
    EXTERNAL = "External"
    PEOPLE = "People"
    PROCESS = "Process"
    SYSTEM = "System"
    RISK_SOURCES = (
        (EXTERNAL, EXTERNAL),
        (PEOPLE, PEOPLE),
        (PROCESS, PROCESS),
        (SYSTEM, SYSTEM)
    )

    REMOTE = "Remote"
    UNLIKELY = "UNLIKELY"
    CREDIBLE = "Credible"
    LIKELY = "Likely"
    ALMOST_CERTAIN = "Almost Certain"
    LIKELIHOODS = (
        (REMOTE, REMOTE),
        (UNLIKELY, UNLIKELY),
        (CREDIBLE, CREDIBLE),
        (LIKELY, LIKELY),
        (ALMOST_CERTAIN, ALMOST_CERTAIN)
    )

    INSIGNIFICANT = "Insignificant"
    MINOR = "Minor"
    MODARATE = "Modarate"
    MAJOR = "Major"
    EXTREME = "Extreme"
    IMPACTS = (
        (INSIGNIFICANT, INSIGNIFICANT),
        (MINOR, MINOR),
        (MODARATE, MODARATE),
        (MAJOR, MAJOR),
        (EXTREME, EXTREME)
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, null=False, blank=False)
    risk_mapping = models.ManyToManyField(RiskMapping)
    thread_mapping = models.ManyToManyField(ThreatMapping)
    category = models.ManyToManyField(RiskCategory)
    risk_source = models.CharField(max_length=32, choices=RISK_SOURCES, null=False, blank=False)
    location = models.CharField(max_length=100, null=False, blank=False)
    risk_scoring_method = models.ForeignKey(RiskScroingMethod, on_delete=models.SET_NULL, null=True, blank=True)
    external_reference_id = models.CharField(max_length=100, null=False, blank=False)
    courrent_likelihood = models.CharField(max_length=32, choices=LIKELIHOODS, null=False, blank=False)
    control_regulation = models.ForeignKey(ControlRegister, on_delete=models.SET_NULL, null=True, blank=True)
    current_impact = models.CharField(max_length=32, choices=IMPACTS, null=False, blank=False)
    control = models.ManyToManyField(ProjectControl, blank=True)
    affected_assets = models.CharField(max_length=100, null=False, blank=False)
    risk_assessment = models.TextField(null=True, blank=True)
    additional_notes = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="owner")
    owner_manager = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="owner_maager")
    supporting_document = models.FileField(upload_to="risk_register/document")
    tags = models.CharField(max_length=255)

class MitigationControl(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)
    description =  models.TextField(null=True, blank=True)

class RiskMitigation(BaseModel):
    ACCEPTED = "Accepted"
    MITIGATE = "Mitigate"
    RESEARCH = "Research"
    TRANSFER = "Transfer"
    WATCH = "Watch"
    PLANNING_STRATEGIES = (
        (ACCEPTED, ACCEPTED),
        (MITIGATE, MITIGATE),
        (RESEARCH, RESEARCH),
        (TRANSFER, TRANSFER),
        (WATCH, WATCH)
    )

    TRIVIAL = "Trivial"
    MINOR = "Minor"
    CONSIDARABLE = "Considarable"
    SIGNIFICANT = "Significant"
    EXCEPTIONAL = "Exceptional"
    MITIGATION_EFFORTS = (
        (TRIVIAL, TRIVIAL),
        (MINOR, MINOR),
        (CONSIDARABLE, CONSIDARABLE),
        (SIGNIFICANT, SIGNIFICANT),
        (EXCEPTIONAL, EXCEPTIONAL)
    )



    CLOSED = "Closed"
    MITIGATION_REVIEWED = "Mitigation Reviewd"
    MITIGATION_PLANNE = "Mitigation Planne"
    NEW = "New"
    RESPONSED = "Responsed"
    TREATED = "Treated"
    UNTREATED = "Untreated"
    STATUSSES = (
        (CLOSED, CLOSED),
        (MITIGATION_REVIEWED, MITIGATION_REVIEWED),
        (MITIGATION_PLANNE, MITIGATION_PLANNE),
        (NEW, NEW),
        (RESPONSED, RESPONSED),
        (TREATED, TREATED),
        (UNTREATED, UNTREATED)
    )

    risk = models.OneToOneField(RiskRegister, on_delete=models.CASCADE)
    submittion_date = models.DateTimeField()
    planned_mitigation_date = models.DateTimeField()
    planning_strategy = models.ForeignKey(PlanningStrategy, on_delete=models.SET_NULL, null=True, blank=True)
    mitigation_effort = models.ForeignKey(MitigationEffort, on_delete=models.SET_NULL, null=True, blank=True)
    mitigation_cost = models.CharField(max_length=255, null=True, blank=True)
    mitigation_owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="mitigation_owner")
    migitation_team = models.ManyToManyField(Team, blank=True)
    mitigation_percent = models.IntegerField(default=0)
    mitigation_control = models.ManyToManyField(MitigationControl, blank=True)
    current_solution = models.CharField(max_length=255, null=True, blank=True)
    security_requirements = models.TextField(null=True, blank=True)
    security_recommendations = models.TextField(null=True, blank=True)
    supporting_documentation = models.TextField(null=True, blank=True)
    status = models.ForeignKey(StatusDB, on_delete=models.SET_NULL, null=True, blank=True)

class Review(BaseModel):
    APPROVE_RISK = "Approve Risk"
    REJECT_RISK_AND_CLOSE = "Reject Risk and Close"
    REVIEWS = (
        (APPROVE_RISK, APPROVE_RISK),
        (REJECT_RISK_AND_CLOSE, REJECT_RISK_AND_CLOSE)
    )

    ACCEPT_UNTILL_NEXT_REVIEW = "Accept Until Next Review"
    CONSIDER_FOR_PROJECT = "Consider for Project"
    SUBMIT_AS_A_PRODUCTION_ISSUE = "Submit as a Production Issue"
    NEXT_STEPS = (
        (ACCEPT_UNTILL_NEXT_REVIEW, ACCEPT_UNTILL_NEXT_REVIEW),
        (CONSIDER_FOR_PROJECT, CONSIDER_FOR_PROJECT),
        (SUBMIT_AS_A_PRODUCTION_ISSUE, SUBMIT_AS_A_PRODUCTION_ISSUE)
    )
    mitigation = models.ForeignKey(RiskMitigation, on_delete=models.CASCADE)
    review_date = models.DateTimeField()
    reviewer = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    review = models.ForeignKey(ReviewStatus, on_delete=models.SET_NULL, null=True, blank=True)
    next_step = models.ForeignKey(NextStep, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    next_date = models.DateField(null=True, blank=True)
    is_different_instend = models.BooleanField(default=False)

class PlanProject(BaseModel):
    UNASSIGNED = "Unassigned"
    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    RESTRICTED = "Restricted"
    DATA_CLASSIFICATIONS = (
        (UNASSIGNED, UNASSIGNED),
        (PUBLIC, PUBLIC),
        (INTERNAL, INTERNAL),
        (CONFIDENTIAL, CONFIDENTIAL),
        (RESTRICTED, RESTRICTED)
    )
    mitigation = models.ForeignKey(MitigationControl, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    priority = models.IntegerField(null=True, blank=True)
    due = models.DateField(null=True, blank=True)
    consultant = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="consultant")
    business_owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="business_owner")
    data_classification = models.ForeignKey(DataClassifiation, on_delete=models.SET_NULL, null=True, blank=True)

class ReviewProject(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    status = models.IntegerField(default=0, validators=[MaxValueValidator(100)])

class Comment(BaseModel):
    mitigation = models.ForeignKey(RiskMitigation, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False, related_name="created_by")