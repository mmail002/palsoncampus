function codeAddress() { /*Using Google maps API, gets lat and long and will load those in the loadWeather 
    func, the lat and long are returned by entering a location in serach bar and hitting enter */
    var address = document.getElementById("address").value; // Looks at input box with id address
    var geocoder = new google.maps.Geocoder(); //Call to Google maps API

    geocoder.geocode( { 'address': address}, function(results, status) {
        var location = results[0].geometry.location; // return location lat and long
        //alert('LAT: ' + location.lat() + ' LANG: ' + location.lng()*-1);
        /*loadWeather(location.lat()+','+location.lng())*/
        
        var uluru = {lat: location.lat(), lng: location.lng()};
            var map = new google.maps.Map(document.getElementById('map'), {
              zoom: 4,
              center: uluru
            });
            var marker = new google.maps.Marker({
              position: uluru,
              map: map
            });
    });
    }
    google.maps.event.addDomListener(window, 'load', codeAddress); //not sure to be honest