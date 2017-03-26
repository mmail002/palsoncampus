
if("geolocation" in navigator) { //If geolocation is available, ask browser
    function success1(position) { // If geolocation is accepted, the func will return data
    var latitude  = position.coords.latitude;
    var longitude = position.coords.longitude;
    loadWeather(latitude+','+longitude);
}
    
    TempLocation = ""; //Var that will stored college from db
    function error1() { //If Geolocation request is denied the func will do this
    
    if(TempLocation != ""){
        document.getElementById("address").value = TempLocation;
        codeAddress()
    } else{
        errorText = "Enter Your Location in Search Bar" //Will be displayed if error1 func is processed
        $(".location").text(errorText); // Render text above in the location position
    }
  }
    navigator.geolocation.getCurrentPosition(success1,error1); /* function that gets position, and if 
    geolocation was allowed with return what success1 gave it else, it will use what error1 gave it*/
} else{
    loadWeather("Plattsburgh,US",""); //If geolocation is not supported it will do this
}

$(document).ready(function(){ 
    setInterval(getWeather,600000); // How often it updates, the 600000 is in miliseconds
    //The weather feed is updated every 4 hours!!!!!
});

function codeAddress() { /*Using Google maps API, gets lat and long and will load those in the loadWeather 
    func, the lat and long are returned by entering a location in serach bar and hitting enter */
    var address = document.getElementById("address").value; // Looks at input box with id address
    var geocoder = new google.maps.Geocoder(); //Call to Google maps API

    geocoder.geocode( { 'address': address}, function(results, status) {
        var location = results[0].geometry.location; // return location lat and long
        //alert('LAT: ' + location.lat() + ' LANG: ' + location.lng()*-1);
        loadWeather(location.lat()+','+location.lng())
    });
    }
    google.maps.event.addDomListener(window, 'load', codeAddress); //not sure to be honest

tempStore = 0 //var needed for func below to work 
countryStore = "" //var needed for func below to work 
highTempStore = 0
lowTempStore = 0
function ChangeTemp(){ /*Func that allows click on /f or /c to work, converts temp, in the loadWeather func
    you will need to change the if to TempTest to artifically use this func*/
    var elem = document.getElementById("convert");//look at the button with id convert in index.html
    if(elem.value == "/ C"){ // if button is set to / C
        temperature = Math.round((tempStore -32)*(5/9))+ '&deg;' + 'C'; // On click it will convert
        day_high = 'Hi: ' +Math.round((highTempStore -32)*(5/9))+ '&deg;' + 'C'; // day high in C
        day_low = 'Low: '+Math.round((lowTempStore -32)*(5/9))+ '&deg;' + 'C'; // day low in C
        //temperature = 100 + '&deg;' + 'C'; //110 degree test
        $(".temperature").html(temperature); // in the tempature location it will render the conveter temp
        $(".day_high").html(day_high);
        $(".day_low").html(day_low);
        elem.value = "/ F"; // set button to / F
    }
    else{
        temperature =  tempStore+ '&deg;' + 'F'; //If button is / F
        day_high = 'Hi: ' +highTempStore + '&deg;' + 'F'; //day high in F
        day_low = 'Low: '+lowTempStore + '&deg;' + 'F'; // day low in F
        $(".temperature").html(temperature); // on click render temp in F
        $(".day_high").html(day_high);
        $(".day_low").html(day_low);
        elem.value = "/ C"; // set button to / C
    }
}

function TempSanityCheck() { // Func that will check the sanity of the tempature pulled
        $(".temperature").text("Inaccurate"); //text that will display in case of error
        document.getElementById("temperature").style.fontSize = "xx-large"; // make render text large
        document.getElementById("temperature").style.left = "50px";//left position on html 
        document.getElementById("temperature").style.top = "70px";//right position on html
        var elem = document.getElementById("convert"); // Get the convert button 
        elem.value == ""; //Set convert button to "" as there was an error
}

function loadWeather(location, woeid,TempTest = false){ /*Main weather loading func, TempTest is used
    to text the func (will allow you to enter any temp you want)*/
    $.simpleWeather({ //call to simpleWeather API
        location: location,
        woeid: woeid,
        unit: 'F', //By default will pull in F
        success: function(weather){ //if it was able to get the simpleWeather API then...
            var elem = document.getElementById("convert");
            tempStore = weather.temp; // Needed for ChangeTemp func to work 
            highTempStore = weather.high
            lowTempStore = weather.low
            countryStore = weather.country // Checks to see if the country entered uses F, needed for ChangeTemp
            if (weather.country == "United States" || weather.country == 'The Bahamas' || 
                weather.country == "Belize" || weather.country == "Cayman Islands" || 
                weather.country == "Palau" || weather.country == "Puerto Rico" ||
                weather.country == "Guam" || weather.country == "US Virgin Islands"){
                if(weather.temp > 120 || weather.temp < -30){
                    TempSanityCheck() // Calls SanityCheck func
                }
                else{
                elem.value = "/ C"; // sets button to / C
                temp = weather.temp + '&deg;' + 'F'; // displays temp in F
                day_high = 'Hi: ' +weather.high + '&deg;' + 'F';
                day_low = 'Low: '+weather.low + '&deg;' + 'F';
                }
            }
            else{
                if(weather.temp > 120 || weather.temp < -30){
                    TempSanityCheck()
                }
                else{
                elem.value = "/ F";// sets button to / F
                temp = Math.round((weather.temp -32)*(5/9))+ '&deg;' + 'C'; // conversion from F to C
                day_high = 'Hi: ' +Math.round((weather.high -32)*(5/9))+ '&deg;' + 'C';
                day_low = 'Low: '+Math.round((weather.low -32)*(5/9))+ '&deg;' + 'C';

            }
            }
            last_update = 'Last Updated: ' + weather.updated /* Gets last time weather feed was updated
            how often that happens is up to the API*/
            region_city =weather.city+","+weather.region // Gets city and region of location
            wcode = '<img class="weathericon" src="images/weathericons/'+weather.code+'.svg">';
            wind = '<p>'+weather.wind.speed+'</p><p>'+weather.units.speed+'</p>'; // gets wind speed
            humidity = weather.humidity+' %'; // Gets humidity
            //Here is where all the info is rendered to the screen
            $(".location").text(region_city);
            $(".temperature").html(temp);
            $(".climate_bg").html(wcode);
            $(".windspeed").html(wind);
            $(".humidity").text(humidity);
            $(".updated").text(last_update);
            $(".day_high").html(day_high);
            $(".day_low").html(day_low);
        },
        error: function(error){ // if error getting to API display the error below
            $(".error").html('<p>'+error+'</p>');
        }
        
    });
}
