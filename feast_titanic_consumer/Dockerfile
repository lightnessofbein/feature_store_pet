FROM python:3.8-slim

# Copy app handler code
COPY titanic_spark_consumer.py titanic_spark_consumer.py

# Install dependencies
RUN pip3 install kafka-python==2.0.2

CMD [ "python", "titanic_spark_consumer.py"]
