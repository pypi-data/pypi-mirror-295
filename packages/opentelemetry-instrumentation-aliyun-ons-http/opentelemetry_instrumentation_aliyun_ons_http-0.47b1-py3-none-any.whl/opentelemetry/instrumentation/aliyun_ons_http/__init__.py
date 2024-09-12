from contextlib import contextmanager
from typing import Collection

from mq_http_sdk.mq_client import MQClient
from mq_http_sdk.mq_consumer import Message, MQConsumer
from mq_http_sdk.mq_exception import MQExceptionBase
from mq_http_sdk.mq_producer import MQProducer, TopicMessage
from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.propagate import extract, inject
from opentelemetry.propagators import textmap
from opentelemetry.semconv.trace import SpanAttributes
from wrapt import wrap_function_wrapper

from .package import _instruments
from .version import __version__

__all__ = ["AliyunOnsHttpInstrumentor", "process_record"]

MESSAGE_NOT_EXIST_CODE = "MessageNotExist"


class OnsContextSetter(textmap.Setter[TopicMessage]):
    def set(self, carrier: TopicMessage, key: str, value: str) -> None:
        if carrier is None or key is None:
            return

        if value:
            carrier.put_property(key, value)


class OnsContextGetter(textmap.Getter[Message]):
    def get(self, carrier: Message | None, key: str) -> list[str] | None:
        if carrier is None:
            return None

        if value := carrier.get_property(key):
            return [value]

        return None

    def keys(self, carrier: Message | None) -> list[str]:
        if carrier is None:
            return []
        return list(carrier.properties.keys())


_ons_setter = OnsContextSetter()
_ons_getter = OnsContextGetter()


class AliyunOnsHttpInstrumentor(BaseInstrumentor):
    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")

        tracer = trace.get_tracer(
            __name__,
            __version__,
            tracer_provider=tracer_provider,
            schema_url="https://opentelemetry.io/schemas/1.11.0",
        )

        wrap_function_wrapper(MQProducer, "publish_message", _wrap_send(tracer))
        wrap_function_wrapper(
            MQConsumer, "consume_message", _wrap_pull(tracer, "Receive Batch")
        )
        wrap_function_wrapper(
            MQConsumer, "consume_message_orderly", _wrap_pull(tracer, "Receive Orderly")
        )

    def _uninstrument(self, **kwargs):
        unwrap(MQProducer, "publish_message")
        unwrap(MQConsumer, "consume_message")
        unwrap(MQConsumer, "consume_message_orderly")


def _enrich_span_with_client(span: trace.Span, mq_client: MQClient):
    if span.is_recording():
        span.set_attribute(SpanAttributes.MESSAGING_SYSTEM, "aliyun_ons_rocketmq")
        span.set_attribute(SpanAttributes.SERVER_ADDRESS, mq_client.host)
        span.set_attribute(SpanAttributes.NETWORK_PROTOCOL_VERSION, mq_client.version)


def _wrap_send(tracer: trace.Tracer):
    def _traced_send(func, instance: MQProducer, args, kwargs):
        topic = instance.topic_name
        span_name = f"Send {topic}"
        with tracer.start_as_current_span(
            span_name, kind=trace.SpanKind.PRODUCER
        ) as span:
            carrier: TopicMessage = args[0]
            inject(carrier, setter=_ons_setter)
            instance_id = instance.instance_id
            span.set_attribute(SpanAttributes.MESSAGING_DESTINATION_NAME, topic)
            span.set_attribute("messaging.ons.instance.id", instance_id)
            _enrich_span_with_client(span, instance.mq_client)
            result: TopicMessage | None = func(*args, **kwargs)
            if result:
                span.set_attribute(
                    SpanAttributes.MESSAGING_MESSAGE_ID, result.message_id
                )
                span.set_attribute(
                    SpanAttributes.MESSAGING_ROCKETMQ_MESSAGE_TAG, result.message_tag
                )

        return result

    return _traced_send


def _wrap_pull(tracer: trace.Tracer, action_name: str):
    def _traced_pull(func, instance: MQConsumer, args, kwargs):
        topic = instance.topic_name
        span_name = f"{action_name} {topic}"
        with tracer.start_as_current_span(
            span_name, kind=trace.SpanKind.CONSUMER
        ) as span:
            _enrich_span_with_client(span, instance.mq_client)
            span.set_attribute(SpanAttributes.MESSAGING_CLIENT_ID, instance.consumer)
            try:
                records: list[Message] = func(*args, **kwargs)
            except MQExceptionBase as e:
                if e.type == MESSAGE_NOT_EXIST_CODE:
                    span.set_attribute(SpanAttributes.MESSAGING_BATCH_MESSAGE_COUNT, 0)
                    span.set_status(trace.StatusCode.OK)
                raise e

            span.set_attribute(
                SpanAttributes.MESSAGING_BATCH_MESSAGE_COUNT, len(records)
            )
            if records:
                span.set_attribute(
                    SpanAttributes.MESSAGING_ROCKETMQ_MESSAGE_KEYS,
                    [i.message_id for i in records],
                )

        return records

    return _traced_pull


_PROCESS_TRACER = trace.get_tracer(f"{__name__}.process_record", __version__)


@contextmanager
def process_record(record: Message, tracer: trace.Tracer | None = None):
    tracer = tracer or _PROCESS_TRACER
    with tracer.start_as_current_span(
        "Process Message",
        kind=trace.SpanKind.CONSUMER,
        context=extract(carrier=record, getter=_ons_getter),
    ) as span:
        span.set_attribute(
            SpanAttributes.MESSAGING_ROCKETMQ_MESSAGE_KEYS, record.message_id
        )
        span.set_attribute(
            SpanAttributes.MESSAGING_ROCKETMQ_MESSAGE_TAG, record.message_tag
        )
        yield span
