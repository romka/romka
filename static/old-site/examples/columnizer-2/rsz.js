window.onload = setClass; 
window.onresize = setClass;

function setClass(){
	var width = document.documentElement.clientWidth;
	var c = (fmt<=800)?':'column-2';
	document.getElementById('column').className=c;
};
