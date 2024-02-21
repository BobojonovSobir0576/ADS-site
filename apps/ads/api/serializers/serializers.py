from rest_framework import serializers

from apps.ads.models import *


class CategoryListSerializers(serializers.ModelSerializer):
    """ Category create update and details """
    icon = serializers.ImageField(read_only=True, required=True)
    name = serializers.CharField(write_only=True)

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'subcategory', 'icon', 'date_create', 'date_update'
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.model_method()
        return super().update(instance, validated_data)


class CountryListSerializers(serializers.ModelSerializer):
    """ Country create update and details """
    class Meta:
        model = Country
        fields = [
            'id', 'name', 'date_create', 'date_update'
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.model_method()
        return super().update(instance, validated_data)


class CityListSerializers(serializers.ModelSerializer):
    """ City create update and details """
    country = serializers.IntegerField(write_only=True)

    class Meta:
        model = City
        fields = [
            'id', 'name', 'country', 'shrt_name', 'date_create', 'date_update'
        ]

    def create(self, validated_data):
        return super().create(**validated_data)

    def update(self, instance, validated_data):
        instance.model_method()
        return super().update(instance, validated_data)


class OptionalFieldListSerializers(serializers.ModelSerializer):

    class Meta:
        model = OptionalField
        fields = []


class OptionalFieldThroughListSerializers(serializers.ModelSerializer):
    job = serializers.IntegerField(write_only=True)
    image = serializers.ImageField(required=True)
    file = serializers.FileField(required=True)

    class Meta:
        model = OptionalFieldThrough
        fields = [
            'id', 'job', 'optional_field', 'value', 'image', 'file'
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.model_method()
        return super().update(instance, validated_data)


class JobListSerializers(serializers.ModelSerializer):
    photo = serializers.ImageField(required=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'category', 'city', 'description', 'contract_number',
            'email', 'name', 'user', 'status', 'photo', 'date_create', 'date_update',
            'is_top', 'is_vip'
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.model_method()
        return super().update(instance, validated_data)


class JobDetailSerializers(serializers.ModelSerializer):
    """ Job details create update and details """
    category = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'category', 'city', 'description', 'contract_number',
            'email', 'name', 'user', 'status', 'photo', 'date_create', 'date_update',
            'is_top', 'is_vip'
        ]

    def get_category(self, obj):
        """ get job category. type : str """
        return Category.objects.filter(id=obj.category.id).values('name')

    def get_city(self, obj):
        """
        get city type. type : list
            {
                "name" : "Barcelona",
                "country": "Spain"
            }
        """
        return list(City.objects.filter(id=obj.city.id).values('name', 'country'))

    def get_user(self, obj):
        """
        get user details
            {
                "email" : "test@test.com",
                "phone" : "+9989912345678",
                ...
            }
        """
        return list(CustomUser.obejcts.filter(id=obj.user.id).values(
            'id', 'email', 'phone', 'first_name', 'last_name', 'photo'
        ))
