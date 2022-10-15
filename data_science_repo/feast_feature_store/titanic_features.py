# This is an example feature definition file

from datetime import timedelta

from feast import Entity, FeatureService, FeatureView, Field
from feast.types import Int32

from titanic_data_sources import driver_stats_push_source


passenger_entity = Entity(name="passenger", join_keys=["PassengerId"])

passenger_stats = FeatureView(
    name="passenger_stats",
    entities=[passenger_entity],
    ttl=timedelta(days=1),
    schema=[
        Field(name="Survived", dtype=Int32),
        Field(name="Pclass", dtype=Int32),
        Field(name="Name", dtype=Int32),
        Field(name="Sex", dtype=Int32),
        Field(name="Age", dtype=Int32),
        Field(name="SibSp", dtype=Int32),
        Field(name="Parch", dtype=Int32),
        Field(name="Ticket", dtype=Int32),
        Field(name="Fare", dtype=Int32),
    ],
    online=True,
    source=driver_stats_push_source,
    tags={},
)
# TODO: delete feature service? It is used to combine features.
passenger_service = FeatureService(name="passenger_activity", features=[passenger_stats])
