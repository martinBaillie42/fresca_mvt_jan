/**
 * Created by Martin Martin on 05/02/14.
 */
var rudeFish = {};

rudeFish.pType = {

    detectHighlightedElement: function () {
        // reference: http://stackoverflow.com/questions/4698259/jquery-highlight-element-under-mouse-cursor
        that.prevElement = null;
        document.getElementById('imported_site').contentDocument.addEventListener('mousemove', function(e) {
//            console.log(2);
                var elem = e.target || e.srcElement;
                if (that.prevElement != null) {
                    $(that.prevElement).css('outline-width', '0');
                }
                $(elem).css('outline', '#ff0000 solid 1px');
                that.prevElement = elem;
                that.highlightedElement = e.srcElement;
        }, true);
        // end reference: http://stackoverflow.com/questions/4698259/jquery-highlight-element-under-mouse-cursor
    },

    rightClickMenu: function() {
        //https://github.com/mar10/jquery-ui-contextmenu
        that.$frame.contextmenu({
            delegate: "*",
            menu: [{title: 'dummy'}],
			beforeOpen: function (event, ui){
				that.currentElement = $(that.highlightedElement).get(0);
	            var id = that.currentElement.id;
	            var classes = that.currentElement.classList;

                // loop through the css to get the styles

                // loop throught the attributes doing the same

				var style = window.getComputedStyle(that.currentElement);
	            var backgroundColour = style.backgroundColor;
	            var colour = style.color;
	            var width = style.width;
	            var height = style.height;

	            newMenu = [
	            	{title: 'id: ' + id},
	            	{title: 'class: ' + classes},
	            	{title: 'background-color: ' + backgroundColour},
	            	{title: 'color: ' + colour},
	            	{title: 'width: ' + width},
	            	{title: 'height: ' + height}
	            ]

	            that.$frame.contextmenu('replaceMenu', newMenu);

			},
			select: function (event, ui) {
				var cssText = $(ui.item.get(0)).find('a').html();
                var cssProperty = cssText.split(':')[0];
                var cssInput = cssText.split(':')[1].replace(' ','');

                if(cssProperty === 'color' || cssProperty === 'background-color') {
                    cssInput = cssInput.replace('rgba', '')
                    	.replace('rgb', '')
                    	.replace('(', '')
                    	.replace(')', '')
                    	.replace(' ', '');
                    cssInputArray = cssInput.split(',');

                    cssInput = '#';
                    for (i = 0; i < cssInputArray.length; i++) {
                        colorNumber = cssInputArray[i];
                        colorNumber = parseInt(colorNumber);
                        colorNumber = colorNumber.toString(16);
                        cssInput += colorNumber;
                    }
                }

				// generate form for elements dynamically
                that.$dialogLabel.html(cssProperty);
                that.$dialogInput.val(cssInput);
                that.$dialog.dialog( "open" );

			},
        });

    },

    doesAttributeValueExist: function (attribute) {
        if (attribute === undefined) {
            return false;
        } else if (attribute.length === 0){
            return false;
        }
        return true;
    },

    constructValidClassString: function (classString) {
    	// console.log(classString);
        var classArr = classString.split(' ');
        var i;

        classString = '';
        for (i = 0; i < classArr.length; i++) {
            classArr[i] = classArr[i].trim();
            if(classArr[i].length > 0) {
                classString += '.' + classArr[i];
            }
        }
        // console.log(classString);
        return classString;
    },

    getLowerCaseTag: function ($el) {
    	return $el.prop('tagName').toLowerCase();
    },

    constructId: function ($el) {
    	var elId = $el.attr('id');
        if(that.doesAttributeValueExist(elId)) {
            return '#' + elId;
        } else {
            return '';
        }
    },

    constructClass: function ($el) {
    	elClass = $el.attr('class')
        if(that.doesAttributeValueExist(elClass)) {
            return that.constructValidClassString(elClass);
        } else {
            return '';
        }
    },

    uniqueId: function (elArr, parentArr) {
    	parentArr = parentArr || undefined;
        var elAllIds = elArr.join('');
        var i;

		if (parentArr === undefined) {
	        for (i = 0; i < elArr.length; i++) {
	            if (that.$frame.find(elArr[i]).length === 1) {
	            	// console.log('1', elArr[i]);
	                return elArr[i];
	            }
	        }
	        if (that.$frame.find(elAllIds).length === 1) {
	        	// console.log('2', elAllIds);
	        	return elAllIds;
	        }
		} else {
	        for (i = 0; i < parentArr.length - 2; i++) {
	            if (that.$frame.find(parentArr[i].elName + parentArr[i].elId + parentArr[i].elClass + ' ' + elAllIds).length === 1) {
	            	// console.log('4', parentArr[i].elName + parentArr[i].elId + parentArr[i].elClass + ' ' + elAllIds);
	                return parentArr[i].elName + parentArr[i].elId + parentArr[i].elClass + ' ' + elAllIds;
	            }
	        }
		}

    	return '';
    },

    createUniqueIdentifier: function() {
        var $element = $(that.currentElement);
        var tagName = that.getLowerCaseTag($element);
        var elementId = that.constructId($element);
        var elementClass = that.constructClass($element);
        var elementAttrArr = [tagName, elementId, elementClass];

        var parentElementsAttrs = $element.parents().map(function() {
					    			return {
						    				elName: that.getLowerCaseTag($(this)),
						    				elId: that.constructId($(this)),
						    				elClass: that.constructClass($(this))
					        				};
								});

        if (that.uniqueId(elementAttrArr).length > 0) return that.uniqueId(elementAttrArr);
        if (that.uniqueId(elementAttrArr, parentElementsAttrs).length > 0) return that.uniqueId(elementAttrArr, parentElementsAttrs);

        console.log('no unique identifier found');
        return undefined;
    },

    constructUniqueIdAndCssObject: function (uniqueId) {
        var cssProperty = that.$dialogLabel.html();
        var cssValue = that.$dialogInput.val();
        var cssObject = {};

        cssObject[cssProperty] = cssValue;

        if (that.savedCss[uniqueId] === undefined) {
            cssObject[cssProperty] = cssValue;
        } else {
            cssObject = that.savedCss[uniqueId];
            cssObject[cssProperty] = cssValue;
        }
//    console.log(cssObject);
        return cssObject;
    },

    outputjQueryCss: function () {
    	that.jQueryScript = '';
    	$.each(that.savedCss, function(selector, cssObj) {
    		var selector = selector.toString();
    		var cssPropValues = '';
		  	$.each(cssObj, function(cssProperty, cssValue) {
		  		cssPropValues += "'" + cssProperty + "': '" + cssValue + "', ";
		  		// console.log(cssProperty);
		  	});
		  	cssPropValues = cssPropValues.slice(0,-2);
		  	// console.log(cssPropValues);
		  	that.jQueryScript += "$('" + selector + "').css({" + cssPropValues + "});\n"
		  	// console.log(selector);
		  	// console.log(cssPropValues);
		});

    	return that.jQueryScript;
    },

    addVersionjQuery: function(jQueryCss) {
    	return 'if(whichMvt === ' + that.whichMvt +') {\n' + jQueryCss + '}';
    },

    recordChangedCss: function() {
        var uniqueIdentifier = that.createUniqueIdentifier();

        if (uniqueIdentifier !== undefined) {
            that.savedCss[uniqueIdentifier] = that.constructUniqueIdAndCssObject(uniqueIdentifier);
        }

//        console.log(that.addVersionjQuery(that.outputjQueryCss()));
        $('[name=variant_js]').val(that.addVersionjQuery(that.outputjQueryCss()));
    },

    updateElementCss: function() {
        var cssObj = {};
        that.$dialogInput.on('keyup', function() {

        	cssObj = {};
        	cssObj[that.$dialogLabel.html()] = $(this).val();
            $(that.currentElement).animate(cssObj, 200);

            that.recordChangedCss();

        });
    },

    setWhichMvt: function() {
//    	if($('.btn.selected').html() === 'Test A') {
//    		return 1;
//    	} else {
    		return 1;
//    	}

    },

    init: function ($extframe) {
        that = this;
        that.whichMvt = that.setWhichMvt();;
        that.$frame = $extframe.contents();
        that.prevElement;
        that.highlightedElement;
        that.currentElement;
        that.savedCss = {};
        that.$dialogLabel = $('label', '#dialog');
        that.$dialogInput = $('input', '#dialog');
        that.$dialog = $('#dialog');
        that.jQueryScript;

        that.detectHighlightedElement();
        that.rightClickMenu();
        that.updateElementCss();
    }
};

function print_ajax(data) {
    console.log(data);
}

$(document).ready(function () {
    $('#dialog').dialog({
    	autoOpen: false
    });
    console.log(1);
    console.log(Dajaxice);
    Dajaxice.mvt_admin.multiply(Dajax.process);

    Dajaxice.mvt_admin.variant_css(Dajax.process);
});

$('#imported_site').load(function () {

    $extSite = $('#imported_site');
    rudeFish.pType.init($extSite);
});

// html atributes and css styling separate.
// translate colours to hex. Include sliders.
// display changes in realtime, maybe on the form then maybe watch the input and
// adjust accordingly in realtime.
// move UP or down the dom
// show html
// option to set maximum or minimum specifity
// to ensure that this only fires on correct page use combo of body class and url detection.
// email jquery to user to drop into client.js, or ftp it somehow? Maybe not poss
// add a way to select other similar elements/multiple elements
// select, add, remove classes in GUI
// document.activeElement for detecting element under mouse
// generate css not jQuery!