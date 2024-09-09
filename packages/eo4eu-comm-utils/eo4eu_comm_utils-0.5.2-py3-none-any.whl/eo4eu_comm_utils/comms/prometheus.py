import prometheus_client
from enum import Enum

from .interface import Comm


class PrometheusComm(Comm):
    def __init__(self, input: dict[Enum,tuple[str,str]]):
        prometheus_client.start_http_server(8000)
        self._metrics = {
            kind: prometheus_client.Counter(name, desc)
            for kind, (name, desc) in input.items()
        }

    def send(self, *kinds: Enum, value: int = 1, **kwargs):
        for kind in kinds:
            self._metrics[kind].inc(value)
