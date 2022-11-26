import factory

from ads.models import Ad
from .category import CategoryFactory
from .user import UserFactory


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    #name = 'New Test Ad'
    name = factory.Faker('name')
    price = 1200
    is_published = False
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)