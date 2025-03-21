"""
! Created On Fri January 03 10:26 PM 2025

! @author: Talha Usman
! Status: Developer
"""

# Login And Sign Up

from . import *
import random as rd


# Universal Functions
def login_required(f):
    """
    Decorator function to ensure a user is logged in before accessing a route.

    If the user is not logged in, they are redirected to the signup page.
    Otherwise, the original function is executed.

    Args:
        f (function): The view function to be decorated.

    Returns:
        function: The decorated function that checks the login status.
    """

    @wraps(f)
    def checking_session(*args, **kwargs):
        """
        Decorator function to ensure a user is logged in before accessing a route.

        If the user is not logged in, they are redirected to the signup page.
        Otherwise, the original function is executed.

        Args:
            f (function): The view function to be decorated.

        Returns:
            function: The decorated function that checks the login status.
        """

        if student_user_name not in session:
            return redirect(url_for("user.signup"))
        return f(*args, **kwargs)

    return checking_session


@user.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handle user signup.

    If the user is already logged in, redirect them to their dashboard.

    If the user submits a signup form, check if the username or email already exists.
    If it does, flash a danger message and show the signup form again.
    If not, create a new user, hash the password, add the user to the database and
    flash a success message, then redirect them to the login page.

    If the user just visits the signup page, show the signup form.

    Returns:
        str: HTML of the signup page.
    """
    if student_user_name in session:
        return redirect(url_for("user.dashboard"))
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_email = request.form["email"]
        user_password = request.form["password"]
        check_user = User.query.filter_by(username=user_name).first()
        check_email = User.query.filter_by(email=user_email).first()
        if check_user or check_email:
            if check_user:
                flash("User already exists", "danger")
            elif check_email:
                flash("Email already exists", "danger")
            return render_template("user/signup.html")
        else:
            new_user = User(username=user_name, email=user_email)
            new_user.set_password(user_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Signup Successful", "success")
            return redirect(url_for("user.login"))
    return render_template("user/signup.html")


@user.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.

    If the user is already logged in, redirect them to the admin dashboard.

    If the user submits a login form, check if the username or email exists.
    If it does, check if the password is correct. If it is, log the user in and
    redirect them to their dashboard. If not, flash a danger message and show
    the login form again.

    If the user just visits the login page, show the login form.

    Returns:
        str: HTML of the login page.
    """
    if student_user_name in session:
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        email_or_username = request.form["email_or_username"]
        password = request.form["password"]
        user_by_name = User.query.filter_by(username=email_or_username).first()
        user_by_email = User.query.filter_by(email=email_or_username).first()
        if user_by_name or user_by_email:
            if user_by_name:
                user_data = verifying_login(user_by_name, password)
            elif user_by_email:
                user_data = verifying_login(user_by_email, password)
            if user_data:
                return redirect(url_for("user.dashboard"))
            else:
                flash("Invalid Password", "danger")
                return redirect(url_for("user.login"))
        else:
            flash("Invalid username or email", "danger")
            return redirect(url_for("user.login"))
    return render_template("user/login.html")


def verifying_login(user_data, password):
    """
    Verify a user's password and log them in if correct.

    Args:
        user_data (User): The user to verify.
        password (str): The password to check.

    Returns:
        bool: True if the password is correct, False if not.
    """
    checking_password = user_data.check_password(password)
    if checking_password:
        session[student_user_name] = user_data.username
        session[student_email] = user_data.email
        session[student_user_id] = user_data.id
        return True
    return False


@user.route("/logout")
def logout():
    """
    Log the user out and redirect them to the login page.

    If the user is not logged in, redirect them to the signup page.

    Returns:
        str: HTML of the login or signup page.
    """
    if student_user_name in session:
        session.pop(student_user_name, None)
        session.pop(student_email, None)
        session.pop(student_user_id, None)
        return redirect(url_for("user.login"))
    return redirect(url_for("user.signup"))


