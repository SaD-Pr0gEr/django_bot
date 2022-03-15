from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from accounts.models import CustomUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_active', 'is_admin')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_admin', 'is_staff', 'date_joined']
    list_display_links = ['email', ]
    search_fields = ['email', 'date_joined', ]
    list_editable = ['is_staff', 'is_admin']
    readonly_fields = ['date_joined', 'is_active', 'email', 'password', 'last_login']
    ordering = ['date_joined', ]
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_active')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'date_joined', 'last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


admin.site.unregister(Group)
