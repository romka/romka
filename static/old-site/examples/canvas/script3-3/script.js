$(document).ready(function() {
  
  var canvas = document.getElementById('working-canvas');
  var fog_canvas = document.getElementById('fog-canvas');
  
  var context = canvas.getContext('2d');
  var fog_context = fog_canvas.getContext('2d');
  
  if (canvas.getContext && fog_canvas.getContext){
    draw(context, fog_context);
  }
  
  // Биндим эффект квадратного ластика на маусдаун
  $(fog_canvas).bind('mousedown', function(e) {
    eraser(e, context, fog_context, 40);
    $(fog_canvas).bind('mousemove', function(e) {
      eraser(e, context, fog_context,40);
    });
  });
  
  $(fog_canvas).bind('mouseup', function() {
    $(fog_canvas).unbind('mousemove');
  });
});

function draw(context, fog_context) {
  var img = new Image(); // Создаём новый объект Image
  img.src = 'ya.jpg';    // Устанавливаем путь к источнику
  img.onload = function() {
    // когда изображение загружено, выводим его на холст
    context.drawImage(img, 200, 200);
    
    // заливаем изображение полупрозрачным фоном
    fog_context.fillStyle = "rgba(0, 200, 200, 0.5)";
    fog_context.fillRect (200, 200, 430, 400);
  }
}

function eraser(e, context, fog_context, radius) {
  /**
   * Пока в эту функцию передаются только рабочий контекст, радиус (пока он используется для задания стороны квадрата ластика) и объект event.
   * Позже, нам понадобится добавить сюда передачу второго контекста
   */
  var mouseX, mouseY;

  if(e.offsetX) {
    mouseX = e.offsetX;
    mouseY = e.offsetY;
  }
  else if(e.layerX) {
    mouseX = e.layerX;
    mouseY = e.layerY;
  } else {
    mouseX = -1000;
    mouseY = -1000;
  }
  
  fog_context.clearRect(mouseX, mouseY, radius, radius);
}