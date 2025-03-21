"""
! Created On Sun December 22 12:41 AM 2024

! @author: Talha Usman
! Status: Developer
"""

from . import *
import random as rd


# Universal Functions
def checking_category_and_role(model_id, list_model=list(), column_name=None):
    """
    Check if a category or role is in use by any specified models.

    This function checks whether a category or role, identified by `model_id`,
    is associated with any records in the models specified in `list_model`. It
    raises an exception if `column_name` or `list_model` is not provided.

    Args:
        model_id (int): The ID of the category or role to check.
        list_model (list): A list of SQLAlchemy model classes to check against.
        column_name (str): The name of the column to compare with `model_id`.

    Returns:
        bool: True if the category or role is in use by any of the models,
        False otherwise.

    Raises:
        Exception: If `column_name` or `list_model` is not provided.
    """

    if not column_name or not list_model:
        raise Exception("column_name and list_model are required")
    conditions = [
        exists().where(getattr(model, column_name) == model_id) for model in list_model
    ]
    checking = db.session.query(or_(*conditions)).scalar()
    return checking


def login_required(f):
    """
    Decorator function to ensure a user is logged in before accessing a route.

    If the user is not logged in, they are redirected to the login page.
    Otherwise, the original function is executed.

    Args:
        f (function): The view function to be decorated.

    Returns:
        function: The decorated function that checks the login status.
    """

    @wraps(f)
    def check_login_session(*args, **kwargs):
        """
        Decorator function to ensure a user is logged in before accessing a route.

        If the user is not logged in, they are redirected to the login page.
        Otherwise, the original function is executed.

        Args:
            f (function): The view function to be decorated.

        Returns:
            function: The decorated function that checks the login status.
        """
        if admin_username not in session:
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)

    return check_login_session


def existing_in_database_or_not(model, column_name, value):
    """
    Check if a value already exists in a column of a model.

    Check whether `value` already exists in the column identified by
    `column_name` in the model `model`. If the value exists, return True,
    otherwise return False.

    Args:
        model (SQLAlchemy model): The model to check in.
        column_name (str): The name of the column to check.
        value (any): The value to check for.

    Returns:
        bool: True if the value exists, False otherwise.
    """
    result = (
        db.session.query(model).filter(getattr(model, column_name) == value).first()
    )
    if result:
        return True
    else:
        return False


@admin.route("/login", methods=["POST", "GET"])
def login():
    """
    Handle admin login.

    If the admin is already logged in, redirect them to the admin dashboard.

    If the admin submits a login form, verify the username and email against
    the database. Check if the provided password matches the stored password.
    If all credentials are correct, log the admin in and redirect them to the
    dashboard. If any credential is incorrect, redirect back to the login page
    with an appropriate error message.

    If the admin visits the login page via GET request, display the login form.

    Returns:
        str: HTML of the login page or a redirect to the dashboard.
    """

    if admin_username in session:
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        user = Admin.query.filter_by(username=username).first()
        if user and user.check_password(password) and email == user.email:
            session[admin_username] = username
            session[email] = email
            return redirect(url_for("admin.dashboard"))
        else:
            if user.username != username:
                return redirect(url_for("admin.login", error="Invalid Username"))
            elif user.email != email:
                return redirect(url_for("admin.login", error="Invalid Email"))
            else:
                return redirect(url_for("admin.login", error="Invalid Password"))
    return render_template("admin/login.html")


@admin.route("/dashboard")
@login_required
def dashboard():
    """
    Render the admin dashboard with an overview of quizzes, users, and results.

    This function retrieves all quizzes, shuffles them for random display, and
    counts the total number of users and results recorded in the database.
    It ensures that only logged-in admins can access the dashboard.

    Returns:
        str: HTML content for the admin dashboard page, displaying the quizzes,
        total number of users, and results.
    """

    quiz = Quiz.query.all()
    rd.shuffle(quiz)
    users = User.query.count()
    results = Result.query.count()
    return render_template(
        "admin/dashboard.html", quizzes=quiz, users=users, results=results
    )


