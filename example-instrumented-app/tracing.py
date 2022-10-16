import os
import random
import time

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import (
  BatchSpanProcessor,
  ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Service name is required for some backends, so
# so it is good to set service name anyways.
resource = Resource(attributes={
  SERVICE_NAME: "instrumented-app-example"
})

OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")

provider = TracerProvider(resource=resource)
# console_processor = BatchSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(console_processor)
otlp_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT))
provider.add_span_processor(otlp_processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)

def emit_trace():
  with tracer.start_as_current_span("foo"):
    print("Doing some work")
    time.sleep(random.random() * 2)
    with tracer.start_as_current_span("bar"):
      print("Doing some work")
      time.sleep(random.random() * 2)
      with tracer.start_as_current_span("baz"):
        print("Doing some work")
        time.sleep(random.random() * 2)
        print("Done with work")

# @tracer.start_as_current_span("do_work")
# def do_work():
#   print("doing some work...")