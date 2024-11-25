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
    ProjectSubControl,
    
    Tenant,
    Framework,
)
from django.core.validators import MaxValueValidator

# class RiskProject(BaseModel):
#     name = models.CharField(max_length=255,null=False, blank=False)
#     project_lead = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
#     framework = models.ForeignKey(Framework, on_delete=models.SET_NULL, null=True, blank=True)
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()

class RiskMapping(BaseModel):
    name = models.CharField(max_length=255)

class ThreatMapping(BaseModel):
    name = models.CharField(max_length=255)

class RiskCategory(BaseModel):
    name = models.CharField(max_length=255)


class RiskScroingMethod(BaseModel):
    name = models.CharField(max_length=255)

class ControlRegister(BaseModel):
    name = models.CharField(max_length=255)


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
    risk_scoring_method = models.ForeignKey(RiskScroingMethod)
    external_reference_id = models.CharField(max_length=100, null=False, blank=False)
    courrent_likelihood = models.CharField(max_length=32, choices=LIKELIHOODS, null=False, blank=False)
    control_regulation = models.ForeignKey(ControlRegister)
    current_impact = models.CharField(max_length=32, choices=IMPACTS, null=False, blank=False)
    control_number = models.CharField(max_length=100, null=False, blank=False)
    affected_assets = models.CharField(max_length=100, null=False, blank=False)
    risk_assessment = models.TextField(null=True, blank=True)
    additional_notes = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="owner")
    owner_manager = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="owner_maager")
    supporting_document = models.FileField(upload_to="risk_register/document")
    tags = models.CharField(max_length=255)


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

    risk = models.OneToOneField(RiskRegister, on_delete=models.CASCADE)
    submittion_date = models.DateTimeField()
    planned_mitigation_date = models.DateTimeField()
    planning_strategy = models.CharField(max_length=255, choices=PLANNING_STRATEGIES, null=True, blank=True)
    mitigation_effort = models.CharField(max_length=255, choices=MITIGATION_EFFORTS, null=True, blank=True)
    mitigation_cost = models.CharField(max_length=255, null=True, blank=True)
    mitigation_owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="mitigation_owner")
    migitation_team = models.ManyToManyField(Account, blank=True)
    mitigation_percent = models.IntegerField(default=0)
    current_solution = models.CharField(max_length=255, null=True, blank=True)
    security_requirements = models.TextField(null=True, blank=True)
    security_recommendations = models.TextField(null=True, blank=True)
    supporting_documentation = models.TextField(null=True, blank=True)

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
    review = models.CharField(max_length=32, choices=REVIEWS, null=True, blank=True)
    next_step = models.CharField(max_length=255, choices=NEXT_STEPS, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    next_date = models.DateField(null=True, blank=True)
    is_different_instend = models.BooleanField(default=False)



class ReviewProject(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    status = models.IntegerField(default=0, validators=[MaxValueValidator(100)])




class Comment(BaseModel):
    mitigation = models.ForeignKey(RiskMitigation, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False)