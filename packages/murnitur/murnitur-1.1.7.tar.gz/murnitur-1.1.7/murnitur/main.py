import os
import re
import json
import murnitur.lit as lit
from murnitur.lit.__helpers import handle_exception
from murnitur.instrumentation.astradb import AstraDBInstrumentor
from contextlib import contextmanager
from functools import wraps
from enum import Enum
from typing import (
    List,
    Dict,
    TypeVar,
    Literal,
    Optional,
    TypedDict,
    Callable,
    Type,
    cast,
)
from murnitur.lit.otel.tracing import trace as t
from murnitur.lit.otel.tracing import TracerProvider
from murnitur.lit.semcov import SemanticConvetion
from opentelemetry.trace import SpanKind, Status, StatusCode, Span
from opentelemetry.trace.propagation import set_span_in_context
from .tracer import setup_tracing
from .util import Util

T = TypeVar("T", bound=Type)


class GuardConfig(TypedDict):
    murnitur_key: str
    provider: Literal["openai", "groq", "anthropic", "custom"]
    model: str
    group: Optional[str]
    api_key: Optional[str]
    base_url: Optional[str]
    headers: Optional[dict]


class Config:
    environment: str
    app_name: str
    api_key: str = ""


allowed_types = ["bool", "str", "bytes", "int", "float"]

_all_instruments = [
    "openai",
    "anthropic",
    "cohere",
    "mistral",
    "bedrock",
    "vertexai",
    "groq",
    "ollama",
    "gpt4all",
    "langchain",
    "llama_index",
    "haystack",
    "embedchain",
    "chroma",
    "pinecone",
    "astradb",
    "qdrant",
    "milvus",
    "transformers",
]

InstrumentLiteral = Literal[
    "openai",
    "anthropic",
    "cohere",
    "mistral",
    "bedrock",
    "vertexai",
    "groq",
    "ollama",
    "gpt4all",
    "langchain",
    "llama_index",
    "haystack",
    "embedchain",
    "chroma",
    "pinecone",
    "astradb",
    "qdrant",
    "milvus",
    "transformers",
]


class Prompt:
    messages = []
    id: str = ""
    name: str = ""
    version: str = ""

    def __init__(self, id: str, name: str, version: str, messages: List) -> None:
        self.id = id
        self.name = name
        self.messages = messages
        self.version = version


class Preset:
    active_version: Prompt = None
    versions: List[Prompt] = []

    def __init__(self, preset):
        active = preset["PresetPrompts"][0]
        self.active_version = Prompt(
            id=active["id"],
            name=active["name"],
            version=active["version"],
            messages=active["prompts"],
        )
        self.versions = [
            Prompt(
                id=curr["id"],
                name=curr["name"],
                version=curr["version"],
                messages=curr["prompts"],
            )
            for curr in preset["PresetPrompts"]
        ]

    def get_prompt_by_version(self, version: int):
        """Get prompt by it's version"""
        for p in self.versions:
            if int(p.version) == int(version):
                return p

    def get_prompt_by_name(self, name: str):
        """Get prompt by it's name"""
        for p in self.versions:
            if p.name == name:
                return p

    def fine_tune(self, version: Optional[int] = None):
        """Fine tune the active version or version if provided"""
        prompt = (
            self.get_prompt_by_version(version=version)
            if version
            else self.active_version
        )
        if prompt:
            _, content = Util().finetune(
                prompts=prompt.messages,
                api_key=os.getenv("MURNITUR_API_KEY", Config.api_key),
            )
            if content:
                return content
            return []
        return []

    def fine_tune_with_dataset(self, dataset_id: str, version: Optional[int] = None):
        """Fine tune the active version or version if provided with a traced dataset as reference"""
        prompt = (
            self.get_prompt_by_version(version=version)
            if version
            else self.active_version
        )
        if prompt:
            _, content = Util().finetune_dataset(
                prompts=prompt.messages,
                dataset_id=dataset_id,
                api_key=os.getenv("MURNITUR_API_KEY", Config.api_key),
            )
            if content:
                return content
            return []
        return []


class Environment(Enum):
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    STAGING = "staging"


