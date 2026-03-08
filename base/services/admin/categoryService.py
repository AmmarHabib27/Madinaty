from rest_framework.exceptions import NotFound
from base.models import Category


def list_categories():
    return Category.objects.all().order_by('name')


def get_category(category_id: int) -> Category:
    try:
        return Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise NotFound('Category not found.')


def create_category(admin_user, validated_data: dict) -> Category:
    return Category.objects.create(created_by=admin_user, **validated_data)


def update_category(category_id: int, validated_data: dict) -> Category:
    category = get_category(category_id)
    for attr, value in validated_data.items():
        setattr(category, attr, value)
    category.save()
    return category


def delete_category(category_id: int) -> None:
    category = get_category(category_id)
    category.delete()