# Quizzes Page
@admin.route("/quizzes")
@login_required
def quizzes():
    """
    Render the admin quizzes page with a list of quizzes.

    This function checks if there is a search query, and if so, it searches
    quizzes by question, category name, or options. If there is no search query, it
    randomly shuffles all quizzes. It ensures that only logged-in admins can
    access the quizzes page.

    Returns:
        str: HTML content for the admin quizzes page, displaying the quizzes.
    """
    search_query = request.args.get("search", "")
    if search_query:
        quiz = (
            db.session.query(Quiz)
            .join(Category)
            .filter(
                or_(
                    Quiz.question.ilike(f"%{search_query}%"),
                    Category.name.ilike(f"%{search_query}%"),
                    Quiz.option1.ilike(f"%{search_query}%"),
                    Quiz.option2.ilike(f"%{search_query}%"),
                    Quiz.option3.ilike(f"%{search_query}%"),
                    Quiz.option4.ilike(f"%{search_query}%"),
                )
            )
            .order_by(func.random())
        )

    else:
        quiz = Quiz.query.all()
        rd.shuffle(quiz)
    return render_template("admin/quizzes.html", quizzes=quiz)


@admin.route("/create_quiz", methods=["POST", "GET"])
@login_required
def create_quiz():
    """
    Handle the creation of a new quiz.

    This function renders the form to create a new quiz and processes the form
    submission. It checks if the request method is POST, retrieves form data,
    validates the correct option, and adds a new quiz to the database. If the
    submission is successful, it redirects to the create quiz page with a success
    message. If the request method is GET, it displays the create quiz form.

    Returns:
        str: The rendered HTML for the create quiz page if the method is GET,
        or a redirect response to the create quiz page with a message if the
        method is POST.
    """

    categories = Category.query.all()
    if request.method == "POST":
        question = request.form["question"].title()
        option1 = request.form["option1"].capitalize()
        option2 = request.form["option2"].capitalize()
        option3 = request.form["option3"].capitalize()
        option4 = request.form["option4"].capitalize()
        correct_option = request.form["correct_option"]
        category = request.form["category"]
        if correct_option == "1":
            correct_option = option1
        elif correct_option == "2":
            correct_option = option2
        elif correct_option == "3":
            correct_option = option3
        elif correct_option == "4":
            correct_option = option4
        else:
            return redirect(url_for("admin.create_quiz", error="Invalid Option"))
        new_quiz = Quiz(
            question=question,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            category_id=category,
        )
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(
            url_for("admin.create_quiz", success="Quiz created successfully")
        )
    return render_template("admin/create_quiz.html", categories=categories)


@admin.route("/edit_quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def edit_quiz(quiz_id):
    """
    Edit a quiz created by the admin.

    This function handles the editing of a quiz. It first checks if the admin is
    logged in. If the admin is logged in, it checks if the request method is POST.
    If the request method is POST, it updates the quiz with the new details and
    redirects to the quizzes page. If the request method is not POST, it renders
    the edit quiz template with the quiz details.

    Args:
        quiz_id (int): The ID of the quiz to be edited.

    Returns:
        A redirect response to the quizzes page if the request method is POST, or
        the edit quiz template if the request method is not POST.
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    categories = Category.query.all()
    if request.method == "POST":
        question = request.form["question"]
        option1 = request.form["option1"]
        option2 = request.form["option2"]
        option3 = request.form["option3"]
        option4 = request.form["option4"]
        correct_option = request.form["correct_option"]
        category = request.form["category"]
        if correct_option == "1":
            correct_option = option1
        elif correct_option == "2":
            correct_option = option2
        elif correct_option == "3":
            correct_option = option3
        elif correct_option == "4":
            correct_option = option4
        else:
            return redirect(
                url_for("admin.edit_quiz", error="Invalid Option", quiz_id=quiz_id)
            )
        quiz.question = question
        quiz.option1 = option1
        quiz.option2 = option2
        quiz.option3 = option3
        quiz.option4 = option4
        quiz.correct_option = correct_option
        quiz.category_id = category
        db.session.commit()
        return redirect(
            url_for(
                "admin.quizzes", success="Quiz updated successfully", quiz_id=quiz_id
            )
        )
    return render_template("admin/edit_quiz.html", quiz=quiz, categories=categories)


@admin.route("/delete_quiz/<int:quiz_id>", methods=["POST", "GET"])
@login_required
def delete_quiz(quiz_id):
    """
    Delete a quiz.

    This function deletes a quiz given its ID. The quiz to be deleted is first
    retrieved from the database using the provided ID. If the quiz does not
    exist, a 404 error is raised. If the quiz exists, it is deleted from the
    database and the changes are committed. Finally, the function redirects to
    the admin dashboard.

    Args:
        quiz_id (int): The ID of the quiz to be deleted.

    Returns:
        A redirect response to the admin dashboard.
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for("admin.dashboard"))


