from unittest import TestCase

from osbot_aws.aws.sts.STS import STS

from osbot_aws.aws.s3.S3 import S3

from osbot_local_stack.local_stack.Local_Stack import Local_Stack
from osbot_local_stack.testing.TestCase__Local_Stack import TestCase__Local_Stack


class test_TestCase__Local_Stack(TestCase__Local_Stack):


    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        assert cls.local_stack.is_local_stack_configured_and_available() is False

    def test__setUpClass(self):
        assert type(self.local_stack)                                     is Local_Stack
        assert self.local_stack.is_local_stack_configured_and_available() is True

    def test_boto3_sessions(self):
        assert S3 ().client().meta.endpoint_url == Local_Stack().local_stack__internal.endpoint_url
        assert STS().client().meta.endpoint_url == Local_Stack().local_stack__internal.endpoint_url