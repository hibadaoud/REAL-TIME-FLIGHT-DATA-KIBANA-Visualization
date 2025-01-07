# IMPORT LIBRARIES
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql.types import StructType, StructField, DoubleType, IntegerType, StringType
from pyspark.sql.functions import from_json , col , when , length, struct
from pyspark.sql.functions import udf


# Define the data schema
schema = StructType([
    StructField("hex", StringType(), True),
    StructField("reg_number", StringType(), True),
    StructField("flag", StringType(), True),
    StructField("lat", DoubleType(), True),
    StructField("lng", DoubleType(), True),
    StructField("alt", DoubleType(), True),
    StructField("dir", DoubleType(), True),
    StructField("speed", IntegerType(), True),
    StructField("v_speed", IntegerType(), True),
    StructField("squawk", StringType(), True),
    StructField("flight_number", StringType(), True),
    StructField("flight_icao", StringType(), True),
    StructField("flight_iata", StringType(), True),
    StructField("dep_icao", StringType(), True),
    StructField("dep_iata", StringType(), True),
    StructField("arr_icao", StringType(), True),
    StructField("arr_iata", StringType(), True),
    StructField("airline_icao", StringType(), True),
    StructField("airline_iata", StringType(), True),
    StructField("aircraft_icao", StringType(), True),
    StructField("updated", IntegerType(), True),
    StructField("status", StringType(), True),
    StructField("type", StringType(), True),
    StructField("dep_time", StringType(), True),
    StructField("dep_estimated", StringType(), True),
    StructField("dep_actual", StringType(), True),
    StructField("dep_time_utc", StringType(), True),
    StructField("dep_estimated_utc", StringType(), True),
    StructField("dep_actual_utc", StringType(), True),
    StructField("dep_time_ts", IntegerType(), True),
    StructField("dep_estimated_ts", IntegerType(), True),
    StructField("dep_actual_ts", IntegerType(), True),
    StructField("arr_terminal", StringType(), True),
    StructField("arr_gate", StringType(), True),
    StructField("arr_baggage", StringType(), True),
    StructField("arr_time", StringType(), True),
    StructField("arr_estimated", StringType(), True),
    StructField("arr_actual", StringType(), True),
    StructField("arr_time_utc", StringType(), True),
    StructField("arr_estimated_utc", StringType(), True),
    StructField("arr_actual_utc", StringType(), True),
    StructField("arr_time_ts", IntegerType(), True),
    StructField("arr_estimated_ts", IntegerType(), True),
    StructField("cs_airline_iata", StringType(), True),
    StructField("cs_flight_number", StringType(), True),
    StructField("cs_flight_iata", StringType(), True),
    StructField("duration", IntegerType(), True),
    StructField("delayed", IntegerType(), True),
    StructField("dep_delayed", IntegerType(), True),
    StructField("arr_delayed", IntegerType(), True),
    StructField("dep_name", StringType(), True),
    StructField("dep_city", StringType(), True),
    StructField("dep_country", StringType(), True),
    StructField("arr_name", StringType(), True),
    StructField("arr_city", StringType(), True),
    StructField("arr_country", StringType(), True),
    StructField("airline_name", StringType(), True),
    StructField("percent", IntegerType(), True),
    StructField("utc", StringType(), True),
    StructField("eta", IntegerType(), True),
])
# Spark configuration
spark_conf = SparkConf() \
    .setAppName("flight_consumer") \
    .setMaster("local") \
    .set("spark.executor.memory", "2g") \
    .set("spark.executor.cores", "2")

# Create a SparkSession
spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()

# Set log level to ERROR
spark.sparkContext.setLogLevel("ERROR")

# Read from the Kafka topic 'flights'
dataframe = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", 'kafka:9092') \
    .option("subscribe", "flights") \
    .load()

#----------------------------
# PROCESSING THE DATA

# Load the CSV file containing the mapping of IATA codes to positions into a dictionary
iata_position_dict = spark.read.csv("airports_external.csv", header=True) \
                            .rdd \
                            .map(lambda row: (row["iata"], (float(row["lat"]), float(row["lon"])))) \
                            .collectAsMap()

# Define a UDF to retrieve position based on IATA code
def get_position(iata):
    return iata_position_dict.get(iata, (0.0, 0.0))

# Register the UDF
get_position_udf = udf(get_position, StructType([
    StructField("lat", DoubleType(), True),
    StructField("lon", DoubleType(), True)
]))

# Define the flight type determination function
def determine_flight_type(dep_country, arr_country):
     
    if dep_country and arr_country:
        if dep_country == arr_country:
            return "Domestic"
        else:
            return "International"
    else:
        return "Unknown"

# Register the UDF
flight_type_udf = udf(determine_flight_type, StringType())

#Filter the data and add attributes
dataframe = dataframe.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*") \
    .withColumn("position", struct(col("lat").alias("lat"), col("lng").alias("lon"))) \
    .drop("lat", "lng","percent","utc","cs_flight_iata","cs_flight_number","cs_airline_iata","arr_estimated_ts")\
    .drop("arr_time_ts","arr_actual_utc","arr_estimated_utc","arr_time_utc","arr_baggage","arr_gate","arr_terminal")\
    .drop("dep_actual_ts","dep_estimated_ts","dep_time_ts","dep_actual_utc","dep_estimated_utc","dep_time_utc")\
    .drop("dep_gate","dep_terminal","squawk")\
    .withColumn("hex", when(length("hex") == 6, col("hex")).otherwise(None))\
    .withColumn("type", flight_type_udf(col("dep_country"), col("arr_country")))\
    .withColumn("dep_airport_pos", get_position_udf(col("dep_iata"))) \
    .withColumn("arr_airport_pos", get_position_udf(col("arr_iata")))
    

dataframe = dataframe.filter(~(col("position.lat").isNull() | col("position.lon").isNull() | col("position").isNull()))
dataframe = dataframe.filter(~(col("dep_pos.lat").isNull() | col("dep_pos.lon").isNull() | col("dep_pos").isNull()))
dataframe = dataframe.filter(~(col("arr_pos.lat").isNull() | col("arr_pos.lon").isNull() | col("arr_pos").isNull()))


# Print the DataFrame schema for debugging
dataframe.printSchema()

# Write the stream to the console for debugging
query = dataframe \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Wait for the query to finish
query.awaitTermination()
