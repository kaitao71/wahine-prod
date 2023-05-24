from django.urls import path, include

from django.contrib import admin
from backend.views import *
from backend.admin import *
# admin.autodiscover()

from django.conf import settings
from django.conf.urls.static import static
from django_registration.backends.activation.views import RegistrationView
# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
	## Creating Assets
	path("assets/bank",assets_bank_modelform,name="assets-bank-createform"),
	path("assets/epf",assets_epf_modelform,name="assets-epf-createform"),
	path("assets/socso",assets_socso_modelform,name="assets-socso-createform"),
	path("assets/insurance",assets_insurance_modelform,name="assets-insurance-createform"),
	path("assets/securities-investment",assets_securities_investment_modelform,name="assets-securities-investment-createform"),
	path("assets/unittrust-investment",assets_unittrust_investment_modelform,name="assets-unittrust-investment-createform"),
	path("assets/property",assets_property_modelform,name="assets-property-createform"),
	path("assets/vehicle",assets_vehicle_modelform,name="assets-vehicle-createform"),
	path("assets/others",assets_other_modelform,name="assets-other-createform"),
	path("assets/crypto",assets_crypto_modelform,name="assets-crypto-createform"),

	## Editing Assets
	path("assets/bank/edit/<uuid>",assets_bank_editform,name="assets-bank-editform"),
	path("assets/epf/edit/<uuid>",assets_epf_editform,name="assets-epf-editform"),
	path("assets/socso/edit/<uuid>",assets_socso_editform,name="assets-socso-editform"),
	path("assets/insurance/edit/<uuid>",assets_insurance_editform,name="assets-insurance-editform"),
	path("assets/securityinvestment/edit/<uuid>",assets_securityinvestment_editform,name="assets-securityinvestment-editform"),
	path("assets/unittrustinvestment/edit/<uuid>",assets_unittrustinvestment_editform,name="assets-unittrustinvestment-editform"),
	path("assets/property/edit/<uuid>",assets_property_editform,name="assets-property-editform"),
	path("assets/vehicles/edit/<uuid>",assets_vehicle_editform,name="assets-vehicle-editform"),
	path("assets/others/edit/<uuid>",assets_other_editform,name="assets-other-editform"),
	path("assets/crypto/edit/<uuid>",assets_crypto_editform,name="assets-crypto-editform"),

	path("assets/bank/delete/<uuid>",assets_bank_deleteform.as_view(),name="assets-bank-deleteform"),
	# path("assets/epf/delete/<uuid>",assets_epf_deleteform,name="assets-epf-deleteform"),
	# path("assets/socso/delete/<uuid>",assets_socso_deleteform,name="assets-socso-deleteform"),
	path("assets/insurance/delete/<uuid>",assets_insurance_deleteform.as_view(),name="assets-insurance-deleteform"),
	path("assets/securityinvestment/delete/<uuid>",assets_securityinvestment_deleteform.as_view(),name="assets-securityinvestment-deleteform"),
	path("assets/unittrustinvestment/delete/<uuid>",assets_unittrustinvestment_deleteform.as_view(),name="assets-unittrustinvestment-deleteform"),
	path("assets/property/delete/<uuid>",assets_property_deleteform.as_view(),name="assets-property-deleteform"),
	path("assets/vehicles/delete/<uuid>",assets_vehicle_deleteform.as_view(),name="assets-vehicle-deleteform"),
	path("assets/others/delete/<uuid>",assets_other_deleteform.as_view(),name="assets-other-deleteform"),
	path("assets/crypto/delete/<uuid>",assets_crypto_deleteform.as_view(),name="assets-crypto-deleteform"),

	path("liabilities/creditcard",liabilities_creditcard_modelform,name="liabilities-creditcard-createform"),
	path("liabilities/personalloan",liabilities_personalloan_modelform,name="liabilities-personalloan-createform"),
	path("liabilities/vehicle",liabilities_vehicleloan_modelform,name="liabilities-vehicleloan-createform"),
	path("liabilities/property",liabilities_propertyloan_modelform,name="liabilities-propertyloan-createform"),
	path("liabilities/others",liabilities_other_modelform,name="liabilities-other-createform"),

	## Editing Liabilities
	path("liabilities/card/edit/<uuid>",liabilities_creditcard_editform,name="liabilities-creditcard-editform"),
	path("liabilities/personal/edit/<uuid>",liabilities_personalloan_editform,name="liabilities-personalloan-editform"),
	path("liabilities/vehicles/edit/<uuid>",liabilities_vehicleloan_editform,name="liabilities-vehicleloan-editform"),
	path("liabilities/property/edit/<uuid>",liabilities_propertyloan_editform,name="liabilities-propertyloan-editform"),
	path("liabilities/others/edit/<uuid>",liabilities_other_editform,name="liabilities-other-editform"),

	path("assets/overview",assets_overview,name="assets-overview"),
	path("liabilities/overview",liabilities_overview,name="liabilities-overview"),

    path('ajax/load-residential-type/', load_residential_type, name='data-residential-type-url'),
	path("",index,name="index"),
	path("joinnow",joinnow,name="joinnow"),
	path("whoweare/",whoweare,name="whoweare"),
	path("contact/",contactus,name="contactus"),
	path("terms-of-service/",terms_of_service,name="terms-of-service"),
	path("privacy-policy/",privacy_policy,name="privacy-policy"),
	path("return-refund-policy/",return_refund_policy,name="return-refund-policy"),
	path("profile/",profile,name="profile"),
	path("plan/",selectplan,name="plan"),
	path("faq/",faq,name="faq"),
	# path("dashboard/",dashboard,name="dashboard"),
	path("dashboard-new/",dashboard_new,name="dashboard-new"),
	path("logout/",logout_view,name="logout"),

	## Onboarding Trigger Events
	path("triggers/notifier/",notifier_list_form,name="notifier_list_form"),
	path("triggers/accesslist/",access_list_form,name="access_list_form"),
 	path("admin/", admin.site.urls),

 	
 	## Django Registration Urls
    path('accounts/register/',
        RegistrationView.as_view(
            form_class=MyCustomUserForm
        ),
        name='django_registration_register',
    ),
    path('accounts/',
        include('django_registration.backends.activation.urls')
    ),
    path('accounts/', include('django.contrib.auth.urls')),
	# path("login/",login_view,name="login"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
