#!/usr/bin/env python3

import sys
import logging
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure logging
logging.basicConfig(
    filename="/tmp/order_reminders_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

def main():
    # GraphQL endpoint
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Calculate date range (last 7 days)
    seven_days_ago = (datetime.now() - timedelta(days=7)).date().isoformat()

    # GraphQL query
    query = gql(
        """
        query getRecentOrders($since: Date!) {
            orders(orderDate_Gte: $since) {
                id
                customer {
                    email
                }
            }
        }
        """
    )

    # Execute query
    try:
        result = client.execute(query, variable_values={"since": seven_days_ago})
        orders = result.get("orders", [])

        for order in orders:
            order_id = order.get("id")
            customer_email = order.get("customer", {}).get("email")
            logging.info(f"Order ID: {order_id}, Customer Email: {customer_email}")

        print("Order reminders processed!")

    except Exception as e:
        logging.error(f"Error fetching orders: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()