from django.urls import path, include

from django.contrib import admin
from backend.views import *
admin.autodiscover()

from django.conf import settings
from django.conf.urls.static import static
# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
	path("",index,name="index"),
	path("joinnow/",joinnow,name="joinnow"),
	path("profile/",profile,name="profile"),
	path("signup/",signup,name="signup"),
	path("plan/",selectplan,name="plan"),
	path("dashboard/",dashboard,name="dashboard"),
	path("assets/bank",bank_account_form,name="bank_account_form"),
	path("assets/epf",epf_socso_form,name="epf_socso_form"),
	path("assets/insurance/",insurance_form,name="insurance_form"),
	path("assets/investment/",investment_form,name="investment_form"),
	path("assets/property/",property_form,name="property_form"),
	path("assets/vehicles/",vehicles_form,name="vehicles_form"),
	path("assets/others/",asset_others_form,name="asset_others_form"),
 	path("admin/", admin.site.urls),
]



urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
