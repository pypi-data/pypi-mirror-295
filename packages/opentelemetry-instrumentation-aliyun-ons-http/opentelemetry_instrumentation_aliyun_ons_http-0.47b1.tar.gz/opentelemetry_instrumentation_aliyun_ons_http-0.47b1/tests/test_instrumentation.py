from unittest import TestCase
import unittest

from mq_http_sdk.mq_consumer import MQConsumer
from mq_http_sdk.mq_producer import MQProducer
from opentelemetry.instrumentation.aliyun_ons_http import AliyunOnsHttpInstrumentor
from wrapt import BoundFunctionWrapper


class TestAliyunOns(TestCase):
    def test_instrument_api(self) -> None:
        instrumentation = AliyunOnsHttpInstrumentor()

        instrumentation.instrument()
        self.assertTrue(isinstance(MQConsumer.consume_message, BoundFunctionWrapper))
        self.assertTrue(
            isinstance(MQConsumer.consume_message_orderly, BoundFunctionWrapper)
        )
        self.assertTrue(isinstance(MQProducer.publish_message, BoundFunctionWrapper))

        instrumentation.uninstrument()
        self.assertFalse(isinstance(MQConsumer.consume_message, BoundFunctionWrapper))
        self.assertFalse(
            isinstance(MQConsumer.consume_message_orderly, BoundFunctionWrapper)
        )
        self.assertFalse(isinstance(MQProducer.publish_message, BoundFunctionWrapper))

if __name__ == '__main__':
    unittest.main()