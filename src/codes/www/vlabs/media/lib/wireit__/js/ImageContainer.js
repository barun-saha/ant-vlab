/**
 * Container represented by an image
 * @class ImageContainer
 * @extends WireIt.Container
 * @constructor
 * @param {Object} options
 * @param {WireIt.Layer} layer
 */
WireIt.ImageContainer = function(options, layer) {
   WireIt.ImageContainer.superclass.constructor.call(this, options, layer);
};

YAHOO.lang.extend(WireIt.ImageContainer, WireIt.Container, {

   /**
    * @method setOptions
    * @param {Object} options the options object
    */
   setOptions: function(options) {
      WireIt.ImageContainer.superclass.setOptions.call(this, options);

      this.options.image = options.image;
      this.options.xtype = "WireIt.ImageContainer";

      this.options.className = options.className || "WireIt-Container WireIt-ImageContainer";

      // Overwrite default value for options:
      this.options.resizable = (typeof options.resizable == "undefined") ? false : options.resizable;
      this.options.ddHandle = (typeof options.ddHandle == "undefined") ? false : options.ddHandle;

      // Added by Barun, 27-Aug-2010
      this.options.title = options.label;
      this.options.category = options.category;
   },

   /**
    * @method render
    */
   render: function() {
      WireIt.ImageContainer.superclass.render.call(this);
      YAHOO.util.Dom.setStyle(this.bodyEl, "background-image", "url("+this.options.image+")");

      // Modifications by Barun 29-Jun-2010
      // Include a place to add node number
      var titleDiv = WireIt.cn('div');
      this.labelField = new inputEx.InPlaceEdit({
		  name: 'title',
		  id: 'title',
	      parentEl: titleDiv,
          value: this.options.title,
          editorField: { type: 'string', inputParams: {} }
       });
       this.el.appendChild(titleDiv);
	   //alert(this.el.nodeName + "," + titleDiv.nodeName + ",");

		var all_childs = "";
	   for (cln in titleDiv.childNodes) {
		   all_childs += cln + "\n";
	   }
	   //alert(all_childs);

	   var all_attrs = "";
	   for (attr in titleDiv.attributes) {
		   all_attrs += attr + "\n";
	   }
	   // End
   },

   getValue: function() {
      return {};
   },

   /**
    * Subclasses should override this method.
    * @method setValue
    * @param {Any} val Value
    */
   setValue: function(val) {
   },


});