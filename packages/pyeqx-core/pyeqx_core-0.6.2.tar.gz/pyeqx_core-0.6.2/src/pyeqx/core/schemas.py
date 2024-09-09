from pyspark.sql.types import (
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

BRONZE_METADATA_SCHEMA = StructType(
    [
        StructField("bronze_data_table", StringType(), False),
        StructField("source_system", StringType(), False),
        StructField("source_type", StringType(), False),
        StructField("source_name", StringType(), False),
        StructField("updated_at", TimestampType(), False),
    ]
)

BRONZE_INGESTION_LOG_SCHEMA = StructType(
    [
        StructField("ingested_timestamp", TimestampType(), False),
        StructField("source_name", StringType(), False),
        StructField("source_count", IntegerType(), False),
        StructField("bronze_data_table", StringType(), False),
        StructField("bronze_data_count", IntegerType(), False),
        StructField("status", StringType(), False),
    ]
)
