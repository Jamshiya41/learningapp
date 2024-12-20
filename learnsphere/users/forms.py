from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Instructors, Course, Event, Banner


class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'admin'
        if commit:
            user.save()
        return user


class InstructorRegistrationForm(UserCreationForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instructor Name'}),
        required=True
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short Bio'}),
        required=False
    )
    expertise = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Python, Data Science'}),
        required=False
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        required=False
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instructor UserName'}),
        required=True
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instructor Email'}),
        required=True
    )
    password1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instructor password'}),
        required=True
    )
    password2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instructor confirm password'}),
        required=True
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'name', 'bio', 'expertise', 'image']

    def save(self, commit=True):
        # Save user fields first
        user = super().save(commit=False)
        user.role = 'instructor'
        if commit:
            user.save()

        # Save additional Instructor fields
        Instructors.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            bio=self.cleaned_data['bio'],
            expertise=self.cleaned_data['expertise'],
            image=self.cleaned_data['image']
        )

        return user
class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructors
        fields = ['name', 'email','bio', 'expertise', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instructor Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short Bio'}),
            'expertise': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Expertise'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']
class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user

class CourseForm(forms.ModelForm):
    instructor = forms.ModelChoiceField(
        queryset=Instructors.objects.all(),  # Fetch all instructors from the database
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select an Instructor"  # Optional: Placeholder for the dropdown
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'instructor', 'duration', 'price','image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Course Description'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 10 hours'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            # Widget for image field
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location','image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Event Description'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event venue'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            # Widget for image field
        }

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'subtitle', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'subtitle': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Event Description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            # Widget for image field
        }
    # Example: Custom validation for the title
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("The title must be at least 5 characters long.")
        return title