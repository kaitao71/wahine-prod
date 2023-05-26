from django.core.mail import send_mail
from django.shortcuts import render,redirect
from backend.forms import *
import uuid
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm #add this
from django.views.generic.edit import UpdateView
from django.db.models import Avg, Count, Min, Sum
import datetime
from django.apps import apps
from django.views.generic.edit import DeleteView, CreateView, UpdateView

from django.contrib.auth.decorators import login_required
# Create your views here.
## TODO
## IF data exist, show existing data/edit mode
## If fields can have multiple entry (eg policy), show no of policies
"""End V2 """

def logout_view(request):
    logout(request)
    return redirect('index')

def terms_of_service(request):
    return render(request,'backend/terms-of-service.html')

def return_refund_policy(request):
    return render(request,'backend/return-refund-policy.html')

def privacy_policy(request):
    return render(request,'backend/privacy-policy.html')

def contactus(request):
    return render(request,'backend/contact-us.html')

def index(request):
    ## Source of data (Database)
    items = Item.objects.filter(item_type="Notifier List") ## Get all notifier list from database
    for item in items: ## Loop
        print(item.data['notifier_event'])   ## Display item type

    return render(request,'backend/index.html')

def whoweare(request):
    return render(request,'backend/who-we-are.html')

def faq(request):
    return render(request,'backend/faq.html')

def joinnow(request):
    return render(request,'backend/joinnow.html')

def signup(request):
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('assets-bank-createform')
            messages.info(request, f"You can login now.")
            return redirect('login')
        else:
            print(form.errors)
            print(form.cleaned_data)
            return render(request,'backend/signup.html', {'form': form})
    form = SignUpForm()
    return render(request,'backend/signup.html', {'form': form})

def login_view(request):
    if request.POST:
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("dashboard-new")
            return redirect('dashboard-new')
        else:
            return render(request,'backend/login.html', {'form': form})
    form = AuthenticationForm()
    print(form)
    return render(request,'backend/login.html', {'form': form})

def selectplan(request):
    if request.POST:
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            plan = form.cleaned_data['plan']
            item = Subscription.objects.create(
                user=request.user,
                plan = plan)
            redirect('profile')
        else:
            return render(request,'backend/select-a-plan.html', {'form': form})
    form = SignUpForm()
    return render(request,'backend/select-a-plan.html', {'form': form})

def profile(request):
    return render(request,'backend/profile.html')

@login_required
def load_residential_type(request):
    property_type = request.GET.get('property_type')
    residential_types = ResidentialType.objects.filter(property_type__name=property_type).order_by('name')
    return render(request, 'backend/residential-type-dropdown-list.html', {'residential_types': residential_types})

