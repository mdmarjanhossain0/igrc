import django_filters
from app.models import (
	Evidence
)

class EvidenceFilterSet(django_filters.FilterSet):
	# division = django_filters.BaseInFilter(field_name='division', lookup_expr='in')
	# district = django_filters.BaseInFilter(field_name='district', lookup_expr='in')
	# region = django_filters.BaseInFilter(field_name='region', lookup_expr='in')
	# institution = django_filters.BaseInFilter(field_name='institution', lookup_expr='in')
	# role = django_filters.BaseInFilter(field_name='role', lookup_expr='in')
    
	class Meta:
		model = Evidence
		fields = [
			"project",
			"task",
			"clause",
			"control",
			"subcontrol"
		]