from netbox.filtersets import NetBoxModelFilterSet
from django.db.models import Q
import django_filters
from . import models

# ThreatSource Filters


class ThreatSourceFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = models.ThreatSource
        fields = ["id", "name", "threat_type", "capability", "intent", "targeting", "description", "notes"]


# ThreatEvent Filters


class ThreatEventFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = models.ThreatEvent
        fields = ["threat_source", "relevance", "likelihood", "impact"]


# Vulnerability Filters


class VulnerabilityFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = models.Vulnerability
        fields = [
            "id",
            "name",
            "cve",
            "description",
            "notes",
            "cvssaccessVector",
            "cvssaccessComplexity",
            "cvssauthentication",
            "cvssconfidentialityImpact",
            "cvssintegrityImpact",
            "cvssavailabilityImpact",
            "cvssbaseScore",
            ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(cve__icontains=value)
            | Q(cvssaccessVector__icontains=value)
        )
        return queryset.filter(qs_filter)


# VulnerabilityAssignment Filters


class VulnerabilityAssignmentFilterSet(NetBoxModelFilterSet):
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(vulnerability__name__icontains=value) 
            | Q(vulnerability__cve__icontains=value)
        )
        return queryset.filter(qs_filter)

    class Meta:
        model = models.VulnerabilityAssignment
        fields = ["vulnerability"]


# Risk Filters


class RiskFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = models.Risk
        fields = ["name", "threat_event", "description", "impact", "likelihood"]

# Control Filters

class ControlFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = models.Control
        fields = [
            "name",
            "description",
            "notes",
            "category",
            "risk",
        ]