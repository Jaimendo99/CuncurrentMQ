# CuncurrentMQ: send emails to all subscribed emails addreses by topic
## How to test
### Publisher
The Publisher is in the *main.py*, the file is a FastApi app with 3 endpoints.
#### 1. '/message/'
  post: publish a messange to the queue to a specific topic. BodySchema: {message:<message>, topic:<topic>
#### 2. '/topic/'
  get: get all default topics
  post: add a new topic

### Reciever
This function is in the reciever.py file. It accepts two Command line arguments. [1]: the email you want to recieve the messages and [2:]: the topic or topics you want to subscribe to
