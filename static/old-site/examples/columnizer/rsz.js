window.onload = setClass; 
window.onresize = setClass;

function setClass(){
  var width = document.documentElement.clientWidth;
  var c = (width<=800)?'':'column-2';
  document.getElementById('column').className=c;
  $.fn.columnize;
};
