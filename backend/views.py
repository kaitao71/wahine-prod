from django.shortcuts import render,redirect
from backend.forms import *
import uuid
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.
## TODO
## IF data exist, show existing data/edit mode
## If fields can have multiple entry (eg policy), show no of policies

def index(request):
    return render(request,'backend/index.html')

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
            return redirect('bank_account_form')
        else:
            print(form.errors)
            print(form.cleaned_data)
            return render(request,'backend/signup.html', {'form': form})
    form = SignUpForm()
    return render(request,'backend/signup.html', {'form': form})

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

def dashboard(request):
    return render(request,'backend/dashboard.html')

def profile(request):
    return render(request,'backend/profile.html')

def bank_account_form(request):
    form = BankAccountForm()
    if request.POST:
        form = BankAccountForm(request.POST)
        if form.is_valid():
            account_type = form.cleaned_data['account_type']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            account_value = form.cleaned_data['account_value']
            item = Item.objects.create(
                user=request.user,
                data={'account_type':account_type,
                    'bank_name':bank_name,
                    'account_no':account_no,
                    'account_value':account_value},
                item_type='Assets',
                created_by=request.user
                )
            messages.add_message(request, messages.INFO, 'Model Form Done.')
            return redirect('epf_socso_form')
        else:
            context = {'form':form}
            return render(request,'backend/assets.html',context)
    context = {'form':form}
    return render(request,'backend/assets.html',context)

def epf_socso_form(request):
    form = EpfSocsoForm()
    if request.POST:
        form = EpfSocsoForm(request.POST)
        if form.is_valid():
            is_epf_member = form.cleaned_data['is_epf_member']
            epf_member_no = form.cleaned_data['epf_member_no']
            epf_nominee_name = form.cleaned_data['epf_nominee_name']
            is_socso_member = form.cleaned_data['is_socso_member']
            socso_nominee_name = form.cleaned_data['socso_nominee_name']
            socso_member_no = form.cleaned_data['socso_member_no']
            epf_account_value = form.cleaned_data['epf_account_value']
            socso_account_value = form.cleaned_data['socso_account_value']
            item = Item.objects.create(
                user=request.user,
                data={'is_epf_member':is_epf_member,
                    'is_socso_member':is_socso_member,
                    'epf_member_no':epf_member_no,
                    'socso_member_no':socso_member_no,
                    'epf_nominee_name':epf_nominee_name,
                    'socso_nominee_name':socso_nominee_name,
                    'epf_account_value':epf_account_value,
                    'socso_account_value':socso_account_value,
                }  ,
                item_type='Assets',
                created_by=request.user
                )
            messages.add_message(request, messages.INFO, 'EPF/Socso Done.')
            return redirect('insurance_form')
        else:
            print(form.errors)
            context = {'form':form}
            return render(request,'backend/assets-2-epf.html',context)
    context = {'form':form}
    return render(request,'backend/assets-2-epf.html',context)

def insurance_form(request):
    form = InsuranceForm()
    if request.POST:
        form = InsuranceForm(request.POST)
        if form.is_valid():
            insurance_type = form.cleaned_data['insurance_type']
            policy_no = form.cleaned_data['policy_no']
            nominee_name = form.cleaned_data['nominee_name']
            account_value = form.cleaned_data['account_value']
            item = Item.objects.create(user=request.user,data={'insurance_type':insurance_type,'policy_no':policy_no,'nominee_name':nominee_name,'account_value':account_value},item_type='Assets',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Done.')
            return redirect('investment_form')
    context = {'form':form}
    return render(request,'backend/assets-3-insurance.html',context)

def investment_form(request):
    form = InvestmentForm()
    if request.POST:
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment_type = form.cleaned_data['investment_type']
            account_no = form.cleaned_data['account_no']
            fund_name = form.cleaned_data['fund_name']
            account_value = form.cleaned_data['account_value']
            item = Item.objects.create(user=request.user,data={'investment_type':investment_type,'account_no':account_no,'fund_name':fund_name,'account_value':account_value},item_type='Assets',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Done.')
            return redirect('property_form')
    context = {'form':form}
    return render(request,'backend/assets-4-investment.html',context)

def property_form(request):
    form = PropertyForm()
    if request.POST:
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_type = form.cleaned_data['property_type']
            residential_type = form.cleaned_data['residential_type']
            address = form.cleaned_data['address']
            spa_price = form.cleaned_data['spa_price']
            item = Item.objects.create(user=request.user,data={'property_type':property_type,'residential_type':residential_type,'address':address,'spa_price':spa_price},item_type='Assets',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Done.')
            return redirect('vehicles_form')
    context = {'form':form}
    return render(request,'backend/assets-5-property.html',context)

def vehicles_form(request):
    form = VehicleForm()
    if request.POST:
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle_type = form.cleaned_data['insurance_type']
            make_model = form.cleaned_data['policy_no']
            registration_no = form.cleaned_data['nominee_name']
            item = Item.objects.create(user=request.user,data={'insurance_type':insurance_type,'policy_no':policy_no,'nominee_name':nominee_name},item_type='Assets',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Done.')
            return redirect('bank_account_form')
    context = {'form':form}
    return render(request,'backend/assets-6-vehicles.html',context)

def asset_others_form(request):
    form = AssetOthersForm()
    if request.POST:
        form = AssetOthersForm(request.POST)
        if form.is_valid():
            asset_name = form.cleaned_data['asset_name']
            asset_value = form.cleaned_data['asset_value']
            item = Item.objects.create(user=request.user,data={'asset_name':asset_name,'asset_value':asset_value},item_type='Assets',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Done.')
            return redirect('bank_account_form')
    context = {'form':form}
    return render(request,'backend/assets-7-others.html',context)
