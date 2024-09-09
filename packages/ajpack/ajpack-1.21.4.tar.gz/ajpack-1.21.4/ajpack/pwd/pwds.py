import secrets

def gen_pwd(length:int, possible_digits:str) -> str:
    """
    Generates a pwd with the length and the digits provided.
    
    :param length: The length of the password.
    :param possible_digits: The possible digits to use in the password.
    :return: A password of the specified length with the possible digits.
    """

    if possible_digits == "": raise ValueError("There are no possible digits defined!")
    
    if length > 0:
        return "".join(secrets.choice(possible_digits) for _ in range(length))
    else:
        raise ValueError("The length of the digits in your password must be grater than 0!")