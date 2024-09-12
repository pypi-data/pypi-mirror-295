from urllib.parse import urlparse

import requests
from loguru import logger
from opentelemetry import context, trace
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from wrapt import wrap_function_wrapper


class CustomRequestsInstrumentor(RequestsInstrumentor):
    def __init__(self, tracer=None):
        super().__init__()
        self._original_send = None
        self._propagator = TraceContextTextMapPropagator()
        self._tracer = tracer or trace.get_tracer(__name__)

    def _instrument(self, **kwargs):
        super()._instrument(**kwargs)

        def instrumented_send(wrapped, instance, args, kwargs):
            # Get the current context
            current_context = context.get_current()
            current_span = trace.get_current_span(current_context)

            logger.info(f"\n\n **  Checking current span {current_span}")

            # Extract request from args or kwargs
            request = args[0] if args else kwargs.get('request')

            if not request:
                return wrapped(*args, **kwargs)

            # Check if the URL should be ignored
            parsed_url = urlparse(request.url)
            if parsed_url.path.startswith('/v1/traces'):
                return wrapped(*args, **kwargs)

            tracer = trace.get_tracer(__name__)
            with self._tracer.start_as_current_span(
                f"HTTP {request.method}",
                context=current_context,
                kind=trace.SpanKind.CLIENT,
                attributes={
                    "http.method": request.method,
                    "http.url": request.url,
                },
            ) as span:
                # Inject the current context into the headers
                self._propagator.inject(request.headers, context=current_context)

                # Add custom trace IDs
                # span_context = span.get_span_context()
                # if span_context.is_valid:
                #     trace_id = format(span_context.trace_id, '032x')
                #     span_id = format(span_context.span_id, '016x')
                #     request.headers['X-acuvity-Trace-ID'] = trace_id
                #     request.headers['X-acuvity-Span-ID'] = span_id
                # Add custom trace IDs
                #if span.is_recording():
                span_context = span.get_span_context()
                trace_id = format(span_context.trace_id, '032x')
                span_id = format(span_context.span_id, '016x')
                request.headers['X-acuvity-Trace-ID'] = trace_id
                request.headers['X-acuvity-Span-ID'] = span_id


                logger.info(f"Outgoing request headers: {request.headers}")

                try:
                    response = wrapped(*args, **kwargs)
                    span.set_attribute("http.status_code", response.status_code)
                    return response
                except Exception as e:
                    span.record_exception(e)
                    raise

        wrap_function_wrapper('requests.sessions', 'Session.send', instrumented_send)

    def _uninstrument(self, **kwargs):
        pass  # The original _uninstrument method should handle this
