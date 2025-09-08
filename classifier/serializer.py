from rest_framework import serializers
from django.contrib.auth.models import User
class PredictSerializer(serializers.Serializer):
    text=serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["username","email","password"]
    
    def create(self,validated_data):
        username=validated_data["username"] 
        email = validated_data["email"]
        password=validated_data["password"]
        user=User.objects.create(
            username=username,
            email=email 
        )
        user.set_password(password)
        user.save()
        return user