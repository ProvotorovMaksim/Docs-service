from confluent_kafka import Consumer
from logging import getLogger
from settings import settings
from document_generator import generate_docs

logger = getLogger("kafka_consumer")
logger.level("info")

consumer_config = {
    'bootstrap.servers': settings.KAFKA_BROKER_URL,
    "group.id":'test-consumer-group',
    "auto.offset.reset":'earliest'
}

def consumer_callback(*args):
    for arg in args:
        print(arg)

def start_consuming():
    with Consumer(consumer_config) as consumer:
        consumer.subscribe(
            topics=['multi-partition'],
        )
        try:
            while True:
                msg = consumer.poll(2.0)
                if msg == None:
                    continue
                if msg.error():
                    print(f"{msg.error()}")
                    continue
                key = msg.key().decode('utf-8') if msg.key() else None
                value = msg.value().decode('utf-8') if msg.value() else None
                generate_docs(value)
                print(f"Сообщение получено: {key}: {value}")
        except KeyboardInterrupt:
            print("Stopping")
        finally:
            consumer.close()
        consumer.close()
