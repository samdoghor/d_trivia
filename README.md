# Trivia API Project (UDACITY)
## Overview
Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game.

This application:

1- Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.

2- Delete questions.

3- Add questions and require that they include question and answer text.

4- Search for questions based on a text query string.

5- Play the quiz game, randomizing either all questions or within a specific category.


## Getting Started 
### Pre-requisites and Local Development

Developers using this project should already have:

- Python
- Pip 
- node 

#### Backend 

inside the backend folder initialize and activate a virtualenv (for Windows users)
```
python -m virtualenv trivia_env
source trivia_env/Scripts/activate
```
>**Note** - In MAC, the `env` path `Scripts` is replaced with `bin` directory. Therefore, you'd use the analogous command shown below:
```
source trivia_env/bin/activate
```

then run ``` python -m pip install -r requirements.txt``` All required packages are included in the requirements file (latest version used for the project).


To run the application run the following commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
The application is run on  ``` http://127.0.0.1:5000/``` by default and is a proxy in the frontend configuration.



#### Frontend

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory of this repository. After cloning, open your terminal and run:

```
$ npm install
```
The frontend app was built using create-react-app. In order to run the app in development mode use npm start. You can change the script in the package.json file.

```
$ npm start
```
Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.


#### Tests

To run the tests, run

```
drop database trivia_test
create database trivia_test
```
login into the database and run 

```
\i trivia.psql
```
to populate database

```
python test_flaskr.py
```

to run test

## API Reference
### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": <error code>,
    "message": <"error message>
}
```

The API will return three major types of errors when requests fail,
These are:
404: Resource Not Found
422: Not Processable
405: Method Not Allowed

Others Include:
400: Bad Request
500: Internal Server Error

### Endpoints
The endpoints include:

GET '/categories'
GET '/categories/<int:id>/questions'
GET '/questions'
POST '/questions'
DELETE '/questions/<int:id>'
POST  '/questions/search'
POST '/quizzes'

**GET /categories**
General:
- Returns a list of categories, success value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

Sample: ```curl http://127.0.0.1:5000/categories```

```
{
  "CATEGORIES": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "SUCCESS": true
}
```

**GET /categories/{id}/questions**
General:
- Returns a list of questions, in the given category, category total_questions and success value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

Sample: ```curl http://127.0.0.1:5000/categories/2/questions```

```
{
  "CURRENT CATEGORY": 2, 
  "QUESTIONS": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "SUCCESS": true, 
  "TOTAL QUESTIONS": 4
}
```

**GET /questions**
General:
- Returns all questions avalaible in database, success value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

Sample: ```curl http://127.0.0.1:5000/questions```

```
{
  "QUESTIONS": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "QUESTIONS ON PAGE": 10,
  "Q_CATEGORIES": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "SUCCESS": true,
  "TOTAL QUESTIONS": 19
}

```

**POST /questions**
General:
- Creates a new question using the submitted title, answer, category and difficulty. Returns the id of the created question id, success value, total questions number, and questions list based on current page number to update the frontend

Sample: ```curl -X POST -H "Content-Type: application/json" -d '{"question":"What was the name of the first man-made satellite launched by the Soviet Union in 1957?", "answer": "Sputnik 1","category" :"1", "difficulty":"2"}' http://127.0.0.1:5000/questions'```


```
{
  "SUCCESS": true,
  "TOTAL QUESTIONS": 20
}
```

**DELETE /questions/{id}**

General:
- Deletes the question of the given ID if it exists. Returns success value.

Sample ```curl -X DELETE http://127.0.0.1:5000/questions/15 ```


```
{
  "QUESTION DELETED": 15,
  "SUCCESS": true,
  "TOTAL QUESTIONS": 19
}
```

**POST /search**
General:
- search for a question using the submitted search term. Returns the results, success value, total questions.

Sample ```curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who"}'```

```
{
  "QUESTIONS": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "SUCCESS": true,
  "TOTAL QUESTIONS": 3
}

```

**POST /quizzes**
General:
- recive the actual question and the category
- return the next question in the same category and success value.

Sample``` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Geography","id":"3"}, "previous_questions":[13]}'``` 

```
{
  "QUESTION": {
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
  },
  "SUCCESS": true
}
```