from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(users)
admin.site.register(stimul_slov)
admin.site.register(otvet)
admin.site.register(vibor_test)
admin.site.register(userlink)
