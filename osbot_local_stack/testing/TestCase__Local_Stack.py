from unittest import TestCase

from osbot_aws.testing.Temp__Random__AWS_Credentials import Temp_AWS_Credentials

from osbot_local_stack.local_stack.Local_Stack import Local_Stack


class TestCase__Local_Stack(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.local_stack = Local_Stack()
        cls.temp_asw_credentials = Temp_AWS_Credentials()
        cls.temp_asw_credentials.set_vars()
        cls.local_stack.activate()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.local_stack.deactivate()
        cls.temp_asw_credentials.restore_vars()
