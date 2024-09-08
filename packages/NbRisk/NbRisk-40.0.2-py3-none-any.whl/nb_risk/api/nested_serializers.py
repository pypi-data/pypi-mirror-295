from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from .. import models, choices

# ThreatSource Nested Serializers

# class NestedThreatSourceSerializer(WritableNestedSerializer):
#     url = serializers.HyperlinkedIdentityField(
#         view_name="plugins-api:nb_risk-api:threatsource-detail"
#     )
#     display = serializers.SerializerMethodField('get_display')
    
#     def get_display(self, obj):
#         return obj.name

#     class Meta:
#         model = models.ThreatSource
#         fields = ["id", "url", "display", "name"]
    
# Risk Nested Serializers

class NestedRiskSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nb_risk-api:risk-detail"
    )
    display = serializers.SerializerMethodField('get_display')
    
    def get_display(self, obj):
        return obj.name

    class Meta:
        model = models.Risk
        fields = ["id", "url", "display", "name"]