from django import forms

from .models import Courses,CategoryChoices,LevelChoices,TypeChoices

class CourseCreateForm(forms.ModelForm):

    class Meta :

        model = Courses

        # fields = ['title','description','image','category','level','fee','offer_fee']
        # fields = '__all__'
        exclude = ['instructor','uuid','active_status']

        widgets = {

            'title': forms.TextInput(attrs={
                                            'class': 'form-control',

                                            'placeholder':'Enter Course Name',

                                            'required':'required'

                                           }),

           'image':forms.FileInput(attrs={
                                         
                                         'class': 'form-control'
                                        
               
                                         }),

            'description' : forms.Textarea(attrs={

                                                 'class': 'form-control',

                                                 'placeholder':'Enter Course Description',

                                                 'required':'required'

                                                 }) ,

            'fee': forms.NumberInput(attrs={
                                       'class':'form-control',

                                       'required':'required',

                                       'placeholder':'Enter Course Fee'
                                       
                                           }),

            'offer_fee': forms.NumberInput(attrs={

                                       'class':'form-control',

                                       'placeholder':'Enter Offer Fee'

                                           })                                                               

        }  
    

    category = forms.ChoiceField(choices=CategoryChoices.choices,widget=forms.Select(attrs={
                                                                                            
                                                                                            'class':'form-select',
                                                                                            
                                                                                            'required':'required'

                                                                                           })) 
    
    level = forms.ChoiceField(choices=LevelChoices.choices,widget=forms.Select(attrs={
                                                                                            
                                                                                            'class':'form-select',

                                                                                            'required':'required'

                                                                                           })) 
    type = forms.ChoiceField(choices=TypeChoices.choices,widget=forms.Select(attrs={
                                                                                            
                                                                                            'class':'form-select',

                                                                                            'required':'required'

                                                                                           }))


    def clean(self):

        validated_data = super().clean()

        if validated_data.get('fee') and validated_data.get('fee') < 0 :

            self.add_error('fee','course fee must be greater than zero')

        if validated_data.get('offer_fee') and validated_data.get('offer_fee') < 0 :

            self.add_error('offer_fee','offer fee must be greater than zero')

        return validated_data
    
    def __init__(self,*args,**kwargs):

        super(CourseCreateForm,self).__init__(*args,**kwargs)

        if not self.instance :

            self.fields.get('image').widget.attrs['required'] = 'required'
    
    