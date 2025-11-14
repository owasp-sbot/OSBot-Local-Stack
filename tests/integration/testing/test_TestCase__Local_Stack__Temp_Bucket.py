from osbot_local_stack.local_stack.Local_Stack__Internal            import DEFAULT__LOCAL_STACK__TARGET_SERVER
from osbot_local_stack.testing.TestCase__Local_Stack__Temp_Bucket   import TestCase__Local_Stack__Temp_Bucket

class test_TestCase__Local_Stack__Temp_Bucket(TestCase__Local_Stack__Temp_Bucket):

    def test_s3(self):
        assert self.s3.client().meta.endpoint_url == DEFAULT__LOCAL_STACK__TARGET_SERVER

    def test_temp_bucket(self):
        assert self.local_stack.is_local_stack_configured_and_available() is True
        with self.s3 as _:
            assert self.s3_bucket in _.buckets()

    def test_temp_bucket_name(self):
        assert self.temp_bucket_name().startswith('local-stack-')