from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    idcode = models.CharField(max_length=12, null=True) 
    dob = models.DateField(null=True)
    contnum = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.user.first_name
    
class markatt(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=350, null=True)
    subject = models.CharField(max_length=150, null=True)
    attendanceNo = models.CharField(max_length=150, null=True)
    # image = models.ImageField(upload_to='attendance_images/', null=True, blank=True)


    def __str__(self):
        return self.attendanceNo 
    
# models.py


class AbsentNote(models.Model):
    issue = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Absent Note created at {self.created_at}"

    
# -------------Faculty---------------------------
    
class FacultyLogin(models.Model):
    fac_name = models.CharField(max_length=100)
    fac_pass = models.CharField(max_length=100)

    def __str__(self):
        return self.fac_name
    
class Notice(models.Model):
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True,null=True)


    def __str__(self):
        return self.text
    
class TimeSlot(models.Model):

    subject = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    photo = models.ImageField(upload_to='timeslot_photos', null=True, blank=True)
    latitude = models.TextField(null=True)  
    longitude = models.TextField(null=True)  

    def __str__(self):
        return f"{self.subject} - {self.date} - {self.start_time} to {self.end_time}"

