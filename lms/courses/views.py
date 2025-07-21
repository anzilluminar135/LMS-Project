from django.shortcuts import render,redirect

from django.views import View

from .models import Courses,CategoryChoices,LevelChoices

from .forms import CourseCreateForm

from instructors.models import Instructors

from django.db.models import Q

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from authentication.permissions import permission_roles

from lms.utility import get_recommended_courses


# Create your views here.


# courses list and create

class CoursesListView(View):

    def get(self,request,*args,**kwargs):

    #    fetching all courses from Courses Model

        query = request.GET.get('query')

        courses = Courses.objects.all()

        if query :

            courses = Courses.objects.filter(Q(title__icontains=query)|
                                             Q(description__icontains=query)|
                                             Q(instructor__name__icontains=query)|
                                             Q(category__icontains=query)|
                                             Q(type__icontains=query)|
                                             Q(level__icontains=query)|
                                             Q(fee__icontains=query))

        

        data = {'courses':courses,'page':'courses-page','query':query}

        return render(request,'courses/courses-list.html',context=data)

class CoursesDetailView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        course = Courses.objects.get(uuid=uuid)

        recommended_courses = get_recommended_courses(course)

        data = {'course':course,'recommended_courses':recommended_courses}


        return render(request,'courses/course-details.html',context=data)

class HomeView(View):

    def get(self,request,*args,**kwargs):

        data = {'page':'home-page'}

        return render(request,'courses/home.html',context=data)
    

# @login_required(login_url='login')

# @method_decorator(login_required(login_url='login'),name='dispatch')

@method_decorator(permission_roles(roles=['Instructor']),name='dispatch')
class InstructorCoursesListView(View):

    def get(self,request,*args,**kwargs):

        instructor = Instructors.objects.get(profile=request.user)

        courses = Courses.objects.filter(instructor=instructor)

        # instructor.courses_set.filter()

        data = {'page':'instructor-courses-page','courses':courses}

        return render(request,'courses/instructor-courses-list.html',context=data)
    
# @method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(permission_roles(roles=['Instructor']),name='dispatch')
class InstructorCoursesDetailView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        course = Courses.objects.get(uuid=uuid)

        data = {'course':course}

        return render(request,'courses/instructor-course-detail.html',context=data)
    

# @method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(permission_roles(roles=['Instructor']),name='dispatch')
class InstructorCourseDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        course = Courses.objects.get(uuid=uuid)

        course.delete()

        return redirect('instructor-courses-list') 
    
# @method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(permission_roles(roles=['Instructor']),name='dispatch')
class InstructorCourseUpdateView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        course = Courses.objects.get(uuid=uuid)

        form = CourseCreateForm(instance=course)

        data = {'form':form}

        return render(request,'courses/instructor-course-update.html',context=data)
    
    def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        course = Courses.objects.get(uuid=uuid)

        form = CourseCreateForm(request.POST,request.FILES,instance=course)

        if form.is_valid():

            form.save()

            return redirect('instructor-courses-list')
        
        data = {'form':form}

        return render(request,'courses/instructor-course-update.html',context=data)
    


#  normal way

# class CourseCreateView(View):

#     def get(self,request,*args,**kwargs):

#         data = {'categories':CategoryChoices,'levels':LevelChoices}

#         return render(request,'courses/course-create.html',context=data)
    

#     def post(self,request,*args,**kwargs):

#         form_data = request.POST

#         image = request.FILES.get('image')

#         title = form_data.get('title')

#         description = form_data.get('description')

#         category = form_data.get('category')

#         level = form_data.get('level')

#         fee = form_data.get('fee')

#         offer_fee = form_data.get('offer_fee')

#         instructor = 'John Doe'

#         course = Courses.objects.create(title=title,description=description,image=image,
                               
#                                category=category,level=level,instructor=instructor,

#                                fee=fee,offer_fee=offer_fee

#                                )
        
#         course.save()
        
#         return redirect('instructor-courses-list')


# with the help of django forms
# @method_decorator(login_required(login_url='login'),name='dispatch')
@method_decorator(permission_roles(roles=['Instructor']),name='dispatch')
class CourseCreateView(View):

    def get(self,request,*args,**kwargs):

        form = CourseCreateForm()

        data = {'form':form}

        return render(request,'courses/course-create.html',context=data)
    

    def post(self,request,*args,**kwargs):

        form = CourseCreateForm(request.POST,request.FILES)

        instructor = Instructors.objects.get(id=1)

        if form.is_valid():

            # print(form.cleaned_data)

            # form.cleaned_data['instructor'] = 'John Doe'

            # form.save()
            
            
            course=form.save(commit=False)

            course.instructor = instructor

            course.save()

            return redirect('instructor-courses-list')
        
        data = {'form':form}
        
        return render(request,'courses/course-create.html',context=data)
    

   
    










        

        


    