from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from base.models import User, Admin, Category, Complaint, ComplaintMedia, News


class AdminCreationForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = ('phone', 'name')


class AdminChangeForm(UserChangeForm):
    class Meta:
        model = Admin
        fields = ('phone', 'name', 'profile_picture', 'is_active')


@admin.register(Admin)
class AdminModelAdmin(UserAdmin):
    add_form = AdminCreationForm
    form = AdminChangeForm
    model = Admin
    list_display = ('phone', 'name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    ordering = ('-created_at',)
    search_fields = ('phone', 'name')
    fieldsets = (
        (None, {'fields': ('phone', 'name', 'password')}),
        ('Info', {'fields': ('profile_picture', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name', 'password1', 'password2'),
        }),
    )
    filter_horizontal = ()


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Complaint)
admin.site.register(ComplaintMedia)
admin.site.register(News)
