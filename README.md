# Real Time ML Pipeline

This example illustrates a working example for a Real Time ML predictions. The example uses a [Uber trips dataset](https://www.kaggle.com/datasets/yasserh/uber-fares-dataset) retrieved from Kaggle. 

Following are the features of the example,
- Trip Events are produced to Kafka
- Events are processed by a Flink processor into model features
- Feast is used as the feature store to manange features for the ML model
- Processed features are ingested into Feast using a Pyspark processor
- Feast server exposes HTTP endpoint to retrive features
- ML model is served with a Flask API for predictions

**Note**: This demo will not cover the training and tuning of ML model. 

## Prerequisites
- Docker
- Python

## Demo

### Start the demo

```bash
./start.sh
```

**Note**: Replace `docker-compose` with `docker compose` for newer versions.

### Get the predictions

Wait for 2-3 minutes for the features to be loaded

```bash
docker exec -it feastserver bash -c "python get_predictions.py -e 104,105"
```

### Clean up

```bash
./stop.sh
```