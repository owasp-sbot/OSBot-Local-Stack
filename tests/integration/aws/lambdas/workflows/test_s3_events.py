# import pytest
# from osbot_aws.aws.s3.S3 import S3
#
# from osbot_utils.utils.Objects import dict_to_obj
#
# from osbot_utils.utils.Json import json_parse
#
# from osbot_utils.utils.Env import set_env
#
# from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda
#
# from osbot_aws.AWS_Config import aws_config
#
# from osbot_aws.aws.lambda_.Lambda import Lambda
#
# from osbot_local_stack.testing.TestCase__Local_Stack                import TestCase__Local_Stack
# from osbot_utils.utils.Dev                                          import pprint
# from osbot_local_stack.aws.lambdas.workflows.s3_events              import run
# from osbot_local_stack.utils.Version                                import version__osbot_local_stack
# from osbot_local_stack.testing.TestCase__Local_Stack__Temp_Lambda   import TestCase__Local_Stack__Temp_Lambda, \
#     LAMBDA__DEPENDENCIES__REQUESTS
#
#
# class test_s3_events__create_bucket_and_lambda(TestCase__Local_Stack__Temp_Lambda):
#     lambda_handler = run
#     delete_after_run = False
#
#     @classmethod
#     def create_temp_lambda(cls):
#         cls.deploy_lambda.add_osbot_utils()
#         cls.deploy_lambda.add_modules(LAMBDA__DEPENDENCIES__REQUESTS)
#         super().create_temp_lambda()
#
#     def test_invoke(self):
#         response = self.lambda_function.invoke()
#         assert response == '200'
#
# #@pytest.mark.skip("Only for local development")
# class test_s3_events(TestCase__Local_Stack):
#     aws_region     = 'eu-central-1'
#     s3_bucket      = "local-stack-gi0c5q1ufu51"
#     lambda_handler = run
#
#     def setUp(self):
#         set_env('OSBOT_LAMBDA_S3_BUCKET', self.s3_bucket)
#
#     def test_update_and_invoke(self):
#
#         with Deploy_Lambda(handler=self.lambda_handler) as _:
#             _.add_osbot_utils()
#             _.add_modules(LAMBDA__DEPENDENCIES__REQUESTS)
#             _.update()
#             response = _.invoke()
#             pprint(response)
#
#     def test_invoke(self):
#         with Deploy_Lambda(handler=self.lambda_handler) as _:
#             pprint(S3().buckets())
#             pprint(Lambda().functions_names())
#
# class test_s3_events__setup_event(TestCase__Local_Stack):
#     aws_region = 'eu-central-1'
#
#     def test_create_event(self):
#         lambda_handler = run
#         #deploy_lambda = Deploy_Lambda(handler=lambda_handler)
#         #pprint(deploy_lambda.lambda_function().function_arn())
#         with Lambda(name=run.__module__) as _:
#             function_arn = _.function_arn()
#
#         notification_configuration = {
#             'LambdaFunctionConfigurations': [
#                 {
#                     'LambdaFunctionArn': function_arn,
#                     'Events': ['s3:ObjectCreated:*',
#                                's3:ObjectRemoved:*']  # Trigger on all object created and deleted events
#                 }
#             ]
#         }
#
#         bucket_name = 'local-stack-fire-events'
#         s3 = S3()
#         result = s3.client().put_bucket_notification_configuration(Bucket=bucket_name,
#                                                                    NotificationConfiguration=notification_configuration)
#
#         pprint(result)
#         pprint(s3.bucket_notification(bucket_name))
#
#         #pprint(s3.bucket_create(bucket_name, self.aws_region))
#         #pprint(S3().buckets())
#
#
#     def test_trigger_event(self):
#         s3 = S3()
#         bucket_name = 'local-stack-fire-events'
#
#         kwargs__create = dict(file_contents = 'some contents',
#                               bucket        = bucket_name    ,
#                               key           = 'an_file_2.txt' )
#         kwargs__delete = dict(bucket        = bucket_name    ,
#                               key           = 'an_file_2.txt' )
#         s3.file_create_from_string(**kwargs__create)
#         s3.file_delete(**kwargs__delete)
#
#
#
#     def test_review_data(self):
#         data = {'event': {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'eu-central-1', 'eventTime': '2024-10-15T11:18:43.983Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AIDAJDPLRKLG7UEXAMPLE'}, 'requestParameters': {'sourceIPAddress': '127.0.0.1'}, 'responseElements': {'x-amz-request-id': '600ac695', 'x-amz-id-2': 'eftixk72aD6Ap51TnqcoF8eFidJG9Z/2'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'a839778c', 'bucket': {'name': 'local-stack-fire-events', 'ownerIdentity': {'principalId': 'A3NL1KOZZKExample'}, 'arn': 'arn:aws:s3:::local-stack-fire-events'}, 'object': {'key': 'an_file.txt', 'sequencer': '0055AED6DCD90281E5', 'eTag': '220c7810f41695d9a87d70b68ccf2aeb', 'size': 13}}}]}}
#         pprint(data)