class TracedSpan:
    def __init__(self, span):
        self._span: Span = span

    def log(self, name: str, payload: Dict):
        if self._span.is_recording():
            __trace = t.get_tracer_provider()
            with __trace.get_tracer(__name__).start_span(
                name=name,
                kind=SpanKind.CLIENT,
            ) as child:
                child.set_attribute("type", "log")
                child.set_attribute("log-data", json.dumps(payload, indent=4))

    def __shield__(self, rules: list, rule: any, triggered: bool, response: str):
        if self._span.is_recording():
            __trace = t.get_tracer_provider()
            with __trace.get_tracer(__name__).start_span(
                name="Murnitur Shield",
                kind=SpanKind.CLIENT,
            ) as child:
                child.set_attribute("type", "shield")
                child.set_attribute("rules", json.dumps(rules, indent=2))
                child.set_attribute("rule", json.dumps(rule, indent=2))
                child.set_attribute("triggered", triggered)
                child.set_attribute("response", str(response))

    def set_result(self, result):
        self._span.set_attribute(SemanticConvetion.GEN_AI_CONTENT_COMPLETION, result)

    def set_metadata(self, metadata: Dict):
        self._span.set_attributes(attributes=metadata)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._span.end()


@contextmanager
def tracer(name: str):
    __trace = t.get_tracer_provider()
    with __trace.get_tracer(__name__).start_as_current_span(
        name,
        kind=SpanKind.CLIENT,
    ) as span:
        yield TracedSpan(span)


def trace(name: Optional[str] = None):
    """
    Generates a telemetry wrapper for messages to collect metrics.
    If called with a name, it will use that name for the span. If no name is provided,
    it will default to the wrapped function's name.
    """
    if callable(name):
        wrapped = name
        name = None
        return _trace_function(wrapped, name)
    else:

        def decorator(wrapped: Callable):
            return _trace_function(wrapped, name)

        return decorator


def task(name: Optional[str] = None):
    """
    Record a task specific to an agent
    Generates a telemetry wrapper for messages to collect metrics.
    If called with a name, it will use that name for the span. If no name is provided,
    it will default to the wrapped function's name.
    """
    if callable(name):
        wrapped = name
        name = None
        return _trace_function(wrapped, name, "task")
    else:

        def decorator(wrapped: Callable):
            return _trace_function(wrapped, name, "task")

        return decorator


def tool(name: Optional[str] = None):
    """
    Record a tool call specific to an agent
    Generates a telemetry wrapper for messages to collect metrics.
    If called with a name, it will use that name for the span. If no name is provided,
    it will default to the wrapped function's name.
    """
    if callable(name):
        wrapped = name
        name = None
        return _trace_function(wrapped, name, "tool")
    else:

        def decorator(wrapped: Callable):
            return _trace_function(wrapped, name, "tool")

        return decorator


def trace_agent(name: Optional[str] = None, auto_instrument: Optional[bool] = True):
    """
    Decorates a class to trace its methods and the class initialization.
    If `name` is a class, it applies the tracing directly. Otherwise, it returns
    a decorator that applies the tracing to a class.

    Args:
        name (Optional[str]): The name of the agent. If None, it uses the class name.
        auto_instrument (Optional[bool]): Whether to automatically instrument class methods.

    Returns:
        Callable[..., Type]: A decorator that applies tracing to a class.
    """
    if callable(name) and isinstance(name, type):
        cls = cast(Type[T], name)
        return _trace_agent_class(cls, None, auto_instrument)
    else:

        def decorator(cls: Type[T]) -> Type[T]:
            return _trace_agent_class(cls, name, auto_instrument)

        return decorator


def log(name: str, payload: Dict):
    __trace = t.get_tracer_provider()
    with __trace.get_tracer(__name__).start_span(
        name=name,
        kind=SpanKind.CLIENT,
    ) as child:
        child.set_attribute("type", "log")
        child.set_attribute("log-data", json.dumps(payload, indent=4))


def set_api_key(api_key: str):
    Config.api_key = api_key
    os.environ["MURNITUR_API_KEY"] = api_key


def get_api_key():
    return Config.api_key


def load_preset(name):
    _, content = Util().get_preset(
        name=name, api_key=os.getenv("MURNITUR_API_KEY", Config.api_key)
    )
    if content:
        return Preset(content)
    return None


def refine_prompt(prompts: list[dict]):
    """Refine your prompt to get the best outputs."""
    _, content = Util().finetune(
        prompts=prompts,
        api_key=os.getenv("MURNITUR_API_KEY", Config.api_key),
    )
    if content:
        return content
    return []


def format_prompt(messages: List, params: Dict):
    def replace_match(match):
        variable_name = match.group(1)
        return str(params.get(variable_name, f"{{{{{variable_name}}}}}"))

    replaced_templates = []
    for template in messages:
        new_template = {}
        for key, value in template.items():
            if isinstance(value, str):
                new_value = re.sub(r"\{\{([\w-]+)\}\}", replace_match, value)
                new_template[key] = new_value
            else:
                new_template[key] = value
        replaced_templates.append(new_template)

    return replaced_templates


