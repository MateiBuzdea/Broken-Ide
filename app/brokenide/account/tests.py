from django.test import TestCase
from account.models import UserAccount
from ide.utils import *


class UserAccountTestCase(TestCase):
    def setUp(self):
        UserAccount.objects.create_user(
            username='test_user_1', password='password1')
        UserAccount.objects.create_user(
            username='../test_user_2', password='password2')
        UserAccount.objects.create_user(
            username='./test_user_3', password='password3')

    def test_users(self):
        """
        Test users and their according jail folder
        """
        user1 = UserAccount.objects.get(username="test_user_1")
        user2 = UserAccount.objects.get(username="../test_user_2")
        user3 = UserAccount.objects.get(username="./test_user_3")

        self.assertEqual(get_user_jail(user1.username),
                         USER_JAILS_PATH / user1.username)
        self.assertEqual(get_user_jail(user2.username),
                         USER_JAILS_PATH / user2.username)
        self.assertEqual(get_user_jail(user3.username),
                         USER_JAILS_PATH / user3.username)

        # rename user to check if jail folder changes name
        user1._old_username = user1.username
        user1.username = 'test_user_1_updated'
        user1.save()
        user1.refresh_from_db()
        self.assertEqual(get_user_jail(user1.username),
                         USER_JAILS_PATH / user1.username)

        user1._old_username = user1.username
        user1.username = '../test_user_1_updated'
        user1.save()
        user1.refresh_from_db()
        self.assertEqual(get_user_jail(user1.username),
                         USER_JAILS_PATH / user1.username)
