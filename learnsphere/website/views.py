import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from users.models import Course, Instructors, Event, Banner, Payment


# Create your views here.
def home(request):
    courses = Course.objects.all()
    banner = Banner.objects.last()  # Get the most recently created banner
    trainers = Instructors.objects.all()
    return render(request, 'home.html', {'banner': banner,'courses': courses,'trainers': trainers})
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})
def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_details.html', {'course': course})
def trainers(request):
    trainers = Instructors.objects.all()
    return render(request, 'trainers.html', {'trainers': trainers})
def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout_session(request, plan_id):
    plan = Course.objects.get(id=plan_id)
    # Stripe Checkout Session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': plan.title,
                        'description': plan.description,
                    },
                    'unit_amount': int(plan.price * 100),  # Convert price to cents
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri('/payment_success/') + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri('/payment_cancel/'),
    )
    return redirect(checkout_session.url)
def payment_success(request):
        # Fetch the session_id from the query parameters
        session_id = request.GET.get('session_id')

        if not session_id:
            return render(request, 'payment_cancel.html',
                          {'error': 'Invalid session ID. Payment could not be verified.'})

        try:
            # Retrieve the Stripe Checkout session details
            sessions = stripe.checkout.Session.retrieve(session_id)
            # Extract customer information and payment details
            customer_email = sessions.customer_details.get('email')
            amount_total = sessions.amount_total / 100  # Convert from cents to dollars
            currency = sessions.currency
            stripe_payment_id = sessions.payment_intent

            # Create a new Payment record in your database
            payment = Payment.objects.create(
                stripe_payment_id=stripe_payment_id,
                customer_email=customer_email,
                amount=amount_total,
                currency=currency,
                status="Success",  # You can update this based on the session status
            )

            # Pass the payment details to the success template
            context = {
                'customer_email': customer_email,
                'amount': amount_total,
                'currency': currency,
                'payment': payment,  # Optional, to display payment details
            }

            return render(request, 'payment_success.html', context)

        except stripe.error.StripeError as e:
            # Handle any errors with Stripe
            print("Stripe Error:", e)
            return render(request, 'payment_cancel.html', {'error': str(e)})

def payment_cancel(request):
    return render(request, 'payment_cancel.html')