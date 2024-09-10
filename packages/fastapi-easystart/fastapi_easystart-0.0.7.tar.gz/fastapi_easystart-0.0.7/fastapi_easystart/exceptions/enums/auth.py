from fastapi_easystart.utils.enums.base import BaseCustomEnum


class UsernameExceptionEnum(BaseCustomEnum):
    USERNAME_ALREADY_EXISTS = 'username already exists.'
    USERNAME_NOT_FOUND = 'username not found.'
    USERNAME_REQUIRED = 'username is required.'


class PasswordExceptionEnum(BaseCustomEnum):
    PASSWORD_ERROR = 'This field is required | Must be (a-z), (0, 9) and minimum 8 characters'
    PASSWORD_NOT_VALID = 'Your password is invalid.'
    PASSWORD_REQUIRED = 'Password is required'
    PASSWORD_RESET_SUCCESS = 'Your password has been reset successfully.'
    PASSWORD_WRONG = 'Enter correct password, your password is incorrect.'
    NEW_AND_OLD_PASSWORD_SAME = 'New and old password cannot be same.'
    NEW_AND_CONFIRM_PASSWORD = 'New and confirm password must be same.'


class AuthenticationExceptionEnum(BaseCustomEnum):
    AUTHENTICATION_FAILED = 'Incorrect authentication credentials.'
    EMAIL_AND_PASSWORD_REQUIRED = 'Email and password are required.'
    USERNAME_AND_PASSWORD_REQUIRED = 'username and password are required.'
    LINK_EXPIRED = 'link is expired, please generate new link.'
    ACCOUNT_ALREADY_EXISTS = "Account Already Exists"
    ACCOUNT_NOT_EXIST = 'Account does not exist!'
    ACCOUNT_VERIFIED = 'your account is verified, please login.'
    ACCOUNT_NOT_ACTIVE = 'Account is not active, Please activate your account.'
    ANONYMOUS__USER = 'Anonymous user'
    LOGOUT_FAILED = 'logout failed'
    VERIFICATION_LINK_EXPIRE = 'This link is expired, please resend your verification link.'
    NOT_AUTHENTICATED = 'Authentication credentials were not provided.'
    UNAUTHORIZED_USER = 'You do not have permission to perform this action.'
    ALREADY_AUTHENTICATED = 'You are already authenticated.'
    # password
    PASSWORD_ERROR = 'This field is required | Must be (a-z), (0, 9) and minimum 8 characters'
    PASSWORD_NOT_VALID = 'Your password is invalid.'
    PASSWORD_REQUIRED = 'Password is required'
    PASSWORD_RESET_SUCCESS = 'Your password has been reset successfully.'
    PASSWORD_WRONG = 'Enter correct password, your password is incorrect.'
    NEW_AND_OLD_PASSWORD_SAME = 'New and old password cannot be same.'
    NEW_AND_CONFIRM_PASSWORD = 'New and confirm password must be same.'

    # username
    USERNAME_ALREADY_EXISTS = 'username already exists.'
    USERNAME_NOT_FOUND = 'username not found.'
    USERNAME_REQUIRED = 'username is required.'
