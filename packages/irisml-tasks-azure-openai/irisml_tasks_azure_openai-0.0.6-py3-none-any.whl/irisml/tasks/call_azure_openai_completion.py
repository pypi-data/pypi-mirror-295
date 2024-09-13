import dataclasses
import logging
import typing
from urllib.parse import urlparse
import irisml.core
from irisml.tasks.create_azure_openai_completion_model import OpenAITextCompletionModel

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Call Azure OpenAI Text Completion API.

    Config:
        endpoint (str): Azure endpoint. Starts with https://
        deployment_name (str): Azure deployment name
        api_key (str): Azure API key
        temperature (float): Temperature parameter. Must be between 0 and 1. Larger value means more random completions.
        top_p (float): Top p parameter. Must be between 0 and 1. Larger value means more random completions.
        max_tokens (int): Maximum number of tokens to generate
        requests_interval (int): Interval between requests in seconds.
        num_responses (int): Number of responses to generate
        response_delimiter (str): Delimiter between responses. Used only if num_responses > 1
    """
    VERSION = '0.2.1'

    @dataclasses.dataclass
    class Inputs:
        prompts: typing.List[str]

    @dataclasses.dataclass
    class Config:
        endpoint: str
        deployment_name: str
        api_key: typing.Optional[str] = None
        temperature: float = 0.0
        top_p: float = 1.0
        max_tokens: int = 100
        requests_interval: int = 0
        num_responses: int = 1
        response_delimiter: str = '<|delimiter|>'

    @dataclasses.dataclass
    class Outputs:
        texts: typing.List[str]

    def execute(self, inputs):
        self._check_config()
        model = OpenAITextCompletionModel(self.config.endpoint, self.config.deployment_name, self.config.api_key, self.config.temperature, self.config.top_p,
                                          self.config.max_tokens, self.config.requests_interval, self.config.num_responses, self.config.response_delimiter)

        model_inputs = (inputs.prompts, [[]] * len(inputs.prompts))
        texts = model(model_inputs)

        logger.info(f"Generated {len(texts)} texts.")
        return self.Outputs(texts=texts)

    def dry_run(self, inputs):
        self._check_config()
        return self.Outputs(texts=['dry run'] * len(inputs.prompts))

    def _check_config(self):
        if not self.config.endpoint:
            raise ValueError("Endpoint is not set")

        if not urlparse(self.config.endpoint).scheme in ('http', 'https'):
            raise ValueError("Endpoint must start with http:// or https://")

        if not self.config.deployment_name:
            raise ValueError("Deployment name is not set")
