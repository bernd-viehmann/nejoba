// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//   Map-Projector Class
// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//
//   The Class is responsible for displaying the stuff we have in the ListExtractor on the map. using openlayers with open-street-map
//
// member-attributes :
// ________________________________________________________________________________________________________________________________________________________________________________
//
//   
//   
//   
//
// member-functions :
// ________________________________________________________________________________________________________________________________________________________________________________
//
// addMarker
//
//
//
//

// global definitions # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
// # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
AutoSizeAnchoredMinSize = OpenLayers.Class(OpenLayers.Popup.Anchored, { 'autoSize': true, 'minSize': new OpenLayers.Size(400, 200)});
AutoSizeFramedCloudMinSize = OpenLayers.Class(OpenLayers.Popup.FramedCloud, { 'autoSize': true, 'minSize': new OpenLayers.Size(400, 30)});
// # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

/*
 *  MapProjector
 *
 *  this class gets data from the ListExtrctor-Class and displays it 
 *  on the map with open-layers stuff. 
 *
 * parameter : displayurl is the url that will be used to show the details of an item
 *
 * 28.06.2013 bervie initial realese
 *
 */
function MapProjector( dispUrl ) {
    //
    // map initialization 
    //
    this.urls = ["http://a.tile.openstreetmap.org/${z}/${x}/${y}.png",
                    "http://b.tile.openstreetmap.org/${z}/${x}/${y}.png",
                    "http://c.tile.openstreetmap.org/${z}/${x}/${y}.png"];


    //this.iconswtch = {
    //    "§EVT": "./style/marker/waiting.png",
    //    "§ANO": "./style/marker/schreibwaren_web.png",
    //    "§INI": "./style/marker/family.png",
    //    "§BUI": "./style/marker/mine.png",
    //    "§LOC": "./style/marker/home-2.png"
    //};

    //this.stndrIcon = "./style/marker/text.png";
    //this.displayUrl = dispUrl;

    this.iconswtch = {
        "§EVT": nejobaUrl("./style/marker/waiting.png"),
        "§ANO": nejobaUrl("./style/marker/schreibwaren_web.png"),
        "§INI": nejobaUrl("./style/marker/family.png"),
        "§BUI": nejobaUrl("./style/marker/mine.png"),
        "§LOC": nejobaUrl("./style/marker/home-2.png")
    };

    this.stndrIcon = nejobaUrl("./style/marker/text.png");
    this.displayUrl = nejobaUrl(dispUrl);

    this.map = new OpenLayers.Map('map');

    this.wms = new OpenLayers.Layer.XYZ("OSM", this.urls, {
        transitionEffect: "resize", buffer: 4, sphericalMercator: true
    });

    this.markers = new OpenLayers.Layer.Markers("pinsOnMap");
    this.map.addLayers([this.wms, this.markers]);
    this.map.updateSize();

    var lonlat = new OpenLayers.LonLat(5.27, 45.82).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
    this.map.setCenter(lonlat);
    this.map.zoomTo(5);


    /**
     * Function: addMarker
     * Add a new marker to the markers layer given the following lonlat, popupClass, and popup contents HTML. Also allow specifying 
     * whether or not to give the popup a close box.
     * 
     * Parameters:
     * ll -              OpenLayers.LonLat       Where to place the marker
     * iconURL           String                  the URL to the marker-icon
     * popupClass -      OpenLayers.Class        Which class of popup to bring up when the marker is clicked.
     * popupContentHTML  String                  What to put in the popup
     * closeBox -        Boolean                 Should popup have a close box?
     * overflow -        Boolean                 Let the popup overflow scrollbars?
     *
     */
    this.addMarker = function(ll, iconURL, popupClass, popupContentHTML, closeBox, overflow) {
        var size = new OpenLayers.Size(32, 37);
        var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
        var newIcon = new OpenLayers.Icon(iconURL, size, offset);

        var feature = new OpenLayers.Feature( this.markers, ll);
        feature.closeBox = closeBox;
        feature.popupClass = popupClass;
        feature.data.popupContentHTML = popupContentHTML;
        feature.data.overflow = (overflow) ? "auto" : "hidden";
        feature.data.icon = newIcon;

        var marker = feature.createMarker();

        var markerClick = function (evt) {
            for (var i = 0; i < projector.map.popups.length; i++) { projector.map.popups[i].hide(); } 
            if (this.popup == null) {
                this.popup = this.createPopup(this.closeBox);
                projector.map.addPopup(this.popup);
                this.popup.show();
            } else {
                this.popup.toggle();
            }
            currentPopup = this.popup;
            OpenLayers.Event.stop(evt);
        };
        marker.events.register("mousedown", feature, markerClick);
        this.markers.addMarker(marker);
    }

    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  
    /*
     * function MapProjector.createHtmlPU creates the link that is shown in the PopUp
     *
     * parameter : dataItem is the item to display
     *
     * HINT: the function uses this.displayUrl to get the URL that will be used as detail-displayer
     *       this attribute is set in the constructor and set by the server. the url depends on if 
     *       user is logged in or not. 
     *       url is set in a hidden server-control
     *
     * 30.06.2013 bervie initial realese
     *
     */
    this.createHtmlPU = function (dataItm) {
        // console.log('MapProjector.createHtmlPU was called');
        var link = this.displayUrl + String(dataItm['_ID']);
        var rslt = '<h5><a href="' + link + '" target="_blank">' + String(dataItm['subject']) + '</a></h5>';

        return rslt;
    }


    /*
     * function MapProjector.defineMrkrIcon defines which marker-icon will be used for this item. 
     *
     * parameter : dataItem is the item to display
     *
     * 30.06.2013 bervie initial realese
     *
     */
    this.defineMrkrIcon = function (dataItm) {
        // console.log('MapProjector.defineMrkrIcon was called');
        if (dataItm.tagZero == undefined) {
            return this.stndrIcon
        }

        if (dataItm.tagZero.length > 0) {
            var typ = dataItm.tagZero.split("_")[0];
            var icon = this.iconswtch[typ];
        }
        else {
            var icon = this.stndrIcon;
        }

        if (typeof icon === "undefined") icon = this.stndrIcon;
        return icon;
    }


    /*
     * display : this function is called from the ListExtractor. It creates and display the markers on the map
     *
     * parameter :  ItemArray 
     *              the array contains all items that should be displayed. the items are chosen from the ListExtractor
     *              this projector-class has no logic for item-selection. it is only a dispaly-idiot
     *
     * 28.06.2013 bervie initial realese
     *
     */
    this.display = function (itemArray) {
        // console.log('MapProjector.display was called ');
        for (var i = 0; i < projector.map.popups.length; i++) { projector.map.popups[i].hide(); }       // 26.07.2013 remove all popups
        this.markers.clearMarkers();                                                                    // remove all markers
        $.each(itemArray, function (i, val) {
            // console.log('MapProjector.display : ' + String(i) + ' , SUBJECT : ' + String(val.subject));

            ll = new OpenLayers.LonLat(val.lon, val.lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
            popupClass = AutoSizeFramedCloudMinSize;
            popupContentHTML = projector.createHtmlPU(val);
            iconURL = projector.defineMrkrIcon(val);
            projector.addMarker(ll, iconURL, popupClass, popupContentHTML, true, true);
        });
        return;
    }
};






