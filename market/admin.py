from BudMarket.utils import get_all_urls  # Import the utility function
from django.contrib import admin
from .models import Category, Product, ProductAttribute, ProductAttributeValue, HomeImage, ProductImage
from .forms import HomeImageAdminForm


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


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', 'available',)
    list_filter = ('available',)
    ordering = ('title',)
    inlines = [ProductAttributeValueInline, ProductImageInline]

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


@admin.register(HomeImage)
class HomeImageAdmin(admin.ModelAdmin):
    form = HomeImageAdminForm
    list_display = ('alt', 'order', 'url')
    list_editable = ('order', 'url')
    ordering = ('order',)
    change_form_template = 'admin/market/homeimage/change_form.html'

    class Media:
        js = ('admin/js/image_preview.js',)

    def get_urls_list(self):
        urls = get_all_urls()
        return urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['url_list'] = self.get_urls_list()
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
