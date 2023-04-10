# ToDoApp_project

<h1> Flask TODO App developed using authentication and using MongoDB as documented-oriented database. </h1>

A Flask to-do app with MongoDB and authentication is a web application that allows users to create and manage their to-do lists. The application is built using the Flask web framework and the MongoDB NoSQL database, which provides a scalable and flexible data storage solution.

The application should have a registration and login system to ensure that each user's to-do list is private and secure. Once a user is authenticated, they can create and delete tasks on their to-do list. The user interface should allow users to add a task description and mark them as important or unimportant to each task.

The application should be built using the Model-View-Controller (MVC) architecture to separate concerns and make the code easier to maintain and update. The model layer should include the data structures and functions that interact with the MongoDB database. The view layer should include the HTML templates and CSS styles that define the user interface. The controller layer should include the Flask routes and functions that handle user input and manage the flow of data between the model and view layers.

<i><h3>Please install the following packages before run the application as follows:</i></h3>

pip install -U Flask

pip install Flask pymongo

pip install bcrypt


<i><h3>To run the application use the command below:</i></h3>

python -m flask run

Registration landing page.
![Screenshot (174)](https://user-images.githubusercontent.com/90685473/230963541-cdd0fc72-42b2-4e45-a095-92a9e54205ce.png)


Registration form details - user must insert their details filling out the form.
![Screenshot (170)](https://user-images.githubusercontent.com/90685473/230963721-e135eddb-9412-4b16-8c29-66da78305296.png).


Page of user logged after being registered - there are also options to go to TodoApp or Exit the App.
![Screenshot (172)](https://user-images.githubusercontent.com/90685473/230963936-90264234-aed1-4c1d-9f0d-50cdd88874f8.png)


The Todo App landing page - user has the option to go back to previous page clicking on the go back link.
![Screenshot (173)](https://user-images.githubusercontent.com/90685473/230964320-a721a313-6aa9-48a2-87bd-cd236393445b.png)
