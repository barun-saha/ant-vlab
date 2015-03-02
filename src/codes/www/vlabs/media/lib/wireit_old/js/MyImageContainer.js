/**
 * Container represented by an image
 * @class MyImageContainer
 * @extends WireIt.Container
 * @constructor
 * @param {Object} options
 * @param {WireIt.Layer} layer
 */
WireIt.MyImageContainer = function(options, layer) {
   WireIt.MyImageContainer.superclass.constructor.call(this, options, layer);
};

YAHOO.lang.extend(WireIt.MyImageContainer, WireIt.Container, {

    /**
    * @method setOptions
    * @param {Object} options the options object
    */
    setOptions: function(options) {
        WireIt.MyImageContainer.superclass.setOptions.call(this, options);

        this.options.image = options.image;
        this.options.xtype = "WireIt.MyImageContainer";

        this.options.className = options.className || "WireIt-Container WireIt-ImageContainer";

        // Overwrite default value for options:
        this.options.resizable = true;  //(typeof options.resizable == "undefined") ? false : options.resizable;
        this.options.ddHandle = (typeof options.ddHandle == "undefined") ? false : options.ddHandle;

        this.options.title = options.label;
    },

    /**
    * @method render
    */
    render: function() {
        WireIt.MyImageContainer.superclass.render.call(this);
        YAHOO.util.Dom.setStyle(this.bodyEl, "background-image", "url(" + this.options.image + ")");

        // Modifications by Barun 27-Aug-2010
	    // Include a place to add label
        var titleDiv = WireIt.cn('div');
        this.labelField = new inputEx.InPlaceEdit({
		    name: 'title',
		    id: 'title',
	        parentEl: titleDiv,
            value: this.options.title,
            editorField: { type: 'string', inputParams: {} }
       });
       this.el.appendChild(titleDiv);

       var all_childs = "";
	   for (cln in titleDiv.childNodes) {
		   all_childs += cln + "\n";
	   }

	   var all_attrs = "";
	   for (attr in titleDiv.attributes) {
		   all_attrs += attr + "\n";
	   }
	   // End
    }

});