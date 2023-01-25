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
# Create your views here.
## TODO
## IF data exist, show existing data/edit mode
## If fields can have multiple entry (eg policy), show no of policies
def load_residential_type(request):
    country_id = request.GET.get('property_type')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'backend/residential_type_dropdown_list_options.html', {'cities': cities})

def assets_bank_modelform(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = BankModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-epf-createform')


        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-bank-create.html",context)

    # we don't want to display the already saved model instances
    formset = BankModelFormset(queryset=Bank.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-bank-create.html",context)

def assets_epf_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='EPF',created_by=request.user)
            if item:
                return redirect('assets-socso-createform')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='EPF',created_by=request.user)
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
        return render(request,"backend/assets-epf-create.html",context)

    # we don't want to display the already saved model instances
    form = EpfForm()
    context = {'form':form}
    return render(request,"backend/assets-epf-create.html",context)

def assets_socso_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get(user=request.user,data={'nodata':True},item_type='Socso',created_by=request.user)
            if item:
                return redirect('assets-insurance-createform')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Socso',created_by=request.user)
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

def assets_insurance_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get(user=request.user,data={'nodata':True},item_type='Insurance',created_by=request.user)
            if item:
                return redirect('assets-investment-createform')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Insurance',created_by=request.user)
            return redirect('assets-investment-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = InsuranceModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-investment-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-insurance-create.html",context)

    # we don't want to display the already saved model instances
    formset = InsuranceModelFormset(queryset=Insurance.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-insurance-create.html",context)

def assets_investment_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get(user=request.user,data={'nodata':True},item_type='Investment',created_by=request.user)
            if item:
                return redirect('assets-property-createform')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Investment',created_by=request.user)
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

def assets_property_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get(user=request.user,data={'nodata':True},item_type='Property',created_by=request.user)
            if item:
                return redirect('assets-vehicle-createform')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Property',created_by=request.user)
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
        return render(request,"backend/assets-property-create.html",context)

    # we don't want to display the already saved model instances
    formset = PropertyModelFormset(queryset=Property.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-property-create.html",context)

def assets_vehicle_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get(user=request.user,data={'nodata':True},item_type='Vehicle',created_by=request.user)
            if item:
                return redirect('assets-other-createform')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Vehicle',created_by=request.user)
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

def assets_other_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get(user=request.user,data={'nodata':True},item_type='Other Assets',created_by=request.user)
            if item:
                return redirect('assets-other-createform')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Other Assets',created_by=request.user)
            return redirect('assets-other-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = OtherAssetModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('assets-other-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/assets-other-create.html",context)

    # we don't want to display the already saved model instances
    formset = OtherAssetModelFormset(queryset=OtherAsset.objects.none())
    context = {'formset':formset}
    return render(request,"backend/assets-other-create.html",context)

def liabilities_creditcard_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get(user=request.user,data={'nodata':True},item_type='Credit Card',created_by=request.user)
            if item:
                return redirect('liabilities-personalloan-createform')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Credit Card',created_by=request.user)
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

def liabilities_personalloan_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get(user=request.user,data={'nodata':True},item_type='Personal Loan',created_by=request.user)
            if item:
                return redirect('liabilities-vehicleloan-createform')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Personal Loan',created_by=request.user)
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

def liabilities_vehicleloan_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get(user=request.user,data={'nodata':True},item_type='Vehicle Loan',created_by=request.user)
            if item:
                return redirect('liabilities-propertyloan-createform')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Vehicle Loan',created_by=request.user)
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

def liabilities_propertyloan_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get(user=request.user,data={'nodata':True},item_type='Property Loan',created_by=request.user)
            if item:
                return redirect('liabilities-other-createform')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Property Loan',created_by=request.user)
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

def liabilities_other_modelform(request):
    if request.method == 'POST':
        if 'skip' in request.POST:
            item = Item.objects.get(user=request.user,data={'nodata':True},item_type='Other Liabilities',created_by=request.user)
            if item:
                return redirect('liabilities-other-createform')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Other Liabilities',created_by=request.user)
            return redirect('liabilities-other-createform')
        post_data = request.POST.copy()
        for i in range(int(post_data['form-TOTAL_FORMS'])):
            post_data['form-%d-user' % i] = request.user
        formset = OtherLiabilityModelFormset(post_data)
        context = {'formset':formset}

        if formset.is_valid():
            formset.save()
            messages.success(request, "Saved successfully.")
            return redirect('liabilities-other-createform')

        messages.error(request, "Please correct the errors in the form and try again.")
        return render(request,"backend/liabilities-other-create.html",context)

    # we don't want to display the already saved model instances
    formset = OtherLiabilityModelFormset(queryset=OtherLiability.objects.none())
    context = {'formset':formset}
    return render(request,"backend/liabilities-other-create.html",context)

def assets_overview_v2(request):
    user = request.user
    """ Check if user skipped form"""
    items = Item.objects.filter(user=user)
    banks = items.filter(item_type='Bank Account').last()
    epf_socso = items.filter(item_type='EPF Socso').last()
    insurances = items.filter(item_type='Insurance').last()
    investments = items.filter(item_type='Investment').last()
    properties = items.filter(item_type='Property').last()
    vehicles = items.filter(item_type='Vehicle').last()
    others = items.filter(item_type='Other Assets').last()
    """ Check if user skipped form"""



    context = {'items':items,'banks':banks,'epf_socso':epf_socso,'insurances':insurances,'investments':investments,'vehicles':vehicles,'properties':properties,'others':others}
    return render(request,'backend/assets-overview.html',context)

class ItemUpdateView(UpdateView):
    model = Item
    fields = ['data']
    template_name_suffix = '_update_form'

def liabilities_overview_v2(request):
    user = request.user
    items = Item.objects.filter(user=user)
    creditcard = items.filter(item_type='Credit Card').last()
    personalloan = items.filter(item_type='Personal Loan').last()
    vehicleloan = items.filter(item_type='Vehicle Loan').last()
    propertyloan = items.filter(item_type='Property Loan').last()
    others_liabilities = items.filter(item_type='Other Liabilities').last()
    context = {'items':items,'creditcard':creditcard,'personalloan':personalloan,'vehicleloan':vehicleloan,'propertyloan':propertyloan,'others_liabilities':others_liabilities}
    return render(request,'backend/liabilities-overview.html',context)

"""End V2 """

def formset_testview(request):
    BankFormSet = modelformset_factory(BankForm,extra=5)
    formset = BankFormSet()
    context = {'formset':formset}
    return render(request,"backend/formset.html",context)


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
                return redirect("bank_account_form")
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
                return redirect("dashboard")
            return redirect('dashboard')
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

def bank_account_form(request):
    form = BankAccountForm()
    # formset = formset_factory(form)
    if request.POST:
        form = BankAccountForm(request.POST)
        # formset = formset_factory(form)
        if form.is_valid():
            account_type = form.cleaned_data['account_type']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            account_value = form.cleaned_data['account_value']
            account_type_2 = form.cleaned_data['account_type_2']
            bank_name_2 = form.cleaned_data['bank_name_2']
            account_no_2 = form.cleaned_data['account_no_2']
            account_value_2 = form.cleaned_data['account_value_2']

            item = Item.objects.create(
                user=request.user,
                data={'account_type':account_type,
                    'bank_name':bank_name,
                    'account_no':account_no,
                    'account_value':account_value},
                item_type='Bank Account',
                created_by=request.user
                )
            messages.add_message(request, messages.INFO, 'Bank data successfully updated.')

            if bank_name_2 and account_no_2:
                item = Item.objects.create(
                user=request.user,
                data={'account_type':account_type_2,
                    'bank_name':bank_name_2,
                    'account_no':account_no_2,
                    'account_value':account_value_2},
                item_type='Bank Account',
                created_by=request.user
                )
                messages.add_message(request, messages.INFO, 'Bank data successfully updated.')
            return redirect('epf_socso_form')
        else:
            context = {'form':form}
            return render(request,'backend/assets-1-bank.html',context)
    context = {'form':form}
    return render(request,'backend/assets-1-bank.html',context)

def edit_bank_account_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    account_type = instance.data['account_type']
    bank_name = instance.data['bank_name']
    account_no = instance.data['account_no']
    account_value = instance.data['account_value']
    item_type = 'Bank Account'

    form = EditItemModelForm(request.POST,instance=instance,initial={'item_type':item_type,
        'account_value':account_value,
        'account_type':account_type,
        'bank_name':bank_name,
        'account_no':account_no
        }
        )

    if request.POST:
        instance.data['account_no'] = form.data['account_no']
        instance.data['account_value'] = form.data['account_value']
        instance.data['account_type'] = form.data['account_type']
        instance.data['bank_name'] = form.data['bank_name']
        instance.data['item_type'] = "Bank Account"
        instance.updated_at = datetime.datetime.now()

        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Bank data successfully updated.')
        return redirect('dashboard')

    context = {'form':form,'account_value':account_value,'account_no':account_no,'bank_name':bank_name,'account_type':account_type}
    return render(request,'backend/edit-assets-1-bank.html',context)

def epf_socso_form(request):
    form = EpfSocsoForm()
    if request.POST:
        form = EpfSocsoForm(request.POST)
        if form.data['yesno'] == 'no':
            messages.add_message(request, messages.INFO, 'No data added.')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='EPF Socso',created_by=request.user)
            return redirect('insurance_form')
        if form.data['is_socso_member'] == 'no':
            # remember old state
            _mutable = form.data._mutable

            # set to mutable
            form.data._mutable = True

            # сhange the values you want
            form.data['socso_member_no'] = 'n/a'
            # set mutable flag back
            form.data._mutable = _mutable
            if form.is_valid():
                is_epf_member = form.cleaned_data['is_epf_member']
                epf_member_no = form.cleaned_data['epf_member_no']
                epf_nominee_name = form.cleaned_data['epf_nominee_name']
                is_socso_member = form.cleaned_data['is_socso_member']
                socso_member_no = form.cleaned_data['socso_member_no']
                epf_account_value = form.cleaned_data['epf_account_value']
                item = Item.objects.create(
                user=request.user,
                data={'is_epf_member':is_epf_member,
                    'is_socso_member':is_socso_member,
                    'epf_member_no':epf_member_no,
                    'socso_member_no':socso_member_no,
                    'epf_nominee_name':epf_nominee_name,
                    'epf_account_value':epf_account_value,
                }  ,
                item_type='EPF Socso',
                created_by=request.user
                )
                messages.add_message(request, messages.INFO, 'EPF/Socso successfully updated.')
                return redirect('insurance_form')
        if form.is_valid():
            is_epf_member = form.cleaned_data['is_epf_member']
            epf_member_no = form.cleaned_data['epf_member_no']
            epf_nominee_name = form.cleaned_data['epf_nominee_name']
            is_socso_member = form.cleaned_data['is_socso_member']
            socso_member_no = form.cleaned_data['socso_member_no']
            epf_account_value = form.cleaned_data['epf_account_value']
            item = Item.objects.create(
                user=request.user,
                data={'is_epf_member':is_epf_member,
                    'is_socso_member':is_socso_member,
                    'epf_member_no':epf_member_no,
                    'socso_member_no':socso_member_no,
                    'epf_nominee_name':epf_nominee_name,
                    'epf_account_value':epf_account_value,
                }  ,
                item_type='EPF Socso',
                created_by=request.user
                )
            messages.add_message(request, messages.INFO, 'EPF/Socso successfully updated.')
            return redirect('insurance_form')
        else:
            print(form.errors)
            context = {'form':form}
            return render(request,'backend/assets-2-epf.html',context)
    context = {'form':form}
    return render(request,'backend/assets-2-epf.html',context)

def edit_epf_socso_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    epf_member_no = instance.data['epf_member_no']
    epf_nominee_name = instance.data['epf_nominee_name']
    socso_member_no = instance.data['socso_member_no']
    epf_account_value = instance.data['epf_account_value']
    item_type = 'EPF Socso'

    form = EditItemModelForm(request.POST,instance=instance,initial={'item_type':item_type,
        'epf_member_no':epf_member_no,
        'epf_nominee_name':epf_nominee_name,
        'socso_member_no':socso_member_no,
        'epf_account_value':epf_account_value
        }
        )

    if request.POST:
        instance.data['epf_member_no'] = form.data['epf_member_no']
        instance.data['epf_nominee_name'] = form.data['epf_nominee_name']
        instance.data['socso_member_no'] = form.data['socso_member_no']
        instance.data['epf_account_value'] = form.data['epf_account_value']
        instance.data['item_type'] = "EPF/Socso"
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'EPF/Socso data successfully updated.')
        return redirect('dashboard')

    context = {'form':form,'epf_member_no':epf_member_no,'epf_nominee_name':epf_nominee_name,'socso_member_no':socso_member_no,'epf_account_value':epf_account_value}
    return render(request,'backend/edit-assets-2-epf.html',context)

def insurance_form(request):
    form = InsuranceForm()
    form2 = InsuranceForm()
    # insuranceformset = formset_factory(InsuranceForm,extra=4)
    # formset = insuranceformset()
    if request.POST:
        form = InsuranceForm(request.POST)
        if form.data['yesno'] == 'no':
            messages.add_message(request, messages.INFO, 'No Insurance Added.')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Insurance',created_by=request.user)
            return redirect('investment_form')
        if form.is_valid():
            insurance_type = form.cleaned_data['insurance_type']
            policy_no = form.cleaned_data['policy_no']
            nominee_name = form.cleaned_data['nominee_name']
            sum_insured = form.cleaned_data['sum_insured']
            provider_name = form.cleaned_data['provider_name']
            item = Item.objects.create(user=request.user,data={'provider_name':provider_name,'insurance_type':insurance_type,'policy_no':policy_no,'nominee_name':nominee_name,'sum_insured':sum_insured},item_type='Insurance',created_by=request.user)
            insurance_type_2 = form.cleaned_data['insurance_type_2']
            policy_no_2 = form.cleaned_data['policy_no_2']
            nominee_name_2 = form.cleaned_data['nominee_name_2']
            provider_name_2 = form.cleaned_data['provider_name_2']
            sum_insured_2 = form.cleaned_data['sum_insured_2']
            if insurance_type_2 and policy_no_2:
                item2 = Item.objects.create(user=request.user,data={'insurance_type':insurance_type_2,'policy_no':policy_no_2,'nominee_name':nominee_name_2,'sum_insured':sum_insured_2},item_type='Insurance',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Insurance data successfully added.')
            messages.add_message(request, messages.INFO, 'Insurance data successfully added.')
            return redirect('investment_form')
        else:
            messages.add_message(request, messages.INFO, 'Something went wrong, please make sure all fields are entered correctly')
            return redirect('insurance_form')

    context = {'form':form}
    return render(request,'backend/assets-3-insurance.html',context)

def edit_insurance_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    insurance_type = instance.data['insurance_type']
    provider_name = instance.data['provider_name']
    policy_no = instance.data['policy_no']
    nominee_name = instance.data['nominee_name']
    sum_insured = instance.data['sum_insured']
    item_type = 'Insurance'

    form = EditItemModelForm(request.POST,instance=instance,initial={'item_type':item_type,
        'insurance_type':insurance_type,
        'provider_name':provider_name,
        'policy_no':policy_no,
        'nominee_name':nominee_name,
        'sum_insured':sum_insured
        }
        )

    if request.POST:
        instance.data['insurance_type'] = form.data['insurance_type']
        instance.data['policy_no'] = form.data['policy_no']
        instance.data['provider_name'] = form.data['provider_name']
        instance.data['nominee_name'] = form.data['nominee_name']
        instance.data['sum_insured'] = form.data['sum_insured']
        instance.data['item_type'] = "Insurance"
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Insurance data successfully updated.')
        return redirect('dashboard')

    context = {'form':form,'insurance_type':insurance_type,'provider_name':provider_name,'policy_no':policy_no,'nominee_name':nominee_name,'sum_insured':sum_insured}
    return render(request,'backend/edit-assets-3-insurance.html',context)

def investment_form(request):
    form = InvestmentForm()
    if request.POST:
        form = InvestmentForm(request.POST)
        if form.data['yesno'] == 'no':
            messages.add_message(request, messages.INFO, 'No Investments Added.')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Investment',created_by=request.user)
            return redirect('property_form')
        if form.is_valid():
            investment_type = form.cleaned_data['investment_type']
            account_no = form.cleaned_data['account_no']
            fund_name = form.cleaned_data['fund_name']
            account_value = form.cleaned_data['account_value']
            investment_type_2 = form.cleaned_data['investment_type_2']
            account_no_2 = form.cleaned_data['account_no_2']
            fund_name_2 = form.cleaned_data['fund_name_2']
            account_value_2 = form.cleaned_data['account_value_2']
            investment_type_3 = form.cleaned_data['investment_type_3']
            account_no_3 = form.cleaned_data['account_no_3']
            fund_name_3 = form.cleaned_data['fund_name_3']
            account_value_3 = form.cleaned_data['account_value_3']
            item = Item.objects.create(user=request.user,data={'investment_type':investment_type,'account_no':account_no,'fund_name':fund_name,'account_value':account_value},item_type='Investment',created_by=request.user)
            if account_no_2 and fund_name_2:
                item2 = Item.objects.create(user=request.user,data={'investment_type':investment_type_2,'account_no':account_no_2,'fund_name':fund_name_2,'account_value':account_value_2},item_type='Investment',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Investment data successfully updated.')
            if account_no_3 and fund_name_3:
                item3 = Item.objects.create(user=request.user,data={'investment_type':investment_type_3,'account_no':account_no_3,'fund_name':fund_name_3,'account_value':account_value_3},item_type='Investment',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Investment data successfully updated.')
            messages.add_message(request, messages.INFO, 'Investment data successfully updated.')
            return redirect('property_form')
        else:
            messages.add_message(request, messages.INFO, 'Something went wrong, please check if all fields are entered correctly.' + str(form.errors))
    context = {'form':form}
    return render(request,'backend/assets-4-investment.html',context)

def edit_investment_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    investment_type = instance.data['investment_type']
    if instance.data['fund_name']:
        fund_name = instance.data['fund_name']
    else:
        fund_name = ''
    account_no = instance.data['account_no']

    if instance.data['account_value']:
        account_value = instance.data['account_value']
    else:
        account_value = ''
    item_type = 'Investment'

    form = EditItemModelForm(request.POST,instance=instance,initial={
        'item_type':item_type,
        'investment_type':investment_type,
        'fund_name':fund_name,
        'account_no':account_no,
        }
        )

    if request.POST:
        instance.data['investment_type'] = form.data['investment_type']
        instance.data['fund_name'] = form.data['fund_name']
        instance.data['account_no'] = form.data['account_no']
        instance.data['account_value'] = form.data['account_value']
        instance.data['item_type'] = "Investment"
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Investment data successfully updated.')
        return redirect('dashboard')
    context = {'form':form,'investment_type':investment_type,'fund_name':fund_name,'account_no':account_no,'account_value':account_value}
    return render(request,'backend/edit-assets-4-investment.html',context)

def property_form(request):
    form = PropertyForm()
    if request.POST:
        form = PropertyForm(request.POST)
        if form.data['yesno'] == 'no':
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Property',created_by=request.user)
            messages.add_message(request, messages.INFO, 'No Property Added.')
            return redirect('vehicles_form')
        if form.is_valid():
            property_type = form.cleaned_data['property_type']
            residential_type = form.cleaned_data['residential_type']
            address = form.cleaned_data['address']
            state = form.cleaned_data['state']
            postcode = form.cleaned_data['postcode']
            titleno = form.cleaned_data['titleno']
            property_type_2 = form.cleaned_data['property_type_2']
            residential_type_2 = form.cleaned_data['residential_type_2']
            address_2 = form.cleaned_data['address_2']
            state_2 = form.cleaned_data['state_2']
            postcode_2 = form.cleaned_data['postcode_2']
            titleno_2 = form.cleaned_data['titleno_2']
            item = Item.objects.create(user=request.user,data={'property_type':property_type,'residential_type':residential_type,'address':address,'state':state,'postcode':postcode,'titleno':titleno},item_type='Property',created_by=request.user)
            if property_type_2 and residential_type_2 and address_2:
                item2 = Item.objects.create(user=request.user,data={'property_type':property_type_2,'residential_type':residential_type_2,'address':address_2,'state':state_2,'postcode':postcode_2,'titleno':titleno_2},item_type='Property',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Property data successfully updated.')
            messages.add_message(request, messages.INFO, 'Property data successfully updated.')
            return redirect('vehicles_form')
    context = {'form':form}
    return render(request,'backend/assets-5-property.html',context)

def edit_property_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    property_type = instance.data['property_type']
    residential_type = instance.data['residential_type']
    address = instance.data['address']
    if instance.data['state']:
        state = instance.data['state']
    else:
        state = ''
    if instance.data['postcode']:
        postcode = instance.data['postcode']
    else:
        postcode = ''
    if instance.data['titleno']:
        titleno = instance.data['titleno']
    else:
        titleno = ''
    spa_price = ''
    item_type = 'Property'

    form = EditItemModelForm(request.POST,instance=instance,initial={'item_type':item_type,
        'property_type':property_type,
        'residential_type':residential_type,
        'address':address,
        'state':state,
        'postcode':postcode,
        'titleno':titleno,
        'spa_price':spa_price,
        }
        )

    if request.POST:
        instance.data['property_type'] = form.data['property_type']
        instance.data['residential_type'] = form.data['residential_type']
        instance.data['address'] = form.data['address']
        instance.data['state'] = form.data['state']
        instance.data['postcode'] = form.data['postcode']
        instance.data['titleno'] = form.data['titleno']
        instance.data['spa_price'] = form.data['spa_price']
        instance.data['item_type'] = 'Property'
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Property data successfully updated.')
        return redirect('dashboard')

    context = {'form':form,'property_type':property_type,'residential_type':residential_type,'address':address,'state':state,'postcode':postcode,'titleno':titleno,'spa_price':spa_price}
    return render(request,'backend/edit-assets-5-property.html',context)

def vehicles_form(request):
    form = VehicleForm()
    if request.POST:
        form = VehicleForm(request.POST)
        if form.data['yesno'] == 'no':
            messages.add_message(request, messages.INFO, 'No Vehicle Added.')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Vehicle',created_by=request.user)
            return redirect('asset_others_form')
        if form.is_valid():
            vehicle_type = form.cleaned_data['vehicle_type']
            make_model = form.cleaned_data['make_model']
            registration_no = form.cleaned_data['registration_no']
            vehicle_type_2 = form.cleaned_data['vehicle_type_2']
            make_model_2 = form.cleaned_data['make_model_2']
            registration_no_2 = form.cleaned_data['registration_no_2']
            item = Item.objects.create(user=request.user,data={'vehicle_type':vehicle_type,'make_model':make_model,'registration_no':registration_no},item_type='Vehicle',created_by=request.user)
            if make_model_2 and registration_no_2:
                item2 = Item.objects.create(user=request.user,data={'vehicle_type':vehicle_type_2,'make_model':make_model_2,'registration_no':registration_no_2},item_type='Vehicle',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Vehicle data successfully updated.')
            messages.add_message(request, messages.INFO, 'Vehicle data successfully updated.')
            return redirect('asset_others_form')
        else:
            messages.add_message(request, messages.INFO, 'Please make sure to fill in all information to proceed.')
            return redirect('vehicles_form')
    context = {'form':form}
    return render(request,'backend/assets-6-vehicles.html',context)

def edit_vehicle_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    vehicle_type = instance.data['vehicle_type']
    make_model = instance.data['make_model']
    registration_no = instance.data['registration_no']
    item_type = 'Vehicle'

    form = EditItemModelForm(request.POST,instance=instance,initial={'item_type':item_type,
        'vehicle_type':vehicle_type,
        'make_model':make_model,
        'registration_no':registration_no,
        }
        )

    if request.POST:
        instance.data['vehicle_type'] = form.data['vehicle_type']
        instance.data['make_model'] = form.data['make_model']
        instance.data['registration_no'] = form.data['registration_no']
        instance.data['item_type'] = 'Vehicle'
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Vehicle data successfully updated.')
        return redirect('dashboard')

    context = {'form':form,'vehicle_type':vehicle_type,'make_model':make_model,'registration_no':registration_no}
    return render(request,'backend/edit-assets-6-vehicle.html',context)

def asset_others_form(request):
    form = AssetOthersForm()
    if request.POST:
        form = AssetOthersForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'No Assets Added.')
                item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Other Assets',created_by=request.user)
                return redirect('assets_overview')
            asset_name = form.cleaned_data['asset_name']
            asset_value = form.cleaned_data['asset_value']
            # asset_name_2 = form.cleaned_data['asset_name']
            # asset_value_2 = form.cleaned_data['asset_value']
            # asset_name_3 = form.cleaned_data['asset_name']
            # asset_value_3 = form.cleaned_data['asset_value']
            item = Item.objects.create(user=request.user,data={'asset_name':asset_name,'asset_value':asset_value},item_type='Other Assets',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Assets successfully updated.')
            return redirect('assets_overview')
    context = {'form':form}
    return render(request,'backend/assets-7-others.html',context)

def edit_asset_others_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    asset_name = instance.data['asset_name']
    asset_value = instance.data['asset_value']
    item_type = 'Other Assets'

    form = EditItemModelForm(request.POST,instance=instance,initial={'item_type':item_type,
        'asset_name':asset_name,
        'asset_value':asset_value,
        }
        )

    if request.POST:
        instance.data['asset_name'] = form.data['asset_name']
        instance.data['asset_value'] = form.data['asset_value']
        instance.data['item_type'] = 'Other Assets'
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Other assets data successfully updated.')
        return redirect('dashboard')

    context = {'form':form,'asset_name':asset_name,'asset_value':asset_value}
    return render(request,'backend/edit-assets-7-others.html',context)


def liability_credit_card_form(request):
    form = CreditCardForm()
    if request.POST:
        form = CreditCardForm(request.POST)
        if form.data['yesno'] == 'no':
            messages.add_message(request, messages.INFO, 'No Credit Card Added.')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Credit Card',created_by=request.user)
            return redirect('personal_loan_form')
        if form.is_valid():
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            amount_outstanding = form.cleaned_data['amount_outstanding']
            bank_name_2 = form.cleaned_data['bank_name_2']
            account_no_2 = form.cleaned_data['account_no_2']
            amount_outstanding_2 = form.cleaned_data['amount_outstanding_2']
            item = Item.objects.create(user=request.user,data={'bank_name':bank_name,'account_no':account_no,'amount_outstanding':amount_outstanding},item_type='Credit Card',created_by=request.user)
            if account_no_2 and bank_name_2:
                item2 = Item.objects.create(user=request.user,data={'bank_name':bank_name_2,'account_no':account_no_2,'amount_outstanding':amount_outstanding_2},item_type='Credit Card',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Credit Card Info Added.')
            messages.add_message(request, messages.INFO, 'Credit Card Info Added.')
            return redirect('personal_loan_form')
    context = {'form':form}
    return render(request,'backend/liabilities-1-credit-card.html',context)


def edit_liability_credit_card_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    if instance.data['amount_outstanding']:
        amount_outstanding = instance.data['amount_outstanding']
    else:
        amount_outstanding = ''
    account_no = instance.data['account_no']
    bank_name = instance.data['bank_name']
    item_type = 'Credit Card'

    form = EditItemModelForm(request.POST,instance=instance,initial={
        'item_type':item_type,
        'bank_name':bank_name,
        'amount_outstanding':amount_outstanding,
        'account_no':account_no,
        }
        )

    if request.POST:
        instance.data['bank_name'] = form.data['bank_name']
        instance.data['amount_outstanding'] = form.data['amount_outstanding']
        instance.data['account_no'] = form.data['account_no']
        instance.data['item_type'] = "Credit Card"
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Credit card data successfully updated.')
        return redirect('dashboard')
    context = {'form':form,'amount_outstanding':amount_outstanding,'bank_name':bank_name,'account_no':account_no}
    return render(request,'backend/edit-liabilities-1-credit-card.html',context)

def personal_loan_form(request):
    form = PersonalLoanForm()
    if request.POST:
        form = PersonalLoanForm(request.POST)
        if form.data['yesno'] == 'no':
            messages.add_message(request, messages.INFO, 'No Personal Loan Added.')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Personal Loan',created_by=request.user)
            return redirect('vehicles_loan_form')
        if form.is_valid():
            loan_tenure = form.cleaned_data['loan_tenure']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            loan_amount = form.cleaned_data['loan_amount']
            loan_tenure_2 = form.cleaned_data['loan_tenure_2']
            bank_name_2 = form.cleaned_data['bank_name_2']
            account_no_2 = form.cleaned_data['account_no_2']
            loan_amount_2 = form.cleaned_data['loan_amount_2']
            item = Item.objects.create(user=request.user,data={'bank_name':bank_name,'account_no':account_no,'loan_amount':loan_amount,'loan_tenure':loan_tenure},item_type='Personal Loan',created_by=request.user)
            if bank_name_2 and account_no_2 and loan_amount_2 and loan_tenure_2:
                item2 = Item.objects.create(user=request.user,data={'bank_name':bank_name_2,'account_no':account_no_2,'loan_amount':loan_amount_2,'loan_tenure':loan_tenure_2},item_type='Personal Loan',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Added Personal Loan.')
            messages.add_message(request, messages.INFO, 'Added Personal Loan.')
            return redirect('vehicles_loan_form')
    context = {'form':form}
    return render(request,'backend/liabilities-2-personal-loan.html',context)

def edit_personal_loan_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    account_no = instance.data['account_no']
    loan_amount = instance.data['loan_amount']
    loan_tenure = instance.data['loan_tenure']
    bank_name = instance.data['bank_name']
    item_type = 'Personal Loan'

    form = EditItemModelForm(request.POST,instance=instance,initial={
        'item_type':item_type,
        'bank_name':bank_name,
        'loan_amount':loan_amount,
        'loan_tenure':loan_tenure,
        'account_no':account_no,
        }
        )

    if request.POST:
        instance.data['bank_name'] = form.data['bank_name']
        instance.data['loan_tenure'] = form.data['loan_tenure']
        instance.data['loan_amount'] = form.data['loan_amount']
        instance.data['account_no'] = form.data['account_no']
        instance.data['item_type'] = "Personal Loan"
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Personal loan data successfully updated.')
        return redirect('dashboard')
    context = {'form':form,'loan_tenure':loan_tenure,'loan_amount':loan_amount,'bank_name':bank_name,'account_no':account_no}
    return render(request,'backend/edit-liabilities-2-personal-loan.html',context)

def vehicles_loan_form(request):
    form = VehicleLoanForm()
    if request.POST:
        form = VehicleLoanForm(request.POST)
        if form.data['yesno'] == 'no':
            messages.add_message(request, messages.INFO, 'No Vehicle Loan Added.')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Vehicle Loan',created_by=request.user)
            return redirect('property_loan_form')
        if form.is_valid():
            loan_tenure = form.cleaned_data['loan_tenure']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            loan_amount = form.cleaned_data['loan_amount']
            loan_tenure_2 = form.cleaned_data['loan_tenure_2']
            bank_name_2 = form.cleaned_data['bank_name_2']
            account_no_2 = form.cleaned_data['account_no_2']
            loan_amount_2 = form.cleaned_data['loan_amount_2']
            item = Item.objects.create(user=request.user,data={'bank_name':bank_name,'account_no':account_no,'loan_amount':loan_amount,'loan_tenure':loan_tenure},item_type='Vehicle Loan',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Vehicle Loan Added.')
            if bank_name_2 and account_no_2:
                item2 = Item.objects.create(user=request.user,data={'bank_name':bank_name_2,'account_no':account_no_2,'loan_amount':loan_amount_2,'loan_tenure':loan_tenure_2},item_type='Vehicle Loan',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Vehicle Loan Added.')
            return redirect('property_loan_form')
    context = {'form':form}
    return render(request,'backend/liabilities-3-vehicle-loan.html',context)

def edit_vehicle_loan_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    account_no = instance.data['account_no']
    loan_amount = instance.data['loan_amount']
    loan_tenure = instance.data['loan_tenure']
    bank_name = instance.data['bank_name']
    item_type = 'Vehicle Loan'

    form = EditItemModelForm(request.POST,instance=instance,initial={
        'item_type':item_type,
        'bank_name':bank_name,
        'loan_amount':loan_amount,
        'loan_tenure':loan_tenure,
        'account_no':account_no,
        }
        )

    if request.POST:
        instance.data['bank_name'] = form.data['bank_name']
        instance.data['loan_tenure'] = form.data['loan_tenure']
        instance.data['loan_amount'] = form.data['loan_amount']
        instance.data['account_no'] = form.data['account_no']
        instance.data['item_type'] = "Vehicle Loan"
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Vehicle loan data successfully updated.')
        return redirect('dashboard')
    context = {'form':form,'loan_tenure':loan_tenure,'loan_amount':loan_amount,'bank_name':bank_name,'account_no':account_no}
    return render(request,'backend/edit-liabilities-3-vehicle-loan.html',context)


def property_loan_form(request):
    form = PropertyLoanForm()
    if request.POST:
        form = PropertyLoanForm(request.POST)
        if form.data['yesno'] == 'no':
            messages.add_message(request, messages.INFO, 'No Property Loan Added.')
            item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Property Loan',created_by=request.user)
            return redirect('liabilities_others_form')
        if form.is_valid():
            loan_tenure = form.cleaned_data['loan_tenure']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            loan_amount = form.cleaned_data['loan_amount']
            loan_tenure_2 = form.cleaned_data['loan_tenure_2']
            bank_name_2 = form.cleaned_data['bank_name_2']
            account_no_2 = form.cleaned_data['account_no_2']
            loan_amount_2 = form.cleaned_data['loan_amount_2']
            item = Item.objects.create(user=request.user,data={'bank_name':bank_name,'account_no':account_no,'loan_amount':loan_amount,'loan_tenure':loan_tenure},item_type='Property Loan',created_by=request.user)
            if bank_name_2 and account_no_2:
                item2 = Item.objects.create(user=request.user,data={'bank_name':bank_name_2,'account_no':account_no_2,'loan_amount':loan_amount_2,'loan_tenure':loan_tenure_2},item_type='Property Loan',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Property Loan Added.')
            messages.add_message(request, messages.INFO, 'Property Loan Added.')
            return redirect('liabilities_others_form')
    context = {'form':form}
    return render(request,'backend/liabilities-4-property.html',context)

def edit_property_loan_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    account_no = instance.data['account_no']
    loan_amount = instance.data['loan_amount']
    loan_tenure = instance.data['loan_tenure']
    bank_name = instance.data['bank_name']
    item_type = 'Property Loan'

    form = EditItemModelForm(request.POST,instance=instance,initial={
        'item_type':item_type,
        'bank_name':bank_name,
        'loan_amount':loan_amount,
        'loan_tenure':loan_tenure,
        'account_no':account_no,
        }
        )

    if request.POST:
        instance.data['bank_name'] = form.data['bank_name']
        instance.data['loan_tenure'] = form.data['loan_tenure']
        instance.data['loan_amount'] = form.data['loan_amount']
        instance.data['account_no'] = form.data['account_no']
        instance.data['item_type'] = "Vehicle Loan"
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Property loan data successfully updated.')
        return redirect('dashboard')
    context = {'form':form,'loan_tenure':loan_tenure,'loan_amount':loan_amount,'bank_name':bank_name,'account_no':account_no}
    return render(request,'backend/edit-liabilities-4-property-loan.html',context)

def liabilities_others_form(request):
    form = LiabilitiesOthersForm()
    if request.POST:
        form = LiabilitiesOthersForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'No Liabilities Added.')
                item = Item.objects.create(user=request.user,data={'nodata':True},item_type='Other Liabilities',created_by=request.user)
                return redirect('notifier_list_form')
            liability_name = form.cleaned_data['liability_name']
            liability_value = form.cleaned_data['liability_value']
            item = Item.objects.create(user=request.user,data={'liability_value':liability_value,'liability_name':liability_name},item_type='Other Liabilities',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Added Other Liabilities.')
            return redirect('liabilities_overview')
    context = {'form':form}
    return render(request,'backend/liabilities-5-others.html',context)

def edit_liabilities_others_form(request,uuid):
    instance = Item.objects.get(uuid=uuid)
    liability_name = instance.data['liability_name']
    liability_value = instance.data['liability_value']
    item_type = 'Other Liabilities'

    form = EditItemModelForm(request.POST,instance=instance,initial={'item_type':item_type,
        'liability_name':liability_name,
        'liability_value':liability_value,
        }
        )
    if request.POST:
        instance.data['liability_name'] = form.data['liability_name']
        instance.data['liability_value'] = form.data['liability_value']
        instance.data['item_type'] = 'Other Liabilities'
        instance.updated_at = datetime.datetime.now()
        instance.save()
        print(instance)
        messages.add_message(request, messages.INFO, 'Other liabilities data successfully updated.')
        return redirect('dashboard')

    context = {'form':form,'liability_name':liability_name,'liability_value':liability_value}
    return render(request,'backend/edit-liabilities-5-others.html',context)

def notifier_list_form(request):
    form = NotifierForm()
    if request.POST:
        form = NotifierForm(request.POST)
        if form.is_valid():
            notifier_name = form.cleaned_data['notifier_name']
            notifier_email = form.cleaned_data['notifier_email']
            notifier_ic = form.cleaned_data['notifier_ic']
            notifier_contactno = form.cleaned_data['notifier_contactno']
            notifier_relationship = form.cleaned_data['notifier_relationship']
            notifier_event = form.cleaned_data['notifier_event']
            notifier_name_2 = form.cleaned_data['notifier_name_2']
            notifier_email_2 = form.cleaned_data['notifier_email_2']
            notifier_ic_2 = form.cleaned_data['notifier_ic_2']
            notifier_contactno_2 = form.cleaned_data['notifier_contactno_2']
            notifier_relationship_2 = form.cleaned_data['notifier_relationship_2']
            notifier_event_2 = form.cleaned_data['notifier_event_2']
            item = Item.objects.create(user=request.user,data={'notifier_name':notifier_name,'notifier_email':notifier_email,'notifier_relationship':notifier_relationship,'notifier_event':notifier_event,'notifier_contactno':notifier_contactno,'notifier_ic':notifier_ic},item_type='Notifier List',created_by=request.user)
            if notifier_name_2 and notifier_contactno_2 and notifier_ic_2:
                item = Item.objects.create(user=request.user,data={'notifier_name':notifier_name_2,'notifier_email':notifier_email_2,'notifier_relationship':notifier_relationship_2,'notifier_event':notifier_event_2,'notifier_contactno':notifier_contactno_2,'notifier_ic':notifier_ic_2},item_type='Notifier List',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Added notifier.')
            messages.add_message(request, messages.INFO, 'Added notifier.')
            return redirect('access_list_form')
        else:
            messages.add_message(request, messages.INFO, 'Please add a valid notifier with name and email.')
            return redirect('notifier_list_form')
    context = {'form':form}
    return render(request,'backend/notifier-list-form.html',context)

def access_list_form(request):
    form = AccessListForm()
    if request.POST:
        form = AccessListForm(request.POST)
        if form.is_valid():
            accesslist_name = form.cleaned_data['accesslist_name']
            accesslist_email = form.cleaned_data['accesslist_email']
            accesslist_ic = form.cleaned_data['accesslist_ic']
            accesslist_contactno = form.cleaned_data['accesslist_contactno']
            accesslist_relationship = form.cleaned_data['accesslist_relationship']

            accesslist_name_2 = form.cleaned_data['accesslist_name_2']
            accesslist_email_2 = form.cleaned_data['accesslist_email_2']
            accesslist_ic_2 = form.cleaned_data['accesslist_ic_2']
            accesslist_contactno_2 = form.cleaned_data['accesslist_contactno_2']
            accesslist_relationship_2 = form.cleaned_data['accesslist_relationship_2']

            item = Item.objects.create(user=request.user,data={'accesslist_name':accesslist_name,'accesslist_email':accesslist_email,'accesslist_relationship':accesslist_relationship,'accesslist_contactno':accesslist_contactno,'accesslist_ic':accesslist_ic},item_type='Access List',created_by=request.user)
            if accesslist_name_2 and accesslist_email_2 and accesslist_contactno_2:
                item = Item.objects.create(user=request.user,data={'accesslist_name':accesslist_name_2,'accesslist_email':accesslist_email_2,'accesslist_relationship':accesslist_relationship_2,'accesslist_contactno':accesslist_contactno_2,'accesslist_ic':accesslist_ic_2},item_type='Access List',created_by=request.user)
                messages.add_message(request, messages.INFO, 'Added Access List.')
            messages.add_message(request, messages.INFO, 'Added Access List.')
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.INFO, 'Please make sure to key in Name and Email.')
    context = {'form':form}
    return render(request,'backend/access-list-form.html',context)

def assets_overview(request):
    user = request.user
    items = Item.objects.filter(user=user)
    banks = items.filter(item_type='Bank Account').last()
    epf_socso = items.filter(item_type='EPF Socso').last()
    insurances = items.filter(item_type='Insurance').last()
    investments = items.filter(item_type='Investment').last()
    properties = items.filter(item_type='Property').last()
    vehicles = items.filter(item_type='Vehicle').last()
    others = items.filter(item_type='Other Assets').last()
    context = {'items':items,'banks':banks,'epf_socso':epf_socso,'insurances':insurances,'investments':investments,'vehicles':vehicles,'properties':properties,'others':others}
    return render(request,'backend/assets-overview.html',context)

class ItemUpdateView(UpdateView):
    model = Item
    fields = ['data']
    template_name_suffix = '_update_form'

def liabilities_overview(request):
    user = request.user
    items = Item.objects.filter(user=user)
    creditcard = items.filter(item_type='Credit Card').last()
    personalloan = items.filter(item_type='Personal Loan').last()
    vehicleloan = items.filter(item_type='Vehicle Loan').last()
    propertyloan = items.filter(item_type='Property Loan').last()
    others_liabilities = items.filter(item_type='Other Liabilities').last()
    context = {'items':items,'creditcard':creditcard,'personalloan':personalloan,'vehicleloan':vehicleloan,'propertyloan':propertyloan,'others_liabilities':others_liabilities}
    return render(request,'backend/liabilities-overview.html',context)

def dashboard(request):
    user = request.user
    items = Item.objects.filter(user=user)
    print(items.count())
    if items.count() == 0:
        return redirect('bank_account_form')
    banks = items.filter(item_type='Bank Account')
    bank_total = 0
    bank_values = banks.values('data')
    for x in bank_values:
        if 'account_value' in x['data']:
            if x['data']['account_value'] == "" or x['data']['account_value'] is None:
                bank_total = bank_total
            else:
                bank_total += float(x['data']['account_value'])

    insurances = items.filter(item_type='Insurance')
    insurance_total = 0
    insurance_values = insurances.values('data')
    for x in insurance_values:
        if 'sum_insured' in x['data']:
            if x['data']['sum_insured'] == "" or x['data']['sum_insured'] is None:
                insurance_total = insurance_total
            else:
                insurance_total += float(x['data']['sum_insured'])

    investments = items.filter(item_type='Investment')
    investment_total = 0
    investment_values = investments.values('data')
    for x in investment_values:
        if 'account_value' in x['data']:
            if x['data']['account_value'] == "" or x['data']['account_value'] is None:
                investment_total = investment_total
            else:
                investment_total += float(x['data']['account_value'])

    epf_socso = items.filter(item_type='EPF Socso')
    properties = items.filter(item_type='Property')
    vehicles = items.filter(item_type='Vehicle')

    others = items.filter(item_type='Other Assets')
    other_asset_total = 0
    asset_values = others.values('data')
    for x in asset_values:
        if 'asset_value' in x['data']:
            if x['data']['asset_value'] == "" or x['data']['asset_value'] is None:
                other_asset_total = other_asset_total
            else:
                other_asset_total += float(x['data']['asset_value'])

    creditcard = items.filter(item_type='Credit Card')
    creditcard_total = 0
    creditcard_values = creditcard.values('data')
    for x in creditcard_values:
        if 'amount_outstanding' in x['data']:
            if x['data']['amount_outstanding'] == "" or x['data']['amount_outstanding'] is None:
                creditcard_total = creditcard_total
            else:
                creditcard_total += float(x['data']['amount_outstanding'])

    personalloan = items.filter(item_type='Personal Loan')
    personalloan_total = 0
    personalloan_values = personalloan.values('data')
    for x in personalloan_values:
        if 'loan_amount' in x['data']:
            if x['data']['loan_amount'] == "" or x['data']['loan_amount'] is None:
                personalloan_total = personalloan_total
            else:
                personalloan_total += float(x['data']['loan_amount'])

    vehicleloan = items.filter(item_type='Vehicle Loan')
    vehicleloan_total = 0
    vehicleloan_values = vehicleloan.values('data')
    for x in vehicleloan_values:
        if 'loan_amount' in x['data']:
            if x['data']['loan_amount'] == "" or x['data']['loan_amount'] is None:
                vehicleloan_total = vehicleloan_total
            else:
                vehicleloan_total += float(x['data']['loan_amount'])

    propertyloan = items.filter(item_type='Property Loan')
    propertyloan_total = 0
    propertyloan_values = propertyloan.values('data')
    for x in propertyloan_values:
        if 'loan_amount' in x['data']:
            if x['data']['loan_amount'] == "" or x['data']['loan_amount'] is None:
                propertyloan_total = propertyloan_total
            else:
                propertyloan_total += float(x['data']['loan_amount'])

    others_liabilities = items.filter(item_type='Other Liabilities')
    other_liabilities_total = 0
    liabilities_values = others_liabilities.values('data')
    for x in liabilities_values:
        if 'liabilities_values' in x['data']:
            if x['data']['liabilities_value'] == "" or x['data']['liabilities_value'] is None:
                other_liabilities_total = other_liabilities_total
            other_liabilities_total += float(x['data']['liabilities_value'])


    context = {'creditcard_total':creditcard_total,'personalloan_total':personalloan_total,'vehicleloan_total':vehicleloan_total,'propertyloan_total':propertyloan_total,'other_liabilities_total':other_liabilities_total,'other_asset_total':other_asset_total,'insurance_total':insurance_total,'investment_total':investment_total,'bank_total':bank_total,'items':items,'banks':banks,'epf_socso':epf_socso,'insurances':insurances,'properties':properties,'investments':investments,'vehicles':vehicles,'others':others,'creditcard':creditcard,'personalloan':personalloan,'vehicleloan':vehicleloan,'propertyloan':propertyloan,'others_liabilities':others_liabilities}
    return render(request,'backend/dashboard.html',context)
