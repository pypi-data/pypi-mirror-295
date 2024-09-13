import os
from pinecone_plugin_interface import PineconePlugin

from pinecone_plugins.assistant.models.evaluation_responses import AlignmentResponse
from pinecone_plugins.assistant.evaluation.core.client.api.metrics_api import MetricsApi
from pinecone_plugins.assistant.evaluation.core.client.model.alignment_request import AlignmentRequest
from pinecone_plugins.assistant.evaluation.core.client import ApiClient as MetricsApiClient


class Metrics:
    def __init__(self, metrics_api):
        self._metrics_api = metrics_api

    def alignment(self, question: str, answer: str, ground_truth_answer: str) -> AlignmentResponse:
        request = AlignmentRequest(question=question, answer=answer, ground_truth_answer=ground_truth_answer)
        return AlignmentResponse.from_openapi(self._metrics_api.metrics_alignment(alignment_request=request))


class Evaluation(PineconePlugin):
    def __init__(self, config, client_builder):
        self.config = config

        self.host = os.getenv("PINECONE_PLUGIN_ASSISTANT_CONTROL_HOST", "https://api.pinecone.io")
        if self.host.endswith("/"):
            self.host = self.host[:-1]
        self._client_builder = client_builder
        self._metrics_api = client_builder(MetricsApiClient, MetricsApi, 'unstable', host=self.host)
        self.metrics = Metrics(self._metrics_api)
