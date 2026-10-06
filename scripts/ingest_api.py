import snowflake.connector
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("ETHERSCAN_API_KEY")
url = f"https://eth-mainnet.g.alchemy.com/v2/{api_key}"

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": "0x0",
            "toBlock": "latest",
            "excludeZeroValue": True,
            "withMetadata": True,
            "category": ["external", "erc20"],
            "maxCount": "0x64"
        }
    ]
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
response.raise_for_status()  # Raise an exception for HTTP errors

transfers = response.json().get("result", {}).get("transfers", [])

print(f"Number of transfers: {len(transfers)}")

if len(transfers) > 0:
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asset_transfers (
            blockNum STRING,
            fromAddress STRING,
            toAddress STRING,
            value STRING,
            asset STRING,
            category STRING,
            hash STRING
        )
    """)

    # Insert transfers into the table
    for transfer in transfers:
        cursor.execute("""
            INSERT INTO asset_transfers (blockNum, fromAddress, toAddress, value, asset, category, hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            transfer.get("blockNum"),
            transfer.get("from"),
            transfer.get("to"),
            transfer.get("value"),
            transfer.get("asset"),
            transfer.get("category"),
            transfer.get("hash")
        ))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()    
