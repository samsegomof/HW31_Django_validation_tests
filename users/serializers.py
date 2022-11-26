from rest_framework import serializers

from users.models import User, Location
from users.validators import EmailValidator


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = serializers.SlugRelatedField(
        required=False,
        queryset=Location.objects.all(),
        many=True,
        slug_field='name'
    )
    email = serializers.EmailField(validators=[EmailValidator])

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('location')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)

        location, _ = Location.objects.get_or_create(name=self._location)
        user.location = location
        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)

    location = serializers.SlugRelatedField(
        required=False,
        queryset=Location.objects.all(),
        many=True,
        slug_field='name'
    )

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('location')
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save()

        location, _= Location.objects.get_or_create(name=self._location)
        user.location = location
        user.save()

        return user

    class Meta:
        model = User
        fields = '__all__'


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]
