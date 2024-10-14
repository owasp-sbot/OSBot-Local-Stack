from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from osbot_aws.aws.s3.S3 import S3

from osbot_local_stack.testing.TestCase__Local_Stack import TestCase__Local_Stack


class TestCase__Local_Stack__Temp_Bucket(TestCase__Local_Stack):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        #cls.temp_bucket = cls.local_stack.create_temp_bucket()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        #cls.local_stack.delete_bucket(cls.temp_bucket)

    @cache_on_self
    def s3(self):
        return S3()