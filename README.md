# clickstream-data-pipeline

## 🚀 Real-Time Clickstream Data Pipeline Using Apache Kafka, Apache Spark, and MySQL

## 📊 Architecture
Kafka Producer → Kafka Topic → Spark Streaming → MySQL

## 🧪 Technologies
- Python (Kafka producer, Spark job)
- Apache Kafka
- Apache Spark (Structured Streaming)
- MySQL
- Linux (Ubuntu)

## 🗂️ Files
- `clickstream_producer.py` — sends events to Kafka
- `spark_streaming_job.py` — reads from Kafka, aggregates, writes to MySQL
- `start_spark_job.sh` — optional launch script
- `Clickstream_Project_Report.pdf` — project documentation

## 🛠️ Steps
#### Step 1: Start Required Services
Start Zookeeper, Kafka, and MySQL in separate terminal tabs.
```
# Start Zookeeper
cd ~/kafka
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka
cd ~/kafka
bin/kafka-server-start.sh config/server.properties

# Start MySQL
sudo service mysql start
```
#### Step 2: Activate Python Virtual Environment
```
cd ~/clickstream_project
source venv/bin/activate
```
#### Step 3: Start the Kafka Producer
This will continuously send simulated user click events.
```
python3 clickstream_producer.py
```
#### Step 4: Run the Spark Streaming Job
This job reads from Kafka, performs windowed aggregations, and writes to MySQL.
```
./start_spark_job.sh
```
Keep this terminal running — it continuously processes incoming Kafka data.
#### Step 5: Check MySQL for Aggregated Output
Open MySQL and view the real-time results:
```
mysql -u clickstream -p

USE clickstream;

SELECT * FROM click_aggregates ORDER BY window_start DESC;
```




## 🔧 Kafka Producer Output
![image](https://github.com/user-attachments/assets/9f8c7159-ee5f-4ddb-a330-ca7a9e0b96fd)


## ⚡ Spark Streaming Output
![image](https://github.com/user-attachments/assets/7eeff6f6-86af-4ce1-9d0c-b6017ff9beaa)


## 💾 MySQL Table Output
![image](https://github.com/user-attachments/assets/b59bd1ca-bc56-49b6-a39e-fb743e740404)

