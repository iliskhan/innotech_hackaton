from rest_framework import serializers

from .models import VkUserPersonal, VkUserOccupation, VkUserEducation, VkUserData


class VkUserPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = VkUserPersonal
        fields = '__all__'


class VkUserOccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VkUserOccupation
        fields = '__all__'


class VkUserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VkUserEducation
        fields = '__all__'


class VkUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VkUserData
        fields = '__all__'


class VkUserDataDetailSerializer(serializers.ModelSerializer):
    personal = VkUserPersonalSerializer(read_only=True)
    occupation = VkUserOccupationSerializer(read_only=True)
    education = VkUserEducationSerializer(read_only=True)

    class Meta:
        model = VkUserData
        fields = '__all__'
