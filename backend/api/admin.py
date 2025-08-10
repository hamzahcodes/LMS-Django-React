from django.contrib import admin
from api import models as api_models

admin.site.register(api_models.Category)
admin.site.register(api_models.Cart)
admin.site.register(api_models.CartOrder)
admin.site.register(api_models.CartOrderItem)
admin.site.register(api_models.Teacher)
admin.site.register(api_models.Lecture)
admin.site.register(api_models.Section)
admin.site.register(api_models.EnrolledCourse)
admin.site.register(api_models.Country)
admin.site.register(api_models.Notification)
admin.site.register(api_models.Note)
admin.site.register(api_models.Certificate)
admin.site.register(api_models.Coupon)
admin.site.register(api_models.Course)