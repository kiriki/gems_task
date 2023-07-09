import csv
import io
from typing import TYPE_CHECKING

from rest_framework import serializers

from django.db.models import Count, Q, Sum

from gems.models import Customer, Deal, GemItem

if TYPE_CHECKING:
    from django.core.files.uploadedfile import UploadedFile

# 5 клиентов, потративших наибольшую сумму за весь период
selected_customers_queryset = Customer.objects.annotate(
    spent_money=Sum('deal__total')
).order_by('-spent_money')

CUSTOMERS_LIMIT = 5


class CustomerSerializer(serializers.ModelSerializer):
    spent_money = serializers.IntegerField(read_only=True)
    gems = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = 'username', 'spent_money', 'gems'

    def get_gems(self, obj: Customer) -> list[str]:
        """Список из названий камней, которые купили как минимум двое из списка
        "5 клиентов, потративших наибольшую сумму за весь период",
        и данный клиент является одним из этих покупателей.
        """
        result_qs = GemItem.objects.annotate(
            num_customers=Count(
                'deal__customer',
                filter=Q(
                    deal__customer__in=selected_customers_queryset[:CUSTOMERS_LIMIT]
                ),
                distinct=True,
            )
        ).filter(num_customers__gte=2, deal__customer__exact=obj)

        return result_qs.values_list('name', flat=True)


class DealSerializerCreate(serializers.ModelSerializer):
    """Serializer for creating Deal objects from CSV file entries."""

    customer = serializers.CharField()
    item = serializers.CharField()

    class Meta:
        model = Deal
        fields = '__all__'

    def create(self, validated_data: dict) -> Deal:
        customer_name = validated_data.pop('customer')
        gem_item_name = validated_data.pop('item')

        customer, _ = Customer.objects.get_or_create(username=customer_name)
        gem_item, _ = GemItem.objects.get_or_create(name=gem_item_name)

        return Deal.objects.create(customer=customer, item=gem_item, **validated_data)


class DealsFileUploadSerializer(serializers.Serializer):
    """Serializer for upload CVS file with deals data."""

    deals = serializers.FileField()

    def create(self, validated_data: dict):
        csv_reader = self.get_reader(validated_data)
        res = import_deals_from_csv_reader(csv_reader)
        return {'Status': 'OK', 'Count': res}

    def get_reader(self, validated_data: dict) -> csv.DictReader:
        csv_file: UploadedFile = validated_data['deals']
        text_data: str = csv_file.read().decode('utf-8')
        return csv.DictReader(io.StringIO(text_data))


def import_deals_from_csv_reader(reader: csv.DictReader) -> int:
    """Import deals data from csv file reader."""
    # Очистка. Для реализации требования п. 2 задания:
    # "Ранее загруженные версии файла deals.csv не должны влиять на результат обработки новых."
    Deal.objects.all().delete()

    for row in reader:
        serializer = DealSerializerCreate(data=row)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    return Deal.objects.count()
