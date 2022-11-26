from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ads.models import Ad, Category, Selection
from ads.validators import is_published_validator
from users.models import User, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        queryset=User.objects.all(),
        slug_field='username'
    )
    category = serializers.SlugRelatedField(
        required=False,
        queryset=Category.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Ad
        fields = "__all__"


class AdCreateSerializer(serializers.ModelSerializer):
    is_published = serializers.BooleanField(validators=[is_published_validator], default=None)
    id = serializers.IntegerField(required=False)
    image = serializers.ImageField(required=False)

    author = serializers.SlugRelatedField(
        required=False,
        queryset=User.objects.all(),
        slug_field='username'
    )
    category = serializers.SlugRelatedField(
        required=False,
        queryset=Category.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Ad
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._author_id = self.initial_data.pop('author_id')
        self._category_id = self.initial_data.pop('category_id')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        ad = Ad.objects.create(
            name=validated_data.get('name'),
            price=validated_data.get('price'),
            description=validated_data.get('description'),
            is_published=validated_data.get('is_published')
        )
        ad.author = get_object_or_404(User, pk=self._author_id)
        ad.category = get_object_or_404(Category, pk=self._category_id)
        ad.save()

        return ad


class AdUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(required=False)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    category = serializers.SlugRelatedField(
        required=False,
        queryset = Category.objects.all(),
        slug_field='name'
    )

    def is_valid(self, raise_exception=False):
        self._category_id = self.initial_data.pop('category_id')
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        ad = super().save()
        ad.category = get_object_or_404(Category, pk=self._category_id)
        ad.save()

        return ad


    class Meta:
        model = Ad
        fields = '__all__'


class AdImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    is_published = serializers.BooleanField(read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'
