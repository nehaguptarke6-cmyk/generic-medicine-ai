SAFETY_MESSAGE = """
Important: This application provides general medicine
information for educational purposes only. It does not
diagnose medical conditions, prescribe medicines, or
replace advice from a qualified healthcare professional.
"""


def add_safety_message(response):
    """
    Add a safety notice to the response.
    """

    return (
        f"{response}\n\n"
        f"{SAFETY_MESSAGE}"
    )