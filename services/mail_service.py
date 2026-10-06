from django.core.mail import send_mail


def send_verification_email(recipient: str, otp: int):
    send_mail(
        subject='Verify Your Email Address | MyEstate',
        message=f'''Hello,

        Thank you for registering with MyEstate.

        To complete your registration, please verify your email address using the One-Time Password (OTP) below:

        Verification Code: {otp}

        This OTP is valid for the next 30 minutes.

        If you did not create an account on MyEstate, you can safely ignore this email.

        For security reasons, please do not share this verification code with anyone.

        Thank you,
        The MyEstate Team
        ''',
        from_email=None,
        recipient_list=[recipient],
    )

def send_password_reset_link(recipient: str, link: str):
    send_mail(
        subject='Reset Your Password | MyEstate',
        message=f'''Hello,

        We received a request to reset the password for your MyEstate account.

        To reset your password, please click the link below:

        {link}

        This password reset link is valid for the next 15 minutes and can only be used once.

        If you did not request a password reset, you can safely ignore this email. Your account will remain secure and no changes will be made.

        For security reasons, please do not share this link with anyone.

        Thank you,
        The MyEstate Team
        ''',
        from_email=None,
        recipient_list=[recipient],
    )