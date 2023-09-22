from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,redirect, reverse, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from HotelApis.models import *
from .models import *
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Sum, Max, Min, Avg
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView, View

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.db.models import Q
import datetime
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import *
from django.contrib.auth.models import User, auth

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

UserModel = get_user_model()



@login_required(login_url='SigninPage')
def HomePage(request):

	return render(request, 'TemplatesApp/home.html')





# def SignupPage(request):
# 	form = MyUserForm()
# 	password = request.POST.get('password1')
# 	password2 = request.POST.get('password2')
# 	email = request.POST.get('email')
# 	username = request.POST.get('username')
# 	phone = request.POST.get('phone')

# 	filter_username= MyUser.objects.filter(username=username)
# 	filter_email= MyUser.objects.filter(email=email)
# 	filter_phone= MyUser.objects.filter(phone=phone)


# 	if request.method == "POST":
		
		

# 		if filter_username.exists():
# 			messages.info(request,f"Registration Failed!, Username {username} already exists")
# 			return redirect('SignupPage')

# 		if filter_email.exists():
# 			messages.info(request,f"Registration Failed!, email {email} already exists")
# 			return redirect('SignupPage')




# 		if password == password2:

# 			form = MyUserForm(request.POST, files=request.FILES)
# 			if form.is_valid():
# 				user = form.save()
# 				login(request, user)
				

# 				messages.success(request, f'{username} is registered successfully')
# 				return redirect('SignupPage')


# 			messages.success(request, 'Registration failed')
# 			return redirect('SignupPage')

# 		else:
# 			messages.info(request, 'The Two Passwords Not Matching')
# 			return redirect('SignupPage')


# 	context = {
# 		"form":form
# 	}



# 	return render(request, 'Account/SignupPage.html', context)



def SignupPage(request):
    if request.method == "POST":
        form = MyUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'{user.username} is registered successfully')
            return redirect('SignupPage')
    else:
        form = MyUserForm()

    context = {
        "form": form
    }
    return render(request, 'Account/SignupPage.html', context)





def SigninPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        UserCodes = request.POST.get('UserCodes')

        # Use Django's authenticate function to check email and password
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Check if UserCodes matches the user's UserCodes
            if user.UserCodes == UserCodes:
                login(request, user)
                return redirect('HomePage')
            else:
                messages.info(request, 'Invalid User Codes')
                return redirect('SigninPage')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('SigninPage')
    else:
        return render(request, 'Account/SigninPage.html')




@login_required(login_url='SigninPage')
def LogoutPage(request):
    auth.logout(request)
    return redirect('SigninPage')




class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    #login_url = 'login'
    success_url = reverse_lazy('HomePage')





def UpdateUser(request, id):
    x = MyUser.objects.get(id=id)
    if request.method == "POST":
        form = UpdateMyUserForm(request.POST, instance=x)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'{x.username} is updated successfully')
            return redirect('UpdateUser',id=id)
    else:
        form = UpdateMyUserForm(instance=x)

    context = {
        "form": form
    }
    return render(request, 'Account/UpdateUser.html', context)























#-------------------CUSTOMERS--------------------------------


@login_required(login_url='SigninPage')
def HotelCustomersPage(request):
    customers = HotelCustomers.objects.all().order_by('-id')
    form = HotelCustomersSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            customer_full_name = form.cleaned_data.get('CustomerFullName', '')
            customer_address = form.cleaned_data.get('CustomerAddress', '')

            # Use Q objects to construct the query
            query = Q()
            if customer_full_name:
                query |= Q(CustomerFullName__icontains=customer_full_name)
            if customer_address:
                query |= Q(CustomerAddress__icontains=customer_address)

            customers = HotelCustomers.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(customers,5)
    page = request.GET.get('page')
    try:
        customers=paginator.page(page)
    except PageNotAnInteger:
        customers=paginator.page(1)
    except EmptyPage:
        customers=paginator.page(paginator.num_pages)

    context = {
        "customers": customers,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelCustomersPage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_customer_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(CustomerFullName__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    customers = HotelCustomers.objects.filter(search)
    mylist= []
    mylist += [x.CustomerFullName for x in customers]
    return JsonResponse(mylist, safe=False)

def Hotel_search_address_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(CustomerAddress__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    customers = HotelCustomers.objects.filter(search)
    mylist= []
    mylist += [x.CustomerAddress for x in customers]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def DeleteCustomerPage(request,id):
    x = HotelCustomers.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"{x.CustomerFullName} was deleted Successfully")
        return redirect('HotelCustomersPage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteCustomerPage.html', context)



@login_required(login_url='SigninPage')
def AddCustomerPage(request):
    
    form = AddCustomerForm()
    
    if request.method == "POST":
        form=AddCustomerForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelCustomersPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddCustomer')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddCustomer.html', context)



@login_required(login_url='SigninPage')
def UpdateCustomerPage(request,id):
    x = HotelCustomers.objects.get(id=id)
    form = AddCustomerForm(instance=x)
    
    if request.method == "POST":
        form=AddCustomerForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"{x.userName}  updated Successfully")
            return redirect('HotelCustomersPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateCustomer.html', context)










