"""
! Created On Sat December 28 8:53 PM 2024

! @author: Talha Usman
! Status: Developer
"""

# import sys
# import os
# from app import app

# # Add the parent directory to sys.path so models can be found
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# # Now you can import from models
# from models.quiz import Quiz  # or whatever module you need
# from models.category import Category

from . import *

quiz_data = [
    # Python Questions
    {
        "question": "Which of the following is used to declare a variable in Python?",
        "options": ["var x = 10", "x = 10", "int x = 10", "let x = 10"],
        "correct_option": 2,
        "category": "Python",
    },
    {
        "question": "What will be the output of the following Python code: print(type(10))?",
        "options": [
            "<class 'float'>",
            "<class 'int'>",
            "<class 'str'>",
            "<class 'bool'>",
        ],
        "correct_option": 2,
        "category": "Python",
    },
    {
        "question": "How do you add a comment in Python?",
        "options": [
            "// This is a comment",
            "/* This is a comment */",
            "# This is a comment",
            "<!-- This is a comment -->",
        ],
        "correct_option": 3,
        "category": "Python",
    },
    {
        "question": "Which of the following methods can be used to remove an item from a list in Python?",
        "options": ["pop()", "del()", "remove()", "all of the above"],
        "correct_option": 4,
        "category": "Python",
    },
    {
        "question": "What does the 'len()' function do in Python?",
        "options": [
            "Returns the length of an object",
            "Returns the data type of an object",
            "Returns the first element of an object",
            "None of the above",
        ],
        "correct_option": 1,
        "category": "Python",
    },
    {
        "question": "Which of the following is used to define a function in Python?",
        "options": [
            "def function_name():",
            "function function_name():",
            "create function_name():",
            "None of the above",
        ],
        "correct_option": 1,
        "category": "Python",
    },
    {
        "question": "What will be the output of the following Python code: print(3 * 'x')?",
        "options": ["xxx", "x3", "error", "None"],
        "correct_option": 1,
        "category": "Python",
    },
    {
        "question": "Which method is used to add an element to the end of a list in Python?",
        "options": ["add()", "insert()", "append()", "extend()"],
        "correct_option": 3,
        "category": "Python",
    },
    {
        "question": "Which of the following is used to start a for loop in Python?",
        "options": [
            "for i = 0 to 10",
            "for i in range(10)",
            "for i in 10",
            "for i = 0; i < 10; i++",
        ],
        "correct_option": 2,
        "category": "Python",
    },
    {
        "question": "Which of the following is the correct way to open a file in Python?",
        "options": [
            "file.open('filename.txt')",
            "open('filename.txt')",
            "fopen('filename.txt')",
            "None of the above",
        ],
        "correct_option": 2,
        "category": "Python",
    },
    # Java Questions
    {
        "question": "Which of the following is the correct way to declare an array in Java?",
        "options": [
            "int[] arr = new int[10];",
            "int arr[] = new int[10];",
            "int arr[10];",
            "Both 1 and 2",
        ],
        "correct_option": 4,
        "category": "Java",
    },
    {
        "question": "What is the default value of a boolean variable in Java?",
        "options": ["true", "false", "null", "undefined"],
        "correct_option": 2,
        "category": "Java",
    },
    {
        "question": "Which of the following is used to declare a constant in Java?",
        "options": ["constant", "final", "const", "immutable"],
        "correct_option": 2,
        "category": "Java",
    },
    {
        "question": "What will be the output of the following code: System.out.println(10 + 5 + 'A');",
        "options": ["15A", "105A", "15", "An error occurs"],
        "correct_option": 2,
        "category": "Java",
    },
    {
        "question": "Which of the following data types can store a decimal value in Java?",
        "options": ["int", "double", "float", "both 2 and 3"],
        "correct_option": 4,
        "category": "Java",
    },
    {
        "question": "Which of the following is the correct syntax for a constructor in Java?",
        "options": [
            "public MyClass() {}",
            "public MyClass {}()",
            "constructor MyClass() {}",
            "MyClass() public {}",
        ],
        "correct_option": 1,
        "category": "Java",
    },
    {
        "question": "Which method is used to compare two strings in Java?",
        "options": ["compare()", "equals()", "compareTo()", "Both 2 and 3"],
        "correct_option": 4,
        "category": "Java",
    },
    {
        "question": "Which keyword is used to create an interface in Java?",
        "options": ["interface", "implements", "extends", "interface class"],
        "correct_option": 1,
        "category": "Java",
    },
    {
        "question": "What is the size of a float in Java?",
        "options": ["32 bits", "64 bits", "128 bits", "16 bits"],
        "correct_option": 1,
        "category": "Java",
    },
    {
        "question": "Which of the following is not a primitive data type in Java?",
        "options": ["int", "boolean", "String", "char"],
        "correct_option": 3,
        "category": "Java",
    },
    # General Knowledge Questions
    {
        "question": "What is the largest continent on Earth?",
        "options": ["Africa", "Asia", "Europe", "North America"],
        "correct_option": 2,
        "category": "General Knowledge",
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "correct_option": 2,
        "category": "General Knowledge",
    },
    {
        "question": "Who was the first President of the United States?",
        "options": [
            "George Washington",
            "Thomas Jefferson",
            "Abraham Lincoln",
            "John Adams",
        ],
        "correct_option": 1,
        "category": "General Knowledge",
    },
    {
        "question": "Which of the following is the longest river in the world?",
        "options": ["Amazon", "Nile", "Yangtze", "Mississippi"],
        "correct_option": 2,
        "category": "General Knowledge",
    },
    {
        "question": "Which language has the most native speakers worldwide?",
        "options": ["English", "Spanish", "Mandarin", "Hindi"],
        "correct_option": 3,
        "category": "General Knowledge",
    },
    {
        "question": "Who invented the telephone?",
        "options": [
            "Thomas Edison",
            "Nikola Tesla",
            "Alexander Graham Bell",
            "Samuel Morse",
        ],
        "correct_option": 3,
        "category": "General Knowledge",
    },
    {
        "question": "What is the capital of Canada?",
        "options": ["Ottawa", "Toronto", "Vancouver", "Montreal"],
        "correct_option": 1,
        "category": "General Knowledge",
    },
    {
        "question": "Which element has the chemical symbol 'O'?",
        "options": ["Oxygen", "Osmium", "Ozone", "Oxygenium"],
        "correct_option": 1,
        "category": "General Knowledge",
    },
    {
        "question": "In which country did the Industrial Revolution begin?",
        "options": ["France", "Germany", "England", "United States"],
        "correct_option": 3,
        "category": "General Knowledge",
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "correct_option": 4,
        "category": "General Knowledge",
    },
    # Programming Questions
    {
        "question": "What does CSS stand for?",
        "options": [
            "Computer Style Sheets",
            "Cascading Style Sheets",
            "Creative Style Sheets",
            "Common Style Sheets",
        ],
        "correct_option": 2,
        "category": "Programming",
    },
    {
        "question": "Which of the following is not a valid loop structure in C?",
        "options": ["for", "while", "repeat", "do-while"],
        "correct_option": 3,
        "category": "Programming",
    },
    {
        "question": "What does 'API' stand for in programming?",
        "options": [
            "Application Process Interface",
            "Application Programming Interface",
            "Applied Programming Interface",
            "All of the above",
        ],
        "correct_option": 2,
        "category": "Programming",
    },
    {
        "question": "Which of the following is used for styling web pages?",
        "options": ["HTML", "CSS", "JavaScript", "PHP"],
        "correct_option": 2,
        "category": "Programming",
    },
    {
        "question": "Which of the following is used to declare a class in C++?",
        "options": [
            "class MyClass {}",
            "MyClass class {}",
            "class MyClass[]",
            "MyClass{}",
        ],
        "correct_option": 1,
        "category": "Programming",
    },
    {
        "question": "What is the correct syntax to declare a variable in JavaScript?",
        "options": ["var x;", "let x;", "const x;", "All of the above"],
        "correct_option": 4,
        "category": "Programming",
    },
    {
        "question": "What is the difference between == and === in JavaScript?",
        "options": [
            "== compares values, === compares values and types",
            "== compares values and types, === compares values",
            "No difference",
            "Both are used for comparison of values only",
        ],
        "correct_option": 1,
        "category": "Programming",
    },
    {
        "question": "Which function is used to read input from the user in JavaScript?",
        "options": ["input()", "scanf()", "prompt()", "read()"],
        "correct_option": 3,
        "category": "Programming",
    },
    {
        "question": "What is the default value of a variable declared with 'var' in JavaScript?",
        "options": ["null", "undefined", "0", "false"],
        "correct_option": 2,
        "category": "Programming",
    },
    {
        "question": "Which of the following is used to include external CSS in an HTML document?",
        "options": [
            "<link href='style.css'>",
            "<script src='style.css'>",
            "<style src='style.css'>",
            "<css src='style.css'>",
        ],
        "correct_option": 1,
        "category": "Programming",
    },
]

