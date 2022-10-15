FROM python:3.8-slim

# Copy app handler code
COPY kafka_main.py kafka_main.py
COPY titanic_train_file_source.parquet titanic_train_file_source.parquet

# Install dependencies
RUN pip3 install kafka-python==2.0.2
RUN pip3 install pandas
RUN pip3 install pyarrow

CMD [ "python", "-u", "kafka_main.py", "--mode", "setup"]