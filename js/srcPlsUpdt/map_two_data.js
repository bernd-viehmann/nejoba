// ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// OPEN-STREET-MAP functionality
// ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

var urls = ["http://a.tile.openstreetmap.org/${z}/${x}/${y}.png",
            "http://b.tile.openstreetmap.org/${z}/${x}/${y}.png",
            "http://c.tile.openstreetmap.org/${z}/${x}/${y}.png"];

var map;


AutoSizeAnchoredMinSize = OpenLayers.Class(OpenLayers.Popup.Anchored, {
    'autoSize': true,
    'minSize': new OpenLayers.Size(400, 400)
});


AutoSizeFramedCloudMinSize = OpenLayers.Class(OpenLayers.Popup.FramedCloud, {
    'autoSize': true,
    'minSize': new OpenLayers.Size(400, 400)
});
function initOsmMap() {
    try {
        map = new OpenLayers.Map('map');

        var wms = new OpenLayers.Layer.XYZ("OSM", urls, {
            transitionEffect: "resize", buffer: 4, sphericalMercator: true
        });
        markers = new OpenLayers.Layer.Markers("zibo");
        map.addLayers([wms, markers]);
        map.updateSize();

        var lonlat = new OpenLayers.LonLat(5.27, 45.82).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
        map.setCenter(lonlat);
        map.zoomTo(4);

        addMarkers();
    }
    catch (err) {
        txt = "There was an error in initOsmMap\n\n";
        txt += "Error description: " + err.message + "\n------------------------------------------------------------------------------------------------------------------------------------------------------------\n";
        console.log(txt);
    }
}



function addMarkers() {
    try {
        var ll, popupClass, popupContentHTML;

        //anchored bubble popup wide long fixed contents autosize closebox overflow
        ll = new OpenLayers.LonLat(5.27, 45.82).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
        popupClass = AutoSizeAnchoredMinSize;
        popupContentHTML = '<img src="../style/pic/hilfe.png"></img>';
        iconURL = '../style/marker/beergarden.png';
        addMarker(ll, iconURL, popupClass, popupContentHTML, true, true);

        //anchored bubble popup wide long fixed contents autosize closebox overflow
        ll = new OpenLayers.LonLat(5.24, 45.84).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
        popupClass = AutoSizeFramedCloudMinSize;
        popupContentHTML = '<img src="../style/pic/hilfe.png"></img>';
        iconURL = '../style/marker/bullfight.png';
        addMarker(ll, iconURL, popupClass, popupContentHTML, true, true);

        //anchored bubble popup wide long fixed contents autosize closebox overflow
        ll = new OpenLayers.LonLat(5.21, 45.81).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
        popupClass = AutoSizeFramedCloudMinSize;
        popupContentHTML = '<img src="../style/pic/hilfe.png"></img>';
        iconURL = '../style/marker/bigcity.png';
        addMarker(ll, iconURL, popupClass, popupContentHTML, true, true);

        //pappelstrasse kreisverkehr
        ll = new OpenLayers.LonLat(6.210592, 51.039806).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
        popupClass = AutoSizeFramedCloudMinSize;
        popupContentHTML = '<img src="../style/pic/hilfe.png"></img>';
        iconURL = '../style/marker/house.png';
        addMarker(ll, iconURL, popupClass, popupContentHTML, true, true);

    }
    catch (err) {
        txt = "There was an error in addMarkers\n\n";
        txt += "Error description: " + err.message + "\n------------------------------------------------------------------------------------------------------------------------------------------------------------\n";
        console.log(txt);
    }
}


/**
* Function: addMarker
* Add a new marker to the markers layer given the following lonlat, 
*     popupClass, and popup contents HTML. Also allow specifying 
*     whether or not to give the popup a close box.
* 
* Parameters:
* ll - {<OpenLayers.LonLat>} Where to place the marker
* iconURL     {String}      
* popupClass - {<OpenLayers.Class>} Which class of popup to bring up when the marker is clicked.
* popupContentHTML - {String} What to put in the popup
* closeBox - {Boolean} Should popup have a close box?
* overflow - {Boolean} Let the popup overflow scrollbars?
*/
function addMarker(ll, iconURL, popupClass, popupContentHTML, closeBox, overflow) {
    try {
        var size = new OpenLayers.Size(32, 32);
        var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
        var newIcon = new OpenLayers.Icon( iconURL, size, offset );

        var feature = new OpenLayers.Feature(markers, ll);
        feature.closeBox = closeBox;
        feature.popupClass = popupClass;
        feature.data.popupContentHTML = popupContentHTML;
        feature.data.overflow = (overflow) ? "auto" : "hidden";
        feature.data.icon = newIcon;

        var marker = feature.createMarker();
        //marker.setUrl('http://maps.google.com/intl/en_us/mapfiles/ms/micons/orange-dot.png');

        var markerClick = function (evt) {
            if (this.popup == null) {
                this.popup = this.createPopup(this.closeBox);
                map.addPopup(this.popup);
                this.popup.show();
            } else {
                this.popup.toggle();
            }
            currentPopup = this.popup;
            OpenLayers.Event.stop(evt);
        };
        marker.events.register("mousedown", feature, markerClick);
        //marker.setUrl('');

        
        markers.addMarker(marker);
    }
    catch (err) {
        txt = "There was an error in initOsmMap\n\n";
        txt += "Error description: " + err.message + "\n------------------------------------------------------------------------------------------------------------------------------------------------------------\n";
        console.log(txt);
    }
}





function startLoad(){
    alert('Load is starting now. ignition !');


}



