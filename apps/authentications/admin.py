from django.contrib import admin

# Register your models here.
from .models import VerificationCode
# Register your models here.


@admin.register(VerificationCode)
class UserModel(admin.ModelAdmin):
    list_display = ("user", "code_partial", "created")
    search_fields = ("code", "user__email", "user__username", "user__id")
    list_per_page = 25
    date_hierarchy = "created"

    @staticmethod
    def code_partial(obj):
        return f"{str(obj.code)[0:2]}***{str(obj.code)[5:6]}"

    code_partial.short_description = "Code"
