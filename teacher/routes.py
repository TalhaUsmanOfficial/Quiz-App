"""
! Created On Mon December 30 12:05 AM 2024

! @author: Talha Usman
! Status: Developer
"""

from . import *

# Global Variables
teacher_user_name = "teacher_username"
teacher_email = "teacher_email"
teacher_id = "teacher_id"
teacher_category_name = "teacher_category_name"
teacher_role = "teacher_role"


# Main Section
@teacher.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles teacher registration.

    GET: Render the registration form
    POST: Register the teacher and redirect to login page if successful
    """
    category = Category.query.all()
    role = Role.query.all()
    if request.method == "POST":
        full_name = request.form["full_name"]
        user_name = request.form["user_name"]
        email = request.form["email"]
        password = request.form["password"]
        contact_number = request.form["contact_number"]
        teacher_info = request.form["teacher_info"]
        additional_notes = request.form["additional_notes"]
        category_id = request.form["category_id"]
        role_id = request.form["role_id"]
        teacher_by_name = Teacher.query.filter_by(user_name=user_name).first()
        teacher_by_email = Teacher.query.filter_by(email=email).first()
        if teacher_by_name:
            flash("Username already exists", "danger")
            return render_template(
                "teacher/register.html", roles=role, categories=category
            )
        if teacher_by_email:
            flash("Email already exists", "danger")
            return render_template(
                "teacher/register.html", roles=role, categories=category
            )

        new_teacher = Teacher(
            full_name=full_name,
            user_name=user_name,
            email=email,
            contact_number=contact_number,
            teacher_info=teacher_info,
            additional_notes=additional_notes,
            category_id=category_id,
            role_id=role_id,
        )
        new_teacher.set_password(password)
        db.session.add(new_teacher)
        db.session.commit()
        flash("Teacher registered successfully", "success")
        return redirect(url_for("teacher.login"))
    return render_template("teacher/register.html", roles=role, categories=category)


@teacher.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles teacher login.

    GET: Render the login form
    POST: Validate the input and redirect to dashboard if successful
    """
    if teacher_user_name in session:
        return redirect(url_for("teacher.dashboard"))
    if request.method == "POST":
        user_name_or_email = request.form["login_credential"]
        password = request.form["password"]
        teacher_by_name = Teacher.query.filter_by(user_name=user_name_or_email).first()
        teacher_by_email = Teacher.query.filter_by(email=user_name_or_email).first()

        if teacher_by_name:
            if teacher_by_name.check_password(password):
                teacher_status = teacher_by_name.status
                if teacher_status != "Approved":
                    return redirect(
                        url_for("teacher.message", teacher_status=teacher_status)
                    )
                session[teacher_user_name] = teacher_by_name.user_name
                session[teacher_email] = teacher_by_name.email
                session[teacher_id] = teacher_by_name.id
                session[teacher_category_name] = teacher_by_name.category.name
                session[teacher_role] = teacher_by_name.role.name

                return redirect(url_for("teacher.dashboard"))
            else:
                flash("Wrong Password", "danger")
                return render_template("teacher/login.html")
        elif teacher_by_email:
            if teacher_by_email.check_password(password):
                teacher_status = teacher_by_email.status
                if teacher_status != "Approved":
                    return redirect(
                        url_for("teacher.message", teacher_status=teacher_status)
                    )
                session[teacher_user_name] = teacher_by_email.user_name
                session[teacher_email] = teacher_by_email.email
                session[teacher_id] = teacher_by_email.id
                session[teacher_category_name] = teacher_by_email.category.name
                session[teacher_role] = teacher_by_email.role.name
                return redirect(url_for("teacher.dashboard"))
            else:
                flash("Wrong Password", "danger")
                return render_template("teacher/login.html")
        else:
            flash("Invalid username or email", "danger")
            return render_template("teacher/login.html")
    return render_template("teacher/login.html")


@teacher.route("/message")
def message():
    """Display a message to the user regarding their account status

    This route is used to provide feedback to the user about their login attempt.
    If the user is not approved, a message is displayed that tells them that
    their account is not yet approved. If the user is approved, they are
    redirected to the login page.

    Args:
        teacher_status (str): The status of the teacher's account. Can be
            "Approved", "Pending", or "Rejected".

    Returns:
        str: The rendered template.
    """
    teacher_status = request.args.get("teacher_status")
    if teacher_status != "Approved":
        return render_template("teacher/message.html", message=teacher_status)
    return redirect(url_for("teacher.login"))


# Forget Password
def forget_password():
    pass


# OTP
def otp():
    pass


