import os, time, logging, requests
import psycopg
from datetime import date
from dateutil.relativedelta import relativedelta

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DB = {
    "host": os.getenv("POSTGRES_HOST", "db"),
    "dbname": os.getenv("POSTGRES_DB", "sid_db"),
    "user": os.getenv("POSTGRES_USER", "sid_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "sid_pass"),
}

# EXEMPLE: source fictive (remplacera par vraie API plus tard)
def fetch_price(asset_code, d):
    # valeur factice pour TP
    return round(100 + hash((asset_code, d)) % 50, 4)

def main():
    with psycopg.connect(**DB) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, code FROM core_asset;")
            assets = cur.fetchall()

            start = date.today() - relativedelta(years=2)
            end = date.today()

            for asset_id, code in assets:
                d = start
                while d <= end:
                    price = fetch_price(code, d)
                    cur.execute(
                        """
                        INSERT INTO core_price (asset_id, date, value_mru, source)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (asset_id, date) DO NOTHING;
                        """,
                        (asset_id, d, price, "demo"),
                    )
                    d += relativedelta(days=1)

        conn.commit()
    logging.info("Scraping terminé avec succès")

if __name__ == "__main__":
    for attempt in range(3):
        try:
            main()
            break
        except Exception as e:
            logging.error(f"Erreur scraper (tentative {attempt+1}/3): {e}")
            time.sleep(5)
