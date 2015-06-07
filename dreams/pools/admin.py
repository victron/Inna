from django.contrib import admin


# Register your models here.

from .models import User, Dreams

class Dreams_inline(admin.TabularInline):
    model = Dreams
    extra = 3


class User_admin_view(admin.ModelAdmin):
    # fields = ['login', 'email', 'registration_date']
    list_display = ('login', 'email')
    fieldsets = [
        (None,              {'fields' : ['login', 'email']}),
        ('Date',            {'fields' : ['registration_date']}),
        ('User details',    {'fields' : ['firstName', 'lastName'],
                             'classes': ['collapse']}),
    ]
    inlines = [Dreams_inline]
    list_filter = ['registration_date']
    search_fields = ['login']


class Dreams_admin_view(admin.ModelAdmin):
    list_display = ('dream_subject', 'dream_date', 'user_login')

# trick to get object from another class
    def user_login(self, obj):
        return obj.user.login




admin.site.register(User, User_admin_view)
admin.site.register(Dreams, Dreams_admin_view)
# admin.AdminSite.site_header = 'rrrrr'
admin.site.site_header = '!!!!!!! Admin page !!!!!!!'