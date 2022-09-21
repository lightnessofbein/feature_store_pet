import feast
import pandas as pd
import yaml
from joblib import dump
from sklearn.linear_model import LogisticRegression

# Load driver order data
entity_df = pd.read_csv("data_engineering/raw_data/titanic_train.csv", usecols=["PassengerId"])
with open("data_engineering/raw_data/titanic_config.yaml") as f:
    config = yaml.load(f, Loader=yaml.loader.SafeLoader)
entity_df["dummy_timestamp"] = config["train"]["timestamp"]

# Connect to your feature store provider
fs = feast.FeatureStore(repo_path="data_science_repo/feast_feature_store")

# Retrieve training data from BigQuery
training_df = fs.get_historical_features(
    entity_df=entity_df,
    features=[
        "passengers_stats:Survived",
        "passengers_stats:Pclass",
        "passengers_stats:Name",
        "passengers_stats:Sex",
    ],
).to_df()

print("----- Feature schema -----\n")
print(training_df.info())

print()
print("----- Example features -----\n")
print(training_df.head())

print()
print("----- Missing in database -----")
print(training_df.isnull().any(axis=1).sum())
# Train model
target_col = "Survived"

reg = LogisticRegression()
train_X = training_df.drop(columns=entity_df.columns.to_list() + [target_col]).dropna()
print(f"train dataset size: {train_X.shape[0]}, request size: {entity_df.shape[0]}")
train_Y = training_df.dropna().loc[:, target_col]
reg.fit(train_X[sorted(train_X)], train_Y)

# Save model
dump(reg, "driver_model.dump")
