$(document).ready(function() {
    // Initialise the table 1
    $("#table-1").tableDnD({
      onDragClass: "myDragClass"
    });
    
    // Initialise the table 2
    $("#table-2").tableDnD({
      onDragClass: "myDragClass",
      dragHandle: "dragHandle"
    });
    
    $("#table-2 tr").hover(function() {
          $(this.cells[0]).addClass('showDragHandle');
    }, function() {
          $(this.cells[0]).removeClass('showDragHandle');
    });

    // Initialise the table 3    
    $("#table-3").tableDnD({
	    onDragClass: "myDragClass",
	    onDrop: function(table, row) {
          var rows = table.tBodies[0].rows;
          var w = "";
          for (var i = 0; i < rows.length; i++) {
            w += rows[i].id + ";";
          }
        
          $.ajax({
        		type: "POST",
         		url: "/examples/table-dnd/table-dnd-example.php",
         		timeout: 5000,
         		data: "w=" + w,
         		success: function(data){$("div#upd-dnd").html(data);},
         		error: function(data){$("div#upd-dnd").html("Error" + data);}
         	});
        }
  	});


});