from typing import Any

from airflow.hooks.base import BaseHook
from airflow.models import BaseOperator
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults


class CustomOperator(BaseOperator):

    @apply_defaults
    def __init__(self, args, **kwargs):
        super(CustomOperator, self).__init__(**kwargs)
        self.args = args or ()

    def execute(self, context):
        print("From operator", self.args)


class CustomHook(BaseHook):

    def get_conn(self) -> Any:
        pass

    def print_argument(self, arg="Hell"):
        print("From hook", self.arg + " " + arg)

    def __init__(self, arg, **kwargs):
        self.arg = arg
        super().__init__()


class CustomSensor(BaseSensorOperator):

    @apply_defaults
    def __init__(self, **kwargs):
        self.rtn = False
        super(CustomSensor, self).__init__(**kwargs)

    def poke(self, context):
        rtn = self.rtn
        self.rtn = not rtn
        return rtn
