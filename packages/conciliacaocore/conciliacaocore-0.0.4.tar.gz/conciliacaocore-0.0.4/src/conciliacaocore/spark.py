from pyspark.sql import SparkSession

spark = None


def create_spark_session():
    global spark
    if spark is None:
        try:
            spark = (
                SparkSession.builder.appName("ConciliacaoAPI")
                .config("spark.driver.memory", "4g")
                .config("spark.executor.memory", "4g")
                .getOrCreate()
            )
        except Exception as e:
            raise Exception(f"Error creating Spark session: {str(e)}")
    return spark


def stop_spark_session():
    global spark
    if spark:
        spark.stop()
        spark = None
