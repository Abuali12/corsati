from .models import Lead, Center, Course, Subject, State
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CenterForm(forms.ModelForm):
    class Meta:
        model= Center
        fields= ['title','logo','discription','subjects','contact_phone','center_type','contact_email','website', 'state', 'address', 'latitude', 'longitude']
        widgets={
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
    

class CourseForm(forms.ModelForm):
    error_css_class= 'error'
    required_css_class= 'required'
    use_required_attribute= True
    class Meta:
        model= Course
        fields= ['title', 'subjects', 'image', 'short_discription','learning_outcomes','course_instructor', 'about_instructor', 'details', 'length', 'course_type', 'price', 'currency', 'installment_available', 'installment_details', 'address', 'online_platform']


class LeadForm(forms.ModelForm):
    class Meta:
        model= Lead
        fields= ['student_name', 'student_phone', 'student_email', 'note']

class SubjectForm(forms.ModelForm):
    class Meta:
        model= Subject
        fields= '__all__'

class StateForm(forms.ModelForm):
    class Meta:
        model= State
        fields= '__all__'

