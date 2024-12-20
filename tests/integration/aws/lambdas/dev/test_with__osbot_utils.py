from osbot_local_stack.aws.lambdas.dev.with__osbot_utils            import run
from osbot_local_stack.utils.Version                                import version__osbot_local_stack
from osbot_local_stack.testing.TestCase__Local_Stack__Temp_Lambda   import TestCase__Local_Stack__Temp_Lambda

class test_with__osbot_utils(TestCase__Local_Stack__Temp_Lambda):

    @classmethod
    def setUpClass(cls):
        cls.lambda_handler = run
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    @classmethod
    def create_temp_lambda(cls):
        cls.deploy_lambda.add_osbot_utils()
        super().create_temp_lambda()

    def test_invoke(self):
        assert self.lambda_function.invoke() == f'(using osbot-utils) current version: {version__osbot_local_stack}'
