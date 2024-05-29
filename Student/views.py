from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
import random
from django.db.models import Count, F, FloatField, ExpressionWrapper
import openpyxl
from django.http import HttpResponse
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime, time
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def indexpg(request):
    return render(request, 'index.html')

def signup(request):
    error = ""
    if request.method == "POST":
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        idcode = request.POST['idcode']
        email = request.POST['emailid']
        password = request.POST['password']

        try:
            user = User.objects.create_user(username=email, password=password, first_name=fname, last_name=lname)
            UserDetails.objects.create(user=user, idcode=idcode)
            error = "no"
        except:
            error = "yes"
    return render(request, 'registration/stureg.html', locals())

def user_login(request):
    error = ""
    if request.method == 'POST':
        e = request.POST['emailid']
        p = request.POST['password']
        user = authenticate(username=e, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'login/stulogin.html', locals())

def home(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    notices = Notice.objects.all()
    if request.method == 'POST':
        issue = request.POST.get('issue')
        AbsentNote.objects.create(issue=issue)
        return redirect('home')
    return render(request, 'dashboard/stuDash.html', {'notices': notices})

def myProfile(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    user = User.objects.get(id=request.user.id)
    userDtls = UserDetails.objects.get(user=user)
    

    if request.method == "POST":
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        dob = request.POST['dob']
        idcode = request.POST['idcode']

        userDtls.user.first_name = fname
        userDtls.user.last_name = lname
        userDtls.dob = dob 
        userDtls.idcode = idcode

        try:
            userDtls.save()
            userDtls.user.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'dashboard/sp/sprofile.html', locals())

# def changePassword(request):
#     if not request.user.is_authenticated:
#         return redirect('signin')
#     error = ""
#     user = request.user
#     if request.method == "POST":
#         c = request.POST['confirmpassword']
#         n = request.POST['newpassword']
#         try:
#             user_email = request.user.email
#             u = User.objects.get(email=user_email)
#             if user.check_password(c):
#                 u.set_password(n)
#                 u.save()
#                 error = "no"
#             else:
#                 error = 'not'
#         except:
#             error = "yes"
#     return render(request, 'forget.html', locals())


def Logout(request):
    logout(request)
    return redirect('indexpg')

def mark(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    users = User.objects.get(id=request.user.id)
    userdtls = UserDetails.objects.get(user=users)
    subjects = TimeSlot.objects.values_list('subject', flat=True).distinct()
    
    if request.method == 'POST':
        subject = request.POST.get('subject') 
        current_time = datetime.now().time()
        current_date = datetime.now().date()

        photo = request.FILES.get('photo')
        
        try:
            time_slot = TimeSlot.objects.get(subject=subject, date=current_date)
            if time_slot.start_time <= current_time <= time_slot.end_time:
                if photo:
                    # Save the uploaded photo to the file system
                    time_slot.photo.save(photo.name, photo)

                # Create a new markatt record
                attendance_record = markatt.objects.create(
                    user=userdtls,
                    subject=subject,
                    attendanceNo="some_unique_identifier"  # Generate or retrieve an appropriate identifier
                )

                # Save the attendance record
                attendance_record.save()

                return HttpResponse("Attendance marked successfully.")
            else:
                return HttpResponse("Attendance can only be marked during the specified time slot.")
        except TimeSlot.DoesNotExist:
            return HttpResponse("No time slot defined for the selected subject and date.")
    else:
        return render(request, 'dashboard/attendance/markatt.html',  {'userdtls': userdtls, 'subjects': subjects})
    
def track(request):
     subject_scheduled = None
     if request.method == 'POST':
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        latitude_str = request.POST.get('latitude')  # Add latitude extraction
        longitude_str = request.POST.get('longitude')

        # Convert start_time and end_time to Time objects
        start_time = datetime.strptime(start_time, '%H:%M').time()
        end_time = datetime.strptime(end_time, '%H:%M').time()
       
        latitude = [float(val.strip()) for val in latitude_str.split(',')]
        longitude = [float(val.strip()) for val in longitude_str.split(',')]

        # Create a new TimeSlot instance
        time_slot = TimeSlot.objects.create(  
            subject=subject,
            date=date,
            start_time=start_time,
            end_time=end_time,
            latitude=latitude[0],  # Take the first value from the list
            longitude=longitude[0]
        )
        subject_scheduled = subject

     else:
        pass
        
     return render(request, 'faculty/tracking.html', {'subject_scheduled': subject_scheduled})


def extract_location_from_image(image_field):
    if image_field:
        image = Image.open(image_field)
        exif_data = image._getexif()

    if exif_data:
        location = None
        time = None
        for tag, value in exif_data.items():
            decoded_tag = TAGS.get(tag, tag)
            if decoded_tag == 'GPSInfo':
                gps_info = {}
                for t, v in value.items():
                    sub_decoded_tag = GPSTAGS.get(t, t)
                    gps_info[sub_decoded_tag] = v

                latitude = gps_info.get('GPSLatitude')
                longitude = gps_info.get('GPSLongitude')
                location = (latitude, longitude)
    
            elif decoded_tag == 'DateTimeOriginal':
                time = value

        return location, time

    return None, None

def loc(request):
    timeslot = TimeSlot.objects.first()  # For example, getting the first timeslot
    
    # Extract location and time from the image
    location, time = extract_location_from_image(timeslot.photo)

    if location:
        latitude, longitude = location
        timeslot.latitude = latitude
        timeslot.longitude = longitude
        timeslot.save()
    else:
        # Handle the case when location is not extracted
        latitude = None
        longitude = None
    
    # Pass the extracted information to the template
    context = {
        'timeslot': timeslot,
        'latitude': latitude,
        'longitude': longitude,
        'time': time
    }

    return render(request, 'myloc.html', context)


# def track(request):
#     if not request.user.is_authenticated:
#         return redirect('signin')
    
#     user = User.objects.get(id=request.user.id)
#     user_details = UserDetails.objects.get(user=user)
#     my_attendance = markatt.objects.filter(user=user_details)

#     # Calculate attendance stats for each course
#     course_attendance = {}
#     for attendance in my_attendance:
#         course_name = attendance.subject
#         if course_name not in course_attendance:
#             course_attendance[course_name] = {
#                 'attended': 0,
#                 'total': 0,
#                 'attendance_percentage': 0
#             }
#         course_attendance[course_name]['attended'] += 1
#         course_attendance[course_name]['total'] += 1
    
#     # Calculate attendance percentage
#     for course in course_attendance:
#         attendance_data = course_attendance[course]
#         total_classes = attendance_data['total']
#         attended_classes = attendance_data['attended']
#         if total_classes > 0:
#             attendance_data['attendance_percentage'] = (attended_classes / total_classes) * 100

#     return render(request, 'dashboard/attendance/attrep.html', {'course_attendance': course_attendance})

def generate_excel(request, course_name, attended, total, attendance_percentage):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.xlsx"'

    # Create a new workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Add headers
    sheet.append(['Course Name', 'Class Attended', 'Number of Classes', 'Attendance %'])

    # Add data
    sheet.append([course_name, attended, total, attendance_percentage])

    # Save the workbook to the HttpResponse
    workbook.save(response)

    return response



# -----------------FACULTY--------------------------------------

def loginpage(request):
    error = ""
    if request.method == 'POST':
        fac_name = request.POST.get('fac_name')
        fac_pass = request.POST.get('fac_pass')
        try:
            faculty_login = FacultyLogin.objects.get(fac_name=fac_name, fac_pass=fac_pass)
            # Authentication successful, redirect to a new page or perform other actions
            return redirect('homepage')
            error = "no"
        except FacultyLogin.DoesNotExist:
            pass
        error = "yes"
    
    return render(request,'faculty/Flogin.html', locals())

def homepage(request):
    absnote = AbsentNote.objects.all()
    if request.method == 'POST':
        text = request.POST.get('issue')
        Notice.objects.create(text=text)
        return redirect('homepage')
    return render(request, 'faculty/homepage.html',{'absnote': absnote})

def mainpage(request):
    return render(request,'faculty/main.html')

def about(request):
    return render(request,'faculty/about.html')

def tracking(request):
    return render(request,'faculty/tracking.html')

def contact(request):
    return render(request,'faculty/contact.html')

def help(request):
    return render(request,'faculty/help.html')

    
def attendance_report(request):
    users = UserDetails.objects.all()
    queryset = markatt.objects.all()
    
    # return render(request,'faculty/attendance_report.html',{'user':user,'queryset':queryset})
    # return render(request,'dashboard/attendance/attrep.html',{'user':user,'queryset':queryset})

    # Process attendance data
    attendance_data = {}
    for entry in queryset:
        user_name = entry.user.user.first_name + ' ' + entry.user.user.last_name
        subject = entry.subject
        if subject not in attendance_data:
            attendance_data[subject] = {}
        if user_name not in attendance_data[subject]:
            attendance_data[subject][user_name] = 0
        attendance_data[subject][user_name] += 1

    return render(request, 'dashboard/attendance/attrep.html', {'attendance_data': attendance_data})

def generate_excel(request, subject):
    queryset = markatt.objects.filter(subject=subject)
    
    # Create an Excel workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance Report"
    
    # Set headers
    ws.append(["Student Name", "Number of Classes Attended"])

    # Add data
    attendance_count = {}
    for entry in queryset:
        user_name = entry.user.user.first_name + ' ' + entry.user.user.last_name
        if user_name not in attendance_count:
            attendance_count[user_name] = 0
        attendance_count[user_name] += 1

    for user_name, count in attendance_count.items():
        ws.append([user_name, count])
    
    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={subject}_attendance_report.xlsx'
    wb.save(response)
    return response

# --------------------ADMIN---------------------------


    