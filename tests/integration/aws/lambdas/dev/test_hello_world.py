from osbot_local_stack.aws.lambdas.dev.hello_world                import run
from osbot_local_stack.testing.TestCase__Local_Stack__Temp_Lambda import TestCase__Local_Stack__Temp_Lambda

class test_hello_world(TestCase__Local_Stack__Temp_Lambda):

    @classmethod
    def setUpClass(cls):
        cls.lambda_handler = run
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_invoke(self):
        assert self.lambda_function.invoke()                 == 'Hello "World"'
        assert self.lambda_function.invoke(dict(name='abc')) == 'Hello "abc"'
