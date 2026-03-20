from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

def create_source(t_env):
    t_env.execute_sql("""
        CREATE TABLE green_trips (
            PULocationID INT,
            DOLocationID INT,
            trip_distance DOUBLE,
            total_amount DOUBLE,
            lpep_pickup_datetime STRING,

            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-trips',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'scan.startup.mode' = 'latest-offset',
            'format' = 'json'
        )
    """)

def create_sink(t_env):
    t_env.execute_sql("""
        CREATE TABLE green_trips_processed (
            PULocationID INT,
            DOLocationID INT,
            trip_distance DOUBLE,
            total_amount DOUBLE,
            pickup_datetime TIMESTAMP
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'green_trips_processed',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        )
    """)

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)  # WAJIB

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    create_source(t_env)
    create_sink(t_env)

    t_env.execute_sql("""
        INSERT INTO green_trips_processed
        SELECT
            PULocationID,
            DOLocationID,
            trip_distance,
            total_amount,
            event_timestamp
        FROM green_trips
    """).wait()

if __name__ == "__main__":
    main()