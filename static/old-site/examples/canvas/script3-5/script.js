$(document).ready(function() {
  
  var canvas = document.getElementById('working-canvas');
  var fog_canvas = document.getElementById('fog-canvas');
  
  var context = canvas.getContext('2d');
  var fog_context = fog_canvas.getContext('2d');
  
  if (canvas.getContext && fog_canvas.getContext){
    draw(context, fog_context);
  }
  
  // ������ ������ ����������� ������� �� ��������
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
  var img = new Image(); // ������ ����� ������ Image
  img.src = 'ya.jpg';    // ������������� ���� � ���������
  img.onload = function() {
    // ����� ����������� ���������, ������� ��� �� �����
    context.drawImage(img, 200, 200);

    // �������� ����������� �������������� �����
    fog_context.fillStyle = "rgba(0, 200, 200, 0.5)";
    fog_context.fillRect (200, 200, 430, 400);
  }
}

function eraser(e, context, fog_context, radius) {
  /**
   * ���� � ��� ������� ���������� ������ ������� ��������, ������ (���� �� ������������ ��� ������� ������� �������� �������) � ������ event.
   * �����, ��� ����������� �������� ���� �������� ������� ���������
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
  
  // ���� ������� ������� ��� �� ��������:
  //context.clearRect(mouseX, mouseY, radius, radius);
  // ������ ���� ���������� �����: ������� �� ������� ������ �������� �������� ������ ��������, �������� ��� ������
  imagedata = context.getImageData(mouseX - radius, mouseY - radius, diameter, diameter);
  fog_imagedata = fog_context.getImageData(mouseX - radius, mouseY - radius, diameter, diameter);
  
  //for(elem in imagedata) {
  //  console.log(elem);
  //}
  
  elem_count = diameter * diameter * 4;
  
  // �����, ���������������� �������� �� ��������� �� 7 �����, ��������������� ������ ��������
  i = 0;
  while(i <= elem_count) {
    // ��������� ���������� ����� � �������. m � ����� � ������, n � ����� ������
    
    /*
     ������ ������� ������� ��� �� ������ ����, � ��������� ���������� �����, �� ���� ��� �������� ��������
     0 - �
     1 - �
     2 - �
     3 - �
     
     ��� m = i / 4 ��������:
     i     - �
     i + 1 - �
     i + 2 - �
     i + 3 - �
     
     
     c
     |
     |\
     | \
     |  \
     |   \
     |____\
     b     a
     
     ac ������ ���� ������ radius
     
     a � ����� �����
    
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
      // ���� ������ ����� � ����, �� ����� ��� ���� ��� �� ������ ������, ����� �������� ���� �� ����� ��� �� ������� ������
      fog_imagedata['data'][i]     = imagedata['data'][i];     // r
      fog_imagedata['data'][i + 1] = imagedata['data'][i + 1]; // g
      fog_imagedata['data'][i + 2] = imagedata['data'][i + 2]; // b
      fog_imagedata['data'][i + 3] = imagedata['data'][i + 3]; // a
    }
    
    i += 4;
  }
  
  // ����� �������� ����� ��������� ������� �� ������� ������:
  fog_context.putImageData(fog_imagedata, mouseX - radius, mouseY - radius);
}