@admin.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """
    Log out the admin.

    This function is used to log out the admin from the session. If the
    'admin_username' key is present in the session, it is removed and the
    function redirects to the admin login page.

    Returns:
        A redirect response to the admin login page.
    """
    if "admin_username" in session:
        session.pop("admin_username", None)
    return redirect(url_for("admin.login"))


@admin.route("/users", methods=["GET", "POST"])
@login_required
def users():
    """
    Render the admin users page with a list of users.

    This function checks if there is a search query, and if so, it searches
    users by username, email, or role name. If there is no search query, it
    retrieves all users. It ensures that only logged-in admins can access the
    users page.

    Returns:
        str: HTML content for the admin users page, displaying the users.
    """

    search_query = request.args.get("search", "")
    if search_query:
        users = (
            db.session.query(User)
            .join(Role)
            .filter(
                or_(
                    User.username.ilike(f"%{search_query}%"),
                    User.email.ilike(f"%{search_query}%"),
                    Role.name.ilike(f"%{search_query}%"),  # Filter by Role name
                )
            )
            .all()
        )
    else:
        users = User.query.all()
        return render_template(
            "admin/users.html", users=users, search_query=search_query
        )
    return render_template("admin/users.html", users=users, search_query=search_query)


@admin.route("/create_user", methods=["GET", "POST"])
@login_required
def create_user():
    """
    Create a new user.

    This function renders the user creation page with a list of roles. If the
    request method is POST, it creates a new user with the submitted details
    and redirects to the same page with a success message if the user is
    created successfully. If the username or email already exists, it redirects
    to the same page with an appropriate error message.

    Returns:
        str: HTML content for the user creation page.
    """
    roles = Role.query.all()
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role_id = request.form["role_id"]
        user_by_name = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()
        if user_by_name:
            return redirect(
                url_for(
                    "admin.create_user",
                    error="Username already exists",
                    username=username,
                    email=email,
                    password=password,
                    roles=roles,
                )
            )

        elif user_by_email:
            return redirect(
                url_for(
                    "admin.create_user",
                    error="Email Already Exists",
                    username=username,
                    email=email,
                    password=password,
                    roles=roles,
                )
            )

        new_user = User(username=username, email=email, role_id=role_id)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(
            url_for(
                "admin.create_user", success="User created successfully", roles=roles
            )
        )
    return render_template(
        "admin/create_user.html", username="", email="", password="", roles=roles
    )


@admin.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    """
    Handle user editing.

    GET: Render the edit user form
    POST: Edit the user and redirect to users list page if successful
    """
    user = User.query.get_or_404(user_id)
    role = Role.query.all()
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role_id = request.form["role_id"]
        if password == "":
            password = user.password
        user.username = username
        user.email = email
        user.role_id = role_id
        user.set_password(password)
        db.session.commit()
        return redirect(
            url_for(
                "admin.users", search_query=request.args.get("search", " "), roles=role
            )
        )
    return render_template("admin/edit_user.html", user=user, roles=role)


