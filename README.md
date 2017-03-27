# User Accounts
This is a Python app built using the Flask framework. It uses *sessions* to login and logout users. A user model has been implemented. In the `app.py` file Register and login view has been implemented. Since each view redirects to templates, the templates for index, Register, and Login have been implemented.


## Register View
The register view will show the users a form which will enable them to sign up into the database with their username, email, and password.


## Login View
The login view will check if the user is in the database. If it's there it will check if the correspondent password is associated with the username. If the username and password don't match, it will throw an exception (`models.DoesNotExist`).


# Templates
I created templates for Login and Register views, each will be invoked upon calling of the views in the `app.py`.
Since same form will be used for login and register view, I created a Macro for rendering same bit of code for both views.

The `app.py` python script can be run using `python3 app.py`. Once the server is running, access `0.0.0.0:8000` to access the application.