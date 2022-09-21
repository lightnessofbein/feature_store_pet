import feast
import pandas as pd
from datetime import datetime

entity_df = pd.read_parquet("feast_feature_store/data/titanic_train_file_source.parquet")

fs = feast.FeatureStore(repo_path="feast_feature_store/.")
entity_df["event_timestamp"] = datetime(2022, 1, 15, 2, 59, 43, 10)
training_df = fs.get_historical_features(
    entity_df=entity_df[["PassengerId", "event_timestamp"]],
    features=[
        "passenger_stats:Survived",
        "passenger_stats:Pclass",
        "passenger_stats:Fare",
    ],
).to_df()
