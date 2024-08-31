from rest_framework import serializers
from django.contrib.auth import get_user_model
from .import models as user_models
from ..admin_app import models as admin_app_models

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    app = serializers.PrimaryKeyRelatedField(queryset=admin_app_models.App.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault()) 

    class Meta:
        model = user_models.Task
        fields = ['id', 'app', 'user', 'points', 'screenshot', 'completed']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Update user data, including password.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
