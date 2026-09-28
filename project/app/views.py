from django.shortcuts import render,get_object_or_404
import razorpay
from .models import employee , Query
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def landing(req):
    return render(req,'landing.html')

def login(req):
    return render(req,'login.html')

def forgetpass(req):
    return render(req,'forgetpass.html')

def send_otp(req):
    if req.method == 'POST':
        e = req.POST.get('email')
        req.session['email']=e

        otp = random.randint(1111, 9999)
        req.session['classotp'] =otp
        send_mail(
            'OTP Verification',
            f'Generate OTP for Corporate Management System is {otp}',
            'roushanrajput12362@gmail.com',
            [e]
        )

        return render(req, 'verify_otp.html')

    return render(req, 'forgetpass.html')


def verify_otp(req):
    if req.method == 'POST':
        user_otp = req.POST.get('otp')
        session_otp = req.session.get('classotp')
        print(session_otp)
        if user_otp == session_otp:
            return render(req, 'resetpass.html')
        else:
            print("OTP wrong")
            return render(req, 'verify_otp.html')
    return render(req, 'verify_otp.html')

def Reset_data(req):
    if (req.method=='POST'):
        p=req.POST.get('Reset_pass')
        cp=req.POST.get('Reset_cpass')
        e=req.session['email']
        print(e)

        print(p,cp)
        if p==cp:
            emp_details=employee.objects.get(email=e)
            print(emp_details.name)

def empdashboard(req):
    return render(req,'empdashboard.html')

def admindashboard(req):
    return render(req,'admindashboard.html')

def add_emp(req):
    return render(req,'add_emp.html')

def login_data(req):
    if req.method == 'POST':
        e = req.POST.get('email')
        p = req.POST.get('pass')
        if e == 'roushanrajput12362@gmail.com' and p == '12362':
            return render(req, 'admindashboard.html')
        m= employee.objects.filter(email=e)
        if m :
            req.session['emp_email'] = e               #session me save krne ke liye aise hm use krte h 
            return render(req, 'empdashboard.html')
        else:
            return render(req, 'login.html', {'error': 'Email ya Password galat hai'})


def emp_data(req):
    if req.method == 'POST':
        e  = req.POST.get('empid')
        n  = req.POST.get('empname')
        em = req.POST.get('empemail')
        p  = req.POST.get('empposition')
        c  = req.POST.get('empcontact')
        s  = req.POST.get('empsalary')
        cp = req.POST.get('emppassword')

        # Duplicate check
        if employee.objects.filter(email=em).exists() or employee.objects.filter(empid=e).exists():
            msg = 'E-mail ya Employee ID already exists!'
            return render(req, 'add_emp.html', {'msg': msg})

        # Save to database
        employee.objects.create(
            empid=e,
            name=n,
            email=em,
            contact=c,
            position=p,
            salary=s,
            Password=cp
        )
        print(e,n,em,c,p,s,)

        # Send email
        send_mail(
            'Company Login Details',

            f"""Hello {n},

Your account has been created.
your data is shown Here!
Email: {em}
Password: {cp}
Please keep this information safe.Maintain your Privacy.

Thanks,
Company Team
""",
            'roushanrajput12362@gmail.com',
            [em],
            fail_silently=False
        )

        return render(req, 'admindashboard.html')

    return render(req, 'add_emp.html')

# def profile(req):

def show_emp(req):
    emp=employee.objects.all()
    data=[]
    for i in emp:
        data.append({
            'empid':i.empid,
            'name':i.name,
            'email':i.email,
            'contact':i.contact,
            'position':i.position,
            'salary':i.salary,
            'Password':i.Password,
        })
    return render(req,'showemp.html', {'emp': emp})

def edit_employee(req,pk):
    print(pk)
    userdata = employee.objects.get(id=pk)
    
    data={
        'id':userdata.empid,
        'name':userdata.name,
        'email':userdata.email,
        'contact':userdata.contact,
        'position':userdata.position,
        'salary':userdata.salary,
        'Password':userdata.Password,
    }
    return render(req,'add_emp.html',{'data':data})

