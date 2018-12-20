## 1. Create the docker-compose file under the ~/w205/flask-with-kafka-and-spark/
##      and cd ~/w205/flask-with-kafka-and-spark/, copy the docker-compose file

## 2. Spin up the docker container

       docker-compose up -d

## 3. Create the event using kafka

     docker-compose exec kafka kafka-topics --create --topic events --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181

## 4. Create the .py file with flask library, save under ~/w205/flask-with-kafka/

## 5. Run flask

     docker-compose exec mids env FLASK_APP=/w205/flask-with-kafka-and-spark/game_api_with_extended_json_events.py flask run --host 0.0.0.0

## 6. Open another SSH session to make the call to the API

     docker-compose exec mids curl http://localhost:5000/purchase_a_sword

#### this calls the api and register the api hits, and return the string "sword purchased"

#### docker-compose exec mids curl http://localhost:5000/purchase_a_frog
#### this calls the api and register the api hits, and retrun the string "frog purchased"

## 7. Read the data from kafka
#### docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning -e
#### Geting the event in Kafka, each event is the json dictionary, which has the event type.  The request line in python file returns the additional fileds such as User-Agent is the kind of device to use for connect to web service, which is the cul command.
```
{"Host": "localhost:5000", "event_type": "default", "Accept": "*/*", "User-Agent": "curl/7.47.0"}
{"Host": "localhost:5000", "event_type": "default", "Accept": "*/*", "User-Agent": "curl/7.47.0"}
{"Host": "localhost:5000", "event_type": "default", "Accept": "*/*", "User-Agent": "curl/7.47.0"}
{"Host": "localhost:5000", "event_type": "purchase_sword", "Accept": "*/*", "User-Agent": "curl/7.47.0"}
{"Host": "localhost:5000", "event_type": "purchase_sword", "Accept": "*/*", "User-Agent": "curl/7.47.0"}
{"Host": "localhost:5000", "event_type": "purchase_sword", "Accept": "*/*", "User-Agent": "curl/7.47.0"}
{"Host": "localhost:5000", "event_type": "purchase_sword", "Accept": "*/*", "User-Agent": "curl/7.47.0"}
```
## 8. Read the event from kafka using Spark

     docker-compose exec spark pyspark

     raw_events = spark.read.format("kafka").option("kafka.bootstrap.servers",   "kafka:29092").option("subscribe","events").option("startingOffsets","earliest").option("endingOffsets", "latest").load()
     events = raw_events.select(raw_events.value.cast('string'))
     extracted_events = events.rdd.map(lambda x: json.loads(x.value)).toDF()
     extracted_events.show()

## 9. Exit spark, spin down the container

    docker-compose down
