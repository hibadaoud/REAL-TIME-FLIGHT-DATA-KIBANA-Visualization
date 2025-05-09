# IMPORT LIBRARIES
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql.types import StructType, StructField, DoubleType, IntegerType
from pyspark.sql.functions import from_json, col, when, length, struct
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# ----------------------------pip install pyspark
# QUERY RELATED
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
    StructField("status", StringType(), True),
])

spark_conf = SparkConf() \
    .setAppName("flight_consumer") \
    .setMaster("local") \
    .set("spark.executor.memory", "2g") \
    .set("spark.executor.cores", "2")

# Create a SparkSession
spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()

# Set log level to ERROR
spark.sparkContext.setLogLevel("ERROR")

# Read from the Kafka topic 'flight'
dataframe = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", 'kafka:9092') \
    .option("subscribe", "flights") \
    .option("startingOffsets", "earliest") \
    .load()

# ----------------------------
# PROCESSING THE DATA

# Load the CSV file containing the mapping of IATA codes to country codes into a dictionary
iata_country_dict = spark.read.csv("airports_external.csv", header=True) \
                            .rdd \
                            .map(lambda row: (row["iata"], row["country_code"])) \
                            .collectAsMap()


# Load the CSV file containing the mapping of IATA codes to positions into a dictionary
iata_position_dict = spark.read.csv("airports_external.csv", header=True) \
                            .rdd \
                            .map(lambda row: (row["iata"], (float(row["lat"]), float(row["lon"])))) \
                            .collectAsMap()


# Load the CSV file containing the mapping of IATA codes to names into a dictionary
iata_name_dict = spark.read.csv("airports_external.csv", header=True) \
                            .rdd \
                            .map(lambda row: (row["iata"], row["Name"])) \
                            .collectAsMap()


# Define the flight type determination function
def determine_flight_type(dep_iata, arr_iata):
    dep_country_code = iata_country_dict.get(dep_iata, None)
    arr_country_code = iata_country_dict.get(arr_iata, None)
    if dep_country_code and arr_country_code:
        if dep_country_code == arr_country_code:
            return "Domestic"
        else:
            return "International"
    else:
        return "Unknown"


# Register the UDF
flight_type_udf = udf(determine_flight_type, StringType())


# Define a UDF to retrieve position based on IATA code
def get_position(iata):
    return iata_position_dict.get(iata, (0.0, 0.0))


# Register the UDF
get_position_udf = udf(get_position, StructType([
    StructField("lat", DoubleType(), True),
    StructField("lon", DoubleType(), True)
]))


# Define a UDF to retrieve name based on IATA code
def get_name(iata):
    return iata_name_dict.get(iata, None)


# Register the UDF
get_name_udf = udf(get_name, StringType())


# Filter the data and add attributes
dataframe = dataframe.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*") \
    .withColumn("position", struct(col("lat").alias("lat"), col("lng").alias("lon"))) \
    .drop("lat", "lng")\
    .withColumn("hex", when(length("hex") == 6, col("hex")).otherwise(None))\
    .withColumn("type", flight_type_udf(col("dep_iata"), col("arr_iata")))\
    .withColumn("dep_pos", get_position_udf(col("dep_iata"))) \
    .withColumn("arr_pos", get_position_udf(col("arr_iata")))\
    .withColumn("Departure", get_name_udf(col("dep_iata")))\
    .withColumn("Arrival", get_name_udf(col("arr_iata")))

dataframe = dataframe.dropna(subset=["flight_icao"])
dataframe = dataframe.dropDuplicates(["flight_icao"])  # Deduplicate based on flight_icao
dataframe = dataframe.filter(~(col("position.lat").isNull() | col("position.lon").isNull() | col("position").isNull()))
dataframe = dataframe.filter(~(col("dep_pos.lat").isNull() | col("dep_pos.lon").isNull() | col("dep_pos").isNull()))
dataframe = dataframe.filter(~(col("arr_pos.lat").isNull() | col("arr_pos.lon").isNull() | col("arr_pos").isNull()))


# ----------------------------
# WRITING INTO ELASTICSEARCH
query = dataframe.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .outputMode("update") \
    .option("es.mapping.id", "flight_icao") \
    .option("es.nodes", "elasticsearch") \
    .option("es.port", "9200") \
    .option("es.nodes.wan.only", "true") \
    .option("checkpointLocation", "tmp/checkpoint2") \
    .option("es.resource", "esflight")\
    .start()

# Writing to console (for test and debug purposes)
# query = dataframe \
#     .writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .option("truncate", False) \
#     .option("numRows", 100) \
#     .start()

query.awaitTermination()
