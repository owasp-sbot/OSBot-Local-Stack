from osbot_local_stack.aws.lambdas.dev.with__requests               import run
from osbot_local_stack.utils.Version                                import version__osbot_local_stack
from osbot_local_stack.testing.TestCase__Local_Stack__Temp_Lambda   import TestCase__Local_Stack__Temp_Lambda

class test_hello_world(TestCase__Local_Stack__Temp_Lambda):

    @classmethod
    def setUpClass(cls):
        cls.lambda_handler = run
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    @classmethod
    def create_temp_lambda(cls):
        cls.deploy_lambda.add_module('requests')
        cls.deploy_lambda.add_module('idna'    )
        cls.deploy_lambda.add_module('certifi' )
        cls.deploy_lambda.add_module('certifi' )
        super().create_temp_lambda()

    def test_invoke(self):
        google_html = self.lambda_function.invoke() #== "<module 'requests' from '/var/task/requests/__init__.py'>"
        assert 'Google' in google_html
