from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor


class CustomJaegerExporter:
    def __init__(self):
        # create a JaegerExporter
        self.jaeger_exporter = JaegerExporter(
            # configure agent
            agent_host_name='localhost',
            agent_port=6831,
            # optional: configure also collector
            # collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
            # username=xxxx, # optional
            # password=xxxx, # optional
            # max_tag_value_length=None # optional
            udp_split_oversized_batches=True
        )
        #self.exporter = OTLPSpanExporter(endpoint=otlp_endpoint)

    def get_processor(self, max_export_batch_size=256, export_timeout_millis=30000, max_queue_size=2048):
        # Create a BatchSpanProcessor and add the exporter to it
        #span_processor = BatchSpanProcessor(self.jaeger_exporter)
        return BatchSpanProcessor(
            self.jaeger_exporter,
            max_export_batch_size=max_export_batch_size,
            export_timeout_millis=export_timeout_millis,
            max_queue_size=max_queue_size
        )
