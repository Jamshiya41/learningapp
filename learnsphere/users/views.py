from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AdminRegistrationForm, InstructorRegistrationForm, StudentRegistrationForm, CustomUserForm, \
    InstructorForm, CourseForm, EventForm, BannerForm
from django.contrib.auth.decorators import user_passes_test, login_required

from .models import Instructors, Course, Event, Banner, Payment


def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page
    else:
        form = AdminRegistrationForm()
    return render(request, 'register.html', {'form': form, 'role': 'Admin'})

def register_instructor(request):
    if request.method == 'POST':
        form = InstructorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('instructor_list')
    else:
        form = InstructorRegistrationForm()
    return render(request, 'add_instructor.html', {'form': form, 'role': 'Instructor'})

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form, 'role': 'Student'})

def LogoutView(request):
    # Log the user out
    logout(request)

    # Redirect to home or login page
    return redirect('login')  # Or use redirect('/') for the home page

def admin_check(user):
    return user.role == 'admin'

@user_passes_test(admin_check)
def admin_dashboard(request):
    instructors_count = Instructors.objects.count()
    courses_count = Course.objects.count()
    events_count = Event.objects.count()
    context = {
        'instructors_count': instructors_count,
        'courses_count': courses_count,
        'events_count': events_count,

    }
    return render(request, 'admin_dashboard.html', context)

def instructor_dashboard(request):
    return render(request, 'instructor_dashboard.html')

def is_admin(user):
    return user.role == 'admin'

@user_passes_test(is_admin)
def admin_only_view(request):
    return render(request, 'users/admin_only.html')


@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return render(request, 'admin_dashboard.html')
    elif request.user.role == 'instructor':
        return render(request, 'instructor_dashboard.html')
    elif request.user.role == 'student':
        return render(request, 'users/student_dashboard.html')
    else:
        return render(request, 'users/unknown_role.html')

def instructor_list(request):
    instructors = Instructors.objects.all()
    return render(request, 'instructor_list.html', {'instructors': instructors})
# Edit Instructor
def edit_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructors, id=instructor_id)
    user = instructor.user  # Access the related CustomUser instance

    if request.method == 'POST':
        # Initialize both forms
        user_form = CustomUserForm(request.POST, instance=user)
        instructor_form = InstructorForm(request.POST, request.FILES, instance=instructor)

        if user_form.is_valid() and instructor_form.is_valid():
            user_form.save()  # Save the user details
            instructor_form.save()  # Save the instructor details
            messages.success(request, 'Instructor updated successfully!')
            return redirect('instructor_list')
    else:
        # Initialize both forms
        user_form = CustomUserForm(instance=user)
        instructor_form = InstructorForm(instance=instructor)

    return render(request, 'edit_instructor.html', {'user_form': user_form, 'instructor_form': instructor_form})


# Delete Instructor
def delete_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructors, id=instructor_id)

    if request.method == 'POST':
        # Optionally delete the related CustomUser as well
        user = instructor.user
        instructor.delete()  # Delete the instructor record
        user.delete()  # Delete the associated user record (if needed)

        messages.success(request, 'Instructor deleted successfully!')
        return redirect('instructor_list')

    return render(request, 'confirm_delete.html', {'instructor': instructor})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the course to the database
            return redirect('course_list')  # Redirect to the course list after adding
    else:
        form = CourseForm()

    return render(request, 'add_course.html', {'form': form})

# Edit Course
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)  # Fetch the course being edited
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course) # Bind the form to the instance
        if form.is_valid():
            form.save()  # Save changes
            messages.success(request, "Course updated successfully!")
            return redirect('course_list')  # Redirect to course list
    else:
        form = CourseForm(instance=course)  # Pre-fill the form with the course data

    return render(request, 'edit_course.html', {'form': form})
# Delete Course
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('course_list')

    return render(request, 'delete_course.html', {'course': course})


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)  # Important to include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})
# Edit Event
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_list')  # Replace with your URL name for the event list
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form})

# Delete Event
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('event_list')  # Replace with your URL name for the event list

    return render(request, 'delete_event.html', {'event': event})

def banner_list(request):
    banner = Banner.objects.all()
    return render(request, 'banner_list.html', {'banner': banner})

def add_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)  # Important to include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner added successfully!')
            return redirect('banner_list')
    else:
        form = BannerForm()
    return render(request, 'add_banner.html', {'form': form})
# Edit Event
def edit_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    if request.method == "POST":
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            messages.success(request, "Banner updated successfully!")
            return redirect('banner_list')  # Replace with your URL name for the event list
    else:
        form = EventForm(instance=banner)

    return render(request, 'edit_banner.html', {'form': form})

# Delete Event
def delete_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    if request.method == "POST":
        banner.delete()
        messages.success(request, "Banner deleted successfully!")
        return redirect('banner_list')  # Replace with your URL name for the event list

    return render(request, 'delete_banner.html', {'banner': banner})

def payment_list(request):
    payments = Payment.objects.all()  # Fetch all payment records
    return render(request, 'payments.html', {'payments': payments})
