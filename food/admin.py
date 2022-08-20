from django.contrib import admin

from food.models import Recipe, Product, RecipeProduct


class RecipeProductInline(admin.TabularInline):
    model = RecipeProduct
    extra = 5
    raw_id_fields = ('product', )

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeProductInline, ]
    exclude = ['products', ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
