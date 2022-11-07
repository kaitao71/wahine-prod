from django.shortcuts import render,redirect
from backend.forms import *
import uuid
from django.contrib import messages

# Create your views here.
## TODO
## IF data exist, show existing data/edit mode
## If fields can have multiple entry (eg policy), show no of policies


def bank_account_form(request):
    form = BankAccountForm2()
    if request.POST:
        form = BankAccountForm(request.POST)
        if form.is_valid():
            bank_type = form.cleaned_data['bank_type']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            item = Item.objects.create(
                user=request.user,
                data={'bank_type':bank_type,
                    'bank_name':bank_name,
                    'account_no':account_no},
                item_type='Assets',
                created_by=request.user
                )
            messages.add_message(request, messages.INFO, 'Model Form Done.')
            return redirect('epf_socso_form')
    context = {'form':form}
    return render(request,'backend/bank-account-form.html',context)

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
            item = Item.objects.create(
                user=request.user,
                data={'is_epf_member':is_epf_member,
                    'is_socso_member':is_socso_member,
                    'epf_member_no':epf_member_no,
                    'socso_member_no':socso_member_no,
                    'epf_nominee_name':epf_nominee_name,
                    'socso_nominee_name':socso_nominee_name,
                }  ,
                item_type='Assets',
                created_by=request.user
                )
            messages.add_message(request, messages.INFO, 'EPF/Socso Done.')
            return redirect('insurance_form')
    context = {'form':form}
    return render(request,'backend/epf-socso-form.html',context)

def insurance_form(request):
    form = InsuranceForm()
    if request.POST:
        form = InsuranceForm(request.POST)
        if form.is_valid():
            insurance_type = form.cleaned_data['insurance_type']
            policy_no = form.cleaned_data['policy_no']
            nominee_name = form.cleaned_data['nominee_name']
            item = Item.objects.create(user=request.user,data={'insurance_type':insurance_type,'policy_no':policy_no,'nominee_name':nominee_name},item_type='Assets',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Done.')
            return redirect('bank_account_form')
    context = {'form':form}
    return render(request,'backend/bank-account-form.html',context)
