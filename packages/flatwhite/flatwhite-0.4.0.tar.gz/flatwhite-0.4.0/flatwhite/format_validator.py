import re

def validate_input(input_value, validate_type, regex_pattern=None):
    """
    Validates an input based on the type of validation (email, phone, password, or custom regex)
    
    Parameters:
    input_value (str): The input to validate.
    validate_type (str): The type of validation('email', 'phone', 'password', 'regex'.
    regex_pattern (str): Custom regex pattern to use if validate_type is 'regex'.

    Returns:
    bool: Returns True if the input is valid, otherwise False.

    Raises:
    ValueError: If an unsupported validate_type is provided or regex_pattern is missing for 'regex' validtation.
    """

    if validate_type == 'email':
        # No uppercase letters allowed in the email
        return bool(re.fullmatch(r'\b[a-z0-9._+-]+@[a-z0-9]+\.[a-z]{2,7}\b', input_value))
    elif validate_type == 'phone':
        phone = re.sub(r'\D', '', input_value)
        return len(phone) == 10
    elif validate_type == 'password':
        return bool(re.fullmatch(r'^(=.*[A-Z])(/=.*\d)(?=.*[\W_]).{8,}$', input_value))
    elif validate_type == 'regex':
        if not regex_pattern:
            raise ValueError("A regex pattern must be provided for 'regex' validation.")
        return bool(re.fullmatch(regex_pattern, input_value))
    else:
        raise ValueError("Unsupported validtation type.")