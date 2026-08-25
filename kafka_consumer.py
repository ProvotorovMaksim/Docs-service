from confluent_kafka import Consumer
from logging import getLogger
from settings import settings
from document_generator import generate_docs
from kafka_producer import produce_message

logger = getLogger("kafka_consumer")
logger.setLevel("Info")

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
                responce = generate_docs(value)
                produce_message(responce)
                logger.info(f"Сообщение получено: {key}: {value}")
        except KeyboardInterrupt:
            print("Stopping")
        finally:
            consumer.close()
        consumer.close()
