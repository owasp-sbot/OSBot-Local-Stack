from unittest import TestCase

from osbot_local_stack.local_stack.Local_Stack import Local_Stack


class TestCase__Local_Stack(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.local_stack = Local_Stack()

    @classmethod
    def tearDownClass(cls) -> None:
        pass