@login_required
def assets_bank_modelform(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        print(post_data)
        formset = BankModelFormset(post_data)
        context = {'formset':formset}
        print(formset.errors)
        print(formset)

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-epf-createform')


        messages.error(request, "Please correct the errors in the form and try again.")
        print(formset.errors)
        return render(request,"backend/assets-bank-create.html",context)

    # we don't want to display the already saved model instances
    formset = BankModelFormset(queryset=Bank.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-bank-create.html",context)

@login_required
def assets_epf_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='EPF',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-socso-createform')
        post_data = request.POST.copy()
        post_data['user'] = request.user
        form = EpfForm(post_data)
        context = {'form':form}

        if form.is_valid():
            form.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-socso-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        print(form.errors)
        return render(request,"backend/assets-epf-create.html",context)

    # we don't want to display the already saved model instances
    form = EpfForm()
    context = {'form':form}
    return render(request,"backend/assets-epf-create.html",context)

@login_required
def assets_socso_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Socso',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-insurance-createform')
        post_data = request.POST.copy()
        post_data['user'] = request.user
        form = SocsoForm(post_data)
        context = {'form':form}

        if form.is_valid():
            form.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-insurance-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-socso-create.html",context)

    # we don't want to display the already saved model instances
    form = SocsoForm()
    context = {'form':form}
    return render(request,"backend/assets-socso-create.html",context)

@login_required
def assets_insurance_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Insurance',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-securities-investment-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = InsuranceModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-securities-investment-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-insurance-create.html",context)

    # we don't want to display the already saved model instances
    formset = InsuranceModelFormset(queryset=Insurance.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-insurance-create.html",context)

@login_required
def assets_investment_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Investment',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-property-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = InvestmentModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-property-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-investment-create.html",context)

    # we don't want to display the already saved model instances
    formset = InvestmentModelFormset(queryset=Investment.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-investment-create.html",context)

@login_required
def assets_securities_investment_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Investment',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-unittrust-investment-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = SecuritiesInvestmentModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-unittrust-investment-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-securities-investment-create.html",context)

    # we don't want to display the already saved model instances
    formset = SecuritiesInvestmentModelFormset(queryset=Investment.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-securities-investment-create.html",context)

@login_required
def assets_unittrust_investment_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Investment',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-property-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = UnitTrustInvestmentModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-property-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-unittrust-investment-create.html",context)

    # we don't want to display the already saved model instances
    formset = UnitTrustInvestmentModelFormset(queryset=Investment.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-unittrust-investment-create.html",context)

@login_required
def assets_property_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Property',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-vehicle-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = PropertyModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-vehicle-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        print(formset.errors)
        return render(request,"backend/assets-property-create.html",context)

    # we don't want to display the already saved model instances
    formset = PropertyModelFormset(queryset=Property.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-property-create.html",context)

@login_required
def assets_vehicle_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Vehicle',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-other-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = VehicleModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-other-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-vehicle-create.html",context)

    # we don't want to display the already saved model instances
    formset = VehicleModelFormset(queryset=Vehicle.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-vehicle-create.html",context)

@login_required
def assets_other_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Other Assets',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-crypto-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = OtherAssetModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-crypto-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-other-create.html",context)

    # we don't want to display the already saved model instances
    formset = OtherAssetModelFormset(queryset=OtherAsset.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-other-create.html",context)

@login_required
def assets_crypto_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Crypto Assets',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('assets-overview')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = CryptoModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-overview')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-crypto-create.html",context)

    # we don't want to display the already saved model instances
    formset = CryptoModelFormset(queryset=Crypto.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-crypto-create.html",context)

@login_required
def liabilities_creditcard_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Credit Card',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-personalloan-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = CreditCardModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-personalloan-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/liabilities-creditcard-create.html",context)

    # we don't want to display the already saved model instances
    formset = CreditCardModelFormset(queryset=CreditCard.objects.none())
    context = {'formset':formset}
    return render(request,"backend/liabilities-creditcard-create.html",context)

@login_required
def liabilities_personalloan_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Personal Loan',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-vehicleloan-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = PersonalLoanModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-vehicleloan-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/liabilities-vehicleloan-create.html",context)

    # we don't want to display the already saved model instances
    formset = PersonalLoanModelFormset(queryset=PersonalLoan.objects.none())
    context = {'formset':formset}
    return render(request,"backend/liabilities-personalloan-create.html",context)

@login_required
def liabilities_vehicleloan_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Vehicle Loan',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-propertyloan-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = VehicleLoanModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-propertyloan-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/liabilities-propertyloan-create.html",context)

    # we don't want to display the already saved model instances
    formset = VehicleLoanModelFormset(queryset=VehicleLoan.objects.none())
    context = {'formset':formset}
    return render(request,"backend/liabilities-vehicleloan-create.html",context)

@login_required
def liabilities_propertyloan_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Property Loan',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-other-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = PropertyLoanModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-other-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/liabilities-other-create.html",context)

    # we don't want to display the already saved model instances
    formset = PropertyLoanModelFormset(queryset=PropertyLoan.objects.none())
    context = {'formset':formset}
    return render(request,"backend/liabilities-propertyloan-create.html",context)

@login_required
def liabilities_other_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Other Liabilities',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-overview')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = OtherLiabilityModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-overview')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/liabilities-other-create.html",context)

    # we don't want to display the already saved model instances
    formset = OtherLiabilityModelFormset(queryset=OtherLiability.objects.none())
    context = {'formset':formset}
    return render(request,"backend/liabilities-other-create.html",context)
    
@login_required
def liabilities_overview(request):
    user = request.user
    items = Item.objects.filter(user=user)
    creditcard = CreditCard.objects.filter(user=user).last()
    personalloan = PersonalLoan.objects.filter(user=user).last()
    vehicleloan = VehicleLoan.objects.filter(user=user).last()
    propertyloan = PropertyLoan.objects.filter(user=user).last()
    others_liabilities = OtherLiability.objects.filter(user=user).last()
    context = {'items':items,'creditcard':creditcard,'personalloan':personalloan,'vehicleloan':vehicleloan,'propertyloan':propertyloan,'others_liabilities':others_liabilities}
    return render(request,'backend/liabilities-overview.html',context)

## Editing Assets ##
def assets_bank_editform(request,uuid):
    instance = Bank.objects.get(uuid=uuid)
    form = BankForm(request.POST or None,instance=instance)
    print(instance.account_type)
    account_type = instance.account_type
    bank_name = instance.bank_name
    account_no = instance.account_no
    account_value = instance.account_value
    item_type = 'Bank Account'
    if request.POST and form.is_valid():
        form.account_no = account_no
        form.account_value = account_value
        form.account_type = account_type
        form.bank_name = bank_name
        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'Bank data successfully updated.')
        return redirect('dashboard-new')

    context = {'instance':instance,'form':form,'account_value':account_value,'account_no':account_no,'bank_name':bank_name,'account_type':account_type}
    return render(request,'backend/edit-assets-1-bank.html',context)

def assets_epf_editform(request,uuid):
    instance = Epf.objects.get(uuid=uuid)
    form = EpfEditForm(request.POST or None,instance=instance)
    account_no = instance.account_no
    account_value = instance.account_value
    nominee_name = instance.nominee_name
    print(instance.user)
    form.user = instance.user
    item_type = 'EPF'
    form.user = request.user
    print(form.is_valid())
    print(form.errors)

    if request.POST and form.is_valid():
        form.account_no = account_no
        form.user = request.user
        form.account_value = account_value
        form.nominee_name = nominee_name
        form.item_type = "EPF"
        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'EPF data successfully updated.')
        return redirect('dashboard-new')

    context = {'instance':instance,'form':form,'account_value':account_value,'account_no':account_no,'nominee_name':nominee_name}
    return render(request,'backend/edit-assets-2-epf.html',context)

def assets_socso_editform(request,uuid):
    instance = Socso.objects.get(uuid=uuid)
    account_no = instance.account_no
    nominee_name = instance.nominee_name
    account_value = instance.account_value
    form = SocsoForm(request.POST or None,instance=instance)
    item_type = 'Socso'

    if request.POST and form.is_valid():
        form.account_no = account_no
        form.account_value = account_value
        form.nominee_name = nominee_name
        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'Socso data successfully updated.')
        return redirect('dashboard-new')

    context = {'instance':instance,'form':form,'account_value':account_value,'account_no':account_no,'nominee_name':nominee_name}
    return render(request,'backend/edit-assets-2-socso.html',context)

def assets_insurance_editform(request,uuid):
    instance = Insurance.objects.get(uuid=uuid)
    form = InsuranceForm(request.POST or None,instance=instance)    
    insurance_type = instance.insurance_type
    provider = instance.provider
    policy_no = instance.policy_no
    nominee_name = instance.nominee_name
    sum_insured = instance.sum_insured

    item_type = 'Insurance'

    print(form.errors)
    if request.POST and form.is_valid():
        form.insurance_type = insurance_type
        form.policy_no = policy_no
        form.provider = provider
        form.nominee_name = nominee_name
        form.sum_insured = sum_insured
        form.item_type = "Insurance"
        form.updated_at = datetime.datetime.now()
        form.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Insurance data successfully updated.')
        return redirect('dashboard-new')

    context = {'instance':instance,'form':form,'insurance_type':insurance_type,'provider':provider,'policy_no':policy_no,'nominee_name':nominee_name,'sum_insured':sum_insured}
    return render(request,'backend/edit-assets-3-insurance.html',context)

def assets_securityinvestment_editform(request,uuid):
    instance = SecuritiesInvestment.objects.get(uuid=uuid)
    form = SecuritiesInvestmentForm(request.POST or None, instance=instance)
    account_type = instance.account_type
    broker_name = instance.broker_name
    account_no = instance.account_no
    account_value = instance.account_value
    item_type = 'Investment'
    print(form.errors)

    if request.POST and form.is_valid():
        form.account_type = account_type
        form.broker_name = broker_name
        form.account_no = account_no
        form.account_value = account_value
        form.updated_at = datetime.datetime.now()
        instance.save()
        messages.add_message(request, messages.INFO, 'Investment data successfully updated.')
        return redirect('dashboard-new')
    context = {'instance':instance,'form':form,'account_type':account_type,'broker_name':broker_name,'account_no':account_no,'account_value':account_value}
    return render(request,'backend/edit-assets-4-securityinvestment.html',context)

def assets_unittrustinvestment_editform(request,uuid):
    instance = UnitTrustInvestment.objects.get(uuid=uuid)
    form = UnitTrustInvestmentForm(request.POST or None, instance=instance)
    unittrust_name = instance.unittrust_name
    account_no = instance.account_no
    agent_name  = instance.agent_name
    agent_contact_no = instance.agent_contact_no
    account_value = instance.account_value
    item_type = 'Investment'

    if request.POST and form.is_valid():
        form.unittrust_name = unittrust_name
        form.account_no = account_no
        form.account_value = account_value
        form.agent_name = agent_name
        form.agent_contact_no = agent_contact_no
        form.updated_at = datetime.datetime.now()
        instance.save()
        messages.add_message(request, messages.INFO, 'Investment data successfully updated.')
        return redirect('dashboard-new')
    context = {'instance':instance,'form':form,'unittrust_name':unittrust_name,'agent_name':agent_name,'agent_contact_no':agent_contact_no,'account_no':account_no,'account_value':account_value}
    return render(request,'backend/edit-assets-4-unittrustinvestment.html',context)

def assets_property_editform(request,uuid):
    instance = Property.objects.get(uuid=uuid)
    form = PropertyForm(request.POST or None, instance=instance)
    property_type = instance.property_type
    residential_type = instance.residential_type
    address = instance.address
    spa_price = instance.spa_price
    state = instance.state
    postcode = instance.postcode
    titleno = instance.titleno
    item_type = 'Property'
    print(form.errors)
    if request.POST and form.is_valid():
        form.property_type = property_type
        form.residential_type = residential_type
        form.address = address
        form.state = state
        form.postcode = postcode
        form.titleno = titleno
        form.updated_at = datetime.datetime.now()
        form.spa_price = spa_price
        form.save()
        messages.add_message(request, messages.INFO, 'Property data successfully updated.')
        return redirect('dashboard-new')

    context = {'instance':instance,'form':form,'property_type':property_type,'residential_type':residential_type,'address':address,'state':state,'postcode':postcode,'titleno':titleno,'spa_price':spa_price}
    return render(request,'backend/edit-assets-5-property.html',context)

def assets_vehicle_editform(request,uuid):
    instance = Vehicle.objects.get(uuid=uuid)
    form = VehicleForm(request.POST or None, instance=instance)
    vehicle_type = instance.vehicle_type
    make_model = instance.make_model
    registration_no = instance.registration_no
    item_type = 'Vehicle'
    print(form.errors)
    if request.POST and form.is_valid():
        form.vehicle_type = vehicle_type
        form.make_model = make_model
        form.registration_no = registration_no
        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'Vehicle data successfully updated.')
        return redirect('dashboard-new')

    context = {'instance':instance,'form':form,'vehicle_type':vehicle_type,'make_model':make_model,'registration_no':registration_no}
    return render(request,'backend/edit-assets-6-vehicle.html',context)

def assets_other_editform(request,uuid):
    instance = OtherAsset.objects.get(uuid=uuid)
    form = OtherAssetForm(request.POST or None, instance=instance)
    name = instance.name
    value = instance.value
    item_type = 'Other Assets'
    print(form.errors)
    if request.POST and form.is_valid():
        form.name = name
        form.value = value
        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'Other assets data successfully updated.')
        return redirect('dashboard-new')

    context = {'instance':instance,'form':form,'name':name,'value':value}
    return render(request,'backend/edit-assets-7-others.html',context)

def assets_crypto_editform(request,uuid):
    instance = Crypto.objects.get(uuid=uuid)
    form = CryptoForm(request.POST or None, instance=instance)
    crypto_type = instance.crypto_type
    wallet_name = instance.wallet_name
    value = instance.value
    item_type = 'Other Assets'
    print(form.errors)
    if request.POST and form.is_valid():
        form.crypto_type = crypto_type
        form.wallet_name = wallet_name
        form.value = value
        form.updated_at = datetime.datetime.now()
        form.save()
        messages.add_message(request, messages.INFO, 'Other assets data successfully updated.')
        return redirect('dashboard-new')

    context = {'instance':instance,'form':form,'crypto_type':crypto_type,'wallet_name':wallet_name,'value':value}
    return render(request,'backend/edit-assets-8-crypto.html',context)

## Editing Assets End ##
def liabilities_creditcard_editform(request,uuid):
    instance = CreditCard.objects.get(uuid=uuid)
    form = CreditCardForm(request.POST or None, instance=instance)
    account_no = instance.account_no
    bank_name = instance.bank_name
    amount_outstanding = instance.amount_outstanding
    item_type = 'Credit Card'
    print(form.errors)

    if request.POST and form.is_valid():
        form.bank_name = bank_name
        form.amount_outstanding = amount_outstanding
        form.account_no = account_no
        form.item_type = "Credit Card"
        form.updated_at = datetime.datetime.now()
        form.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Credit card data successfully updated.')
        return redirect('dashboard-new')
    context = {'instance':instance,'form':form,'amount_outstanding':amount_outstanding,'bank_name':bank_name,'account_no':account_no}
    return render(request,'backend/edit-liabilities-1-credit-card.html',context)

def liabilities_personalloan_editform(request,uuid):
    instance = PersonalLoan.objects.get(uuid=uuid)
    form = PersonalLoanForm(request.POST or None, instance=instance)
    account_no = instance.account_no
    amount_outstanding = instance.amount_outstanding
    loan_tenure = instance.loan_tenure
    bank_name = instance.bank_name
    item_type = 'Personal Loan'

    if request.POST and form.is_valid():
        form.bank_name = bank_name
        form.loan_tenure = loan_tenure
        form.amount_outstanding = amount_outstanding
        form.account_no = account_no
        form.updated_at = datetime.datetime.now()
        form.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Personal loan data successfully updated.')
        return redirect('dashboard-new')
    context = {'instance':instance,'form':form,'loan_tenure':loan_tenure,'amount_outstanding':amount_outstanding,'bank_name':bank_name,'account_no':account_no}
    return render(request,'backend/edit-liabilities-2-personal-loan.html',context)

def liabilities_vehicleloan_editform(request,uuid):
    instance = VehicleLoan.objects.get(uuid=uuid)
    form = VehicleLoanForm(request.POST or None, instance=instance)
    account_no = instance.account_no
    amount_outstanding = instance.amount_outstanding
    loan_tenure = instance.loan_tenure
    bank_name = instance.bank_name
    item_type = 'Vehicle Loan'

    if request.POST and form.is_valid():
        form.bank_name = bank_name
        form.loan_tenure = loan_tenure
        form.amount_outstanding = amount_outstanding
        form.account_no = account_no
        form.updated_at = datetime.datetime.now()
        form.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Vehicle loan data successfully updated.')
        return redirect('dashboard-new')
    context = {'form':form,'loan_tenure':loan_tenure,'amount_outstanding':amount_outstanding,'bank_name':bank_name,'account_no':account_no}
    return render(request,'backend/edit-liabilities-3-vehicle-loan.html',context)

def liabilities_propertyloan_editform(request,uuid):
    instance = PropertyLoan.objects.get(uuid=uuid)
    form = PropertyLoanForm(request.POST or None, instance=instance)
    account_no = instance.account_no
    amount_outstanding = instance.amount_outstanding
    loan_tenure = instance.loan_tenure
    bank_name = instance.bank_name
    item_type = 'Property Loan'

    if request.POST and form.is_valid():
        form.bank_name = bank_name
        form.loan_tenure = loan_tenure
        form.amount_outstanding = amount_outstanding
        form.account_no = account_no
        instance.data['item_type'] = "Vehicle Loan"
        form.updated_at = datetime.datetime.now()
        form.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Property loan data successfully updated.')
        return redirect('dashboard-new')
    context = {'form':form,'loan_tenure':loan_tenure,'amount_outstanding':amount_outstanding,'bank_name':bank_name,'account_no':account_no}
    return render(request,'backend/edit-liabilities-4-property-loan.html',context)

def liabilities_other_editform(request,uuid):
    instance = OtherLiability.objects.get(uuid=uuid)
    form = OtherLiabilityForm(request.POST or None, instance=instance)
    liability_name = instance.name
    liability_value = instance.value
    item_type = 'Other Liabilities'

    if request.POST and form.is_valid():
        form.name = liability_name
        form.value = liability_value
        form.updated_at = datetime.datetime.now()
        form.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Other liabilities data successfully updated.')
        return redirect('dashboard-new')

    context = {'instance':instance,'form':form,'liability_name':liability_name,'liability_value':liability_value}
    return render(request,'backend/edit-liabilities-5-others.html',context)

def notifier_list_form(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Notifier List',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('access_list_form')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = NotifierModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            for i in formset: 
                email = i.cleaned_data.get('email')
                triggers = i.cleaned_data.get('event')[1:-1].replace("'","")
                send_mail(
                    "Wahine - You have been added as a notifier",
                    "You have been added as a notifier by " + str(request.user.last_name) + " with the trigger events of " + triggers +". Please contact us at hellowahine if any of these trigger events happens",
                    "wahine@wcapital.asia",
                    [email],
                    fail_silently=False,
                    )
            messages.success(request, "Saved successfully.")
            return redirect('access_list_form')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/notifier-list-form.html",context)

    # we don't want to display the already saved model instances
    formset = NotifierModelFormset(queryset=Notifier.objects.none())
    context = {'formset':formset}
    return render(request,"backend/notifier-list-form.html",context)

def access_list_form(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get_or_create(user=request.user,data={'nodata':True},item_type='Access List',created_by=request.user)
            messages.success(request, "Saved successfully.")
            return redirect('dashboard-new')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = NotifierModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('dashboard-new')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/access-list-form.html",context)

    # we don't want to display the already saved model instances
    formset = NotifierModelFormset(queryset=Notifier.objects.none())
    context = {'formset':formset}
    return render(request,"backend/access-list-form.html",context)

def assets_overview(request):
    user = request.user
    banks = Bank.objects.filter(user=user).last()
    epf = Epf.objects.filter(user=user).last()
    socso = Socso.objects.filter(user=user).last()
    insurances = Insurance.objects.filter(user=user).last()
    
    investments = SecuritiesInvestment.objects.filter(user=user).last()
    investments = UnitTrustInvestment.objects.filter(user=user).last()
    properties = Property.objects.filter(user=user).last()
    vehicles = Vehicle.objects.filter(user=user).last()
    others = OtherAsset.objects.filter(user=user).last()
    cryptos = Crypto.objects.filter(user=user).last()
    context = {'banks':banks,'epf':epf,'socso':socso,'investments':investments,'insurances':insurances,'vehicles':vehicles,'properties':properties,'others':others,'cryptos':cryptos}
    return render(request,'backend/assets-overview.html',context)

def dashboard_new(request):
    user = request.user
    items = Item.objects.filter(user=user)
    banks = Bank.objects.filter(user=user)
    if banks.count() == 0:
        return redirect('assets-bank-createform')
    bank_total = 0
    bank_values = banks.values('account_value')
    for x in bank_values:
        if x['account_value'] == "" or x['account_value'] is None:
            bank_total = bank_total
        else:
            bank_total += float(x['account_value'])

    insurances = Insurance.objects.filter(user=user)
    insurance_total = 0
    insurance_values = insurances.values('sum_insured')
    for x in insurance_values:
        if x['sum_insured'] == "" or x['sum_insured'] is None:
            insurance_total = insurance_total
        else:
            insurance_total += float(x['sum_insured'])

    security_investments = SecuritiesInvestment.objects.filter(user=user)
    unittrust_investments = UnitTrustInvestment.objects.filter(user=user)
    investment_total = 0
    security_investment_values = security_investments.values('account_value')
    unittrust_investment_values = unittrust_investments.values('account_value')
    for x in security_investment_values:
        if x['account_value'] == "" or x['account_value'] is None:
            investment_total = investment_total
        else:
            investment_total += float(x['account_value'])
    for x in unittrust_investment_values:
        if x['account_value'] == "" or x['account_value'] is None:
            investment_total = investment_total
        else:
            investment_total += float(x['account_value'])

    epf = Epf.objects.filter(user=user)
    epf_total = 0
    epf_values = epf.values('account_value')
    for x in epf_values:
        if x['account_value'] == "" or x['account_value'] is None:
            epf_total = epf_total
        else:
            epf_total += float(x['account_value'])

    socso = Socso.objects.filter(user=user)
    socso_total = 0
    socso_values = socso.values('account_value')
    for x in socso_values:
        if x['account_value'] == "" or x['account_value'] is None:
            socso_total = socso_total
        else:
            socso_total += float(x['account_value'])
    
    vehicles = Vehicle.objects.filter(user=user)
    # vehicles_total = 0
    # vehicles_values = vehicles.values('spa_price')
    # for x in vehicles_values:
    #     if x['spa_price'] == "" or x['spa_price'] is None:
    #         vehicles_total = vehicles_total
    #     else:
    #         vehicles_total += float(x['spa_price'])

    properties = Property.objects.filter(user=user)
    properties_total = 0
    properties_values = properties.values('spa_price')
    for x in properties_values:
        if x['spa_price'] == "" or x['spa_price'] is None:
            properties_total = properties_total
        else:
            properties_total += float(x['spa_price'])

    cryptos = Crypto.objects.filter(user=user)
    crypto_total = 0
    crypto_values = cryptos.values('value')
    for x in crypto_values:
        if x['value'] == "" or x['value'] is None:
            crypto_total = crypto_total
        else:
            crypto_total += float(x['value'])

    other_assets = OtherAsset.objects.filter(user=user)
    other_asset_total = 0
    asset_values = other_assets.values('value')
    for x in asset_values:
        if x['value'] == "" or x['value'] is None:
            other_asset_total = other_asset_total
        else:
            other_asset_total += float(x['value'])

    creditcard = CreditCard.objects.filter(user=user)
    creditcard_total = 0
    creditcard_values = creditcard.values('amount_outstanding')
    for x in creditcard_values:
        if x['amount_outstanding'] == "" or x['amount_outstanding'] is None:
            creditcard_total = creditcard_total
        else:
            creditcard_total += float(x['amount_outstanding'])

    personalloan = PersonalLoan.objects.filter(user=user)
    personalloan_total = 0
    personalloan_values = personalloan.values('amount_outstanding')
    for x in personalloan_values:
        if x['amount_outstanding'] == "" or x['amount_outstanding'] is None:
            personalloan_total = personalloan_total
        else:
            personalloan_total += float(x['amount_outstanding'])

    vehicleloan = VehicleLoan.objects.filter(user=user)
    vehicleloan_total = 0
    vehicleloan_values = vehicleloan.values('amount_outstanding')
    for x in vehicleloan_values:
        if x['amount_outstanding'] == "" or x['amount_outstanding'] is None:
            vehicleloan_total = vehicleloan_total
        else:
            vehicleloan_total += float(x['amount_outstanding'])

    propertyloan = PropertyLoan.objects.filter(user=user)
    propertyloan_total = 0
    propertyloan_values = propertyloan.values('amount_outstanding')
    for x in propertyloan_values:
        if x['amount_outstanding'] == "" or x['amount_outstanding'] is None:
            propertyloan_total = propertyloan_total
        else:
            propertyloan_total += float(x['amount_outstanding'])

    other_liabilities = OtherLiability.objects.filter(user=user)
    other_liabilities_total = 0
    liabilities_values = other_liabilities.values('value')
    for x in liabilities_values:
        if x['value'] == "" or x['value'] is None:
            other_liabilities_total = other_liabilities_total
        other_liabilities_total += float(x['value'])

    context = {'bank_total':bank_total,
                'banks':banks,
                'epf':epf,
                'socso':socso,
                'epf_total':epf_total,
                'socso_total':socso_total,
                'insurance_total':insurance_total,
                'insurances':insurances,
                'security_investments':security_investments,
                'unittrust_investments':unittrust_investments,
                'investment_total':investment_total,
                'properties':properties,
                'properties_total':properties_total,
                'vehicles':vehicles,
                # 'vehicles_total':vehicles_total,
                'cryptos':cryptos,
                'crypto_total':crypto_total,
                'other_assets':other_assets,
                'other_asset_total':other_asset_total,
                'creditcard':creditcard,
                'creditcard_total':creditcard_total,
                'personalloan':personalloan,
                'personalloan_total':personalloan_total,
                'vehicleloan':vehicleloan,
                'vehicleloan_total':vehicleloan_total,
                'propertyloan':propertyloan,
                'propertyloan_total':propertyloan_total,
                'other_liabilities':other_liabilities,
                'other_liabilities_total':other_liabilities_total
                }
    return render(request,'backend/dashboard-new.html',context)

class assets_bank_deleteform(DeleteView):
    model = Bank
    context_object_name = 'bank'
    success_url = '/dashboard-new'

    def get_object(self, queryset=None):
        return Bank.objects.get(uuid=self.kwargs.get("uuid"))
    
    def form_valid(self, form):
        messages.success(self.request, "The item was deleted successfully.")
        return super(assets_bank_deleteform,self).form_valid(form)

class assets_insurance_deleteform(DeleteView):
    model = Insurance
    context_object_name = 'insurance'
    success_url = '/dashboard-new'

    def get_object(self, queryset=None):
        return Insurance.objects.get(uuid=self.kwargs.get("uuid"))
    
    def form_valid(self, form):
        messages.success(self.request, "The item was deleted successfully.")
        return super(assets_insurance_deleteform,self).form_valid(form)

class assets_securityinvestment_deleteform(DeleteView):
    model = SecuritiesInvestment
    context_object_name = 'securityinvestment'
    success_url = '/dashboard-new'

    def get_object(self, queryset=None):
        return SecuritiesInvestment.objects.get(uuid=self.kwargs.get("uuid"))
    
    def form_valid(self, form):
        messages.success(self.request, "The item was deleted successfully.")
        return super(assets_securityinvestment_deleteform,self).form_valid(form)

class assets_unittrustinvestment_deleteform(DeleteView):
    model = UnitTrustInvestment
    context_object_name = 'unittrustinvestment'
    success_url = '/dashboard-new'

    def get_object(self, queryset=None):
        return UnitTrustInvestment.objects.get(uuid=self.kwargs.get("uuid"))
    
    def form_valid(self, form):
        messages.success(self.request, "The item was deleted successfully.")
        return super(assets_unittrustinvestment_deleteform,self).form_valid(form)

class assets_property_deleteform(DeleteView):
    model = Property
    context_object_name = 'property'
    success_url = '/dashboard-new'

    def get_object(self, queryset=None):
        return Property.objects.get(uuid=self.kwargs.get("uuid"))
    
    def form_valid(self, form):
        messages.success(self.request, "The item was deleted successfully.")
        return super(assets_property_deleteform,self).form_valid(form)

class assets_vehicle_deleteform(DeleteView):
    model = Vehicle
    context_object_name = 'vehicle'
    success_url = '/dashboard-new'

    def get_object(self, queryset=None):
        return Vehicle.objects.get(uuid=self.kwargs.get("uuid"))
    
    def form_valid(self, form):
        messages.success(self.request, "The item was deleted successfully.")
        return super(assets_vehicle_deleteform,self).form_valid(form)

class assets_other_deleteform(DeleteView):
    model = OtherAsset
    context_object_name = 'otherasset'
    success_url = '/dashboard-new'

    def get_object(self, queryset=None):
        return OtherAsset.objects.get(uuid=self.kwargs.get("uuid"))
    
    def form_valid(self, form):
        messages.success(self.request, "The item was deleted successfully.")
        return super(assets_other_deleteform,self).form_valid(form)

class assets_crypto_deleteform(DeleteView):
    model = Crypto
    context_object_name = 'crypto'
    success_url = '/dashboard-new'

    def get_object(self, queryset=None):
        return Crypto.objects.get(uuid=self.kwargs.get("uuid"))
    
    def form_valid(self, form):
        messages.success(self.request, "The item was deleted successfully.")
        return super(assets_crypto_deleteform,self).form_valid(form)