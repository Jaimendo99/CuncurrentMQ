from fastapi import FastAPI
from pydantic import BaseModel
import pika

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
except Exception:
    print("Error connecting to RabbitMQ")

topics = ['sports.football.laliga', 'sports.football.premierleague',
          'news.politics.ecuador', 'news.politics.argentina',
          'news.tech.openai', 'news.tech.webdev']

app = FastAPI()


class Message(BaseModel):
    message: str
    topic: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/message/")
async def create_message(message: Message):
    if message.topic not in topics:
        return {"message": "Topic not found"}

    channel.basic_publish(
        exchange='topic_logs', routing_key=message.topic, body=message.message)

    return message


@app.post("/topic/")
async def create_topic(topic: str):
    topics.append(topic)
    return {"message": "Topic created", 'topics': topics}


@app.get("/topic/")
async def get_topics():
    return {'topics': topics}

# Path: main.py
