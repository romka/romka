$(document).ready(function() {
  
  var canvas = document.getElementById('working-canvas');
  var fog_canvas = document.getElementById('fog-canvas');
  
  var context = canvas.getContext('2d');
  var fog_context = fog_canvas.getContext('2d');
  
  if (canvas.getContext && fog_canvas.getContext){
    draw(context, fog_context);
  }
});

function draw(context, fog_context) {
  var img = new Image(); // Создаём новый объект Image
  img.src = 'ya.jpg';    // Устанавливаем путь к источнику
  img.onload = function() {
    context.drawImage(img, 200, 200);
  }
}