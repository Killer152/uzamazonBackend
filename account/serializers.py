import json
import re

from rest_framework import serializers

from account.models import UserModel, TokenModel, ProfileModel
from account.utils import send_sms_code, generate_code


class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    dob = serializers.DateField()
    gender = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'dob', 'gender', 'password1', 'password2']
        depth = 1


class RegistrationTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = TokenModel
        fields = ['code', 'username']


class PasswordSetSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()


class RegistrationCompleteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', default=None)

    def create(self, validated_data):
        user = self.context['user']
        user.email = validated_data.pop('user').get('email')
        user.save()
        return UserModel.objects.create(user=user, **validated_data)

    class Meta:
        model = UserModel
        fields = ['avatar', 'fio', 'about', 'role', 'email']


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'email']


class PasswordForgetCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=12)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['dob', 'gender', 'avatar']


class ProfileSerializer(serializers.ModelSerializer):
    profile = serializers.JSONField()

    def to_representation(self, instance):
        self.fields['profile'] = ProfileUpdateSerializer(read_only=True)
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        if 'email' in validated_data.keys():
            instance.email = validated_data['email']
        if 'first_name' in validated_data.keys():
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data.keys():
            instance.last_name = validated_data['last_name']
        instance.save()

        if 'dob' in profile_data and 'gender' in profile_data:
            profile = instance.profile
            profile.dob = profile_data['dob']
            profile.gender = profile_data['gender']
            profile.save()

        return instance

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']
        read_only_fields = ['id', 'username']
        depth = 1


class ProfileAvatarSerializer(serializers.ModelSerializer):
    def save(self, *args, **kwargs):
        if self.instance.avatar:
            self.instance.avatar.delete()
        return super().save(**kwargs)

    class Meta:
        model = ProfileModel
        fields = ['avatar']