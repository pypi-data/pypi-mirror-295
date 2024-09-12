"""
Provide hints, answers, and checks for questions in beginner python course.
"""

def reverse_list_hint():
    """Provides a hint for reversing a list."""
    print("Hint: You can use slicing to reverse a list. Try using lst[::-1].")


def variable_swap_check(a, b):
    if not (a==[30, 20, 10] and b==[10, 20, 30]):
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

def variable_swap_hint():
    print(
        """
        Try using a third variable, like 'z', as an interim step.
        """
    )


def variable_swap_solution():
    print(
        """
        Use an interim variable to store one of the values.
        z = x
        x = y
        y = z

        A more "Pythonic" (and fun) way is to use a concept called tuple unpacking.

        Try:
        a, b = b, a        
        """
    )

def list_index_check(part):
    if not part == "TCM":
        print("That's not quite right!")
    else:
        print(
            """
            Very Nice!!

            You can see that it is possible to use nested list indexing to get this sub-list value.

            Some solutions that would work are:
            truck_parts[1][2]
            truck_parts[-2][-1]
            """
        )

def list_index_hint():
    print(
        """
        First think about how you could return the list that contains TCM.  
        
        Start by figuring out how to reach the outer list, and then drill down to the item you're looking for inside it.  
        
        There is a concept called "nested indexing"
        """
    )

def list_index_solution():
    print(
        """
        Use a concept called "nested indexing".
        truck_parts[1][2]

        truck_parts[1] will return ["ECM", "ACM", "TCM"]
        And then the [2] further indexes this sub list to return "TCM".

        truck_parts[-2][-1] would also work.
        
        """
    )

def sort_order_check(student_answer, correct_answer = "c"):
    if student_answer.lower() == correct_answer:
        print(
            """
            That's correct! The reason is due to how functions and methods differ.

            Think of a method as giving direct instructions to the list. 
            When you tell the list to do something (like add or remove items), it changes the list itself. 
            It's like asking someone to change something for you—once they do it, the thing is different.
            
            A function is like a copy machine. 
            It works with the list and might give you a new result or do something with it, 
            but it doesn’t change the original list. 
            The original list stays the same unless you specifically tell it to change.

            Methods don't always operate like this but they often do. I just present this here to start 
            having you think about functions and methods differently.
            """
        )
    elif student_answer == "0":
        print("You need to replace the 0 with a letter.")
    else:
        print(
            """
            Try again.  One is a function and one is a method.  
            We didn't actually discuss this, so it's not 100% a fair question.
            Try looking up Python's documentation for List Methods and note the phrase "in place"
            """
        )


def sort_order_hint():
    print(
        """
        One is a function and one is a method.  
        We didn't actually discuss this, so it's not 100% a fair question.
        Try looking up Python's documentation for List Methods and note the phrase "in place"
        """
    )

def sort_order_solution():
    print(
        """
        The correct answer is c.

        The reason is due to how functions and methods differ.

        Think of a method as giving direct instructions to the list. 
        When you tell the list to do something (like add or remove items), it changes the list itself. 
        It's like asking someone to change something for you—once they do it, the thing is different.
        
        A function is like a copy machine. 
        It works with the list and might give you a new result or do something with it, 
        but it doesn’t change the original list. 
        The original list stays the same unless you specifically tell it to change.

        Methods don't always operate like this but they often do. I just present this here to start 
        having you think about functions and methods differently.        
        """
    )
    
def truck_count_check(student_answer, correct_answer = 5):
    if student_answer == correct_answer:
        print(
            """
            That's right! Nice Job!
            You probably could write your own function but why? 
            Python already has a built in method.  
            It's a good idea to check documentation if you are unsure if there is already an existing function.
            """
        )
    elif student_answer == 0:
        print("You need to replace the 0 with a number.")

    else:
        print(
        """
        That is not correct!
        """
        )

def truck_count_hint():
    print(
        """
        Did you find this link? https://docs.python.org/3/tutorial/datastructures.html
        """
    )

def truck_count_solution():
    print(
        """
        Check out https://docs.python.org/3/tutorial/datastructures.html
        
        list.count(x) --> Return the number of times x appears in the list.
        
        locs.count("Santiago") 
        """
    )