@admin.route("/delete_user/<int:user_id>", methods=["POST", "GET"])
@login_required
def delete_user(user_id):
    """
    Deletes a user.

    This function deletes a user given its ID. The user to be deleted is first
    retrieved from the database using the provided ID. If the user does not
    exist, a 404 error is raised. If the user exists, it is deleted from the
    database and the changes are committed. Finally, the function redirects to
    the users list page.

    Args:
        user_id (int): The ID of the user to be deleted.

    Returns:
        A redirect response to the users list page.
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin.users"))


# Settings Category
@admin.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """
    Handle the settings page for the admin.

    GET: Render the settings page with a list of categories and roles
    POST: Not implemented
    """
    search_query = request.args.get("search", "")
    if search_query:
        category = Category.query.filter(Category.name.like(f"%{search_query}%")).all()
    else:
        category = Category.query.all()
    roles = Role.query.all()
    return render_template(
        "admin/settings.html",
        categories=category,
        search_query=search_query,
        roles=roles,
        category_types=category_types,
    )


@admin.route("/add_category", methods=["GET", "POST"])
@login_required
def add_category():
    """
    Handle the addition of a new category.

    This function processes the form submission for adding a new category.
    If the request method is POST, it checks if the category name already
    exists in the database. If the category exists, it flashes an error
    message and redirects back to the settings page. If the category does
    not exist, it adds the new category to the database and commits the
    changes. Finally, the function redirects to the settings page.

    Returns:
        A redirect response to the admin settings page.
    """

    if request.method == "POST":
        category_name = request.form["name"].upper()
        checking = existing_in_database_or_not(Category, "name", category_name)
        if checking:
            flash("Category Already Exists", "danger")
            return redirect(url_for("admin.settings"))
        category_desc = request.form["description"]
        category_type = request.form.getlist("category_type")
        category = Category(
            name=category_name, description=category_desc, category_type=category_type
        )
        db.session.add(category)
        db.session.commit()
    category = Category.query.all()
    return redirect(url_for("admin.settings"))


@admin.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    """
    Handle the editing of a category.

    GET: Render the edit category form
    POST: Edit the category and redirect to settings page if successful
    """

    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        name = request.form["name"].upper()
        description = request.form["description"]
        category_type = request.form.getlist("category_type")
        rating = request.form["rating"]
        rating = float(rating)
        lock_rating = "lock_rating" in request.form
        if rating < 0 and rating >= -5:
            rating *= -1
        elif rating > 5:
            rating = 5
        category.name = name
        category.description = description
        category.category_type = category_type
        category.rating = rating
        category.lock_rating = lock_rating

        db.session.commit()
        return redirect(url_for("admin.settings"))
    return render_template(
        "admin/edit_category.html", category=category, category_types=category_types
    )


@admin.route("/delete_category/<int:category_id>", methods=["POST", "GET"])
@login_required
def delete_category(category_id):
    """
    Delete a category from the database.

    If the category is associated with a quiz, result, or teacher, it cannot be
    deleted. If the category is not associated with any of the above, it is
    deleted from the database and the changes are committed.

    Returns:
        A redirect response to the settings page.
    """
    category = Category.query.get_or_404(category_id)
    checking = checking_category_and_role(
        model_id=category_id,
        list_model=[Quiz, Result, Teacher],
        column_name="category_id",
    )
    if checking:
        flash("This Category Is In Use", "danger")
    else:
        db.session.delete(category)
        db.session.commit()
    return redirect(url_for("admin.settings"))


@admin.route("/view_category/<int:category_id>", methods=["GET", "POST"])
@login_required
def view_category(category_id):
    """
    View a category's details.

    This function renders the view category template with the category's details.

    Args:
        category_id (int): The ID of the category to view.

    Returns:
        A rendered template response.
    """
    category = Category.query.get_or_404(category_id)
    return render_template("admin/view_category.html", category=category)


# Results
@admin.route("/results", methods=["GET", "POST"])
@login_required
def results():
    """
    Handle the results page.

    This function renders the results template with the all results retrieved
    from the database and a dictionary of users. The dictionary of users is
    used to map the user ID to the user details in the template.

    Returns:
        A rendered template response.
    """
    results = Result.query.all()
    users = User.query.all()
    users_dict = {user.id: user for user in users}
    return render_template("admin/result.html", results=results, users_dict=users_dict)


@admin.route("/create_result", methods=["GET", "POST"])
@login_required
def create_result():
    """
    Create a new result.

    This function renders the create result template with the students and
    categories retrieved from the database. The user can then select a student
    and category, and enter the score and date of the result. If the form is
    submitted, the result is added to the database and the user is redirected
    back to this page.

    Returns:
        A rendered template response.
    """
    students = User.query.all()
    categories = Category.query.all()
    if request.method == "POST":
        user_id = request.form["student_id"]
        score = request.form["score"]
        category_id = request.form["category_id"]
        result_date = datetime.strptime(request.form["result_date"], "%Y-%m-%d").date()
        new_result = Result(
            user_id=user_id,
            score=score,
            result_date=result_date,
            category_id=category_id,
        )
        db.session.add(new_result)
        db.session.commit()
        return redirect(url_for("admin.create_result"))
    return render_template(
        "admin/create_result.html", students=students, categories=categories
    )


@admin.route("/edit_result/<int:result_id>", methods=["GET", "POST"])
@login_required
def edit_result(result_id):
    """
    Edit a result.

    This function renders the edit result template with the result and users
    retrieved from the database. The user can then edit the student, score,
    category, and date of the result. If the form is submitted, the changes
    are saved to the database and the user is redirected to the results page.

    Args:
        result_id (int): The ID of the result to edit.

    Returns:
        A rendered template response.
    """
    result = Result.query.get_or_404(result_id)
    categories = Category.query.all()
    if result:
        result_date = result.result_date.strftime("%Y-%m-%d")
    students = User.query.all()
    if request.method == "POST":
        student_id = request.form["student_id"]
        score = request.form["score"]
        result_date = datetime.strptime(request.form["result_date"], "%Y-%m-%d").date()
        result.user_id = student_id
        result.score = score
        result.category_id = request.form["category_id"]
        result.result_date = result_date
        db.session.commit()
        return redirect(url_for("admin.results"))
    return render_template(
        "admin/edit_result.html",
        result=result,
        students=students,
        result_date=result_date,
        categories=categories,
    )


@admin.route("/delete_result/<int:result_id>", methods=["POST", "GET"])
@login_required
def delete_result(result_id):
    """
    Delete a result from the database.

    This function deletes a result identified by its ID. It ensures that the
    user is logged in to perform the deletion. Upon deletion, the user is
    redirected to the results page.

    Args:
        result_id (int): The ID of the result to delete.

    Returns:
        A redirect response to the results page.
    """

    result = Result.query.get_or_404(result_id)
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for("admin.results"))


@admin.route("/view_result/<int:result_id>", methods=["GET", "POST"])
@login_required
def view_result(result_id):
    """
    View a result from the database.

    This function renders the view result template with the result and user
    retrieved from the database. The user can then view the student, score,
    category, and date of the result.

    Args:
        result_id (int): The ID of the result to view.

    Returns:
        A rendered template response.
    """
    result = Result.query.get_or_404(result_id)
    user = User.query.get_or_404(result.user_id)
    return render_template("admin/view_result.html", result=result, user=user)


# Roles Section
@admin.route("/add_role", methods=["GET", "POST"])
@login_required
def add_role():
    """
    Add a new role to the database.

    This function handles the addition of a new role to the database. If the
    request method is POST, it checks if the role name already exists in the
    database. If the role exists, it flashes an error message and redirects
    back to the settings page. If the role does not exist, it adds the new role
    to the database and commits the changes. Finally, the function redirects to
    the settings page.

    Returns:
        A redirect response to the admin settings page.
    """
    if request.method == "POST":
        role_name = request.form["name"].upper()
        checking = existing_in_database_or_not(Role, "name", role_name)
        if checking:
            flash("Role Already Exists", "danger")
            return redirect(url_for("admin.settings"))
        role = Role(name=role_name)
        db.session.add(role)
        db.session.commit()
    return redirect(url_for("admin.settings"))


@admin.route("/edit_role/<int:role_id>", methods=["GET", "POST"])
@login_required
def edit_role(role_id):
    """
    Edit a role in the database.

    This function handles the editing of a role in the database. If the
    request method is POST, it updates the role name in the database and
    commits the changes. Finally, the function redirects to the settings page.

    Args:
        role_id (int): The ID of the role to edit.

    Returns:
        A redirect response to the admin settings page.
    """
    role = Role.query.get_or_404(role_id)
    if request.method == "POST":
        role_name = request.form["name"]
        role.name = role_name.upper()
        db.session.commit()
        return redirect(url_for("admin.settings"))
    return render_template("/admin/edit_role.html", role=role)


@admin.route("/delete_role/<int:role_id>", methods=["POST", "GET"])
@login_required
def delete_role(role_id):
    """
    Delete a role from the database.

    This function attempts to delete a role specified by the `role_id` from the database.
    It first checks if the role is associated with any users or teachers using the
    `checking_category_and_role` function. If the role is in use, a flash message is
    displayed indicating that the role cannot be deleted. Otherwise, the role is deleted
    and the changes are committed to the database.

    Args:
        role_id (int): The ID of the role to delete.

    Returns:
        A redirect response to the admin settings page.
    """

    role = Role.query.get_or_404(role_id)
    checking = checking_category_and_role(
        model_id=role_id, list_model=[User, Teacher], column_name="role_id"
    )
    if checking:
        print(checking)
        flash("This Role Is In Use", "danger")
    else:
        print(checking)
        db.session.delete(role)
        db.session.commit()
    return redirect(url_for("admin.settings"))


# Teachers
@admin.route("/teachers")
@login_required
def teachers():
    """
    Show all teacher registration requests.

    This function renders the admin/teachers_approvals.html template, passing a
    list of all teacher registration requests and the value "All" for the
    filtered_value parameter.

    Returns:
        A rendered template response.
    """
    teachers_request = Teacher.query.all()
    return render_template(
        "admin/teachers_approvals.html", requests=teachers_request, filtered_value="All"
    )


@admin.route("/register_teacher")
@login_required
def register_teacher():
    """
    Register a new teacher.

    This function handles the registration of a new teacher. It is accessible
    only to logged-in administrators. Upon successful registration, the function
    redirects to the admin teachers page.

    Returns:
        A redirect response to the admin teachers page.
    """

    return redirect(url_for("admin.teachers"))


@admin.route("/edit_teachers_profile/<int:teacher_id>", methods=["GET", "POST"])
@login_required
def edit_teachers_profile(teacher_id):
    """
    Edit a teacher's profile.

    This function allows administrators to edit the profile of a teacher
    specified by the `teacher_id`. It handles both GET and POST requests.

    - GET: Renders the teacher's profile for editing with roles and categories.
    - POST: Updates the teacher's profile with the submitted form data and
      commits the changes to the database. After a successful update,
      redirects to the teachers' page.

    Args:
        teacher_id (int): The ID of the teacher whose profile is to be edited.

    Returns:
        A rendered template response for GET request or a redirect to the
        teachers' page for POST request.
    """

    teacher = Teacher.query.get_or_404(teacher_id)
    roles = Role.query.all()
    categories = Category.query.all()
    if request.method == "POST":
        teacher.full_name = request.form["full_name"]
        teacher.user_name = request.form["user_name"]
        teacher.email = request.form["email"]
        teacher.contact_number = request.form["contact_number"]
        teacher.teacher_info = request.form["teacher_info"]
        teacher.additional_notes = request.form["additional_notes"]
        teacher.status = request.form["status"]
        db.session.commit()
        return redirect(url_for("admin.teachers"))
    return render_template(
        "admin/view_teachers_profile.html",
        teacher=teacher,
        roles=roles,
        categories=categories,
    )


def block_teacher():
    pass


def unblock_teacher():
    pass


@admin.route("/filter_teacher_approvals", methods=["GET", "POST"])
@login_required
def filter_teacher_approvals():
    """
    Filter and search teacher approvals based on query parameters.

    This function handles filtering and searching through teacher approval
    requests. It supports GET requests with optional query parameters:
    - 'search': A search query to filter teachers by full name, username, or email.
    - 'filter': A filter to specify approval status ('all', 'pending', 'approved', or 'rejected').

    Returns:
        A rendered template displaying the filtered list of teacher approvals.
    """

    search_query = request.args.get("search", "")
    filter_status = request.args.get("filter", "all")
    if not filter_status:
        filter_status = "all"
    query = Teacher.query
    if search_query:
        query = query.filter(
            or_(
                Teacher.full_name.ilike(f"%{search_query}%"),
                Teacher.user_name.ilike(f"%{search_query}%"),
                Teacher.email.ilike(f"%{search_query}%"),
            )
        )
    if filter_status != "all":
        query = query.filter_by(status=filter_status.capitalize())
    teachers_request = query.all()
    return render_template(
        "admin/teachers_approvals.html",
        requests=teachers_request,
        filtered_value=filter_status.capitalize(),
    )


@admin.route("/approve_teacher/<int:teacher_id>", methods=["GET", "POST"])
@login_required
def approve_teacher(teacher_id):
    """
    Approve a teacher's registration request.

    This route is accessible only to logged-in administrators and handles
    the approval of a teacher's registration request. When accessed via
    a POST request, it updates the teacher's status to "Approved" in the
    database and commits the change. After approval, it redirects to the
    admin teachers page.

    Args:
        teacher_id (int): The ID of the teacher to approve.

    Returns:
        A redirect response to the admin teachers page upon successful approval.
    """

    if request.method == "POST":
        teacher = Teacher.query.get_or_404(teacher_id)
        teacher.status = "Approved"
        db.session.commit()
        return redirect(url_for("admin.teachers"))


@admin.route("/reject_teacher/<int:teacher_id>", methods=["GET", "POST"])
@login_required
def reject_teacher(teacher_id):
    """
    Reject a teacher's registration request.

    This route is accessible only to logged-in administrators and handles
    the rejection of a teacher's registration request. When accessed via
    a POST request, it updates the teacher's status to "Rejected" in the
    database and commits the change. After rejection, it redirects to the
    admin teachers page.

    Args:
        teacher_id (int): The ID of the teacher to reject.

    Returns:
        A redirect response to the admin teachers page upon successful rejection.
    """

    if request.method == "POST":
        teacher = Teacher.query.get_or_404(teacher_id)
        teacher.status = "Rejected"
        db.session.commit()
        return redirect(url_for("admin.teachers"))


@admin.route("/view_teachers_profile/<int:teacher_id>", methods=["GET", "POST"])
@login_required
def view_teachers_profile(teacher_id):
    """
    View a teacher's profile and edit their details.

    This route is accessible only to logged-in administrators and handles
    viewing a teacher's profile and editing their details. When accessed via
    a GET request, it renders a template displaying the teacher's information.
    When accessed via a POST request, it redirects to the edit teacher profile
    page.

    Args:
        teacher_id (int): The ID of the teacher to view.

    Returns:
        A rendered template displaying the teacher's information upon a GET request.
        A redirect response to the edit teacher profile page upon a POST request.
    """
    return redirect(url_for("admin.edit_teachers_profile", teacher_id=teacher_id))


# Reviews
@admin.route("/reviews")
@login_required
def reviews():
    """
    Display all user reviews.

    This route is accessible only to logged-in administrators and retrieves
    all user reviews from the database. It renders the reviews page,
    displaying the list of reviews.

    Returns:
        A rendered template displaying all user reviews.
    """

    reviews = Review.query.all()
    return render_template("admin/reviews.html", reviews=reviews)