# Panel
@user.route("/panel", methods=["GET", "POST"])
@login_required
def dashboard():
    """
    Render the user dashboard with various quiz categories and leaderboard.

    This function handles the display of the user's dashboard, showing different
    categories of quizzes such as featured, hot, and simple categories, as well as
    top-rated categories and a leaderboard of top results. It ensures that only
    logged-in users can access the dashboard. If the user is not logged in, they
    are redirected to the signup page.

    Returns:
        str: HTML content for the user's dashboard page.
    """

    if student_user_name not in session:
        return redirect(url_for("user.signup"))
        # featured.in_ is used database instead of in of python
    session.pop(result_token, None)
    featured_categories = (
        db.session.query(Category)
        .filter(text("json_extract(category.category_type, '$') LIKE :featured"))
        .params(featured=f"%{featured}%")
        .all()
    )
    hot_categories = (
        db.session.query(Category)
        .filter(text("json_extract(category.category_type, '$') LIKE :hot"))
        .params(hot=f"%{hot}%")
        .all()
    )
    simple_categories = (
        db.session.query(Category)
        .filter(text("json_extract(category.category_type, '$') LIKE :simple"))
        .params(simple=f"%{simple}%")
        .all()
    )

    top_rated_categories = Category.query.order_by(Category.rating.desc()).all()
    leaderboard = Result.query.order_by(Result.score.desc()).all()

    return render_template(
        "user/dashboard.html",
        featured_categories=featured_categories,
        hot_categories=hot_categories,
        simple_categories=simple_categories,
        top_rated_categories=top_rated_categories,
        leaderboard=leaderboard[:8],
        user_name=session[student_user_name],
    )


@user.route("/settings")
@login_required
def settings():
    """
    Render the user settings page.

    This function retrieves the currently logged-in user's information
    from the database using the user ID stored in the session. It then
    renders the 'user/settings.html' template, passing the user object to
    the template context for display.

    Returns:
        A rendered HTML page for user settings.
    """

    user = User.query.get_or_404(session[student_user_id])
    return render_template("user/settings.html", user=user)


@user.route("/update_settings", methods=["POST"])
@login_required
def update_settings():
    """
    Update the current user's settings.

    This function handles the submission of the user settings form.
    It retrieves the logged-in user's information from the session,
    updates the username, email, and password if provided, and commits
    the changes to the database. The user is then redirected back to
    the settings page.

    Returns:
        A redirect response to the user settings page.
    """

    if request.method == "POST":
        user = User.query.get_or_404(session[student_user_id])
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if not password or " " in password or password is None:
            pass
        else:
            # Update Password
            user.set_password(password)

        user.username = username
        user.email = email
        db.session.commit()
    return redirect(url_for("user.settings"))


# Quizzes Section
@user.route("/start_quiz/<int:category_id>", methods=["GET", "POST"])
@login_required
def start_quiz(category_id):
    """
    Start a quiz for a given category.

    This function is responsible for rendering the quiz page for a given
    category. It generates a list of questions for the category, shuffles
    them, and stores them in the session. It then renders the 'user/quiz.html'
    template, passing the questions, category ID, and quiz category name
    to the template context for display.

    Args:
        category_id (int): The ID of the category to generate the quiz for.

    Returns:
        A rendered HTML page for the quiz.
    """

    answers_ = f"{answers}-{category_id}"
    questions__ = f"{questions_}-{category_id}"
    if answers_ not in session:
        session[answers_] = {}
    if questions__ not in session:
        questions = db.session.query(Quiz).filter_by(category_id=category_id).all()
        rd.shuffle(questions)
        session[questions__] = [
            {
                "id": question.id,
                "category_id": category_id,
                "question": question.question,
                "options": [
                    question.option1,
                    question.option2,
                    question.option3,
                    question.option4,
                ],
                "correct_option": question.correct_option,
            }
            for question in questions
        ]

    questions = session[questions__]
    quiz_category = Category.query.filter_by(id=category_id).first()
    return render_template(
        "user/quiz.html",
        questions=questions,
        category_id=category_id,
        answers=answers_,
        quiz_category=quiz_category.name,
    )


@user.route("/save_selected_answers_count", methods=["POST"])
@login_required
def save_selected_answers_count():
    """
    Save the number of selected answers for a given category in the user's session.

    This is an AJAX endpoint that receives the number of selected answers and
    the category ID from the user's browser and saves it in the session. This
    allows the user to leave the quiz page and come back without having to
    re-select all the answers.

    Args:
        selected_count (int): The number of selected answers.
        category_id (int): The ID of the category.

    Returns:
        A JSON response containing a success or error message.
    """
    data = request.get_json()
    selected_count_ = data.get(selected_count, 0)
    category_id = data.get("category_id", None)
    if category_id is not None:
        session[f"{selected_count}-{category_id}"] = selected_count_
        print(
            f"Session for {category_id}: {session[f'{selected_count}-{category_id}']}"
        )
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Selected answers count and category received successfully.",
                }
            ),
            200,
        )
    else:
        return jsonify({"status": "error", "message": "Category ID not found"}), 400


