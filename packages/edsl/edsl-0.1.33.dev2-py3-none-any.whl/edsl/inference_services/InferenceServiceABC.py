from abc import abstractmethod, ABC
from typing import Any
import re
from edsl.config import CONFIG


class InferenceServiceABC(ABC):
    """Abstract class for inference services."""

    # check if child class has cls attribute "key_sequence"
    def __init_subclass__(cls):
        if not hasattr(cls, "key_sequence"):
            raise NotImplementedError(
                f"Class {cls.__name__} must have a 'key_sequence' attribute."
            )
        if not hasattr(cls, "model_exclude_list"):
            raise NotImplementedError(
                f"Class {cls.__name__} must have a 'model_exclude_list' attribute."
            )

    def get_tpm(cls):
        key = f"EDSL_SERVICE_TPM_{cls._inference_service_.upper()}"
        if key not in CONFIG:
            key = "EDSL_SERVICE_TPM_BASELINE"
        return int(CONFIG.get(key))

    def get_rpm(cls):
        key = f"EDSL_SERVICE_RPM_{cls._inference_service_.upper()}"
        if key not in CONFIG:
            key = "EDSL_SERVICE_RPM_BASELINE"
        return int(CONFIG.get(key))

    @abstractmethod
    def available() -> list[str]:
        pass

    @abstractmethod
    def create_model():
        pass

    @staticmethod
    def to_class_name(s):
        """Convert a string to a valid class name.

        >>> InferenceServiceABC.to_class_name("hello world")
        'HelloWorld'
        """

        s = re.sub(r"[^a-zA-Z0-9 ]", "", s)
        s = "".join(word.title() for word in s.split())
        if s and s[0].isdigit():
            s = "Class" + s
        return s


if __name__ == "__main__":
    pass
    # deep_infra_service = DeepInfraService("deep_infra", "DEEP_INFRA_API_KEY")
    # deep_infra_service.available()
    # m = deep_infra_service.create_model("microsoft/WizardLM-2-7B")
    # response = m().hello()
    # print(response)

    # anthropic_service = AnthropicService("anthropic", "ANTHROPIC_API_KEY")
    # anthropic_service.available()
    # m = anthropic_service.create_model("claude-3-opus-20240229")
    # response = m().hello()
    # print(response)
    # factory = OpenAIService("openai", "OPENAI_API")
    # factory.available()
    # m = factory.create_model("gpt-3.5-turbo")
    # response = m().hello()

    # from edsl import QuestionFreeText
    # results = QuestionFreeText.example().by(m()).run()

    # collection = InferenceServicesCollection([
    #     OpenAIService,
    #     AnthropicService,
    #     DeepInfraService
    # ])

    # available = collection.available()
    # factory = collection.create_model_factory(*available[0])
    # m = factory()
    # from edsl import QuestionFreeText
    # results = QuestionFreeText.example().by(m).run()
    # print(results)
