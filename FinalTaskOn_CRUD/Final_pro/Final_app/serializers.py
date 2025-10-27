from rest_framework import serializers
from .models import Insta_Acc

class InstaAccSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insta_Acc
        fields = ['userid', 'username', 'password', 'email', 'profile_pic']

    def validate_profile_pic(self, value):
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError('File size exceeds 5MB.')

        allowed_types = ['image/jpeg', 'image/png']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError('Only JPEG and PNG are allowed.')
        return value
