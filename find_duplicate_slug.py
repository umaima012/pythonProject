import os
import django
from django.conf import settings
from myapp.models import Product
from django.db.models import Count

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pythonProject.settings")  # Replace with your project's settings module
django.setup()

# Find products with duplicate slugs
duplicate_slugs = Product.objects.values('slug').annotate(slug_count=Count('slug')).filter(slug_count__gt=1)

# Print the duplicate slugs
for item in duplicate_slugs:
    print(item)