import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--data-type', default='yellow', help='yellow, green, or zone')
@click.option('--year', default=2021, type=int, help='Year of data (for yellow/green)')
@click.option('--month', default=1, type=int, help='Month of data (for yellow/green)')
@click.option('--target-table', required=True, help='Target table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db,
        data_type, year, month, target_table, chunksize):
        
    """
    Ingest NYC taxi (yellow, green, zone lookup) data into PostgreSQL database.
    """
    
    engine = create_engine(
        f'postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    )

    # ===============================
    # SELECT DATA SOURCE
    # ===============================

    if data_type == 'yellow':
        prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
        url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    elif data_type == 'green':
        prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
        url = f'{prefix}/green_tripdata_{year}-{month:02d}.parquet'

    elif data_type == 'zone':
        url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'

    else:
        raise ValueError("Invalid data_type. Choose from: yellow, green, zone")

    print(f"📥 Downloading & reading data from: {url}")

    # ===============================
    # INGEST PARQUET (GREEN)
    # ===============================

    if url.endswith(".parquet"):
        df = pd.read_parquet(url)

        print("🚀 Creating table...")
        df.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists='replace'
        )

        print("🚀 Inserting data...")
        df.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )

        print("✅ Green taxi data ingested successfully!")

    # ===============================
    # INGEST CSV (YELLOW / ZONE)
    # ===============================

    else:
        # zone lookup does not need dtype parsing
        if data_type == 'zone':
            df = pd.read_csv(url)

            df.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )

            df.to_sql(
                name=target_table,
                con=engine,
                if_exists='append'
            )

            print("✅ Taxi zone lookup ingested successfully!")

        else:
            # yellow taxi (csv.gz)
            df_iter = pd.read_csv(
                url,
                dtype=dtype,
                parse_dates=[
                    "tpep_pickup_datetime",
                    "tpep_dropoff_datetime"
                ],
                iterator=True,
                chunksize=chunksize,
            )

            first = True

            for df_chunk in tqdm(df_iter):
                if first:
                    df_chunk.head(0).to_sql(
                        name=target_table,
                        con=engine,
                        if_exists='replace'
                    )
                    first = False

                df_chunk.to_sql(
                    name=target_table,
                    con=engine,
                    if_exists='append'
                )

            print("✅ Yellow taxi data ingested successfully!")


if __name__ == '__main__':
    run()