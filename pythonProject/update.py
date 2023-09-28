# update_duplicate_slugs.py
from myapp.models import Product
from django.db import models

def update_duplicate_slugs():
    # Find products with the same slug
    duplicate_products = Product.objects.values('slug').annotate(count=models.Count('id')).filter(count__gt=1)

    for duplicate in duplicate_products:
        products = Product.objects.filter(slug=duplicate['slug'])
        # Update the slug to make it unique for each product
        for index, product in enumerate(products):
            new_slug = f"{product.slug}-{index}"
            product.slug = new_slug
            product.save()

if __name__ == '__main__':
    update_duplicate_slugs()