@teacher.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Logs out the currently logged-in teacher.

    This function handles the logout process for a teacher by clearing the
    session data associated with the teacher's account and redirecting
    them to the login page. If no teacher is logged in, it redirects to
    the login page. If the session does not contain a logged-in teacher,
    it redirects to the registration page.

    Returns:
        A redirect response to the login page or registration page.
    """

    if teacher_user_name not in session:
        return redirect(url_for("teacher.login"))
    if teacher_user_name in session:
        session.pop(teacher_user_name, None)
        session.pop(teacher_email, None)
        session.pop(teacher_id, None)
        session.pop(teacher_category_name, None)
        session.pop(teacher_role, None)
        return redirect(url_for("teacher.login"))
    return redirect(url_for("teacher.register"))


@teacher.route("/dashboard")
def dashboard():
    """
    Render the teacher dashboard with various options.

    This function handles the display of the teacher's dashboard, showing various
    options such as creating a new quiz, managing existing quizzes, viewing student
    results, and managing the teacher's profile. If the teacher is not logged in, it
    redirects them to the login page.

    Returns:
        A rendered template of the teacher's dashboard page.
    """
    if teacher_user_name not in session:
        return redirect(url_for("teacher.login"))
    return render_template("teacher/dashboard.html")


# Profile Section
@teacher.route("/profile", methods=["GET", "POST"])
def profile():
    """
    Render the teacher's profile with editable information.

    This function handles the display of the teacher's profile page, showing
    their full name, username, email, contact number, teacher information, and
    additional notes. If the teacher is not logged in, it redirects them to the
    login page.

    Returns:
        A rendered template of the teacher's profile page.
    """
    if teacher_user_name not in session:
        return redirect(url_for("teacher.login"))
    teacher = Teacher.query.get_or_404(session[teacher_id])
    return render_template("teacher/profile.html", teacher=teacher)


@teacher.route("/update_profile", methods=["GET", "POST"])
def update_profile():
    """
    Update the teacher's profile information.

    This function handles updating the teacher's profile by accepting POST
    requests with the updated full name, email, and contact number. It then
    saves these changes to the database. If the teacher is not logged in,
    they are redirected to the login page. After a successful update, the
    function redirects to the profile page and displays a success message.
    If there is an error, it displays the error message on the profile page.

    Returns:
        A redirect response to the login page if not logged in, or the
        profile page after updating the details.
    """

    if teacher_user_name not in session:
        return redirect(url_for("teacher.login"))
    if request.method == "POST":
        teacher = Teacher.query.get_or_404(session[teacher_id])
        teacher.full_name = request.form["full_name"]
        teacher.email = request.form["email"]
        teacher.contact_number = request.form["contact_number"]
        db.session.commit()
        flash("Action Successful", "success")
        return redirect(url_for("teacher.profile"))
    error = request.args.get("error")
    flash(error, "error")
    return redirect(url_for("teacher.profile"))


@teacher.route("/change_password", methods=["GET", "POST"])
def change_password():
    """
    Change the teacher's password.

    This function handles the change password process for a teacher.
    It checks if the teacher is logged in, and if so, it checks if the
    current password is correct. If the current password is correct,
    it checks if the new password and confirm password are the same.
    If they are the same, it sets the new password and redirects to
    the profile page. If any of the checks fail, it redirects to the
    profile page with an error message.

    Returns:
        A redirect response to the profile page.
    """
    if teacher_user_name not in session:
        return redirect(url_for("teacher.login"))
    if request.method == "POST":
        teacher = Teacher.query.get_or_404(session[teacher_id])
        if teacher.check_password(request.form["current_password"]):
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]
            if new_password == confirm_password:
                teacher.set_password(new_password)
                db.session.commit()
                return redirect(url_for("teacher.profile", error=""))
            else:
                return redirect(
                    url_for(
                        "teacher.update_profile",
                        error="New Password Is Not Similar To Confirm Password",
                    )
                )
        else:
            return redirect(url_for("teacher.update_profile", error="Wrong Password"))

    return redirect(url_for("teacher.profile", error=""))


# Quizzes Section
@teacher.route("/create_quiz", methods=["GET", "POST"])
def create_quiz():
    """
    Create a new quiz.

    This function handles the creation of a new quiz. It first checks if the
    teacher is logged in. If the teacher is logged in, it checks if the request
    method is POST. If the request method is POST, it adds the new quiz to the
    database and redirects to the create quiz page. If the request method is not
    POST, it renders the create quiz template with the category name and ID.

    Returns:
        A redirect response to the create quiz page if the request method is
        POST, or the create quiz template if the request method is not POST.
    """
    if teacher_user_name not in session:
        return redirect(url_for("teacher.login"))
    teacher_data = Teacher.query.get_or_404(session[teacher_id])
    category_name = teacher_data.category.name
    category_id = teacher_data.category.id
    if request.method == "POST":
        question = request.form["question"]
        option1 = request.form["option1"]
        option2 = request.form["option2"]
        option3 = request.form["option3"]
        option4 = request.form["option4"]
        correct_option_number = request.form["correct_option"]
        match correct_option_number:
            case "1":
                correct_option = option1
            case "2":
                correct_option = option2
            case "3":
                correct_option = option3
            case "4":
                correct_option = option4

        new_quiz = Quiz(
            question=question,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            category_id=category_id,
        )
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for("teacher.create_quiz"))

    return render_template(
        "teacher/create_quiz.html", category_name=category_name, category_id=category_id
    )


@teacher.route("/manage_quizzes")
def manage_quizzes():
    """
    Render the manage quizzes page for the teacher.

    This function checks if the teacher is logged in, and if so, retrieves
    and displays the quizzes created by the teacher. It supports searching
    quizzes by question text or options. If a search query is provided, it
    filters quizzes based on the query; otherwise, it retrieves all quizzes
    for the teacher's category. The results are then rendered in the
    'manage_quizzes.html' template.

    Returns:
        A rendered HTML page for managing quizzes.
    """

    if teacher_user_name not in session:
        return redirect(url_for("teacher.login"))
    search_query = request.args.get("search", "")
    if search_query:
        quizzes = (
            db.session.query(Quiz)
            .join(Category)
            .filter(
                or_(
                    Quiz.question.ilike(f"%{search_query}%"),
                    Quiz.option1.ilike(f"%{search_query}%"),
                    Quiz.option2.ilike(f"%{search_query}%"),
                    Quiz.option3.ilike(f"%{search_query}%"),
                    Quiz.option4.ilike(f"%{search_query}%"),
                    Quiz.correct_option.ilike(f"%{search_query}%"),
                ),
                Category.name == session[teacher_category_name],
            )
        )
    else:
        quizzes = (
            db.session.query(Quiz)
            .join(Category)
            .filter(Category.name == session[teacher_category_name])
        ).order_by(func.random())
    return render_template("teacher/manage_quizzes.html", quizzes=quizzes)


@teacher.route("/edit_quiz/<int:quiz_id>", methods=["GET", "POST"])
def edit_quiz(quiz_id):
    """
    Edit a quiz created by the teacher.

    This function first checks if the teacher is logged in. If the teacher is
    logged in, it checks if the request method is POST. If the request method is
    POST, it updates the quiz with the new details and redirects to the manage
    quizzes page. If the request method is not POST, it renders the edit quiz
    template with the quiz details.

    Args:
        quiz_id (int): The ID of the quiz to be edited.

    Returns:
        A redirect response to the manage quizzes page if the request method is
        POST, or the edit quiz template if the request method is not POST.
    """
    if teacher_user_name not in session:
        return redirect(url_for("teacher.login"))
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == "POST":
        question = request.form["question"]
        option1 = request.form["option1"]
        option2 = request.form["option2"]
        option3 = request.form["option3"]
        option4 = request.form["option4"]
        correct_option = request.form["correct_option"]
        match correct_option:
            case "1":
                correct_option = option1
            case "2":
                correct_option = option2
            case "3":
                correct_option = option3
            case "4":
                correct_option = option4
        quiz.question = question
        quiz.option1 = option1
        quiz.option2 = option2
        quiz.option3 = option3
        quiz.option4 = option4
        quiz.correct_option = correct_option
        db.session.commit()
        return redirect(url_for("teacher.manage_quizzes"))
    return render_template(
        "teacher/edit_quiz.html", quiz=quiz, category=session[teacher_category_name]
    )


@teacher.route("/delete_quiz/<int:quiz_id>", methods=["GET", "POST"])
def delete_quiz(quiz_id):
    """
    Deletes a quiz.

    This function deletes a quiz given its ID. The teacher needs to be logged in to
    access this endpoint. If the request method is POST, it deletes the quiz and
    redirects to the manage quizzes page. If the request method is not POST, it
    renders the manage quizzes template.

    Args:
        quiz_id (int): The ID of the quiz to be deleted.

    Returns:
        A redirect response to the manage quizzes page if the request method is
        POST, or the manage quizzes template if the request method is not POST.
    """
    if teacher_user_name not in session:
        return redirect(url_for("teacher.login"))
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for("teacher.manage_quizzes"))


# Students Section
@teacher.route("/view_results")
def view_results():
    """
    Renders the student results page for the teacher.

    This function renders the student results page for the teacher. It first checks
    if the teacher is logged in. If the teacher is logged in, it checks if the
    request method is GET. If the request method is GET, it retrieves and displays
    the results of the students in the teacher's category. It supports searching
    results by student username or email. If a search query is provided, it
    filters the results based on the query; otherwise, it retrieves all results
    for the teacher's category. The results are then rendered in the
    'results.html' template.

    Returns:
        A rendered HTML page for viewing student results.
    """

    if teacher_user_name not in session:
        return redirect(url_for("teacher.login"))
    search_query = request.args.get("search", "")
    if search_query:
        results = (
            db.session.query(Result)
            .join(User)
            .join(Category)
            .filter(
                or_(
                    User.username.ilike(f"%{search_query}%"),
                    User.email.ilike(f"%{search_query}%"),
                ),
                Category.name == session[teacher_category_name],
            )
        )
    else:
        results = (
            db.session.query(Result)
            .join(User)
            .join(Category)
            .filter(Category.name == session[teacher_category_name])
        )
    return render_template("teacher/results.html", results=results)
