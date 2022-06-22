from hashlib import new
import os
import select
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

#from models import setup_db, Question, Category

from models import *  # DoghorSamuel

QUESTIONS_PER_PAGE = 10

# Pagination of questions


def paginating_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    fmt_questions = [y.format() for y in selection]
    paged_questions = fmt_questions[start:end]

    return paged_questions  # DoghorSamuel


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)  # DoghorSamuel
    CORS(app, resources={'/': {'origins': '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Origins', '*')
        return response  # DoghorSamuel

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        # Access this endpoint locally with http://127.0.0.1:5000/categories
        try:
            all_cat = Category.query.order_by(Category.id).all()
            fmt_cat = [x.format() for x in all_cat]

            if len(all_cat) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'categories': fmt_cat
            })

        except BaseException:
            abort(404)

    # Get all avalaible categories without pagination

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_question():
        # Access this endpoint locally with http://127.0.0.1:5000/questions
        all_quest = Question.query.order_by(Question.category).all()
        all_cat = Category.query.all()
        fmt_cat = [z.type for z in all_cat]
        see_quest = paginating_questions(request, all_quest)

        if len(see_quest) == 0:
            abort(404)

        try:
            return jsonify({
                'success': True,
                'questions': see_quest,
                'questions on page': len(see_quest),
                'total questions': len(all_quest),
                'q_categories': fmt_cat
            })

        except BaseException:
            abort(404)

    # EXTRA: For single view
    @app.route('/questions/<int:question_id>', methods=['GET'])
    def view_one_question(question_id):

        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            total = Question.query.all()

            fmt_one = question_id

            if question is None:
                abort(404)

            return jsonify({
                'success': True,
                'viewed question is': fmt_one,
                'total questions': len(total)
            })

        except BaseException:
            abort(404)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        fmt_one = question_id

        if (question is None):
            abort(404)

        try:
            question.delete()

            return jsonify({
                'success': True,
                'question deleted': fmt_one,
                'total questions': len(Question.query.all())
            })
        except BaseException:
            abort(405)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty_level = body.get('difficulty')

        if ((new_question is None) or (new_answer is None) or (
                new_category is None) or (new_difficulty_level is None)):
            abort(422)

        try:
            add_question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty_level,
                category=new_category)

            add_question.insert()

            return jsonify({
                'success': True,
                'total questions': len(Question.query.all())
            })
        except BaseException:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()
            search_term = body.get('searchTerm', None)

            selection = Question.query.order_by(
                Question.id).filter(
                Question.question.ilike(
                    '%{}%'.format(search_term)))

            if not selection.count():
                abort(404)

            current_questions = paginating_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total questions': len(selection.all()),
            })

        except BaseException:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        questions = Question.query.filter(
            Question.category == str(category_id)).all()

        if len(questions) == 0:
            abort(404)

        try:
            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total questions': len(questions),
                'current category': category_id
            })
        except BaseException:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body=request.get_json()
            quiz_category=body.get('quiz_category')
            previous_questions=body.get('previous_questions')
            category_id = quiz_category['id']
    
            if ((quiz_category is None) or (previous_questions is None)):
                abort(404)

            if (category_id is None):
                view_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            
            else:
                view_questions = Question.query.filter_by(category=category_id).filter(Question.id.notin_(previous_questions)).all() #As seen in https://developpaper.com/translation-nested-query-using-sqlalchemy-orm/

            if(view_questions):
                question = random.choice(view_questions) #As seen in https://www.w3schools.com/python/ref_random_choice.asp

            return jsonify({
                'success': True,
                'question': question.format(),
                'category': category_id
            })

        except BaseException:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
