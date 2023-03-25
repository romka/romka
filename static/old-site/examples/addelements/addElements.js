function addInput() {
	var id = document.getElementById("default-id").value;
  id++;
  $("form[name=testform]").append('<div id="div-' + id + '"><input name="input-' + id + '" id="input-' + id + '" value="' + id + '"><a href="javascript:{}" onclick="removeInput(\'' + id + '\')">Удалить</a></div>');
  document.getElementById("default-id").value = id;
}

function removeInput(id) {
	$("#div-" + id).remove();
}


function addOption() {
	var id = document.getElementById("default-option-id").value;
  id++;
  $("select[name=testselect]").append('<option value="option-' + id + '">option ' + id + '</option>');  	
  document.getElementById("default-option-id").value = id;
}