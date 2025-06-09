from django.shortcuts import render,redirect

from django.views import View

from courses.models import Courses

from .models import Payments,Transactions
# Create your views here.

from students.models import Students

import razorpay

import datetime


from decouple import config

class EnrollConfirmationView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        course = Courses.objects.get(uuid=uuid)

        payment,created = Payments.objects.get_or_create(student=Students.objects.get(profile=request.user),course=course,amount= course.offer_fee if course.offer_fee else course.fee)


        data = {'payment':payment}

        return render(request,'payments/enroll-confirmation.html',context=data)
    

class RazorpayView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        course = Courses.objects.get(uuid=uuid)

        payment = Payments.objects.get(student__profile = request.user,course=course)

        transaction = Transactions.objects.create(payment=payment)

        print(config("RZP_CLIENT_ID"))

        client = razorpay.Client(auth=('rzp_test_bGEeEr9cRMTArM', 'W1BZXfBBXKdHnbou591mAm5g'))

        data = { "amount": payment.amount*100, "currency": "INR", "receipt": "order_rcptid_11" }

        order = client.order.create(data=data) # Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
        
        rzp_order_id = order.get('id')

        transaction.rzp_order_id = rzp_order_id

        transaction.save()

        data = {'client_id':'rzp_test_bGEeEr9cRMTArM','rzp_order_id':rzp_order_id,'amount':payment.amount*100}

        
        return render(request,'payments/payment-page.html',context=data)
    

class PaymentVerifyView(View):

    def post(self,request,*args,**kwargs):

        rzp_order_id = request.POST.get('razorpay_order_id')

        rzp_payment_id = request.POST.get('razorpay_payment_id')

        rzp_payment_signature = request.POST.get('razorpay_signature')

        client = razorpay.Client(auth=("rzp_test_bGEeEr9cRMTArM", "W1BZXfBBXKdHnbou591mAm5g"))

        transaction = Transactions.objects.get(rzp_order_id=rzp_order_id)

        time_now =   datetime.datetime.now()  

        transaction.transaction_at = time_now

        transaction.rzp_payment_id = rzp_payment_id

        transaction.rzp_payment_signature = rzp_payment_signature

        try :
            
            client.utility.verify_payment_signature({
                                            'razorpay_order_id': rzp_order_id,
                                            'razorpay_payment_id': rzp_payment_id,
                                            'razorpay_signature': rzp_payment_signature
                                            })
            
            transaction.status = 'Success'

            transaction.save() 

            transaction.payment.status = 'Success'

            transaction.payment.paid_at = time_now

            transaction.payment.save()

            return redirect('home') 

        except:

            transaction.status = 'Failed'

            transaction.save()   

            return redirect('razorpay-view',uuid=transaction.payment.course.uuid)  

           
