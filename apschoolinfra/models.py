from django.db import models
from django.contrib.auth.models import User


class Mandal(models.Model):
	district_name = models.CharField(max_length=125)
	mandal_name = models.CharField(max_length=125)

	def __str__(self):
		return self.mandal_name+'-'+self.district_name

class Employee(models.Model):
	employee = models.OneToOneField(User)
	district_name = models.CharField(max_length=100)

	def __str__(self):
		return self.employee.username


class School(models.Model):
	mandal = models.ForeignKey(Mandal, related_name="schools")
	school_name = models.CharField(max_length=100)
	city_name = models.CharField(max_length=100)
	address = models.TextField()
	pincode = models.IntegerField()

	def __str__(self):
		return self.school_name+'-'+self.mandal.mandal_name
	

class Teacher(models.Model):
	teacher = models.OneToOneField(User)
	school = models.ForeignKey(School, related_name="teachers")

	def __str__(self):
		return self.teacher.username

class Device(models.Model):
	school = models.ForeignKey(School, related_name="devices")
	device_name = models.CharField(max_length=125)
	CHOICES = (('ok','ok'),('warning','warninig'),('critical','critical'))
	status = models.CharField(max_length=10, choices=CHOICES, default="ok")

	def __str__(self):
		return self.device_name

	
class Incident(models.Model):
	creater = models.ForeignKey(Teacher, related_name="incident_creator") 
	device = models.ForeignKey(Device, related_name="incidents")
	title = models.CharField(max_length=125)
	description = models.TextField()
	creation_time = models.DateTimeField(auto_now_add=True)
	CHOICES = (('open','open'),('work_in_progress','work_in_progress'),('hold','hold'),('resolved','resolved'))
	status = models.CharField(max_length=100, choices=CHOICES,default="open")

	def __str__(self):
		return self.title+'-'+self.device.device_name

class IncidentActions(models.Model):
	assignee = models.ForeignKey(Employee, related_name="sop_assigne")
	incident = models.ForeignKey(Incident,related_name="sop_incidents")
	updated = models.DateTimeField(auto_now=True)
	description = models.TextField()

	def __str__(self):
		return self.incident.title+' SOP'

class IncidentWork(models.Model):
	incident = models.ForeignKey(Incident)
	updated = models.DateTimeField(auto_now=True)
	description = models.TextField()
