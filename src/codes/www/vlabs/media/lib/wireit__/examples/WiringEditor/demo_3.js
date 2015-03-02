var demoLanguage = {
	
	// Set a unique name for the language
	languageName: "meltingpotDemo",

	// inputEx fields for pipes properties
	propertiesFields: [
		// default fields (the "name" field is required by the WiringEditor):
		{"type": "string", inputParams: {"name": "name", label: "Title", typeInvite: "Enter a title" } },
		//{"type": "text", inputParams: {"name": "description", label: "Description", cols: 30} },
		
		// Additional fields
//		{"type": "boolean", inputParams: {"name": "isTest", value: true, label: "Test"}},
//		{"type": "select", inputParams: {"name": "category", label: "Category", selectValues: ["Demo", "Test", "Other"]} }
	],
	
	// List of node types definition
	modules: [	            
            {
                "name":     "Actor",
                "container": {
                    "xtype":    "WireIt.ImageContainer",
                    "className": "WireIt-Container WireIt-ImageContainer StickFigure",
                    // "icon":     "../../res/icons/color_wheel.png",
                    "icon":     "/isad/v_media/lib/wireit/res/icons/color_wheel.png",
                    "image":    "/isad/v_media/images/uml/use-case-actor-stick.png",
                    "title":    "StickFigure",
                    "terminals": [
                        { "direction": [-1, -1], "offsetPosition": { "left": 12, "top": -20 }, "name": "top" },
                        { "direction": [1, -1], "offsetPosition": { "left": 38, "top": 14 }, "name": "right" },
                        { "direction": [1, 1], "offsetPosition": { "left": -15, "top": 14 }, "name": "left" }
                    ],
                    "label": "Role",
                    "category": "Actor"
                }
            },
            {
                "name":     "Use case",
                "container": {
                    "xtype":    "WireIt.ImageContainer",
                    "className": "WireIt-Container WireIt-ImageContainer UseCase",
                    // "icon":     "../../res/icons/color_wheel.png",
                    "icon":     "/isad/v_media/lib/wireit/res/icons/color_wheel.png",
                    "image":    "/isad/v_media/images/uml/use-case.png",
                    "title":    "StickFigure",
                    "terminals": [
                        { "direction": [-1, -1], "offsetPosition": { "left": 50, "top": -10 }, "name": "top" },
                        { "direction": [1, 1], "offsetPosition": { "left": -17, "top": 16 }, "name": "left" },
                        { "direction": [1, -1], "offsetPosition": { "left": 117, "top": 16 }, "name": "right" },
                        { "direction": [-1, 1], "offsetPosition": { "left": 50, "top": 50 }, "name": "bottom" },
                    ],
                    "label": "Use case",
                    "category": "UseCase"
                }
            },
        ]
};