def update_data(req,pk):
    if (req.method=='POST'):
        e=req.POST.get('empid')
        n=req.POST.get('empname')
        em=req.POST.get('empemail')
        p=req.POST.get('empposition')
        c=req.POST.get('empcontact')
        s=req.POST.get('empsalary')
        cp=req.POST.get('emppassword')

        data = employee.objects.get(empid=pk)

        data.empid=e
        data.name=n
        data.email=em
        data.contact=c
        data.position=p
        data.salary=s
        data.Password=cp
        data.save()

        send_mail(
            'Company Details are updated',
            f"""Hello {n},

Your account Details has been Updated.
your new data is shown Here!
Employee ID:{e}
Name:{n}
Email: {em}
Position:{p}
Salary:{s}
Password:{cp}

Please keep this information safe.

Thank You!!,
Company Team
""",
            'roushanrajput12362@gmail.com',
            [em],
            fail_silently=False
        )

        return render(req, 'showemp.html')
    
def emp_query(req):
    if req.method=='POST':
        user=req.session.get('emp_email')
        ti=req.POST.get('title')
        mssg=req.POST.get('query')

        Query.objects.create(employe_mailid=user,title=ti,question=mssg)

    return render(req,'empdashboard.html',)

def showquery(req):
    queries=Query.objects.all()
    return render(req,'showquery.html',{'queries':queries})

def attendance(req):
    return render(req,'attendance.html')

def leaves(req):
    return render(req,'leaves.html')

def Pay_salary(request,pk):
    emp = employee.objects.get(id=pk)   # ya jo tumhara model hai
    print(emp)
    request.session["emp"]=pk
    return render(request, "paycard.html", {"emp": emp})

@csrf_exempt
def payment(request):
    global payment
    if request.method == "POST":
        # amount in paisa
        salary = int(request.POST.get('amount'))
        amount = salary* 100
        print(amount)
        client = razorpay.Client(auth =("rzp_test_SBgtTkwvybHJf0" , "gY3kY8r2vLVW4obdtOE95aVC"))
        # create order
        
        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        print(payment)
        empid = request.session.get("emp")
        emp = employee.objects.get(id=empid)
        
        # print(payment)
        return render(request,'paycard.html',{'amount':salary,'payment':payment,"emp":emp})
    
@csrf_exempt
def payment_status(request):
    em=request.POST.get('empemail')
    if request.method != "POST":
        
        return render("admindashboard")

    client = razorpay.Client(
        auth=("rzp_test_SBgtTkwvybHJf0", "gY3kY8r2vLVW4obdtOE95aVC")
    )

    data = {
        'razorpay_order_id': request.POST.get('razorpay_order_id'),
        'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
        'razorpay_signature': request.POST.get('razorpay_signature')
    }

    try:
        client.utility.verify_payment_signature(data)

        emp= employee.objects.get(order_id=data['razorpay_order_id'])
        emp.razorpay_payment_id = data['razorpay_payment_id']
        

        emp.paid = True
        send_mail(
            'Company Details are updated',
            f"""Hello {em},
Your Salary Was Credited In Your Bank Account .

Please keep this information safe.

Thank You!!,
Company Team
""",
            'roushanrajput12362@gmail.com',
            [em],
            fail_silently=False
        )
        emp.save()
        return render(request, 'showemp.html', {'status': True})
    
    except:
        return render(request, 'showemp.html', {'status': False})

def del_employee(req,pk):
        userdata=employee.objects.get(id=pk)
        em=req.POST.get('empemail')
    
        userdata.delete()
        send_mail(
            'From XYZ Company',
            f"""Hello {em},
Your Account Was Delected Successfully from XYZ Company.
All the Best For your Future.

Thank You!!,
Company Team
""",
            'roushanrajput12362@gmail.com',
            [em],
            fail_silently=False
        )
        return render(req,'showemp.html')

def logout(req):
    if req.session.get('admin'):
        req.session.flush()
    return render(req,'landing.html')