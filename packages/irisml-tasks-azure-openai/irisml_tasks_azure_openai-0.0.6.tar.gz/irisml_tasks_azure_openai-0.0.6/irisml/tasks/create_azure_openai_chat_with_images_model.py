import base64
import dataclasses
import io
import logging
import time
from typing import List, Optional, Tuple
from urllib.parse import urlparse
import torch.utils.data
import torchvision.transforms
import irisml.core
from irisml.tasks.create_azure_openai_chat_model import OpenAIChatClient

IMAGE_PLACEHOLDER = '<|image|>'
logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create a model that generates text using Azure OpenAI chat API with images.

    This task calls the Azure OpenAI GPT-V chat API.

    Currently this implementation supports a single system message and a single user message.

    The model input is (prompts_batch, images_batch) where:
    - prompts_batch is a list of prompts, each prompt is a string with one or more IMAGE_PLACEHOLDER
    - images_batch is one of the following:
        - A list of lists of images, where each image is a tensor of shape (3, H, W).
        - A list of images, where each image is a tensor of shape (3, H, W).
        - A tensor of shape (N, 3, H, W) where N is the number of prompts and H, W are the image dimensions.

    The model output is a list of generated texts, one for each prompt.

    Config:
        endpoint (str): Azure endpoint
        deployment_name (str): Azure deployment name
        api_key (str): Azure API key
        temperature (float): Temperature parameter for text generation
        max_tokens (int): Maximum number of tokens to generate
        requests_interval (int): Interval between requests in seconds
        system_message (str): System message to be sent to the model
        num_responses (int): Number of responses to generate
        response_delimiter (str): Delimiter to join multiple responses
    """
    VERSION = '0.1.2'

    @dataclasses.dataclass
    class Config:
        endpoint: str
        deployment_name: str
        api_key: Optional[str] = None
        temperature: float = 0.0
        max_tokens: int = 100
        requests_interval: int = 0
        system_message: str = ''
        num_responses: int = 1
        response_delimiter: str = '<|delimiter|>'
        json_schema: Optional[dict] = None

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module

    def execute(self, inputs):
        self._check_configs()
        client = OpenAIChatWithImagesClient(self.config.endpoint, self.config.deployment_name, self.config.api_key, self.config.temperature,
                                            self.config.max_tokens, self.config.num_responses, self.config.response_delimiter, self.config.system_message, self.config.json_schema)
        model = OpenAITextGenerationWithImagesModel(client, self.config.requests_interval)
        return self.Outputs(model)

    def dry_run(self, inputs):
        self._check_configs()
        return self.Outputs(FakeModel())

    def _check_configs(self):
        if not self.config.endpoint:
            raise ValueError("Endpoint is not set")

        if not urlparse(self.config.endpoint).scheme in ('http', 'https'):
            raise ValueError("Endpoint must start with http:// or https://")

        if not self.config.deployment_name:
            raise ValueError("Deployment name is not set")


class OpenAIChatWithImagesClient(OpenAIChatClient):
    def get_url(self):
        return '/chat/completions?api-version=2023-12-01-preview'

    def make_request_body(self, inputs: Tuple[str, List[bytes]]):
        assert isinstance(inputs, tuple) and len(inputs) == 2 and isinstance(inputs[0], str) and isinstance(inputs[1], list)
        prompt, prompt_images = inputs
        prompt_parts = prompt.split(IMAGE_PLACEHOLDER)
        assert len(prompt_parts) == len(prompt_images) + 1

        content = []
        for text, image_bytes in zip(prompt_parts, prompt_images):
            for t in text.splitlines():
                content.append({'type': 'text', 'text': t.strip()})
            content.append({'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + base64.b64encode(image_bytes).decode('ascii')}})

        if prompt_after_last_image := prompt_parts[-1].strip():
            content.append({'type': 'text', 'text': prompt_after_last_image})

        messages = []
        if self._system_message:
            messages.append({'role': 'system', 'content': self._system_message})
        messages.append({'role': 'user', 'content': content})
        return {'messages': messages}


class OpenAITextGenerationWithImagesModel(torch.nn.Module):
    def __init__(self, client, requests_interval):
        super().__init__()
        self._client = client
        self._requests_interval = requests_interval
        self._last_request_timestamp = None

    def forward(self, inputs):
        if isinstance(inputs[1], torch.Tensor):
            assert len(inputs[1].shape) == 4
            images_batch = [[image] for image in inputs[1]]
        else:
            assert isinstance(inputs[1], list)
            if isinstance(inputs[1][0], torch.Tensor) and len(inputs[1][0].shape) == 3:
                images_batch = [[image] for image in inputs[1]]
            else:
                images_batch = inputs[1]

        texts = []
        for prompt, prompt_images in zip(inputs[0], images_batch):
            if prompt.count(IMAGE_PLACEHOLDER) != len(prompt_images):
                raise ValueError(f"Number of images ({len(prompt_images)}) does not match the number of placeholders ({prompt.count(IMAGE_PLACEHOLDER)})")

            image_bytes = [self._tensor_to_image_bytes(image) for image in prompt_images]
            if self._last_request_timestamp:
                time.sleep(max(0, self._requests_interval - (time.time() - self._last_request_timestamp)))

            try:
                result, _ = self._client.post((prompt, image_bytes))
                self._last_request_timestamp = time.time()
            except Exception:
                logger.exception(f"Failed to generate text for prompt: {prompt}")
                result = ''
            texts.append(result)
            logger.info(f"Generated text: {repr(result)}")
        return texts

    @staticmethod
    def _tensor_to_image_bytes(image: torch.Tensor) -> bytes:
        pil_image = torchvision.transforms.ToPILImage()(image)
        bytes_io = io.BytesIO()
        pil_image.save(bytes_io, format='PNG')
        return bytes_io.getvalue()

    def __getstate__(self):
        return {'client': self._client, 'requests_interval': self._requests_interval}

    def __setstate__(self, state):
        super().__init__()
        self._client = state['client']
        self._requests_interval = state['requests_interval']
        self._last_request_timestamp = None


class FakeModel(torch.nn.Module):
    def forward(self, inputs):
        return [''] * len(inputs)
