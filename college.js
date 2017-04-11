var xhr = new XMLHttpRequest();
xhr.responsetype = 'json';

// api_key need to be changed to the one used for the project.
var api_key = api_key="iISiVMY34WrNnYh3reQGYUshNnNKu3QyuprdcKh1";
var url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?api_key=" + api_key +  "&school.name=Plattsburgh&_fields=id,school.name,school.state,school.city,school.zip"
xhr.open('GET', url, true);
xhr.onreadystatechange = function(){
	console.log(xhr.response);
};
xhr.send();
