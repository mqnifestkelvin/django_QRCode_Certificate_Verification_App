from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from . models import Certificate
from .forms import VerifyForm, EmailForm, OTPForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.core.mail import send_mail
import random
import datetime
import json


def verify(request):
    user_form = VerifyForm(request.POST or None)

    if request.method == 'POST' and user_form.is_valid():
        encrypted_byte_code = user_form.cleaned_data.get('encrypted_byte_code')

        try:
            certificate = Certificate.objects.get(encrypted_byte_code=encrypted_byte_code)

            # Store the harshcode (encrypted_byte_code) in the session for later verification
            request.session['userHarshcode'] = encrypted_byte_code

            # Redirect to the email verification page
            return redirect('enter-email')
        except Certificate.DoesNotExist:
            return redirect('inexistent')

    return render(request, 'certificate/verify.html', {'user_form': user_form})


def exist(request, certificate_slug=None):
    # Check if the user has been verified
    if not request.session.get('verified_access'):
        return redirect('select')

    try:
        # Fetch the certificate details
        user_certificate = Certificate.objects.get(slug=certificate_slug)
    except Certificate.DoesNotExist:
        return redirect('inexistent')

    context = {'user_certificate': user_certificate}
    
    # Clear the verified_access to make it a one-time access
    if 'verified_access' in request.session:
        del request.session['verified_access']

    return render(request, 'certificate/exist.html', context=context)


def inexistent(request):
    return render(request, 'certifications/inexistent.html')


def qr_scan_redirect(request, hashcode=None):
    # Store the hashcode in the session
    request.session['userHarshcode'] = hashcode

    # Redirect the user to the email input view
    return redirect('enter-email')


@method_decorator(csrf_exempt, name='dispatch')
def qr_scan_view(request):
    return render(request, 'certificate/qr-scan.html')


def select_option(request):
    if request.method == 'POST':
        method = request.POST.get('verificationMethod')
        if method == 'hashcode':
            # Handle hash code verification
            return redirect('verify')
        elif method == 'qrcode':
            # Handle QR code verification
            return redirect('qr-scan')
    else:
        return render(request, 'certificate/select.html')


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    subject = 'Certificate Verfication OTP'
    message = f'Your OTP code is: {otp}'
    from_email = 'from@example.com'
    recipient_list = [email]

    send_mail(
        subject,
        message,
        from_email, 
        recipient_list, 
        fail_silently=False)
    

def request_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        otp = generate_otp()
        harshcode = request.POST.get('harshcode', None)

        request.session['email_for_otp'] = email

        # Store OTP in cache with a 10 minute timeout
        cache.set(email, otp, 600)

        # Send OTP via email
        send_otp_email(email, otp)

        # Redirect to enter-otp view or wherever you want the user to input the OTP
        return redirect('enter-otp') 

    user_email = EmailForm()
    return render(request, 'certificate/enter-email.html', context={'user_email': user_email})


def verify_otp(request):
    user_harshcode = request.session.get('userHarshcode', None)  # Get the stored hashcode

    if request.method == "POST":
        entered_otp = request.POST.get('otp')

        # Retrieve email from the session
        user_email = request.session.get('email_for_otp')
        if not user_email:
            return HttpResponse("Session expired. Please start the verification process again.")

        stored_otp = cache.get(user_email)

        if not stored_otp:
            return redirect("inexistent")

        if entered_otp == stored_otp:
            cache.delete(user_email)  # Clear the OTP from cache using the email as key
            del request.session['email_for_otp']  # Clear the email from the session

            # Set verified_access to True because the user has successfully verified their OTP
            request.session['verified_access'] = True

            # Extract the slug from the user_harshcode if it's a full URL
            slug = user_harshcode.split('/')[-1]
            return redirect('exist', certificate_slug=slug)

        return HttpResponse("Incorrect OTP!")
    else:
        user_otp = OTPForm()
        return render(request, 'certificate/enter-otp.html', context={'user_otp': user_otp})


def store_harshcode(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Parse the raw POST data as JSON
        request.session['userHarshcode'] = data.get('harshcode', None)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def test(request):
    return render(request, 'certifications/test.html')

