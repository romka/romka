jQuery(function($){
	$('a[href$=".doc"], a[href$=".mp3"], a[href$=".m4u"], a[target$=_blank]').each(function(){
		// looking at the href of the link, if it contains .pdf or .doc or .mp3
		var link = $(this);
		var bits = this.href.split('.');
		var type = bits[bits.length -1];
		
		
		var url= "http://json-head.appspot.com/?url="+encodeURI($(this).attr('href'))+"&callback=?";
	
		// then call the json thing and insert the size back into the link text
		 $.getJSON(url, function(json){
			if(json.ok && json.headers['Content-Length']) {
				var length = parseInt(json.headers['Content-Length'], 10);
				
				// divide the length into its largest unit
				var units = [
					[1024 * 1024 * 1024, 'GB'],
					[1024 * 1024, 'MB'],
					[1024, 'KB'],
					[1, 'bytes']
				];
				
				for(var i = 0; i < units.length; i++){
					
					var unitSize = units[i][0];
					var unitText = units[i][1];
					
					if (length >= unitSize) {
						length = length / unitSize;
						// 1 decimal place
						length = Math.ceil(length * 10) / 10;
						var lengthUnits = unitText;
						break;
					}
				}
				
				// insert the text directly after the link and add a class to the link
				link.after(' (' + type + ' ' + length + ' ' + lengthUnits + ')');
				link.addClass(type);
			} else if (json.ok && json.headers['Last-Modified']) {
			  link.after(' (Last Modified: ' + json.headers['Last-Modified'] + ')');
			}
		});
	});
});