import openpyxl
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from .models import Profile, Resturant, FoodItem, Order, OrderItem, Cart, CartItem, Review


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')


@admin.register(Resturant)
class ResturantAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'resturant', 'get_location', 'price','is_veg')
    list_filter = ('resturant','is_veg')
    change_list_template = "admin/fooditem_changelist.html"
    actions = ['export_to_excel']

    def get_location(self, obj):
        return obj.resturant.location
    get_location.short_description = 'Location'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.import_excel, name='fooditem_import_excel'),
        ]
        return custom_urls + urls

    def import_excel(self, request):
        if request.method == "POST":
            form = ExcelUploadForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = request.FILES["excel_file"]
                wb = openpyxl.load_workbook(excel_file)
                sheet = wb.active

                updated_count = 0
                skipped_count = 0

                for row in sheet.iter_rows(min_row=2, values_only=True):
                    food_name, is_veg = row

                    if not food_name:
                        skipped_count += 1
                        continue

                    veg_value = str(is_veg).strip().lower() if is_veg is not None else "yes"
                    is_veg_bool = veg_value in ["yes", "true", "1", "veg"]

                    matching_items = FoodItem.objects.filter(name=food_name)
                    for item in matching_items:
                        item.is_veg = is_veg_bool
                        item.save()
                        updated_count += 1

                messages.success(
                    request,
                    f"Import complete: {updated_count} food items updated, {skipped_count} rows skipped."
                )
                return redirect("..")
        else:
            form = ExcelUploadForm()

        return render(request, "admin/excel_upload.html", {"form": form})
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'rating', 'created_at')
    list_filter = ('rating',)

    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery'].queryset = User.objects.filter(profile__role='DELIVERY')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = ('id', 'customer', 'delivery', 'status', 'is_paid', 'payment_method', 'created_at')
    list_filter = ('status', 'is_paid', 'payment_method')
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(payment_method='ONLINE', is_paid=False)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'food', 'quantity')