#---------------BUSINESS UNIT--------------------

@login_required(login_url='SigninPage')
def HotelBusinessUnitPage(request):
    queryset = HotelBusinessUnit.objects.all().order_by('-id')
    form = HotelBusinessUnitSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Description:
                query |= Q(Description__icontains=Description)

            queryset = HotelBusinessUnit.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelBusinessUnitPage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_Code_Business_Unit_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelBusinessUnit.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

def Hotel_search_Description_Business_Unit_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelBusinessUnit.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelBusinessUnit(request,id):
    x = HotelBusinessUnit.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Business Unit with code {x.Code} was deleted Successfully")
        return redirect('HotelBusinessUnitPage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelBusinessUnit.html', context)



@login_required(login_url='SigninPage')
def AddHotelBusinessUnit(request):
    
    form = AddHotelBusinessUnitForm()
    
    if request.method == "POST":
        form=AddHotelBusinessUnitForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelBusinessUnitPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelBusinessUnit')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelBusinessUnit.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelBusinessUnit(request,id):
    x = HotelBusinessUnit.objects.get(id=id)
    form = AddHotelBusinessUnitForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelBusinessUnitForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelBusinessUnitPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelBusinessUnit.html', context)





















#---------------LOCATION CODE UNIT--------------------

@login_required(login_url='SigninPage')
def HotelLocationCodePage(request):
    queryset = HotelLocationCode.objects.all().order_by('-id')
    form = HotelLocationCodeSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Description:
                query |= Q(Description__icontains=Description)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = HotelLocationCode.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }



    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            BusinessUnit = form['BusinessUnit'].value()

            

                                            
            queryset = HotelLocationCode.objects.filter(
                                            Code__icontains=form['Code'].value(),
                                            Description__icontains=form['Description'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (BusinessUnit != ''):
                queryset = HotelLocationCode.objects.all()
                queryset = queryset.filter(BusinessUnit_id=BusinessUnit)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelLocationCodePage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_Code_Location_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelLocationCode.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

def Hotel_search_Description_Location_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelLocationCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelLocationCode(request,id):
    x = HotelLocationCode.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Business Unit with code {x.Code} was deleted Successfully")
        return redirect('HotelLocationCodePage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelLocationCode.html', context)



@login_required(login_url='SigninPage')
def AddHotelLocationCode(request):
    
    form = AddHotelLocationCodeForm()
    
    if request.method == "POST":
        form=AddHotelLocationCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelLocationCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelLocationCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelLocationCode.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelLocationCode(request,id):
    x = HotelLocationCode.objects.get(id=id)
    form = AddHotelLocationCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelLocationCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelLocationCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelLocationCode.html', context)












#----------------------HOTEL PROCESS CONFIG-----------------------




@login_required(login_url='SigninPage')
def HotelProcessConfigPage(request):
    queryset = HotelProcessConfig.objects.all().order_by('-id')
    form = HotelProcessConfigSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            ProcesId = form.cleaned_data.get('ProcesId', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if ProcesId:
                query |= Q(ProcesId__icontains=ProcesId)
            if Description:
                query |= Q(Description__icontains=Description)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = HotelProcessConfig.objects.filter(query)


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    

    return render(request, 'TemplatesApp/HotelProcessConfigPage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_ProcesId_process_config_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(ProcesId__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelProcessConfig.objects.filter(search)
    mylist= []
    mylist += [x.ProcesId for x in filters]
    return JsonResponse(mylist, safe=False)

def Hotel_search_Description_process_config_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelProcessConfig.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelProcessConfig(request,id):
    x = HotelProcessConfig.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Data deleted Successfully")
        return redirect('HotelProcessConfigPage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelProcessConfig.html', context)



@login_required(login_url='SigninPage')
def AddHotelProcessConfig(request):
    
    form = AddHotelProcessConfigForm()
    
    if request.method == "POST":
        form=AddHotelProcessConfigForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelProcessConfigPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelProcessConfig')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelProcessConfig.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelProcessConfig(request,id):
    x = HotelProcessConfig.objects.get(id=id)
    form = AddHotelProcessConfigForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelProcessConfigForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelProcessConfigPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelProcessConfig.html', context)





















#---------------HOTEL STORE CODE--------------------

@login_required(login_url='SigninPage')
def HotelStoreCodePage(request):
    queryset = HotelStoreCode.objects.all().order_by('-id')
    form = HotelStoreCodeSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Description:
                query |= Q(Description__icontains=Description)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = HotelStoreCode.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }



    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            Location = form['Location'].value()

            

                                            
            queryset = HotelStoreCode.objects.filter(
                                            Code__icontains=form['Code'].value(),
                                            Description__icontains=form['Description'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (Location != ''):
                queryset = HotelStoreCode.objects.all()
                queryset = queryset.filter(Location_id=Location)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }




    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            Process = form['Process'].value()

            

                                            
            queryset = HotelStoreCode.objects.filter(
                                            Code__icontains=form['Code'].value(),
                                            Description__icontains=form['Description'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (Process != ''):
                queryset = HotelStoreCode.objects.all()
                queryset = queryset.filter(Process_id=Process)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelStoreCodePage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_Code_store_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelStoreCode.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

def Hotel_search_Description_store_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelStoreCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelStoreCode(request,id):
    x = HotelStoreCode.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Data {x.Code} was deleted Successfully")
        return redirect('HotelStoreCodePage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelStoreCode.html', context)



@login_required(login_url='SigninPage')
def AddHotelStoreCode(request):
    
    form = AddHotelStoreCodeForm()
    
    if request.method == "POST":
        form=AddHotelStoreCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelStoreCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelStoreCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelStoreCode.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelStoreCode(request,id):
    x = HotelStoreCode.objects.get(id=id)
    form = AddHotelStoreCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelStoreCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelStoreCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelStoreCode.html', context)
















#----------------------HOTEL STORE BIN CODE-----------------------




@login_required(login_url='SigninPage')
def HotelStoreBinCodePage(request):
    queryset = HotelStoreBinCode.objects.all().order_by('-id')
    form = HotelStoreBinCodeSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            StoreBinCode = form.cleaned_data.get('StoreBinCode', '')
            Description = form.cleaned_data.get('Description', '')
            CardNo = form.cleaned_data.get('CardNo', '')

            # Use Q objects to construct the query
            query = Q()
            if StoreBinCode:
                query |= Q(StoreBinCode__icontains=StoreBinCode)
            if Description:
                query |= Q(Description__icontains=Description)

            if CardNo:
                query |= Q(CardNo__icontains=CardNo)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = HotelStoreBinCode.objects.filter(query)


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    

    return render(request, 'TemplatesApp/HotelStoreBinCodePage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_StoreBinCode_store_bin_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(StoreBinCode__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelStoreBinCode.objects.filter(search)
    mylist= []
    mylist += [x.StoreBinCode for x in filters]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Hotel_search_CardNo_store_bin_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(CardNo__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelStoreBinCode.objects.filter(search)
    mylist= []
    mylist += [x.CardNo for x in filters]
    return JsonResponse(mylist, safe=False)


def Hotel_search_Description_store_bin_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelStoreBinCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelStoreBinCode(request,id):
    x = HotelStoreBinCode.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Data deleted Successfully")
        return redirect('HotelStoreBinCodePage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelStoreBinCode.html', context)



@login_required(login_url='SigninPage')
def AddHotelStoreBinCode(request):
    
    form = AddHotelStoreBinCodeForm()
    
    if request.method == "POST":
        form=AddHotelStoreBinCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelStoreBinCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelStoreBinCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelStoreBinCode.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelStoreBinCode(request,id):
    x = HotelStoreBinCode.objects.get(id=id)
    form = AddHotelStoreBinCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelStoreBinCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelStoreBinCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelStoreBinCode.html', context)













