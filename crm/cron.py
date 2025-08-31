import logging
from datetime import datetime
import requests

def update_low_stock():
    log_file = "/tmp/low_stock_updates_log.txt"
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    mutation = """
    mutation {
        updateLowStockProducts {
            success
            updatedProducts {
                id
                title
                stock
            }
        }
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": mutation},
            timeout=10
        )
        data = response.json()
        updates = data.get("data", {}).get("updateLowStockProducts", {})

        with open(log_file, "a") as f:
            f.write(f"{timestamp} - {updates.get('success')}\n")
            for product in updates.get("updatedProducts", []):
                f.write(f"  - {product['title']} new stock: {product['stock']}\n")

    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Error: {e}\n")