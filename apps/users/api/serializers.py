from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import *


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'last_name')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthGroup
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name')


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)
    password2 = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': 'Debe ingresar ambas contraseñas iguales'}
            )
        return data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'name': instance['name'],
            'username': instance['username'],
            'email': instance['email'],
            'last_name': instance['last_name'],
        }


class UserAux(serializers.Serializer):
    name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    group = serializers.IntegerField()

    def validate(self, data):
        return data


class GroupAux(serializers.Serializer): 
    user_id = serializers.IntegerField()

    def validate(self, data):
        return data


class UserAux2(serializers.Serializer):
    user = serializers.CharField()

    def validate(self, data):
        return data
class UserGroupserializer(serializers.ModelSerializer):

    class Meta:
        model = UsersUserGroups
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': instance.user.username if instance.user is not None else '',
            'group': instance.group.name if instance.group is not None else '',
        }

class UserGroupAuxserializer(serializers.ModelSerializer):
    
    class Meta:
        model = UsersUserGroups
        fields = '__all__'

 