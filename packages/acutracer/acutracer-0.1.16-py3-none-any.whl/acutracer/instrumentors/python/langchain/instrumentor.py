import logging
from importlib.metadata import PackageNotFoundError
from importlib.util import find_spec
from typing import Any

from loguru import logger
from openinference.semconv.resource import ResourceAttributes
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from exporters.jaeger_exporter import JaegerExporter
from instrumentors.python.langchain import (
    LangChainInstrumentor as Instrumentor,
)


class LangChainInstrumentor(Instrumentor):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if find_spec("langchain_core") is None:
            raise PackageNotFoundError(
                "Missing `langchain-core`. Install with `pip install langchain-core`."
            )
        super().__init__()

    def instrument(self) -> None:
        tracer_provider = trace_sdk.TracerProvider(
            resource=Resource({ResourceAttributes.PROJECT_NAME: "acutracer"}),
            span_limits=trace_sdk.SpanLimits(max_attributes=10_000),
        )
        tracer_provider.add_span_processor(SimpleSpanProcessor(JaegerExporter()))
        super().instrument(skip_dep_check=True, tracer_provider=tracer_provider)
