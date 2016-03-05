from django.contrib import admin
admin.autodiscover()
from collegeTimetableSystem.models import Teacher,Subject,WorkDetails


admin.site.register(Teacher)
admin.site.register(WorkDetails)
admin.site.register(Subject)
