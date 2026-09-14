# Adding Redis, Kafka, vector search or file storage

Declaring it in `substrait.yaml` is the **only** trigger. Installing a client library does
nothing — the service won't exist and the app will crash at runtime with no build warning.

```yaml
services:
  - object-storage   # durable private bucket -> OBJECT_STORAGE_BUCKET
  - redis            # -> REDIS_URL
  - kafka            # -> KAFKA_BROKERS
  - qdrant           # -> QDRANT_URL
```

**For file uploads use `object-storage`.** Files written to the container filesystem are
lost on every restart and redeploy.
