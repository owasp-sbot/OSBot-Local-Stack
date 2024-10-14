from osbot_aws.AWS_Config import ENV_NAME__AWS_ENDPOINT_URL
from osbot_local_stack.local_stack.Local_Stack__Internal import Local_Stack__Internal, \
    ENV_NAME__LOCAL_STACK__TARGET_SERVER
from osbot_utils.utils.Env import get_env, set_env, del_env

from osbot_utils.base_classes.Type_Safe import Type_Safe

class Local_Stack(Type_Safe):
    endpoint_url__saved  : str                   = None
    local_stack__internal: Local_Stack__Internal

    def __enter__(self):
        self.activate()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deactivate()
        return self


    def activate(self):
        endpoint_url = self.local_stack__internal.endpoint_url
        self.endpoint_url__saved = get_env(ENV_NAME__AWS_ENDPOINT_URL)
        set_env(ENV_NAME__AWS_ENDPOINT_URL, endpoint_url)
        return self

    def deactivate(self):
        if self.endpoint_url__saved is None:
            del_env(ENV_NAME__AWS_ENDPOINT_URL)
        else:
            set_env(ENV_NAME__AWS_ENDPOINT_URL, self.endpoint_url__saved)
        return self

    def local_stack__health(self):
        return self.local_stack__internal.get__internal_health()


