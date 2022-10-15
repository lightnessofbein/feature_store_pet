from feast import FileSource, PushSource


titanic_file_source = FileSource(path="data/titanic_train_file_source.parquet", timestamp_field="dummy_timestamp")

driver_stats_push_source = PushSource(name="titanic_passenger_push_source", batch_source=titanic_file_source)
