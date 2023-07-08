import csv
import logging
import os
from collections.abc import Iterator
from datetime import datetime
from typing import TypedDict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

import django

django.setup()

from gems.models import Customer, Deal, GemItem

log = logging.getLogger(__name__)

class DealDict(TypedDict):
    customer: str
    item: str
    total: str
    quantity: str
    date: str


def import_deals_from_csv(file_path):
    Deal.objects.all().delete()
    with open(file_path) as csv_file:
        reader: Iterator[DealDict] = csv.DictReader(csv_file)
        for row in reader:
            customer_name = row['customer']
            gem_item_name = row['item']
            total = int(row['total'])
            quantity = int(row['quantity'])
            date_str = row['date']
            date = datetime.fromisoformat(date_str)

            customer, _ = Customer.objects.get_or_create(username=customer_name)
            gem_item, _ = GemItem.objects.get_or_create(name=gem_item_name)

            deal = Deal(
                customer=customer,
                item=gem_item,
                total=total,
                quantity=quantity,
                date=date,
            )
            deal.save()

    log.info('Imported %s deals', Deal.objects.count())


if __name__ == '__main__':
    import_deals_from_csv('csv_data/deals.csv')
