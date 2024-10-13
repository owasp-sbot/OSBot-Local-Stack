import requests
from osbot_utils.utils.Objects import dict_to_obj

from osbot_utils.utils.Http import url_join_safe

from osbot_utils.utils.Env import get_env

from osbot_utils.base_classes.Type_Safe import Type_Safe

ENV_NAME__LOCAL_STACK__TARGET_SERVER = 'LOCAL_STACK__TARGET_SERVER'
DEFAULT__LOCAL_STACK__TARGET_SERVER  = 'http://localhost:4566'

class Local_Stack__Internal(Type_Safe):

    def target_server(self):
        return get_env(ENV_NAME__LOCAL_STACK__TARGET_SERVER, DEFAULT__LOCAL_STACK__TARGET_SERVER)

    def get__aws_lambda_runtimes(self):
        return self.requests__aws__get('lambda/runtimes')

    def get__internal_diagnose(self):
        return self.requests__internal__get('diagnose')

    def get__internal_health(self):
        return self.requests__internal__get('health')

    def get__internal_init(self):
        return self.requests__internal__get('init')

    def get__internal_plugins(self):
        return self.requests__internal__get('plugins')

    def requests__aws__get(self, action):
        path = f'/_aws/{action}'
        return self.requests__get(path)

    def requests__internal__get(self, action):
        path = f'/_localstack/{action}'
        return self.requests__get(path)

    def requests__get(self, path):
        url = url_join_safe(self.target_server(), path)
        json_data = requests.get(url).json()
        obj_data = dict_to_obj(json_data)
        return obj_data
