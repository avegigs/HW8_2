import json
import re
from mongoengine import connect
from models import Author, Quote

# Підключення до бази даних MongoDB Atlas
mongo_uri = "mongodb+srv://<username>:<password>@krabaton.5mlpr.gcp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
connect(host=mongo_uri)

# Завантаження даних з JSON файлів у базу даних
def load_data():
    with open('authors.json', 'r', encoding='utf-8') as authors_file:
        authors_data = json.load(authors_file)
        for author_data in authors_data:
            author = Author(**author_data)
            author.save()

    with open('quotes.json', 'r', encoding='utf-8') as quotes_file:
        quotes_data = json.load(quotes_file)
        for quote_data in quotes_data:
            author_name = quote_data['author']
            author = Author.objects(fullname=author_name).first()
            if author:
                quote_data['author'] = author
                quote = Quote(**quote_data)
                quote.save()

def search_quotes():
    while True:
        command = input("Введіть команду (name: автор, tag: тег, tags: теги, exit: завершити): ").strip()
        if re.match(r'^name:[\s\S]*$', command):
            author_name = command.split('name:')[1].strip()
            author = Author.objects(fullname=author_name).first()
            if author:
                quotes = Quote.objects(author=author)
                for quote in quotes:
                    print(quote.quote)
        elif re.match(r'^tag:[\s\S]*$', command):
            tag = command.split('tag:')[1].strip()
            quotes = Quote.objects(tags=tag)
            for quote in quotes:
                print(quote.quote)
        elif re.match(r'^tags:[\s\S]*$', command):
            tag_list = command.split('tags:')[1].strip().split(',')
            quotes = Quote.objects(tags__in=tag_list)
            for quote in quotes:
                print(quote.quote)
        elif command == 'exit':
            break


if __name__ == "__main__":
    load_data()  
    search_quotes() 
