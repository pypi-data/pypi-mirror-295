from fastapi import status

from fastapi_easystart.exceptions.base import BaseHTTPException
from fastapi_easystart.utils.enums import ResponseEnum


# Custom exception for handling permission denied errors
class PermissionDeniedException(BaseHTTPException):
    """
    Exception raised when a user does not have the necessary permissions to perform an action.
    """
    response_code = ResponseEnum.EXCEPTIONS.PERMISSION.PERMISSION_DENIED.response_key
    message = ResponseEnum.EXCEPTIONS.PERMISSION.PERMISSION_DENIED.value
    detail = "You do not have permission to perform this action."
    status_code = status.HTTP_403_FORBIDDEN


# Custom exception for handling cases where specific permission is required
class PermissionRequiredException(BaseHTTPException):
    """
    Exception raised when a specific permission is required to access a resource or perform an action.
    """
    response_code = ResponseEnum.EXCEPTIONS.PERMISSION.PERMISSION_REQUIRED.response_key
    message = ResponseEnum.EXCEPTIONS.PERMISSION.PERMISSION_REQUIRED.value
    detail = "Permission is required to access this resource. Please ensure you have the correct permissions."
    status_code = status.HTTP_403_FORBIDDEN


# Custom exception for handling restricted access errors
class AccessRestrictedException(BaseHTTPException):
    """
    Exception raised when access to a resource is restricted.
    """
    response_code = ResponseEnum.EXCEPTIONS.PERMISSION.ACCESS_RESTRICTED.response_key
    message = ResponseEnum.EXCEPTIONS.PERMISSION.ACCESS_RESTRICTED.value
    detail = "Access to this resource is restricted. Contact support if you believe this is an error."
    status_code = status.HTTP_403_FORBIDDEN


# Custom exception for handling cases where the user's role is not authorized
class RoleNotAuthorizedException(BaseHTTPException):
    """
    Exception raised when the user's role does not have the necessary authorization.
    """
    response_code = ResponseEnum.EXCEPTIONS.PERMISSION.ROLE_NOT_AUTHORIZED.response_key
    message = ResponseEnum.EXCEPTIONS.PERMISSION.ROLE_NOT_AUTHORIZED.value
    detail = "The role associated with your account does not have the necessary authorization to perform this action."
    status_code = status.HTTP_403_FORBIDDEN


# Custom exception for handling cases of insufficient privileges
class InsufficientPrivilegesException(BaseHTTPException):
    """
    Exception raised when the user’s account lacks sufficient privileges to perform an action.
    """
    response_code = ResponseEnum.EXCEPTIONS.PERMISSION.INSUFFICIENT_PRIVILEGES.response_key
    message = ResponseEnum.EXCEPTIONS.PERMISSION.INSUFFICIENT_PRIVILEGES.value
    detail = "Your account does not have sufficient privileges to perform this action."
    status_code = status.HTTP_403_FORBIDDEN


# Custom exception for handling cases where a resource is locked
class ResourceLockedException(BaseHTTPException):
    """
    Exception raised when a resource is locked and cannot be accessed.
    """
    response_code = ResponseEnum.EXCEPTIONS.PERMISSION.RESOURCE_LOCKED.response_key
    message = ResponseEnum.EXCEPTIONS.PERMISSION.RESOURCE_LOCKED.value
    detail = "The resource is currently locked and cannot be accessed at this time."
    status_code = status.HTTP_423_LOCKED
