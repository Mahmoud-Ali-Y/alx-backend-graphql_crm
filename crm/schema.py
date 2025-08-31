import graphene
from properties.models import Property  # assuming products are in properties app
from graphene_django.types import DjangoObjectType

class ProductType(DjangoObjectType):
    class Meta:
        model = Property  # replace with your actual Product model
        fields = ("id", "title", "description", "price", "location", "created_at", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # no arguments required

    success = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        low_stock_products = Property.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10  # simulate restocking
            product.save()
            updated_products.append(product)

        return UpdateLowStockProducts(
            success=f"Restocked {len(updated_products)} products",
            updated_products=updated_products
        )


class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()