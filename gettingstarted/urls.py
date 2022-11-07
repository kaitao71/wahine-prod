from django.urls import path, include

from django.contrib import admin
from backend.views import *
admin.autodiscover()


# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
	path("bank/",bank_account_form,name="bank_account_form"),
	path("epf/",epf_socso_form,name="epf_socso_form"),
	path("insurance/",insurance_form,name="insurance_form"),
 	path("admin/", admin.site.urls),
]
