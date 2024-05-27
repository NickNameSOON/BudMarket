from django.contrib import admin
from .models import Category, Product, ProductAttribute, ProductAttributeValue


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    ordering = ('name',)
    inlines = [ProductAttributeInline]

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['attribute'].queryset = ProductAttribute.objects.none()

        if obj and obj.category:
            formset.form.base_fields['attribute'].queryset = ProductAttribute.objects.filter(category=obj.category)

        return formset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', 'available',)
    list_filter = ('available',)
    ordering = ('title',)
    inlines = [ProductAttributeValueInline]

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}

    class Media:
        js = ('admin/js/product_attribute_filter.js',)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    ordering = ('name',)


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    ordering = ('product',)
