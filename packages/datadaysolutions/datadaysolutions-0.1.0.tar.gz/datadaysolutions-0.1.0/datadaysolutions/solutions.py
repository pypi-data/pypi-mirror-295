"""
Provide hints, answers, and checks for questions in beginner python course.
"""

def reverse_list_hint():
    """Provides a hint for reversing a list."""
    print("Hint: You can use slicing to reverse a list. Try using lst[::-1].")


def variable_swap_check(a, b):
    if not (a==[3, 2, 1] and b==[1, 2, 3]):
        print("That is not correct!")
    else:
        print(
            """
            Nice Job!

            You probably used a temporarly third variable, but Python has another 
            solution that is more "Pythonic" and is what really makes coding fun!

            Try:
            a, b = b, a
            """
        )