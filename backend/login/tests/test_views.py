from django.test import TestCase
from login.views import get_unique_initials, get_unique_username
from login.models import User
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class GetUniqueInitialsTest(TestCase):
    def setUp(self):
        # Create some users for testing
        try:
            User.objects.create(first_name='John', last_name='Doe', initials='JD', username='jd@mail.com')
            User.objects.create(first_name='Jane', last_name='Doe', initials='JD01', username='jd01@mail.com')
            User.objects.create(first_name='Jack', last_name='Doe', initials='JD02', username='jd02@mail.com')
            User.objects.create(first_name='Jim', last_name='Tran', initials='JT', username='jt@mail.com')
            User.objects.create(first_name='Jonny', middle_name='Smith', last_name='Tank', initials='JST', username='jst@mail.com')
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

# class GetUniqueUsernameTest(TestCase):
#     def setUp(self):
#         User.objects.create(username='jdoe', email='jdoe@mail.com')
#         User.objects.create(username='jdoe01', email='jdoe01@mail.com')
#         User.objects.create(username='jdoe02', email='jdoe02@mail.com')
#         User.objects.create(username='jfdoe', email='jdoe@mail.com')

#     def test_get_unique_username(self):
#         username = get_unique_username('John', 'F', 'Doe')
#         self.assertEqual(username, 'jfdoe01')

#         username = get_unique_username('John', '', 'Doe')
#         self.assertEqual(username, 'jdoe03')

#         username = get_unique_username('Jane', 'F', 'Doe')
#         self.assertEqual(username, 'jfdoe02')