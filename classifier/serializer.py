from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class PredictSerializer(serializers.Serializer):
    text=serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["username","email","password","password2"]

    def validate_password(self, value):
        print(value)
        validate_password(value)
        
        return value
    
    def validate_email(self,email):
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError("Enter valid email")
        return email
    
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Passwords must match."})
        return data
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