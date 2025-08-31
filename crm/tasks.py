import logging
from datetime import datetime
import requests
from celery import shared_task

@shared_task
def generate_crm_report():
    log_file = "/tmp/crm_report_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    query = """
    query {
        customers {
            id
        }
        orders {
            id
            totalAmount
        }
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": query},
            timeout=10
        )
        data = response.json().get("data", {})

        customers = data.get("customers", [])
        orders = data.get("orders", [])

        total_customers = len(customers)
        total_orders = len(orders)
        total_revenue = sum(float(o.get("totalAmount", 0)) for o in orders)

        message = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue"

        with open(log_file, "a") as f:
            f.write(message + "\n")

    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Error generating report: {e}\n")