def init(
    project_name: str,
    environment: Environment = Environment.DEVELOPMENT,
    enabled_instruments: List[InstrumentLiteral] = [],
):
    tracer_provider = t.get_tracer_provider()
    if isinstance(tracer_provider, TracerProvider):
        return
    if os.getenv("MURNITUR_API_KEY"):
        set_api_key(os.getenv("MURNITUR_API_KEY"))

    if not Config.api_key:
        raise ValueError("Please provide a valid API key!")

    Config.app_name = project_name
    Config.environment = environment.value

    __init(
        project_name=project_name,
        environment=environment,
        enabled_instruments=enabled_instruments,
    )


def __init(
    project_name: str,
    environment: Environment,
    enabled_instruments: List[InstrumentLiteral],
):
    try:
        if enabled_instruments:
            disabled_instruments = [
                instr
                for instr in _all_instruments
                if instr not in enabled_instruments and instr != "astradb"
            ]
        else:
            disabled_instruments = []
        # Setup tracer
        tracer = setup_tracing(
            application_name=project_name,
            environment=environment.value,
            otlp_headers=f"x-murnix-trace-token={Config.api_key}",
            disable_batch=False,
            tracer=None,
        )

        lit.init(
            environment=environment.value,
            application_name=project_name,
            disable_metrics=True,
            tracer=tracer,
            disable_batch=False,
            disabled_instrumentors=disabled_instruments,
            pricing_json="https://raw.githubusercontent.com/murnitur/llm-pricing/main/pricing.json",
        )

        if "astradb" in enabled_instruments or not enabled_instruments:
            # instrument astraDB
            AstraDBInstrumentor().instrument(
                environment=environment.value,
                application_name=project_name,
                tracer=tracer,
                pricing_info=None,
                trace_content=True,
                metrics_dict=None,
                disable_metrics=True,
            )
    except Exception as e:
        lit.logging.error("Error during Murnitur initialization: %s", e)


def _trace_function(wrapped: Callable, name: Optional[str], type: Optional[str] = None):
    """
    Traces the given function, adding telemetry and handling errors.
    """

    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        __trace = t.get_tracer_provider()
        if type:
            span_name = f"{name}.{wrapped.__name__}" if name else wrapped.__name__
        else:
            span_name = name or wrapped.__name__

        parent_span = getattr(args[0], "_root_span", None) if args else None
        tracer = __trace.get_tracer(__name__)
        context = set_span_in_context(parent_span) if parent_span else None

        with tracer.start_as_current_span(
            name=span_name, kind=SpanKind.CLIENT, context=context
        ) as span:
            try:
                response = wrapped(*args, **kwargs)
                span.set_attribute(
                    SemanticConvetion.GEN_AI_CONTENT_COMPLETION, response or ""
                )
                if type:
                    span.set_attribute("type", type)
                span.set_status(Status(StatusCode.OK))
            except Exception as e:
                response = None
                handle_exception(span, e)
                lit.logging.error(f"Error in {wrapped.__name__}: {e}", exc_info=True)

            # Adding function arguments as metadata
            try:
                span.set_attribute("function.args", str(args))
                span.set_attribute("function.kwargs", str(kwargs))
                span.set_attribute(
                    SemanticConvetion.GEN_AI_APPLICATION_NAME, Config.app_name
                )
                span.set_attribute(
                    SemanticConvetion.GEN_AI_ENVIRONMENT, Config.environment
                )
            except Exception as meta_exception:
                lit.logging.error(
                    f"Failed to set metadata for {wrapped.__name__}: {meta_exception}",
                    exc_info=True,
                )
                handle_exception(span, meta_exception)

            return response

    return wrapper


def _trace_agent_class(
    cls: Type[T], name: Optional[str], auto_instrument: Optional[bool]
) -> Type[T]:
    original_init = cls.__init__

    @wraps(original_init)
    def init_wrapper(self, *args, **kwargs):
        __trace = t.get_tracer_provider()
        span_name = f"{name}" if name else cls.__name__
        tracer = __trace.get_tracer(__name__)

        with tracer.start_as_current_span(name=span_name, kind=SpanKind.CLIENT) as span:
            self._root_span = span
            try:
                span.set_attribute("type", "agent")
                original_init(self, *args, **kwargs)
            except Exception as e:
                handle_exception(span, e)
                lit.logging.error(
                    f"Error in {original_init.__name__}: {e}", exc_info=True
                )
                raise e

    cls.__init__ = init_wrapper

    if auto_instrument:
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and attr_name not in ("__init__", "__new__"):
                # Ensure the method is not already decorated
                if not (
                    hasattr(attr_value, "_is_traced") or hasattr(attr_value, "_is_task")
                ):
                    setattr(cls, attr_name, task(name)(attr_value))

    return cls
