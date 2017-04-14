
/* 
 * @author: Jayant Arora <jaistudy1996@gmail.com>
 * @description: This file runs scripts to fetch college names from collegescorecard api
 * @date: Apr 14, 2017.
 */


var getCollegeInfo = function(school_name){
	var xhr = new XMLHttpRequest();
	
	// api_key need to be changed to the one used for the project.
	var api_key = "iISiVMY34WrNnYh3reQGYUshNnNKu3QyuprdcKh1";
	var url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?api_key=" + api_key +  "&school.name=" + school_name + "&_fields=id,school.name,school.state,school.city,school.zip";
	xhr.open('GET', url, true);
	xhr.responseType = 'json';
	var dataListDiv = document.getElementById('campus_names_data_div');
	xhr.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			if(dataListDiv.childNodes.length > 0){
				dataListDiv.removeChild(dataListDiv.firstChild);
			}
			var dataList = document.createElement('datalist');
			dataList.id = 'campus_names_data';
			for(var i=0; i<xhr.response.results.length; i++){
				var option = document.createElement('option');
				option.value = xhr.response.results[i]["school.name"];
				dataList.appendChild(option);
			}
			dataListDiv.appendChild(dataList);
		}
	};
	xhr.send();
}

var campus = document.getElementById('campus');
campus.onkeyup = function(){
	var school_name = campus.value;
	getCollegeInfo(school_name);
}
