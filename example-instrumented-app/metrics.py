import os
import random

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.view import View, ExplicitBucketHistogramAggregation
from opentelemetry.sdk.metrics.export import (
  ConsoleMetricExporter,
  PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# Service name is required for some backends, so
# so it is good to set service name anyways.
resource = Resource(attributes={
  SERVICE_NAME: "instrumented-app-example"
})

OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")

otlp_exporter = OTLPMetricExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT)

provider = MeterProvider(
  resource=resource,
  metric_readers=[
    PeriodicExportingMetricReader(ConsoleMetricExporter()),
    PeriodicExportingMetricReader(otlp_exporter)
  ],
  views=[
    View(
      instrument_name="*", 
      aggregation=ExplicitBucketHistogramAggregation((1,10,100,1000))
    ),
  ],
)

# Sets the global default meter provider
metrics.set_meter_provider(provider)

# Creates a meter from the global meter provider
meter = metrics.get_meter(__name__)

staging_labels = {"environment": "staging"}
counter = meter.create_counter(name="example_counter", unit="1", description="example counter")
histogram = meter.create_histogram(name="example_histogram", unit="1", description="example histogram")

def emit_metrics():
  counter.add(random.randint(1, 10), staging_labels)
  histogram.record(random.random() * 1500, staging_labels)