from import_export import resources
from .models import PolishedUrl


class PolishedUrlResource(resources.ModelResource):
    class Meta:
        model = PolishedUrl