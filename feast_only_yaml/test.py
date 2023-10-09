from pprint import pprint
from feast import FeatureStore

store = FeatureStore(repo_path=".")
print(store)
feature_view = store.get_feature_view("driver_hourly_stats")
print('222')
feature_vector = store.get_online_features(
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
    ],
    entity_rows=[
        # {join_key: entity_value}
        {"driver_id": 1004},
        {"driver_id": 1005},
    ],
).to_dict()

pprint(feature_vector)