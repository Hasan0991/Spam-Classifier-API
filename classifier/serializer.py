from rest_framework import serializers

class PredictSerializer(serializers.Serializer):
    text=serializers.CharField()