# This will safe the answers of the users when the page is refreshed
@user.route("/save_user_answers", methods=["POST"])
@login_required
def save_user_answers():
    """
    Save the user's answers to the session.

    This endpoint is used to save the user's answers when the user leaves the quiz page.
    The answers are saved in the session for the current user.

    Args:
        data (dict): A dictionary with the answers. The dictionary should contain a key
            named "answers" that contains a list of dictionaries with the following keys:

            * question_id (int): The ID of the question.
            * selected_answer (str): The selected option for the question.

    Returns:
        A JSON response containing a success or error message.
    """
    data = request.get_json()
    if answers in data:
        # save or update the answers
        session[answers] = session.get(answers, {})
        for answer in session[answers]:
            question_id = str(answer["question_id"])
            selected_option = answer["selected_answer"]
            session[answers][question_id] = selected_option
        return jsonify({"message": "Answers saved successfully"}), 200
    return jsonify({"error": "No answers provided"}), 400


@user.route("/submit_quiz/<int:category_id>", methods=["GET", "POST"])
@login_required
def submit_quiz(category_id):
    """
    This endpoint is used to submit a quiz. It is accessed when the user clicks on the
    "Submit Quiz" button. The user's answers are saved in the session and the score is
    calculated. The user is then redirected to the rate quiz page.

    Args:
        category_id (int): The ID of the category.

    Returns:
        A redirect response to the rate quiz page.
    """
    if request.method == "POST":
        questions = session[f"{questions_}-{category_id}"]
        score = 0
        for question in request.form:
            print(question.split("_")[1])
            question_id = int(question.split("_")[1])
            correct_option_number = request.form[
                question
            ]  # in the form of option1, option2, option3, option4
            for q in questions:
                if q["id"] == question_id:
                    user_option = int(correct_option_number[-1])
                    user_option = q["options"][user_option - 1]
                    correct_option = q["correct_option"]
                    # print(f"{i}){user_option} == {correct_option}")
                    if user_option == correct_option:
                        score += 1
        score = int(score / len(questions) * 100)
        result = Result(
            user_id=session[student_user_id],
            category_id=category_id,
            score=score,
        )
        db.session.add(result)
        db.session.commit()
        session.pop(f"{questions_}-{category_id}", None)
        session[result_token] = str(uuid.uuid4())

        return redirect(url_for("user.rate_quiz", category_id=category_id, score=score))
    return redirect(url_for("user.start_quiz", category_id=category_id))


@user.route("/rate_quiz/<int:category_id>", methods=["GET", "POST"])
@login_required
def rate_quiz(category_id):
    """
    This endpoint is used to rate a quiz after the user has completed it. The user is
    presented with a form to rate the quiz from 1 to 5 and write a review. The rating
    and review are then stored in the Reviews table and the category's total rating
    is updated.

    Args:
        category_id (int): The ID of the category.

    Returns:
        A redirect response to the same page if the form is submitted successfully or
        a rendered template of the quiz result page if the form is not submitted.
    """
    score = request.args.get("score")
    if result_token not in session:
        return redirect(url_for("user.dashboard"))
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        rating = request.form["rating"]
        rating = int(rating)
        review = request.form["review"]
        new_review = Review(
            user_id=session[student_user_id],
            category_id=category_id,
            rating=rating,
            comment=review,
        )
        category = Category.query.get_or_404(category_id)
        if not category.total_rating:
            category.total_rating = 0
        if not category.len_rating:
            category.len_rating = 0
        category.total_rating += rating
        category.len_rating += 1
        category.calculate_rating()
        db.session.add(new_review)
        db.session.commit()
        session.pop(result_token, None)
        return redirect(url_for("user.rate_quiz", category_id=category_id, score=score))

    return render_template("user/quiz_result.html", score=score, category=category)


@user.route("/past_quizzes")
@login_required
def past_quizzes():
    """
    This endpoint is used to display the user's past quizzes. It is accessed when the user
    clicks on the "Past Quizzes" link in the navbar. The user's results are retrieved from
    the database and passed to the template to be displayed.

    Returns:
        A rendered template of the past quizzes page.
    """

    user = User.query.get_or_404(session[student_user_id])
    results = user.results
    return render_template("user/past_quizzes.html", results=results)


@user.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html", user_=user, results=user.results)
