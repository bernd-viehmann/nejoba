var urls = ["http://a.tile.openstreetmap.org/${z}/${x}/${y}.png",
                "http://b.tile.openstreetmap.org/${z}/${x}/${y}.png",
                "http://c.tile.openstreetmap.org/${z}/${x}/${y}.png"];

var map;

function init() {
    map = new OpenLayers.Map('map');
/*
    var wms = new OpenLayers.Layer.WMS(
                    "OpenLayers WMS", "http://vmap0.tiles.osgeo.org/wms/vmap0",
                    { layers: 'basic' }
                );
*/
    var wms = new OpenLayers.Layer.XYZ("OSM (with buffer)", urls, {
        transitionEffect: "resize", buffer: 4, sphericalMercator: true
    });

    var layer = new OpenLayers.Layer.Vector("Menschen", {
        strategies: [new OpenLayers.Strategy.BBOX({ resFactor: 1.1 })],
        protocol: new OpenLayers.Protocol.HTTP({
            url: "aktimap_dataSource.aspx",
            //url: "data/text-layer-data.tsv",
            format: new OpenLayers.Format.Text()
        })
    });

    map.addLayers([wms, layer]);
    map.zoomTo(3);
    map.updateSize()

    //map.zoomToMaxExtent();

    // Interaction; not needed for initial display.
    selectControl = new OpenLayers.Control.SelectFeature(layer);
    map.addControl(selectControl);
    selectControl.activate();
    layer.events.on({
        'featureselected': onFeatureSelect,
        'featureunselected': onFeatureUnselect
    });
}


// Needed only for interaction, not for the display.
function onPopupClose(evt) {
    // 'this' is the popup.
    var feature = this.feature;
    if (feature.layer) { // The feature is not destroyed
        selectControl.unselect(feature);
    } else { // After "moveend" or "refresh" events on POIs layer all 
        //     features have been destroyed by the Strategy.BBOX
        this.destroy();
    }
}
function onFeatureSelect(evt) {
    feature = evt.feature;
    popup = new OpenLayers.Popup.FramedCloud("featurePopup",
                                         feature.geometry.getBounds().getCenterLonLat(),
                                         new OpenLayers.Size(100, 100),
                                         "<h2>" + feature.attributes.title + "</h2>" +
                                         feature.attributes.description,
                                         null, true, onPopupClose);
    feature.popup = popup;
    popup.feature = feature;
    map.addPopup(popup, true);
}
function onFeatureUnselect(evt) {
    feature = evt.feature;
    if (feature.popup) {
        popup.feature = null;
        map.removePopup(feature.popup);
        feature.popup.destroy();
        feature.popup = null;
    }
}



/*
var urls = [
    "http://a.tile.openstreetmap.org/${z}/${x}/${y}.png",
    "http://b.tile.openstreetmap.org/${z}/${x}/${y}.png",
    "http://c.tile.openstreetmap.org/${z}/${x}/${y}.png"
];

var map = new OpenLayers.Map({
    div: "map",
    layers: [
        new OpenLayers.Layer.XYZ("OSM (with buffer)", urls, {
            transitionEffect: "resize", buffer: 4, sphericalMercator: true
        })
    ],
    controls: [
        new OpenLayers.Control.Navigation({
            dragPanOptions: {
                enableKinetic: true
            }
        }),
        new OpenLayers.Control.PanZoom(),
        new OpenLayers.Control.Attribution()
    ],
    center: [0, 0],
    zoom: 3
});



var textLayer = new OpenLayers.Layer.Text(
    "deutsche Landeshauptst&auml;dte", 
    {location: "data/text-layer-data.tsv"}
); 

map.addLayer(textLayer); 
*/

