# Assuming proto_class is the class generated by Protocol Buffers for your schema
#from your_proto_module import YourProtoClass  # Replace with the actual module and class name
from feast.protos.feast.core import FeatureView.proto
# Hardcoded proto value
hardcoded_proto_value = b'\x0a\x0a\x04\x01\x99\xda\x1b\ndriver_hourly_stats_fresh'

# Deserialize the proto value
deserialized_proto = FeatureView.FromString(hardcoded_proto_value)

# Now, you can use deserialized_proto as needed