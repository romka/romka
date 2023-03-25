$(document).ready(function() {
  
  var canvas = document.getElementById('working-canvas');
  var hidden_canvas = document.getElementById('hidden-canvas');
  
  var context = canvas.getContext('2d');
  var hidden_context = hidden_canvas.getContext('2d');
  
  $(canvas1).bind('mousedown', function(e) {
    eraser(e, context1, context2, 40);
    $(canvas1).bind('mousemove', function(e) {
      eraser(e, context1, context2, 40);
    });
  });
  
  $(canvas1).bind('mouseup', function() {
    $(canvas1).unbind('mousemove');
  });
  
  if (canvas1.getContext && canvas2.getContext && hidden_canvas.getContext){
    draw(context1, context2, hidden_context);
  }
});