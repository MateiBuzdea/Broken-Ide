from django.test import TestCase
from account.models import UserAccount
from ide.models import UserScript
from ide.utils import *


class UserScriptTestCase(TestCase):
    def setUp(self):
        # create users and their scripts
        user1 = UserAccount.objects.create_user(
            username='test_user_1', password='password1')

        UserScript.objects.create(
            name='test_script_11', user=user1)
        UserScript.objects.create(
            name='../test_script_12', user=user1)

        # UserAccount.objects.create_user(
        #     username='../test_user_2', password='password2')
        # UserScript.objects.create(
        #     name='./test_script_21', user='../test_user_2')
        # UserScript.objects.create(
        #     name='./test_script_22', user='../test_user_2')

    def test_scripts(self):
        """
        Test the user's scripts location and their content
        """
        user1 = UserAccount.objects.get(username="test_user_1")
        script11 = UserScript.objects.get(
            name='test_script_11', user=user1)
        script12 = UserScript.objects.get(
            name='../test_script_12', user=user1)

        # test for names
        self.assertEqual(script11.file_name, 'test_script_11.c')
        self.assertEqual(script12.file_name, '../test_script_12.c')

        # test for files
        save_user_script(
            username=user1.username,
            script_file_name=script11.file_name,
            script_content='Test script11 content',
        )
        self.assertEqual(
            get_user_script(user1.username, script11.file_name),
            b'Test script11 content',
        )
