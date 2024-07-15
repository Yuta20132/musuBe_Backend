from rest_framework import serializers
from .models import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'affiliation')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        affiliation = self.initial_data.get('affiliation')
        if '大学' in affiliation or '研究所' in affiliation:
            if not value.endswith('ac.jp'):
                raise serializers.ValidationError("大学や研究所の所属の場合、メールアドレスはac.jpドメインである必要があります。")
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            affiliation=validated_data['affiliation'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user