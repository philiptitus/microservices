import pika, json, os

from main import app, Product, db

params = pika.URLParameters(os.environ.get('pika_url'))

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    with app.app_context():
        data = json.loads(body)
        print(data)

        method_type = properties.content_type if properties.content_type else 'product_created'

        if method_type == 'product_created':
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print('Product Received Created')

        elif method_type == 'product_updated':
            product = Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            print('Product Updated')

        elif method_type == 'product_deleted':
            product = Product.query.get(data)
            db.session.delete(product)
            db.session.commit()
            print('Product Deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
