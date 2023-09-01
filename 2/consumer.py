import pika
import json
from models import Contact  

# Функція-заглушка для імітації надсилання email
def send_email(contact_id):
    print(f"Відправлено email до контакту з ID: {contact_id}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message.get('contact_id')
    
    if contact_id:
        contact = Contact.objects(id=contact_id).first()
        
        if contact and not contact.sent_email:
            send_email(contact_id)
            contact.sent_email = True
            contact.save()
            print(f"Позначено контакт {contact_id} як надісланий")

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Чекаю на повідомлення. Для виходу натисніть Ctrl+C')
channel.start_consuming()
