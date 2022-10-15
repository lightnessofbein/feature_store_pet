# This is an example feature definition file

from datetime import timedelta
from pyspark.sql import DataFrame

from feast import Entity, FeatureService, FeatureView, Field
from feast.types import Int64, Float32
from feast.stream_feature_view import stream_feature_view

from titanic_data_sources import titanic_file_source, titanic_stream_source


passenger_entity = Entity(name="passenger", join_keys=["PassengerId"])

passenger_stats = FeatureView(
    name="passenger_stats",
    entities=[passenger_entity],
    ttl=timedelta(days=1),
    schema=[
        Field(name="Survived", dtype=Int64),
        Field(name="Pclass", dtype=Int64),
        Field(name="Name", dtype=Int64),
        Field(name="Sex", dtype=Int64),
        Field(name="Age", dtype=Int64),
        Field(name="SibSp", dtype=Int64),
        Field(name="Parch", dtype=Int64),
        Field(name="Ticket", dtype=Int64),
        Field(name="Fare", dtype=Int64),
        Field(name="Cabin", dtype=Int64),
        Field(name="Embarked", dtype=Int64),
    ],
    online=True,
    source=titanic_file_source,
    tags={},
)
# TODO: delete feature service? It is used to combine features.
passenger_service = FeatureService(name="passenger_activity", features=[passenger_stats])


@stream_feature_view(
    entities=[passenger_entity],
    ttl=timedelta(seconds=8640000000),
    mode="spark",
    schema=[
        Field(name="Fare", dtype=Float32),
        Field(name="Pclass", dtype=Float32),
    ],
    timestamp_field="dummy_timestamp",
    online=True,
    source=titanic_stream_source,
    tags={},
)
def driver_hourly_stats_stream(df: DataFrame):
    return df
