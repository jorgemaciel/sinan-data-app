from pyspark.sql import SparkSession
import pyspark.sql.functions as F


spark = SparkSession \
    .builder \
    .appName("test reading s3") \
    .config("spark.executor.instances", "4") \
    .config("spark.executor.memory", "2g") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")\
    .getOrCreate()

df = spark.range(0, 100_000_000)

df = df.withColumn("content", F.lit("Anything"))

(
    df.write
    .format("parquet")
    .mode("overwrite")
    .save("s3a://raw/sample")
)

spark.stop()
