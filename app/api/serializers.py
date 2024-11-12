from rest_framework import serializers
from app.models import Framework

class FrameWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Framework
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
