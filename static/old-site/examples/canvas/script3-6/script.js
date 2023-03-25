$(document).ready(function() {
  
  var canvas = document.getElementById('working-canvas');
  var fog_canvas = document.getElementById('fog-canvas');
  
  var context = canvas.getContext('2d');
  var fog_context = fog_canvas.getContext('2d');
  
  if (canvas.getContext && fog_canvas.getContext){
    draw(context, fog_context);
  }
  
  // Ѕиндим эффект квадратного ластика на маусдаун
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
  var img_moroz = new Image(); // —оздаЄм новый объект Image
  img_moroz.src = 'moroz-small.png'; // ”станавливаем путь к источнику
  img_moroz.onload = function() {

    var img = new Image(); // —оздаЄм новый объект Image
    img.src = 'ya.jpg';    // ”станавливаем путь к источнику
    img.onload = function() {
      // когда изображение загружено, выводим его на холст
      context.drawImage(img, 200, 200);

      var pattern = context.createPattern(img_moroz, "repeat");
      fog_context.rect(200,200,420,400);
      fog_context.fillStyle = pattern;
      fog_context.fill();
      
      // заливаем изображение полупрозрачным фоном
      //context.fillStyle = "rgba(0, 200, 200, 0.5)";
    }
  }
}

function eraser(e, context, fog_context, radius) {
  /**
   * ѕока в эту функцию передаютс€ только рабочий контекст, радиус (пока он используетс€ дл€ задани€ стороны квадрата ластика) и объект event.
   * ѕозже, нам понадобитс€ добавить сюда передачу второго контекста
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
  
  // Ётот вариант ластика нам не подходит:
  //context.clearRect(mouseX, mouseY, radius, radius);
  // вместо него используем такой: сначала из скрытого холста получаем значени€ цветов пикселов, попавших под ластик
  fog_imagedata = fog_context.getImageData(mouseX - radius, mouseY - radius, diameter, diameter);
  imagedata = context.getImageData(mouseX - radius, mouseY - radius, diameter, diameter);
  
  //for(elem in imagedata) {
  //  console.log(elem);
  //}
  
  elem_count = diameter * diameter * 4;
  
  i = 0;
  while(i <= elem_count) {
    // определ€ю координаты точки в матрице. m Ч номер в строке, n Ч номер строки
    
    /*
     каждый элемент массива это не массив ргба, а отдельна€ компонетна цвета, то есть дл€ нулевого элемента
     0 - р
     1 - г
     2 - б
     3 - а
     
     дл€ m = i / 4 элемента:
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
     
     a Ч центр круга
    
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
      // ≈сли пиксел не попал в круг, то оставл€ю его цвет как на рабочем холсте, иначе мен€ю цвет на такой как на скрытом холсте
      fog_imagedata['data'][i]     = imagedata['data'][i];     // r
      fog_imagedata['data'][i + 1] = imagedata['data'][i + 1]; // g
      fog_imagedata['data'][i + 2] = imagedata['data'][i + 2]; // b
      fog_imagedata['data'][i + 3] = imagedata['data'][i + 3]; // a
    }
    
    i += 4;
  }
  
  // «атем замен€ем этими пикселами пикселы на рабочем холсте:
  fog_context.putImageData(fog_imagedata, mouseX - radius, mouseY - radius);
}