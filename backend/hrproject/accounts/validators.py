from django.core.exceptions import ValidationError
import re




def validate_username(value):
    if not re.match(r'^[\s\S]*$', value):  
        raise ValidationError('Enter a valid username. This value may contain any character.')