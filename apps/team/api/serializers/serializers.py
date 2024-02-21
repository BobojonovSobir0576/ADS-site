from rest_framework import serializers

from apps.team.models import *


class TeamRoleListSerializers(serializers.ModelSerializer):
    """ Team Role create update and details """

    class Meta:
        model = TeamRole
        fields = ['id', 'name']

    def create(self, validated_data):
        return super().create(**validated_data)

    def update(self, instance, validated_data):
        instance.model_method()
        return super().update(instance, validated_data)


class TeamListSerializers(serializers.ModelSerializer):
    """ Team create update"""

    role = serializers.IntegerField(write_only=True)
    photo = serializers.ImageField(required=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'photo', 'role', 'date_create', 'date_update'
        ]

    def create(self, validated_data):
        return super().create(**validated_data)

    def update(self, instance, validated_data):
        instance.model_method()
        return super().update(instance, validated_data)


class TeamDetailSerializers(serializers.ModelSerializer):
    """ Team details"""

    role = TeamRoleListSerializers(read_only=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'photo', 'role', 'date_create', 'date_update'
        ]