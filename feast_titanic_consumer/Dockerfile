FROM python:3.8-slim

# Copy app handler code
COPY . .

# Install dependencies
RUN pip3 install kafka-python==2.0.2
RUN pip3 install requests

CMD [ "python", "titanic_spark_consumer.py"]
