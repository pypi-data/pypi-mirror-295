OpenTelemetry Aliyun Ons Http SDK Instrumentation
===================================================

This library provides automatic and manual instrumentation of Aliyun Ons **mq_http_sdk**

auto-instrumentation using the opentelemetry-instrumentation package is also supported.


Installation
------------

.. code-block:: shell

    pip install opentelemetry-instrumentation-aliyun-ons-http

Usage
------

.. code-block:: python

    from opentelemetry.instrumentation.aliyun_ons_http import AliyunOnsHttpInstrumentor

    AliyunOnsHttpInstrumentor.instrument()


Note:

    Consumers are in batches, so it is not possible to automatically add trace information to each message.
    
    When process messages, manually call it.

.. code-block:: python

    from opentelemetry.instrumentation.aliyun_ons_http import process_record
    ...
    messages = consumer.consume_message():
    for message in messages:
        with process_record(message):
            # do your business



References
----------

* `OpenTelemetry Project <https://opentelemetry.io/>`_
* `OpenTelemetry Python Examples <https://github.com/open-telemetry/opentelemetry-python/tree/main/docs/examples>`_