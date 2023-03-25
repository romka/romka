/*
 * Tagnetic — plugin for jQuery 1.2.6
 *
 * Copyright (c) 2008 Roman Arkharov http://romka.eu
 *
 * Date: 2008-10-13
 */
jQuery.tagnetic = function(options) {    
  
  var defaults = {
    container: "ul#tagnetic",
    tag: "li",
    new_container_name: "new-tagnetic",
    div_width: 600,
    path_to_skins: "",
    skin: 'refrigerator-600',
    paddings: 30,
    margin: 5,    
    background_top: "background-top.jpg",
    background_middle: "background-middle.jpg",
    background_bottom: "background-bottom.jpg",
    handle: 'none',
    handle_width: 275,
    handle_line: 5,
    ovals: 1,
    squares: 8,
    beat_x: 4,
    beat_y: 4,
    ellipse_width: "70,50",
    ellipse_height: "29,21",
    ellipse_text_width: "60,35",
    ellipse_text_height: "19,18",
    loader: true,
    loader_max_time: 15000
  };  
  
  var options = $.extend(defaults, options);
  
  if(options.tag == "none") {
    $(options.container + " a").each(function(){
      $(this).wrap("<li class=\"tag\"></li>");
    });
    options.tag = "li";
  }

  c = 0;
  function imagesLoadCounter(i, j) {
    alert(i + "; " + j);
    c++;
  }
  squares = Array();
  
  for(i = 1; i <= options.squares; i++) {
    squares[i] = Array();
    for(j = 0; j <= 8; j++) {
      squares[i][j] = new Image();
    }
    squares[i][0].src = options.path_to_skins + "skins/" + options.skin + "/squares/square-l-t-" + i + ".png";
    squares[i][1].src = options.path_to_skins + "skins/" + options.skin + "/squares/square-m-t-" + i + ".png";
    squares[i][2].src = options.path_to_skins + "skins/" + options.skin + "/squares/square-r-t-" + i + ".png";
    squares[i][3].src = options.path_to_skins + "skins/" + options.skin + "/squares/square-l-m-" + i + ".png";
    squares[i][4].src = options.path_to_skins + "skins/" + options.skin + "/squares/square-m-m-" + i + ".png";
    squares[i][5].src = options.path_to_skins + "skins/" + options.skin + "/squares/square-r-m-" + i + ".png";
    squares[i][6].src = options.path_to_skins + "skins/" + options.skin + "/squares/square-l-b-" + i + ".png";
    squares[i][7].src = options.path_to_skins + "skins/" + options.skin + "/squares/square-m-b-" + i + ".png";
    squares[i][8].src = options.path_to_skins + "skins/" + options.skin + "/squares/square-r-b-" + i + ".png";
  }

  // Ellipses width and heights
  options.ellipse_width += ",0";
  options.ellipse_height += ",0";
  options.ellipse_text_width += ",0";
  options.ellipse_text_height += ",0";  
  
  ew = Array();
  ew = options.ellipse_width.split(",");
  eh = Array();
  eh = options.ellipse_height.split(",");
  etw = Array();
  etw = options.ellipse_text_width.split(",");
  eth = Array();
  eth = options.ellipse_text_height.split(",");
  ellipses = 9999;
  
  
  for(i = 0; i <= ew.length - 1; i++) ew[i] = parseInt(ew[i]);
  if(i <= ellipses) ellipses = i;
  for(i = 0; i <= eh.length - 1; i++) eh[i] = parseInt(eh[i]);
  if(i <= ellipses) ellipses = i;
  for(i = 0; i <= etw.length - 1; i++) etw[i] = parseInt(etw[i]);
  if(i <= ellipses) ellipses = i;
  for(i = 0; i <= eth.length - 1; i++) eth[i] = parseInt(eth[i]); 
  if(i <= ellipses) ellipses = i;
  ellipses--;
 
  margins = options.margin * 2;
  
  function randOrd() {
    return (Math.round(Math.random())-0.5); 
  } 
  
  function rand() {
    return (1 + Math.round(Math.random() * (options.squares - 1)));
  }
  
  function buildMagnet(width, height, html, size) {
    size = size || 0;
    rnd = rand();
    
    el = false;
    
    for(k = 0; k <= ellipses; k++) {      
      if(width > 0.75 * etw[k] && width < etw[k] && height > 0.75 * eth[k] && height < eth[k] && !el && Math.round(Math.random()) == 1) {
        el = true;
        magnet = "<div class=\"tc\"><table class=\"\magnet\" style=\"width: " + ew[k] + "px; height: " + eh[k] + "px; background: url(" + options.path_to_skins + "skins/" + options.skin + "/ellipses/ellipse-" + (k + 1) + ".png) no-repeat;\"><tr><td><div style=\"display: block; text-align: center; width: " + ew[k] + "px; height: " + eh[k] + "px; text-align: center; vertical-align: middle;\" class=\"tag_line " + size + "\">" + html + "</div></td></tr></table></div>";
        //magnet += "<span style=\"display: none;\">magnet dimensions (w/h): " + width + " / " + height + "</span>";
        return magnet;
      }
    }
    
    if(!el) {
      /*
      -------------------
      | 1-1 | 1-2 | 1-3 |
      -------------------
      | 2-1 | 2-2 | 2-3 |
      -------------------
      | 3-1 | 3-2 | 1-3 |
      -------------------    
      */
      
      // left top corner (1-1)
      magnet = "<div class=\"tc\"><table class=\"magnet\"><tr><td class=\"corner\"><img src=\"" + squares[rnd][0].src + "\"></td>";
      // middle top line (1-2)
      magnet += "<td style=\"background: url(" + squares[rnd][1].src + ") repeat-x;\"></td>";
      // right top corner (1-3)
      magnet += "<td class=\"corner\"><img src=\"" + squares[rnd][2].src + "\"></td></tr>";
      // left middle div (2-1)
      magnet += "<tr><td class=\"corner\" style=\"background: url(" + squares[rnd][3].src + ") repeat-y;\"></td>";
      // center div with data (2-2)      
      magnet += "<td style=\"background: url(" + squares[rnd][4].src + ");\"><div style=\"display: inline; float: left; width: " + width + "px; height: " + height + "px;\" class=\"tag_line " + size + "\">" + html + "</div></td>";    
      // right middle div (2-3)
      magnet += "<td class=\"corner\" style=\"background: url(" + squares[rnd][5].src + ") repeat-y;\"></td></tr>";
      // left bottom corner (3-1)
      magnet += "<tr><td class=\"corner\"><img src=\"" + squares[rnd][6].src + "\"></td>";
      // middle bottom line (3-2)
      magnet += "<td style=\"background: url(" + squares[rnd][7].src + ") repeat-x;\"></td>";
      // right bottom corner (3-3)
      magnet += "<td class=\"corner\"><img src=\"" + squares[rnd][8].src + "\"></td></tr></table></div>";
      //magnet += "<span style=\"display: none;\">magnet dimensions (w/h): " + width + " / " + height + "</span>";
     
      return magnet;
    } else {
      return "";
    }
  }
  
  var tags = Array();
  var i = 0;
  var min_height = 200;
  var max_height = 0;
  var min_width = 200;
  var max_width = 0;
  
  $(options.container + " > " + options.tag).each(function(){
    $(this).css({display: "inline"});    
    tags[i] = Array();
    tags[i]['width'] = $(this).width();        
    tags[i]['height'] = $(this).height();    
    tags[i]['data'] = $(this).html();
    tags[i]['size'] = $(this).attr("class");
    tags[i]['used'] = false;
    if(tags[i]['height'] > max_height)max_height = tags[i]['height'];
    if(tags[i]['height'] < min_height)min_height = tags[i]['height'];
    if(tags[i]['width'] < min_width)min_width = tags[i]['width'];
    if(tags[i]['width'] > max_width)max_width = tags[i]['width'];
    $(this).append("<span style=\"display:none\">[" + tags[i]['data'] + "] w/h = " + tags[i]['width'] + "/ " + tags[i]['height'] + "</span>");
    $(this).append("<br>");
    i++;
  });
//* 
  tags.sort(randOrd);

  var tagnetic = Array();
  ratio = Math.round(max_height / min_height);
  j = 0;
  mh = 0;
  // process (concat) small items
  for(i = 0; i <= tags.length - 1; i++) {    
    if(tags[i]['height'] <= (max_height / 2) + margins && tags[i]['used'] == false) {
      tags[i]['used'] = true;
      if(mh == 0) {
        tagnetic[j] = Array();
        tagnetic[j]['data'] = "<div class=\"tag container\" id=\"tag-block-" + j + "\">";
        tagnetic[j]['width'] = tags[i]['width'] + options.paddings;
        lines = 0;
      }
      //"<div style=\"display: inline; float: left;\"><img src=\"" + options.path_to_skins + "skins/" + options.skin + "/squares/square-l-t-" + rnd + ".png\"></div><div style=\"display: inline; float: left; width: " + $(this).width() + "px; background: url(skins/" + options.skin + "/squares/square-m-t-" + rnd + ".png) repeat-x;\"><img src=\"" + options.path_to_skins + "skins/" + options.skin + "/squares/square-m-t-" + rnd + ".png\"></div><div style=\"display: inline; float: left;\"><img src=\"" + options.path_to_skins + "skins/" + options.skin + "/squares/square-r-t-" + rnd + ".png\"></div><div style=\"clear: both;\"/><div style=\"display: inline; float: left; height: " + $(this).height() + "px; background: url(skins/" + options.skin + "/squares/square-l-m-" + rnd + ".png) repeat-y;\"><img src=\"" + options.path_to_skins + "skins/" + options.skin + "/squares/square-l-m-" + rnd + ".png\"></div>"
      
      tagnetic[j]['data'] += buildMagnet(tags[i]['width'], tags[i]['height'], tags[i]['data'], tags[i]['size']);
      
      lines++;
      
      if(tags[i]['width'] + options.paddings > tagnetic[j]['width'])tagnetic[j]['width'] = tags[i]['width'] + options.paddings;
      
      mh += tags[i]['height'];
      if(mh + min_height >= max_height && lines > 1) {
        //tagnetic[j]['data'] += "<span style=\"display: none\">(" + tagnetic[j]['width'] + ")</span>";
        tagnetic[j]['data'] += "</div>";
        j++;
        mh = 0;
      }
    }
  }
  if(mh != 0) {
    tagnetic[j]['data'] += "</center></div>";
    j++;
  }

  // process big items
  for(i = 0; i <= tags.length - 1; i++) {
    if(tags[i]['height'] > (max_height / 2) + 5 && tags[i]['used'] == false) {
      tags[i]['used'] = true;
      tagnetic[j] = Array();
      tagnetic[j]['width'] = tags[i]['width'] + options.paddings;
      
      tagnetic[j]['data'] = "<div class=\"tag single\" id=\"tag-block-" + j + "\">";      
      tagnetic[j]['data'] += buildMagnet(tags[i]['width'], tags[i]['height'], tags[i]['data'], tags[i]['size']);
      tagnetic[j]['data'] += "</div>"; 
      
      //tagnetic[j]['data'] += "<span style=\"display: none\">(" + tagnetic[j]['width'] + ")</span>";
      j++;
    }
  }
  
  tagnetic.sort(randOrd);
  
  result = "";
  result += "<div class=\"bl\"><img src=\"" + options.path_to_skins + "skins/" + options.skin + "/" + options.background_top + "\"></div><div class=\"clr\"></div>";
  result += "<div id=\"magnets\"><div class=\"nl\">";  
  j = 0;
  k = 0;  
  is_k = true;
  lines_counter = 1;
  for(i = 0; i <= tagnetic.length - 1; i++) {
    if(j + margins + options.paddings + tagnetic[i]['width'] > options.div_width) {
      result += "</div><div class=\"clr\"></div><div class=\"nl\">";      
      j = 0;
      if(is_k) lines_counter++;
    }
    if(k >= options.handle_line && is_k && j == 0 && options.handle != 'none') {
      // draw handle
      result += "<div id=\"tagnetic-handle\" style=\"float: left; position: relative; width: " + options.handle_width + ";\"><img src=\"" + options.path_to_skins + "skins/" + options.skin + "/" + options.handle + "\"></div>";
      j += options.handle_width + margins;      
      is_k = false;
    } else {
      // draw simple magnet
      result += tagnetic[i]['data'];
      j += tagnetic[i]['width'] + margins;      
       k++;
    }
  }
  if(j != 0 )result += "</div><div class=\"clr\"></div>";
  result += "</div><div class=\"bl\"><img src=\"" + options.path_to_skins + "skins/" + options.skin + "/" + options.background_bottom + "\"></div><div class=\"clr\"></div>";

  // remove old nasty container and add new beauty 
  $(options.container).after("<div id=\"" + options.new_container_name + "\" style=\"background: url('" + options.path_to_skins + "skins/" + options.skin + "/" + options.background_middle + "') repeat-y; width: " + options.div_width + "px; text-align: center;\"></div>").remove(); 
  $("div#" + options.new_container_name).html(result);

  // move magnets in double blocks
  $("div.container > div.tc > table.magnet").each(function(){    
    padd = Math.round(10 + Math.random() * (($(this).parent().width() - 10) / options.beat_x));
    if($(this).width() < $(this).parent().width() * 0.75) {
      $(this).parent().css({"padding-left": padd});
    }
  });  

  if(options.loader) {
    $("div#magnets").css({visibility: "hidden"});
    $("div#magnets").before("<div id=\"tagnetic-loader\"><img src=\"" + options.path_to_skins + "ajax-loader.gif\"></div>");
    //$("div#magnets").onImagesLoad({
    //    callback: function() {$("div#tagnetic-loader").remove();$("div#magnets").css({visibility: "visible"});}
    //});
    //t = setTimeout(function() {if(c == options.squares * 9) {clearTimeout(t); $("div#tagnetic-loader").remove(); $("div#magnets").css({visibility: "visible"});}}, 1000);
    $(window).load(function() {$("div#tagnetic-loader").remove();$("div#magnets").css({visibility: "visible"});});
    si = setInterval('$("div#tagnetic-loader").remove();$("div#magnets").css({visibility: "visible"}); clearInterval(si);', options.loader_max_time);
  }
  

  // move magnets to center (h)
  i = 0;
  nl_height = 0;
  $("div#" + options.new_container_name + " > div#magnets > div.nl").each(function(){
    i++;
    nl_height += $(this).height();
    if(i != lines_counter || options.handle == 'none') {
      marg = Math.round((options.div_width - $(this).width()) / 3);
      $(this).css({"padding-left": marg});
      //$(this).after("<span style=\"display: none;\">" + marg + " = " + options.div_width  + " - " + $(this).width() + " / 3; " + $(this).height() + "</span>");
    }
  });
  
  nl_height = nl_height / i / options.beat_y;  
  // move magnets to center (v)  
  $(options.new_container_name + " > div#magnets > div.nl > div.tag").each(function(){
    if(Math.round(Math.random()) == 1) s = true;
    else s = false;
    if(s) $(this).css({"margin-top": Math.round((nl_height / 2) + Math.random() * (nl_height / 2) )});
  });  
//*/  
};
