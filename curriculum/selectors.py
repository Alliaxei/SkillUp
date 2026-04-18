from django.db.models import QuerySet

from .models import Module


def get_module_with_content(module_id: int) -> Module:
    return Module.objects.prefetch_related("materials", "tasks").get(id=module_id)
