import pika, json, os

params = pika.URLParameters(os.environ.get('pika_url'))

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(content_type=method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)

