import requests
import os
from dotenv import load_dotenv
import duckdb

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("ETHERSCAN_API_KEY")
url = f"https://eth-mainnet.g.alchemy.com/v2/{api_key}"

os.makedirs("data", exist_ok=True)

con = duckdb.connect("data/raw_data.duckdb")

con.execute("""
CREATE TABLE IF NOT EXISTS raw_alchemy_transfers (
    blockNum VARCHAR,
    hash VARCHAR,
    fromAddress VARCHAR,
    toAddress VARCHAR,
    value VARCHAR,
    asset VARCHAR,
    category VARCHAR,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

TARGET_ROWS = 1000000

total_inserted_rows = con.execute("SELECT COUNT(*) FROM raw_alchemy_transfers").fetchone()[0]

headers = {"Content-Type": "application/json"}

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": "0x1000000",
            "toBlock": "latest",
            "excludeZeroValue": True,
            "withMetadata": True,
            "category": ["external", "erc20"],
            "maxCount": "0x3e8"  # 1000 in hex
        }
    ]
}

page_key = None

while total_inserted_rows < TARGET_ROWS:
  if page_key:
    payload["params"][0]["pageKey"] = page_key

  try:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    data = response.json()
  except Exception as e:
    print(f"Ошибка запроса к API: {e}")
    break

  if "result" in data and "transfers" in data["result"]:
    transfers = data["result"]["transfers"]
    if not transfers:
      print("Данные в блокчейне закончились раньше, чем достигли лимита.")
      break

    rows = []
    for t in transfers:
      rows.append((
          t.get("blockNum"),
          t.get("hash"),
          t.get("from"),
          t.get("to"),
          t.get("value"),
          t.get("asset"),
          t.get("category"),
      ))

    con.executemany(
        """
            INSERT INTO raw_alchemy_transfers (blockNum, hash, fromAddress, toAddress, value, asset, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )

    total_inserted_rows += len(rows)
    print(f"Загружено. Всего в базе: {total_inserted_rows:,} / {TARGET_ROWS:,}")

    page_key = data["result"].get("pageKey")
    if not page_key:
      print("Пагинация Alchemy завершена (pageKey отсутствует).")
      break
  else:
    print("Ошибка в ответе API:", data)
    break


con.close()

print(f"Загрузка завершена. Всего загружено: {total_inserted_rows:,} строк.")
