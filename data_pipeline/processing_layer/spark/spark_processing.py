from pyspark.sql import SparkSession
import os

print("\nRunning PySpark processing...\n")

# Create Spark session
spark = SparkSession.builder \
    .appName("Clinical Data Processing") \
    .getOrCreate()

# Load integrated dataset
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

data_path = os.path.join(
    BASE_DIR,
    "Integration/patient_integrated_profile.csv"
)

df = spark.read.csv(
    data_path,
    header=True,
    inferSchema=True
)

# Show schema
df.printSchema()

# Example transformation
print("\nPatient count by risk flag:\n")
df.groupBy("risk_flag").count().show()

# Example filter
print("\nHigh BMI patients:\n")
df.filter(df.bmi_y > 30).select("patient_id", "bmi_y").show()

# Save as Parquet (data lake layer)
output_path = os.path.join(BASE_DIR, "data_lake/patient_data.parquet")

df.write.mode("overwrite").parquet(output_path)

print("\nData saved to Parquet (data lake layer)\n")

spark.stop()
