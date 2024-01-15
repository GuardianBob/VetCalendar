from django.test import TestCase
from login.views import get_unique_initials
from login.models import User
from django.core.exceptions import ValidationError

class GetUniqueInitialsTest(TestCase):
    def setUp(self):
        # Create some users for testing
        try:
            User.objects.create(first_name='John', last_name='Doe', initials='JD')
            User.objects.create(first_name='Jane', last_name='Doe', initials='JD01')
            User.objects.create(first_name='Jack', last_name='Doe', initials='JD02')
            User.objects.create(first_name='Jim', last_name='Tran', initials='JT')
            User.objects.create(first_name='Jonny', middle_name='Smith', last_name='Tank', initials='JST')
        except ValidationError as e:
            print(e)

    def test_get_unique_initials(self):
        print("Running get_unique_initials test")
        # Test with initials that are not yet used
        initials = get_unique_initials('James', 'Robert', 'Doe')
        self.assertEqual(initials, 'JRD')

        # Test with initials that are not yet used and no middle name
        initials = get_unique_initials('James', '', 'Doe')
        self.assertEqual(initials, 'JD03')

        # Test with initials that are not yet used and different last name
        initials = get_unique_initials('John', '', 'Smith')
        self.assertEqual(initials, 'JS')

        # Test with initials that are not yet used and middle name
        initials = get_unique_initials('John', 'Robert', 'Thompson')
        self.assertEqual(initials, 'JRT')

        # Test with initials that are not yet used and middle name
        initials = get_unique_initials('John', 'Smith', 'Thompson')
        self.assertEqual(initials, 'JT01')