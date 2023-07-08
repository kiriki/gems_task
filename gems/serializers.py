from rest_framework import serializers

from django.db.models import Count, Q

from gems.models import Customer, GemItem


class CustomerSerializer(serializers.ModelSerializer):
    spent_money = serializers.IntegerField(read_only=True)
    gems = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = 'username', 'spent_money', 'gems'

    def get_gems(self, obj: Customer) -> list[str]:
        from gems.views import CustomersViewSet

        qs = CustomersViewSet.queryset

        result_qs = GemItem.objects.annotate(
            num_customers=Count(
                'deal__customer', filter=Q(deal__customer__in=qs), distinct=True
            )
        ).filter(num_customers__gte=2, deal__customer__exact=obj)

        return result_qs.values_list('name', flat=True)
