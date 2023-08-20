from rest_framework import serializers
from UserProfile_API import models

class UserProfileSerializer(models.UserProfile):
    """Serializes UserProfile model"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'username', 'email', 'date_of_birth', 'can_be_contacted',
                  'can_be_shared', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
                }
            }

    def create(self, validated_data):
        """Create and return new user"""
        user = models.UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            date_of_birth=validated_data['date_of_birth'],
            can_be_contacted=validated_data['can_be_contacted'],
            can_be_shared=validated_data['can_be_shared']
        )

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
 
        return super().update(instance, validated_data)