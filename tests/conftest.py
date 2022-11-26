from pytest_factoryboy import register

from tests.factories.ad import AdFactory
from tests.factories.category import CategoryFactory
from tests.factories.user import UserFactory

pytest_plugins = 'tests.fixtures'

register(UserFactory)
register(AdFactory)
register(CategoryFactory)
