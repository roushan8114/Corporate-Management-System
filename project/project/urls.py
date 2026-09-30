"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.landing,name='landing'),
    path('login/',views.login,name='login'),
    path('login_data/',views.login_data,name='login_data'),
    path('forgetpass/',views.forgetpass,name='forgetpass'),
    path('send_otp/',views.send_otp,name='send_otp'),
    path('verify_otp',views.verify_otp,name='verify_otp'),    
    path('Reset_data',views.Reset_data,name='Reset_data'),    
    path('empdashboard',views.empdashboard,name='empdashboard'),
    path('admindashboard',views.admindashboard,name='admindashboard'),
    path('attendance',views.attendance,name='attendance'),
    path('leaves',views.leaves,name='leaves'),
    path('reports',views.reports,name='reports'),
    
    
    path('add_emp/',views.add_emp,name='add_emp'),
    path('emp_data/',views.emp_data,name='emp_data'),
    path('show_emp/',views.show_emp,name='show_emp'),
    path('edit_employee/<int:pk>/',views.edit_employee,name='edit_employee'),
    path('showquery/',views.showquery,name='showquery'),
    path('logout/',views.logout,name='logout'),
    path('Pay_salary/<int:pk>',views.Pay_salary,name='Pay_salary'),
    
    path('update_data/<str:pk>/',views.update_data,name='update_data'),
    path('del_employee/<int:pk>/',views.del_employee,name='del_employee'),

    # for Queries
    path('emp_query/',views.emp_query,name='emp_query'),

    # for payments
    path('payment/',views.payment,name='payment'),

    path('payment_status/',views.payment_status,name='payment_status')
    
]
