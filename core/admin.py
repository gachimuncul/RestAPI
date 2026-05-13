from django.contrib import admin
from .models import User, Role, UserRole, Resource, Action, PermissionRule

admin.site.register(User)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Resource)
admin.site.register(Action)
admin.site.register(PermissionRule)