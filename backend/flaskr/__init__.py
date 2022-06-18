from hashlib import new
import os
import select
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

#from models import setup_db, Question, Category

from models import * #DoghorSamuel

QUESTIONS_PER_PAGE = 10

#Pagination of questions

def paginating_questions(request, selection):
    page=request.args.get('Page', 1, type=int)
    start=(page - 1) * QUESTIONS_PER_PAGE
    end=start + QUESTIONS_PER_PAGE

    fmt_questions=[y.format() for y in selection]
    paged_questions=fmt_questions[start:end]

    return paged_questions #DoghorSamuel


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

   
   
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app) #DoghorSamuel
    CORS(app, resources={'/': {'origins': '*'}})

  
  
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Origins', '*')
        return response #DoghorSamuel

   
   
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
    #Access this endpoint locally with http://127.0.0.1:5000/categories
        all_cat=Category.query.order_by(Category.id).all()
        fmt_cat=[x.format() for x in all_cat]
       
        if len(all_cat)==0:
            abort(404)

        return jsonify({
            'Success': True,
            'Categories': fmt_cat
        })
    
    #Get all avalaible categories without pagination

   
   
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
    #Access this endpoint locally with http://127.0.0.1:5000/questions
        all_quest=Question.query.order_by(Question.category).all()
        all_cat=Category.query.all()
        fmt_cat=[z.type for z in all_cat]

        see_quest=paginating_questions(request, all_quest)

        if len(all_quest)==0:
            abort(404)
            
        return jsonify({
            'SUCCESS': True,
            'QUESTIONS': see_quest,
            'QUESTIONS ON PAGE': len(see_quest),
            'TOTAL QUESTIONS': len(all_quest),
            'Q_CATEGORIES': fmt_cat
        })

    #EXTRA: For single view
    @app.route('/questions/<int:question_id>', methods=['GET'])
    def view_one_question(question_id):
        question=Question.query.filter(Question.id==question_id).one_or_none()

        total=Question.query.all()

        fmt_one=question_id

        if question is None:
            abort(404)

        return jsonify ({
            'SUCCESS': True,
            'VIEWED QUESTION IS': fmt_one,
            'TOTAL QUESTIONS': len(total)
        })

   
   
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question=Question.query.filter(Question.id==question_id).one_or_none()

        fmt_one=question_id

        if (question is None):
            abort(404)

        try:
            question.delete()

            return jsonify ({
            'SUCCESS': True,
            'QUESTION DELETED': fmt_one,
            'TOTAL QUESTIONS': len(Question.query.all())
            })
        except:
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
        body=request.get_json()

        new_question=body.get('question')
        new_answer=body.get('answer')
        new_category=body.get('category')
        new_difficulty_level=body.get('difficulty')

        if ((new_question is None) or (new_answer is None) or (new_category is None) or (new_difficulty_level is None)):
            abort(422)        
        
        try:
            add_question=Question(question=new_question, answer=new_answer,               difficulty=new_difficulty_level, category=new_category)
           
            add_question.insert()
     
            return jsonify({
                'SUCCESS': True,
                'TOTAL QUESTIONS': len(Question.query.all())
            })
        except:
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

        body = request.get_json()
        search_term = body.get('searchTerm', None)
    
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term)))

        if not selection.count():
            abort(404)

        current_questions = paginating_questions(request, selection)

        return jsonify({
        'SUCCESS': True,
        'QUESTIONS': current_questions, 
        'TOTAL QUESTIONS': len(selection.all()),
        })




    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):

        try:
            questions = Question.query.filter(Question.category == str(category_id)).all()

            return jsonify({
                'SUCCESS': True,
                'QUESTIONS': [question.format() for question in questions],
                'TOTAL QUESTIONS': len(questions),
                'CURRENT CATEGORY': category_id
            })
        except:
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
            body = request.get_json()

            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(422)

            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            if category['type'] == 'click':
                available_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            else:
                available_questions = Question.query.filter_by(
                    category=category['id']).filter(Question.id.notin_((previous_questions))).all()

            new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(available_questions) > 0 else None

            return jsonify({
                'SUCCESS': True,
                'QUESTION': new_question
            })

        except:
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