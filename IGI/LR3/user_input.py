def get_float(prompt: str, min : float = None, max : float = None) -> float:
    """
    Get float number from user
    
    Args:
        prompt: Message for user
        min: Min number
        max: Max number

    Returns:
        float: Float number
    """

    while True:
        try:
            value = float(input(prompt))

            if min is not None and value <= min:
                raise ValueError(f"Value must be greater than {min}")
            if max is not None and value >= max:
                raise ValueError(f"Value must be less than {max}")

            return value
        except ValueError as error:
            print(f"Invalid input: {error}")    

def get_yes_or_no(prompt: str) -> bool:
    """
    Get user answer yes or mo
    
    Args:
        prompt: Message for user

    Returns:
        boll: User answer
    """

    while True:
        answer = input(prompt).lower()
        if answer == "yes" or answer == "y":
            return True
        if answer == "no" or answer == "n":
            return False
        print("Wrong answer! Enter yes(y) or no(n)")
