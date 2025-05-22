from django.shortcuts import render

from django.views import View

# Create your views here.


class StudentRegisterView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'students/student-register.html')