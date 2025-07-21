from django.urls import path
from . import views
urlpatterns =[

    path('course-detail/<str:uuid>/',views.CoursesDetailView.as_view(),name='course-detail'),

    path('home/',views.HomeView.as_view(),name='home'),

    path('instructor-courses-list/',views.InstructorCoursesListView.as_view(),name='instructor-courses-list'),

    path('create-course/',views.CourseCreateView.as_view(),name='create-course'),
    
    path('instructor-course-detail/<str:uuid>/',views.InstructorCoursesDetailView.as_view(),name='instructor-course-detail'),

    path('instructor-course-delete/<str:uuid>/',views.InstructorCourseDeleteView.as_view(),name='instructor-course-delete'),

    path('instructor-course-update/<str:uuid>/',views.InstructorCourseUpdateView.as_view(),name='instructor-course-update'),
]