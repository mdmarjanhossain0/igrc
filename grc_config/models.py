from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from account.models import Account, Audit

class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class StatusDB(BaseModel):
    name = models.CharField(max_length=32)

class RiskSource(BaseModel):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

class LikelyHood(BaseModel):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

class Impact(BaseModel):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    value = models.IntegerField(default=1, validators=[MaxValueValidator(100)])

class PlanningStrategy(BaseModel):
    name = models.CharField(max_length=32)

class MitigationEffort(BaseModel):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

class RiskStatus(BaseModel):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)


class NextStep(BaseModel):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

class DataClassifiation(BaseModel):
    name = models.CharField(max_length=32)




# EXTERNAL = "External"
#     PEOPLE = "People"
#     PROCESS = "Process"
#     SYSTEM = "System"
#     RISK_SOURCES = (
#         (EXTERNAL, EXTERNAL),
#         (PEOPLE, PEOPLE),
#         (PROCESS, PROCESS),
#         (SYSTEM, SYSTEM)
#     )
    # REMOTE = "Remote"
    # UNLIKELY = "UNLIKELY"
    # CREDIBLE = "Credible"
    # LIKELY = "Likely"
    # ALMOST_CERTAIN = "Almost Certain"
    # LIKELIHOODS = (
    #     (REMOTE, REMOTE),
    #     (UNLIKELY, UNLIKELY),
    #     (CREDIBLE, CREDIBLE),
    #     (LIKELY, LIKELY),
    #     (ALMOST_CERTAIN, ALMOST_CERTAIN)
    # )

    # INSIGNIFICANT = "Insignificant"
    # MINOR = "Minor"
    # MODARATE = "Modarate"
    # MAJOR = "Major"
    # EXTREME = "Extreme"
    # IMPACTS = (
    #     (INSIGNIFICANT, INSIGNIFICANT),
    #     (MINOR, MINOR),
    #     (MODARATE, MODARATE),
    #     (MAJOR, MAJOR),
    #     (EXTREME, EXTREME)
    # )



# ACCEPTED = "Accepted"
#     MITIGATE = "Mitigate"
#     RESEARCH = "Research"
#     TRANSFER = "Transfer"
#     WATCH = "Watch"
#     PLANNING_STRATEGIES = (
#         (ACCEPTED, ACCEPTED),
#         (MITIGATE, MITIGATE),
#         (RESEARCH, RESEARCH),
#         (TRANSFER, TRANSFER),
#         (WATCH, WATCH)
#     )



    # TRIVIAL = "Trivial"
    # MINOR = "Minor"
    # CONSIDARABLE = "Considarable"
    # SIGNIFICANT = "Significant"
    # EXCEPTIONAL = "Exceptional"
    # MITIGATION_EFFORTS = (
    #     (TRIVIAL, TRIVIAL),
    #     (MINOR, MINOR),
    #     (CONSIDARABLE, CONSIDARABLE),
    #     (SIGNIFICANT, SIGNIFICANT),
    #     (EXCEPTIONAL, EXCEPTIONAL)
    # )



    # CLOSED = "Closed"
    # MITIGATION_REVIEWED = "Mitigation Reviewd"
    # MITIGATION_PLANNE = "Mitigation Planne"
    # NEW = "New"
    # RESPONSED = "Responsed"
    # TREATED = "Treated"
    # UNTREATED = "Untreated"
    # STATUSSES = (
    #     (CLOSED, CLOSED),
    #     (MITIGATION_REVIEWED, MITIGATION_REVIEWED),
    #     (MITIGATION_PLANNE, MITIGATION_PLANNE),
    #     (NEW, NEW),
    #     (RESPONSED, RESPONSED),
    #     (TREATED, TREATED),
    #     (UNTREATED, UNTREATED)
    # )

# APPROVE_RISK = "Approve Risk"
#     REJECT_RISK_AND_CLOSE = "Reject Risk and Close"
#     REVIEWS = (
#         (APPROVE_RISK, APPROVE_RISK),
#         (REJECT_RISK_AND_CLOSE, REJECT_RISK_AND_CLOSE)
#     )


    # ACCEPT_UNTILL_NEXT_REVIEW = "Accept Until Next Review"
    # CONSIDER_FOR_PROJECT = "Consider for Project"
    # SUBMIT_AS_A_PRODUCTION_ISSUE = "Submit as a Production Issue"
    # NEXT_STEPS = (
    #     (ACCEPT_UNTILL_NEXT_REVIEW, ACCEPT_UNTILL_NEXT_REVIEW),
    #     (CONSIDER_FOR_PROJECT, CONSIDER_FOR_PROJECT),
    #     (SUBMIT_AS_A_PRODUCTION_ISSUE, SUBMIT_AS_A_PRODUCTION_ISSUE)
    # )

# UNASSIGNED = "Unassigned"
#     PUBLIC = "Public"
#     INTERNAL = "Internal"
#     CONFIDENTIAL = "Confidential"
#     RESTRICTED = "Restricted"
#     DATA_CLASSIFICATIONS = (
#         (UNASSIGNED, UNASSIGNED),
#         (PUBLIC, PUBLIC),
#         (INTERNAL, INTERNAL),
#         (CONFIDENTIAL, CONFIDENTIAL),
#         (RESTRICTED, RESTRICTED)
#     )
