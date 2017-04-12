# events

Code for events

The code below in main.py is where you need to change the html page that you want the server to run:
Below you can see where I changed it to button.html where it was index.html

@app.route('/')
def index():
    #return render_template('index.html')
    return render_template('button.html')


 If you run the dev_appserver it will pull up the button page, but on click it does not go to the event.html....
 It may mean we need to add code to main.py to get it to look for the next page

 Remove pop-up window for time being, not sure how to do a pop-up window using flask and js

 Am now using the same background and text style as home screen 
