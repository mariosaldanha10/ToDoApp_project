# ToDoApp_project

<h1> Flask TODO App developed using authentication and using MongoDB as documented-oriented database. </h1>

A Flask to-do app with MongoDB and authentication is a web application that allows users to create and manage their to-do lists. The application is built using the Flask web framework and the MongoDB NoSQL database, which provides a scalable and flexible data storage solution.

The application should have a registration and login system to ensure that each user's to-do list is private and secure. Once a user is authenticated, they can create and delete tasks on their to-do list. The user interface should allow users to add a task description and mark them as important or unimportant to each task.

The application should be built using the Model-View-Controller (MVC) architecture to separate concerns and make the code easier to maintain and update. The model layer should include the data structures and functions that interact with the MongoDB database. The view layer should include the HTML templates and CSS styles that define the user interface. The controller layer should include the Flask routes and functions that handle user input and manage the flow of data between the model and view layers.

Please install the following packages before run the application as follows:

pip install -U Flask
pip install Flask pymongo
pip install bcrypt

To run the application use the command below:

python -m flask run