quiz_data = [
    # Python Questions
    {
        "question": "Which of the following is the correct syntax for creating a function in Python?",
        "options": [
            "def myFunction():",
            "function myFunction():",
            "create function myFunction():",
            "func myFunction()",
        ],
        "correct_option": 1,
        "category": "Python",
    },
    {
        "question": "Which of the following is the proper way to create a list in Python?",
        "options": ["list = []", "list = ()", "list = {}", "list = <>"],
        "correct_option": 1,
        "category": "Python",
    },
    {
        "question": "What will be the output of `print(2**3)` in Python?",
        "options": ["6", "8", "9", "3"],
        "correct_option": 2,
        "category": "Python",
    },
    {
        "question": "What is the default value for the `max()` function in Python?",
        "options": ["None", "0", "1", "Infinity"],
        "correct_option": 1,
        "category": "Python",
    },
    {
        "question": "How do you add an element to the end of a list in Python?",
        "options": ["list.add()", "list.append()", "list.push()", "list.insert()"],
        "correct_option": 2,
        "category": "Python",
    },
    {
        "question": "Which of the following is used to declare a variable in Python?",
        "options": ["var", "let", "int", "No keyword is required"],
        "correct_option": 4,
        "category": "Python",
    },
    {
        "question": "Which function is used to get the length of a list in Python?",
        "options": ["length()", "size()", "count()", "len()"],
        "correct_option": 4,
        "category": "Python",
    },
    {
        "question": "How do you start a comment in Python?",
        "options": ["//", "#", "/*", "<!--"],
        "correct_option": 2,
        "category": "Python",
    },
    {
        "question": "What is the purpose of the `pass` statement in Python?",
        "options": [
            "It terminates a loop",
            "It defines a function",
            "It acts as a placeholder",
            "It throws an exception",
        ],
        "correct_option": 3,
        "category": "Python",
    },
    {
        "question": "Which method is used to remove all items from a Python dictionary?",
        "options": ["clear()", "delete()", "remove()", "pop()"],
        "correct_option": 1,
        "category": "Python",
    },
    # Java Questions
    {
        "question": "Which keyword is used to define a class in Java?",
        "options": ["def", "class", "function", "struct"],
        "correct_option": 2,
        "category": "Java",
    },
    {
        "question": "Which method is used to print output to the console in Java?",
        "options": ["printf()", "println()", "print()", "echo()"],
        "correct_option": 2,
        "category": "Java",
    },
    {
        "question": "Which of the following is used to create a comment in Java?",
        "options": ["// comment", "/* comment */", "# comment", "comment()"],
        "correct_option": 1,
        "category": "Java",
    },
    {
        "question": "What is the default value of an instance variable in Java?",
        "options": ["null", "0", "false", "undefined"],
        "correct_option": 1,
        "category": "Java",
    },
    {
        "question": "Which method is called when an object is created in Java?",
        "options": ["constructor", "init()", "main()", "new()"],
        "correct_option": 1,
        "category": "Java",
    },
    {
        "question": "Which of these is the correct way to declare an array in Java?",
        "options": [
            "int[] arr = new int[10];",
            "arr = new int[10];",
            "int arr[] = 10;",
            "array arr[10];",
        ],
        "correct_option": 1,
        "category": "Java",
    },
    {
        "question": "What is the purpose of the `this` keyword in Java?",
        "options": [
            "Refers to the current class",
            "Refers to the current object instance",
            "Refers to the parent class",
            "Refers to the superclass constructor",
        ],
        "correct_option": 2,
        "category": "Java",
    },
    {
        "question": "In Java, which data type can hold multiple values of different types?",
        "options": ["Array", "List", "Map", "Object"],
        "correct_option": 3,
        "category": "Java",
    },
    {
        "question": "Which of the following is not a valid data type in Java?",
        "options": ["int", "float", "string", "boolean"],
        "correct_option": 3,
        "category": "Java",
    },
    {
        "question": "What is the return type of the `main()` method in Java?",
        "options": ["void", "int", "String", "boolean"],
        "correct_option": 1,
        "category": "Java",
    },
    # General Knowledge Questions
    {
        "question": "Which country has the largest population in the world?",
        "options": ["India", "China", "USA", "Indonesia"],
        "correct_option": 2,
        "category": "General Knowledge",
    },
    {
        "question": "What is the capital city of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "correct_option": 3,
        "category": "General Knowledge",
    },
    {
        "question": "Who wrote the play 'Romeo and Juliet'?",
        "options": ["Shakespeare", "Dickens", "Hemingway", "Austen"],
        "correct_option": 1,
        "category": "General Knowledge",
    },
    {
        "question": "What is the smallest planet in our solar system?",
        "options": ["Earth", "Mars", "Mercury", "Venus"],
        "correct_option": 3,
        "category": "General Knowledge",
    },
    {
        "question": "Which ocean is the largest by area?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "correct_option": 4,
        "category": "General Knowledge",
    },
    {
        "question": "Which of the following is the longest river in the world?",
        "options": ["Amazon", "Nile", "Yangtze", "Ganges"],
        "correct_option": 2,
        "category": "General Knowledge",
    },
    {
        "question": "Which element has the chemical symbol 'O'?",
        "options": ["Oxygen", "Osmium", "Ozone", "Oganesson"],
        "correct_option": 1,
        "category": "General Knowledge",
    },
    {
        "question": "Who invented the telephone?",
        "options": [
            "Thomas Edison",
            "Alexander Graham Bell",
            "Nikola Tesla",
            "Michael Faraday",
        ],
        "correct_option": 2,
        "category": "General Knowledge",
    },
    {
        "question": "Which country is the largest by land area?",
        "options": ["Canada", "China", "United States", "Russia"],
        "correct_option": 4,
        "category": "General Knowledge",
    },
    {
        "question": "Which country won the 2018 FIFA World Cup?",
        "options": ["Brazil", "France", "Germany", "Argentina"],
        "correct_option": 2,
        "category": "General Knowledge",
    },
    # Programming Questions
    {
        "question": "Which data structure is implemented by a stack?",
        "options": ["LIFO", "FIFO", "Linked List", "Array"],
        "correct_option": 1,
        "category": "Programming",
    },
    {
        "question": "Which of the following is an example of a binary tree traversal?",
        "options": ["In-order", "Pre-order", "Post-order", "All of the above"],
        "correct_option": 4,
        "category": "Programming",
    },
    {
        "question": "What is the time complexity of accessing an element in an array?",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
        "correct_option": 1,
        "category": "Programming",
    },
    {
        "question": "What is the use of the `break` statement in loops?",
        "options": [
            "It breaks the loop and ends the program",
            "It exits the loop prematurely",
            "It terminates the program",
            "It pauses the loop",
        ],
        "correct_option": 2,
        "category": "Programming",
    },
    {
        "question": "Which of the following sorting algorithms has the best worst-case time complexity?",
        "options": ["Quick Sort", "Merge Sort", "Bubble Sort", "Selection Sort"],
        "correct_option": 2,
        "category": "Programming",
    },
]

# Repeat the list until it reaches 100+ questions
# If you need all questions up to 100+ in a single list, just repeat the pattern.

# This is an extended list of questions. You can keep adding more questions based on this structure.


@auto_script.route("/generate_quizzes")
def generate_quizzes():
    for idx, item in enumerate(quiz_data):
        question = item["question"]
        option1 = item["options"][0]
        option2 = item["options"][1]
        option3 = item["options"][2]
        option4 = item["options"][3]
        correct_option = item["options"][item["correct_option"] - 1]
        category = item["category"]
        category = category.strip()
        # Query the Category by name using filter_by or filter
        category_id = Category.query.filter(
            func.lower(Category.name) == func.lower(category)
        ).first()

        print(category_id)
        new_quiz = Quiz(
            question=question,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            category_id=category_id.id,
        )
        db.session.add(new_quiz)
    db.session.commit()
    print("Added Successfully")
    return render_template("user/base.html")
