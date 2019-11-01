var myChart;
window.onload=function(){
	var ctx = document.getElementById('myChart');
	myChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [{
				label: 'temperature',
				fill: false,
				backgroundColor: "#000000",
				data: temperature,
				borderColor: "#000000",
				borderWidth: 1,
				pointRadius: 0,
				spanGaps: false
			},
			{
				label: 'min',
				fill: false,
				spanGaps: true,
				backgroundColor: '#0000ff',
				data: min,
				borderColor: '#0000ff',
				borderWidth: 1,
				pointRadius: 0,
				lineTension: 0
			},
			{
				label: 'max',
				fill: false,
				backgroundColor: '#ff0000',
				data: max,
				borderColor: '#ff0000',
				borderWidth: 1,
				pointRadius: 0,
				lineTension: 0
			}]
		},
		options: {
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero: false
					}
				}],
				xAxes:[{
					type: 'time',
					time: {
						unit: 'minute',
						displayFormats: {
							minute: 'HH:mm',
							hour: 'DD-MM HH:mm',
							day: 'DD MM'
						}
					}
			   
				}]
			},
			plugins: {
				zoom: {
					zoom: {
						enabled: true,
						drag: true,
						mode: 'xy',
						rangeMin: {
							x: null,
							y: null
						},
						rangeMax: {
							x: null,
							y: null
						},
						speed: 0.1,
					}
				}	
			},
			maintainAspectRatio: false,
			responsive: true
		}
	});


	function setDataSet(){
		myChart.data.labels = [];
		myChart.data.datasets[0].data = [];
		myChart.data.datasets[1].data = [];
		myChart.data.datasets[2].data = [];
		for (var i = 0; i < group.length; i++) {
			
			if (group.item(i).checked && group.item(i).value == "all") {
				myChart.data.datasets[0].data = temperature;
				myChart.data.labels = labels;
				myChart.data.datasets[1].data = min;
				myChart.data.datasets[2].data = max;
			}else if (group.item(i).checked && group.item(i).value == "week") {
				for(var j = 0; j<labels.length; j++){
					if(moment(labels[j]).toDate().getTime() > (new Date().getTime()-604800000)){
						myChart.data.datasets[0].data.push(temperature[j]);
						myChart.data.labels.push(labels[j]);
						myChart.data.datasets[1].data.push(min[j]);
						myChart.data.datasets[2].data.push(max[j]);
					}
				}
			}else if (group.item(i).checked && group.item(i).value == "day") {
				for(var j = 0; j<labels.length; j++){
					if(moment(labels[j]).toDate().getTime() > (new Date().getTime()-86400000)){
						myChart.data.datasets[0].data.push(temperature[j]);
						myChart.data.labels.push(labels[j]);
						myChart.data.datasets[1].data.push(min[j]);
						myChart.data.datasets[2].data.push(max[j]);
					}
				}
			}else if (group.item(i).checked && group.item(i).value == "hour") {
				for(var j = 0; j<labels.length; j++){
					if(moment(labels[j]).toDate().getTime() > (new Date().getTime()-3600000)){
						myChart.data.datasets[0].data.push(temperature[j]);
						myChart.data.labels.push(labels[j]);
						myChart.data.datasets[1].data.push(min[j]);
						myChart.data.datasets[2].data.push(max[j]);
					}
				}
			} 
		}


		if(myChart.data.datasets[0].data.length < 30){
			myChart.options.scales.xAxes[0].time.unit='minute';	
			myChart.options.scales.xAxes[0].time.unitStepSize=1;
			myChart.update();
		}else if(myChart.data.datasets[0].data.length < 150){
			myChart.options.scales.xAxes[0].time.unit='minute';	
			myChart.options.scales.xAxes[0].time.unitStepSize=5;
			myChart.update();
		}else if(myChart.data.datasets[0].data.length < 1800){
			myChart.options.scales.xAxes[0].time.unit='hour';	
			myChart.options.scales.xAxes[0].time.unitStepSize=1;
			myChart.update();
		}else if(myChart.data.datasets[0].data.length < 10800){
			myChart.options.scales.xAxes[0].time.unit='hour';	
			myChart.options.scales.xAxes[0].time.unitStepSize=6;
			myChart.update();
		}else{
			myChart.options.scales.xAxes[0].time.unit='day';
			myChart.options.scales.xAxes[0].time.unitStepSize=1;	
			myChart.update();		
		}
	}
	
	var group = document.getElementsByName("set");
	for (var i = 0; i < group.length; i++) {
		group[i].addEventListener('change', setDataSet);
	}
	setDataSet();
	// Get the modal
	var modal = document.getElementById("myModal");

	// Get the button that opens the modal
	var btn = document.getElementById("myBtn");

	// Get the <span> element that closes the modal
	var span = document.getElementsByClassName("close")[0];
	
	var submit = document.getElementById("submit");

	// When the user clicks the button, open the modal 
	btn.onclick = function() {  
	   var xmlhttp = new XMLHttpRequest();

	    xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
		   if (xmlhttp.status == 200) {
		       setItems(xmlhttp.responseText);
		       modal.style.display = "block";
		   }
		   else if (xmlhttp.status == 400) {
		      alert('There was an error 400');
		   }
		   else {
		       alert('something else other than 200 was returned');
		   }
		}
	    };

	    xmlhttp.open("GET", "/setup_get", true);
	    xmlhttp.send();
	};


	submit.onclick = function() {  
	   var xmlhttp = new XMLHttpRequest();

	    xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
		   if (xmlhttp.status == 200) {
		       setItems(xmlhttp.responseText);
		   }
		   else if (xmlhttp.status == 400) {
		      alert('There was an error 400');
		   }
		   else {
		       alert('something else other than 200 was returned');
		   }
		}
	    };

	    xmlhttp.open("POST", "/setup_set", true);
	    xmlhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
	    xmlhttp.send("min="+ document.getElementById("minValue").value + "&max=" + document.getElementById("maxValue").value + "&start="+ document.getElementById("startValue").value);
	};

	// When the user clicks on <span> (x), close the modal
	span.onclick = function() {
	  modal.style.display = "none";
	};

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	  if (event.target == modal) {
	    modal.style.display = "none";
	  }
	};
};
	
	
function setItems(data){
   result = JSON.parse(data)["items"];
   htmlData = "";
   lastItem = null;
   for(i = 0; i< result.length; i++){
      htmlData += "Temperatuur tussen " + result[i][0] + " en " + result[i][1] + " start " + result[i][2] + "</br>";
      lastItem = result[i];
   }
   if(lastItem==null){
      lastStart = moment().format("YYYY-MM-DDTHH:mm");
   }else{
      lastStart = moment(lastItem[2]).format("YYYY-MM-DDTHH:mm");
   }
   document.getElementById("startValue").value = lastStart;
   document.getElementById("startValue").min = lastStart;  
   document.getElementById("program_items").innerHTML = htmlData;  
}



