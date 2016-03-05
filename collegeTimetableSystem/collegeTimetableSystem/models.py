from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from time import time
from datetime import date
from datetime import datetime
from django.utils.encoding import python_2_unicode_compatible


class Teacher(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    user = models.ForeignKey(User)
    teacherName = models.CharField(max_length=100)
    mobileNo = models.IntegerField()
    qualification = models.TextField()
    workExperience = models.FloatField()
    workDetails = models.ManyToManyField('WorkDetails')
    areaOfInterest = models.ManyToManyField('Subject')

    def __unicode__(self):
        return self.teacherName


class WorkDetails(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    academicYear = models.IntegerField()
    subject = models.ManyToManyField('Subject')
    weekWorkTheoryHoursCompletedYet = models.FloatField() #in hours
    weekWorkPracticalHoursCompletedYet = models.FloatField() #in hours
    minWeekWorkTheoryHours = models.FloatField() #in hours
    minWeekWorkPracticalHours = models.FloatField() #in hours

    def __unicode__(self):
        return str(self.academicYear)+" Lectures hours Completed yet: "+str(self.weekWorkTheoryHoursCompletedYet)


class Subject(models.Model):
    subjectName = models.TextField()
    semester = models.IntegerField(null=True)
    courseName = models.CharField(max_length=50,null=True)
    courseYear = models.IntegerField(null=True)

    def __unicode__(self):
        return str(self.subjectName)+" "+str(self.courseName)+" "+str(self.semester)
