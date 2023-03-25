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
      eraser(e, context, fog_context, 40);
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
  
  var diameter = radius * 2;

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
  
  // Этот вариант ластика нам не подходит:
  //context.clearRect(mouseX, mouseY, radius, radius);
  // вместо него используем такой: сначала из нижнего холста получаем значения цветов пикселов, попавших под ластик
  imagedata = context.getImageData(mouseX - radius, mouseY - radius, diameter, diameter);
  fog_imagedata = fog_context.getImageData(mouseX - radius, mouseY - radius, diameter, diameter);
  
  //for(elem in imagedata) {
  //  console.log(elem);
  //}
  
  elem_count = diameter * diameter * 4;
  
  // Затем, воспользовавшись знаниями из геометрии за 7 класс, преобразовываем массив пикселов
  i = 0;
  while(i <= elem_count) {
    // определяю координаты точки в матрице. m — номер в строке, n — номер строки
    
    /*
     каждый элемент массива это не массив ргба, а отдельная компонетна цвета, то есть для нулевого элемента
     0 - р
     1 - г
     2 - б
     3 - а
     
     для m = i / 4 элемента:
     i     - р
     i + 1 - г
     i + 2 - б
     i + 3 - а
     
     
     c
     |
     |\
     | \
     |  \
     |   \
     |____\
     b     a
     
     ac должно быть меньше radius
     
     a — центр круга
    
     */
    m = i / 4;
    if (m < diameter) {
      n = 0;
    } else {
      n = 0;
      while(m >= diameter) {
        m -= diameter;
        n++;
      }
    }
    
    bc = radius - m;
    if(bc < 0) {
      bc = -bc;
    }
    
    ab = radius - n;
    if(ab < 0) {
      ab = -ab;
    }
    
    if(Math.sqrt(bc * bc + ab * ab) < radius) {
      // Если пиксел попал в круг, то меняю его цвет как на нижнем холсте, иначе оставляю цвет на такой как на верхнем холсте
      fog_imagedata['data'][i]     = imagedata['data'][i];     // r
      fog_imagedata['data'][i + 1] = imagedata['data'][i + 1]; // g
      fog_imagedata['data'][i + 2] = imagedata['data'][i + 2]; // b
      fog_imagedata['data'][i + 3] = imagedata['data'][i + 3]; // a
    }
    
    i += 4;
  }
  
  // Затем заменяем этими пикселами пикселы на рабочем холсте:
  fog_context.putImageData(fog_imagedata, mouseX - radius, mouseY - radius);
}