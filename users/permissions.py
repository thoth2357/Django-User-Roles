from .models import User
def is_principal(user):
    '''
    # Check if user is a principal
    '''
    try:
        user_type = User.objects.get(email=user)
        return user.is_authenticated and user_type.type == 'PRINCIPAL'
    except Principal.DoesNotExist:
        return False
