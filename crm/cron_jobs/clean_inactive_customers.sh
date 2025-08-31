#!/bin/bash

# Navigate to the project root (adjust path if needed)
cd "$(dirname "$0")/../.."

# Run Django shell command to delete inactive customers
DELETED_COUNT=$(echo "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(
    orders__isnull=True,
    created_at__lt=one_year_ago
).delete()
print(deleted)
" | python manage.py shell 2>/dev/null)

# Log result with timestamp
echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $DELETED_COUNT\" >> /tmp/customer_cleanup_log.txt
["count"]