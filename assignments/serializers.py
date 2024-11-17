from rest_framework_mongoengine import serializers
from .models import User, Assignment
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_admin']
    
    def validate_username(self, value):
        # Ensure username is not empty
        if not value:
            raise ValidationError("Username cannot be empty.")
        return value

    def validate_password(self, value):
        # Password should be at least 6 characters long
        if len(value) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
        return value


class AssignmentSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Assignment
        fields = ['user_id', 'task', 'admin', 'submitted_at', 'status']

    def validate_task(self, value):
        # Ensuring task is not empty
        if not value:
            raise ValidationError("Task cannot be empty.")
        return value

    def validate_admin(self, value):
        # Ensuring that the admin exists or is valid
        if not value:
            raise ValidationError("Admin field cannot be empty.")
        return value

    def validate(self, data):
        if not data.get('user_id'):
            raise ValidationError("User ID is required.")
        return data