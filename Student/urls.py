from django.urls import path
from Student.views import *
urlpatterns = [
    path('', indexpg, name='indexpg'),
    path('signin/', user_login, name='signin'),
    path('regis/', signup, name='regis'),
    path('home/', home, name='home'),
    
    path('profile/', myProfile, name='profile'),
    # path('forgot/', changePassword, name='changePassword'),
    path('logout/', Logout, name='logout'),
    path('mark/', mark, name='mark'),
    path('track/', track, name='track'),
     path('generate-excel/<str:course_name>/<int:attended>/<int:total>/<str:attendance_percentage>/', generate_excel, name='generate_excel'),


path('flogin/', loginpage, name='login'),
path('homepage/', homepage, name='homepage'),
path('main/', mainpage, name='mainpage'),
path('about/', about, name='about'),
path('tracking', tracking, name='tracking'),
path('contact/', contact, name='contact'),
path('help/', help, name='help'),
path('r/', attendance_report, name='attendance_report'),
path('generate_excel/<str:subject>/', generate_excel, name='generate_excel'),

]
