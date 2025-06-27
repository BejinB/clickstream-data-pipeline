from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, from_unixtime
from pyspark.sql.types import StructType, StringType, LongType

# Define schema for clickstream events
schema = StructType() \
    .add("user", StringType()) \
    .add("page", StringType()) \
    .add("timestamp", LongType())

# Create Spark session
spark = SparkSession.builder \
    .appName("ClickstreamProcessing") \
    .getOrCreate()

# Read streaming data from Kafka
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "clickstream") \
    .option("startingOffsets", "latest") \
    .load()




# Parse JSON data
json_df = raw_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Convert epoch to timestamp
clicks_df = json_df.withColumn("event_time", from_unixtime(col("timestamp")).cast("timestamp"))

# Aggregate clicks per page in 10-second windows
# Add watermark to event_time (say, 1 minute late allowed)
agg_df = clicks_df \
    .withWatermark("event_time", "1 minute") \
    .groupBy(
        window(col("event_time"), "10 seconds"),
        col("page")
    ).count()


# Function to write each micro-batch to MySQL
# Function to write each micro-batch to MySQL
def write_to_mysql(batch_df, batch_id):
    batch_df.select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("page"),
        col("count").alias("click_count")
    ).write.format("jdbc") \
        .option("url", "jdbc:mysql://localhost:3306/clickstream") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "click_aggregates") \
        .option("user", "clickstream") \
        .option("password", "Click@1234") \
        .mode("append") \
        .save()



# Start streaming query
query = agg_df.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_mysql) \
    .start()


query.awaitTermination()





