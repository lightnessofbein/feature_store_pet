# This is an example feature definition file

from datetime import timedelta

from feast import Entity, FeatureService, FeatureView, Field, FileSource
from feast.types import Int64

# Read data from parquet files. Parquet is convenient for local development mode. For
# production, you can use your favorite DWH, such as BigQuery. See Feast documentation
# for more info.
titanic_file_source = FileSource(
    path="data/titanic_train_file_source.parquet",
    timestamp_field="dummy_timestamp",
)

# Define an entity for the driver. You can think of entity as a primary key used to
# fetch features.
driver = Entity(name="passenger", join_keys=["PassengerId"])

# Our parquet files contain sample data that includes a driver_id column, timestamps and
# three feature column. Here we define a Feature View that will allow us to serve this
# data to our model online.
passenger_stats = FeatureView(
    name="passenger_stats",
    entities=[driver],
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

driver_stats_fs = FeatureService(name="passenger_activity", features=[passenger_stats])
