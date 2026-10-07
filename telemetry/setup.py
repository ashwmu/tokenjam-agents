from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def setup_tracer(service_name: str):
    """
    Initialize OTLP tracer for TokenJam ingestion.
    TokenJam reads from localhost:4317 by default.
    """
    provider = TracerProvider()
    exporter = OTLPSpanExporter(
        endpoint="http://localhost:4317",
        insecure=True
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)
