from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth import (authenticate, login, logout)
from django.contrib import messages
from django.core.context_processors import csrf

from .models import *
from .forms import *

from django.forms.models import model_to_dict

def home(request):
	return render(request,'index.html',{})

def login_user(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request,user)
			return render(request,'index.html',{})
		else:
			messages.error(
				request,'Invalid Credentials'
				)

	return render(request,'login.html')

def logout_user(request):
	logout(request)
	return HttpResponseRedirect("/")

def register_user(request):
	context = {}
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		context['form'] = form
		if form.is_valid():
			form.save()
	else:
		context['form'] = UserCreationForm()
	return render(request,'register_teacher.html',context)
def register_success(request):
	return HttpResponse('hi')

def teacher_login(request):
	context = {}
	if request.method == "POST":
		try:
			fl = request.POST['login']
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if Teacher.objects.filter(teacher=user):
					login(request,user)
					context["logged_in"] = 1;
					messages.success(request,'Logged in as %s'%user.username)
					request.session["user"] = "teacher"
				else:
					messages.warning(request,'You are not Teacher')
			else:
				messages.error(request,"Invalid Credentials")
				context["login"]=1
		except Exception,e:
			form = TeacherForm(request.POST)
			print 'creg'
			if form.is_valid():
				try:
					school_id = form.cleaned_data['school_code']
					username = form.cleaned_data['username']
					email = username
					password = form.cleaned_data['password1']
					user = User.objects.create_user(username,email,password)
					user.is_active = True
					user.save()
					teacher = Teacher.objects.create(teacher=user,school=School.objects.get(pk=school_id))
					teacher.save()
					messages.success(request,"Registered ...")
					context["registered"]=1
				except Exception,e:
					print e
					context["form"] = form

			else:
				context["register"]=1
				context["form"] = form

	else:
		try:
			request.GET["login"]
			context["login"] = 1
		except:
			context["register"] = 1
			try:
				form= TeacherForm()
				context["form"]=form
			except Exception,e:
				print e
	return render(request,'teacher_login.html',context)

def teacher_view(request):
	context = {}
	if request.user.is_authenticated():
		if request.method == "POST":
			context = {}
		else:
			details = {}
			teacher = Teacher.objects.filter(teacher=request.user)[0]
			school = teacher.school
			devices = Device.objects.filter(school=school)
			incidents = Incident.objects.filter(creater=teacher)
			allincidents = Incident.objects.filter(device__in=devices)
			context["devices"] = devices
			context["incidents"] = incidents
			context["allincidents"] = allincidents
			context["school"] = model_to_dict(school)
			
	else:
		return HttpResponseRedirect("/")
	return render(request,"teacher_view.html",context)

def add_device(request):
	context = {}
	if request.method == "POST":
		form = DeviceForm(request.POST)
		if form.is_valid():
			teacher = Teacher.objects.filter(teacher=request.user)[0]
			new = 1
			for device in Device.objects.filter(school = teacher.school):
				if device.device_name == form.cleaned_data['device_name']:
					new = 0
					break
			if new == 1:
				post = Device(school=teacher.school,device_name=form.cleaned_data['device_name'],status=form.cleaned_data['status'])
				post.save()
				context['device_added'] = 1
				messages.success(request,"New Device Added")
			else:
				messages.warning(request,"Asset Already Existed")
				context["form"] = form
		else:
			context["form"] = form
			messages.error(request,'Enter Correct Details')
	else:
		form = DeviceForm()
		context["form"] = form
	return render(request,"add_device.html",context)

def create_incident(request):
	context = {}
	teacher = Teacher.objects.filter(teacher=request.user)
	devices = Device.objects.filter(school=teacher[0].school)
	if request.method == "POST":
		form = IncidentForm(request.POST)
		if form.is_valid():
			print 'coming'
			form.save()
			messages.success(request,"Incident Created")
		else:
			form.fields["creater"].queryset = teacher
			form.fields['device'].queryset = devices
			context["form"] = form
	else:
		try:
			form = IncidentForm()
			form.fields["creater"].queryset = teacher
			form.fields['device'].queryset = devices
			context["form"] = form
		except Exception,e:
			print e
	return render(request,"create_incident.html",context)

def technician_login(request):
	context = {}
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if Employee.objects.filter(employee=user):
					login(request,user)
					context["logged_in"] = 1;
					messages.success(request,'Logged in as %s'%user.username)
					request.session["user"] = "technician"
				else:
					messages.warning(request,'You are not a Techincian')
			else:
				context["form"] = form
				messages.error(request,"Invalid Credentials")
		else:
			context["form"] = form
	else:
		context["form"] = LoginForm()
	return render(request,"technician_login.html",context)
def technician_view(request):
	context = {}
	if request.user.is_authenticated():
		employee = Employee.objects.filter(employee=request.user)[0]
		if request.method == "POST":
			incident = Incident.objects.get(pk=request.POST["incident_id"])
			incident.status="work_in_progress"
			incident.save()
			try:
				assi = IncidentActions(assignee=employee,incident=incident,description = "none")
				assi.save()
			except Exception,e:
				print e
			return HttpResponse("<div class='alert alert-success'>Assigned to "+str(employee)+"</div>")
		else:
			details = {}
			schools = School.objects.filter(mandal=Mandal.objects.filter(district_name=employee.district_name))
			devices = Device.objects.filter(school__in=schools)
			allincidents = Incident.objects.filter(device__in=devices)
			open_inc = allincidents.filter(status="open")
			context["devices"] = devices
			context["allincidents"] = allincidents
			context["open_inc"] = open_inc
			context["my_inc"] = [incident.incident for incident in IncidentActions.objects.filter(assignee=employee)]
			context["schools"] = schools
			
	else:
		return HttpResponseRedirect("/")
	return render(request,"technician_view.html",context)

def admin_view(request):
	context = {}
	if request.method == "GET":
		devices = Device.objects.all()
		context['devices'] = devices
		device_meta = []
		mandals = Mandal.objects.all()
		all_devices = []
		for mandal in mandals.values_list('district_name',flat=True).distinct():
			total_dev = devices.filter(school__in=(School.objects.filter(mandal__in=mandals.filter(district_name=mandal))))
			if total_dev.count() > 0:
				dist = {"district":mandal}
				dist["ok"] = total_dev.filter(status="ok").count()
				dist["danger"] = total_dev.count()-dist["ok"]
				device_meta.append(dist)
				all_devices.append({"district":mandal,"devices":total_dev})
		employees = Employee.objects.all()
		assigned_incidents = IncidentActions.objects.all()
		employee_incidents =  []
		for employee in employees:
			employee_incidents.append({'employee':employee.employee.username,'count':assigned_incidents.filter(assignee=employee).count(),'district':employee.district_name})

		incidents = Incident.objects.all()

		context["device_meta"] = device_meta
		context["employee_incidents"] = employee_incidents
		context["all_devices"] = all_devices
		context["open_in"] = incidents.filter(status="open")
		context["incidents"] = list(set(incidents)-set(context["open_in"]))

	return render(request,"admin_view.html",context)