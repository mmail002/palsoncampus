# palsoncampus

#Weather Widget

Css and inital html taken from  https://github.com/subhroisback/weather-app/archive/master.zip

Serach using google api, using lat and long taken from http://stackoverflow.com/questions/11033451/find-the-latitude-and-longitude-using-javascript (author Abhishek)

The app now will ask for location and if access is denied then it will display text saying enter your location (not preferable, but becuase of firefox where if the user say don't give my location the load weather for a location won't work I coded it like mentioned to be consistant on any browser)

do git clone (my git url) and then open the index.html to see the app

Edited the code so if you are in a country that uses Fahrenheitit will show Fahrenheit and respectivly for Celcius

The weather feed from Yahoo is updated every 4 hours, which makes since concidering the info is free

It seems as though the wind speed that is pulled from the API is quite wrong, so please note that

And if you find an issue where you set your browser to allow location services (say for a day like in safari) and you load the app and the geolocation takes too long, so you enter the desired location, and after a min the text "Enter your location in the serach bar " replace your location, that is because the geolocation has timed out and is going to it's fallback of showing that text

Now does sanity check on temp

Added daily high and low 

not yet implemented on the unix server yet

Need to get with html page writer and have him implement the code into html