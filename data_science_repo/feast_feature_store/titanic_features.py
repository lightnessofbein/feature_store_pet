# This is an example feature definition file

from datetime import timedelta

from feast import Entity, FeatureService, FeatureView, Field
from feast.types import Int64

from titanic_data_sources import titanic_file_source


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
