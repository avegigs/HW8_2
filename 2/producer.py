import pika
import json
from faker import Faker
from mongoengine import connect
from models import Contact  

# Підключення до RabbitMQ сервера
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='email_queue')

# Підключення до MongoDB
connect('mydatabase')

fake = Faker()

# Генерування та збереження фейкових контактів у базу даних та відправка їх до черги
for _ in range(10):  
    contact_data = {
        'full_name': fake.name(),
        'email': fake.email(),
        'sent_email': False 
    }
    contact = Contact(**contact_data)
    contact.save()

    # Надсилаємо ObjectID створеного контакту до черги
    message = {
        'contact_id': str(contact.id)
    }
    channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))

print("Сгенеровано та відправлено контакти до черги")

connection.close()
