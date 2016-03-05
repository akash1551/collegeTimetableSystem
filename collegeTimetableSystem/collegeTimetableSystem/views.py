from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from models import Teacher
import json
from django import forms
from django.db import IntegrityError
import re
from datetime import datetime
from datetime import date
from datetime import timedelta
import time
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import calendar
from django.db import transaction
from django.core.validators import EmailValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max

## script for validating email address
def validateEmail(email):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

## script for validating mobile number
def validate_mobile(value):
    rule = re.compile(r'^(\+91[\-\s]?)?[0]?[1789]\d{9}$')
    if not rule.search(value):
        return False
    else:
        return value

## teacher registration
def teacher_registration(request):
    jsonObj=json.loads(request.body)
    jsonObj=jsonObj['userInfo']

    if User.objects.filter(username = jsonObj['userName']).exists():
        print "Username already Exist."
        return HttpResponse(json.dumps({"validation":"Username is already exist.","status":False}), content_type="application/json")
    username = jsonObj['userName'].strip()
    teacherName = jsonObj['teacherName'].strip()

    password = jsonObj['password']
    confirmPassword = jsonObj['confirmPassword']
    if password != confirmPassword:
        print "Passwords Are not Matching"
        return HttpResponse(json.dumps({"validation":"Passwords are not Matched","status":False}), content_type="application/json")
    email = validateEmail(jsonObj['email'])
    if email != True:
        print "Email is already Exist."
        return HttpResponse(json.dumps({"validation":"Email is already exist.Try with another Email.","status":False}), content_type="application/json")
    else:
        email = jsonObj['email']

    mobileNo = jsonObj['mobileNo']
    mobileNo = int(mobileNo)
    mobileNo = validate_mobile(str(mobileNo))
    if mobileNo == False:
        return HttpResponse(json.dumps([{"validation": "This mobile number is already used..please try with another one.", "status": False}]), content_type = "application/json")
    else:
        workExperience = jsonObj['workExperience']
        areaOfInterestList = jsonObj['areaOfInterestList']
        qualification = jsonObj['qualification']
        userObj = User(username=userName,email=email,password=password)
        userObj.set_password(password)
        userObj.save()
        teacherObj = Teacher(user=userObj,
                            teacherName=teacherName,
                            qualification=qualification,
                            mobileNo=mobileNo,
                            workExperience=workExperience)
        teacherObj.save()

        for i in areaOfInterestList:
            subjectName = i.subjectName
            semester = i.semester
            courseName = i.courseName
            courseYear = i.courseYear
            subjectObj = Subject(subjectName=subjectName,
                                semester=semester,
                                courseName=courseName,
                                courseYear=courseYear)
            teacherObj.areaOfInterest.add(subjectObj)
            teacherObj.save()
        print "Registration Successful"
        return HttpResponse(json.dumps({"validation":"Registration Successful.","redirecturl":"#/login","status":True}), content_type="application/json")

## teacher login
def teacher_login(request):
    data_dict = json.loads(request.body)
    username = data_dict['userName']
    password = data_dict['password']

    user = auth.authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            auth.login(request,user)
            print "Login Successful"
            return HttpResponse(json.dumps({"validation":"Login Successful","status":True,'redirecturl':"/userHome"}), content_type="application/json")
        else:
            print "Login Failed"
            return HttpResponse(json.dumps({"validation":"Invalid Login","status":False}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"validation":"Invalid Login Credentials","status":False}), content_type="application/json")

## assign teacher for lecture based on his/her Work Experience and Area Of Interest.
def assign_teacher_for_lecture(request):
    if request.user.is_authenticated():
        jsonObj = json.loads(request.body)
        #semester = jsonObj['semester']
        subjectName = jsonObj['subjectName'].strip()
        maxWorkExperience = Teacher.objects.filter(areaOfInterest__subjectName=subjectName).aggregate(Max('workExperience'))
        print maxWorkExperience
        teacherWithMaxWorkExperience = Teacher.objects.get(areaOfInterest__subjectName=subjectName,workExperience=maxWorkExperience.get('workExperience__max'))
        Obj = {"Teacher Name": teacherWithMaxWorkExperience.teacherName, "Qualification":teacherWithMaxWorkExperience.qualification,"workExperience":teacherWithMaxWorkExperience.workExperience}
        return HttpResponse(json.dumps({"validation":Obj,"status":True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"validation":"You are not logged in yet.Please login to continue.","status":False}), content_type="application/json")
