if (!window.jQuery) throw("jQuery must be referenced before using the 'onImagesLoad' plugin.");
/* 
* jQuery 'onImagesLoaded' plugin 1.0.2
* Fires a callback function when all images have loaded within a particular selector.
*
* Copyright (c) Cirkuit Networks, Inc. (http://www.cirkuit.net), 2008.
* Dual licensed under the MIT and GPL licenses:
*   http://www.opensource.org/licenses/mit-license.php
*   http://www.gnu.org/licenses/gpl.html
*
* For documentation and usage, visit "http://includes.cirkuit.net/js/jquery/plugins/onImagesLoad/1.0/documentation/"
*/
(function($) {
  $.fn.onImagesLoad = function(options) {
    var opts = $.extend({}, $.fn.onImagesLoad.defaults, options);
    
    return this.each(function() {
      imgs = $('img', this);
      if(imgs.length==0 && opts.callbackIfNoImagesExist && opts.callback) opts.callback(this); //call callback immediately if no images were in selection
      $(imgs).bind('load', {totalImgCnt:imgs.length, loadedImgCnt:0, container:this}, function(event){
        if (++event.data.loadedImgCnt == event.data.totalImgCnt){
          if(opts.callback) opts.callback(event.data.container);
        }
      }).each(function() {
        if(this.complete){ //needed for cached images
          this.src = this.src;
        }
      });
    });

  };

  $.fn.onImagesLoad.defaults = {
    callback: null, //the function you want called when all images within $(yourSelector) have loaded
    callbackIfNoImagesExist: true //if no images exist within $(yourSelector), should the callback be called?
  };

})(jQuery);