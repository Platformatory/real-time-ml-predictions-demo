#!/bin/bash

echo "Remove any previous instances"
./stop.sh
echo ""

echo "Deploy Kafka Cluster"
docker-compose up -d zookeeper kafka
echo ""

echo "Wait for Kafka to be in a running state"
sleep 60
while true; do
    if nc -z -w 1 localhost 9092; then
        echo "Kafka is up and running"
        break
    else
        echo "Kafka is not yet Up. Retrying in 10 seconds..."
        sleep 10
    fi
done
echo ""

echo "Create topics and generate input data"
docker-compose up -d kafka_events
echo ""

echo "Deploy Flink Cluster"
docker-compose up -d jobmanager taskmanager
sleep 10
while true; do
    if nc -z -w 1 localhost 8081; then
        echo "Flink Cluster is up and running"
        break
    else
        echo "Flink Cluster is not yet Up. Retrying in 10 seconds..."
        sleep 10
    fi
done
echo ""

echo "Create Flink Stream Processing Job"
docker-compose up -d jobrunner
echo ""

echo "Deploy Redis and Postgres for online Store and Feature registry"
docker-compose up -d postgres redis
echo ""

echo "Deploy Feast server"
docker-compose up -d feastserver
echo ""

sleep 10

echo "Ingest features from Kafka into Feast"
docker-compose up -d feastingest

echo "Deploy Model Serving Layer"
docker-compose up -d modelapi