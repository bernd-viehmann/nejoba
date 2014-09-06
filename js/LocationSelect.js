var map;
var markers;

OpenLayers.Control.Click = OpenLayers.Class(OpenLayers.Control, {
    defaultHandlerOptions: {
        'single': true,
        'double': false,
        'pixelTolerance': 0,
        'stopSingle': false,
        'stopDouble': false
    },

    initialize: function (options) {
        this.handlerOptions = OpenLayers.Util.extend(
                    {}, this.defaultHandlerOptions
                );
        OpenLayers.Control.prototype.initialize.apply(
                    this, arguments
                );
        this.handler = new OpenLayers.Handler.Click(
                    this, {
                        'click': this.trigger
                    }, this.handlerOptions
                );
    },
    trigger: function (e) {
        var lonlat = map.getLonLatFromPixel(e.xy)
        var point = map.getLonLatFromPixel(e.xy).transform(new OpenLayers.Projection("EPSG:900913"), new OpenLayers.Projection("EPSG:4326"));
        $('#CoPlaBottom_txbx_lat').val(point.lat);
        $('#CoPlaBottom_txbx_lon').val(point.lon);



        var size = new OpenLayers.Size(21, 25);
        var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
        var icon = new OpenLayers.Icon('http://www.openlayers.org/dev/img/marker.png', size, offset);
        var mrklyr = map.getLayersByName('Markers')[0];
        mrklyr.clearMarkers();
        mrklyr.addMarker(new OpenLayers.Marker(new OpenLayers.LonLat(lonlat.lon, lonlat.lat), icon));

        //var msg = 'Clicked lat : ' + lonlat.lat + '\n' + '        lat : ' + lonlat.lon;
        //console.log(msg);
    }
});

function initMap() {
    map = new OpenLayers.Map('map');
    var proj4326 = new OpenLayers.Projection("EPSG:4326");
    var projmerc = new OpenLayers.Projection("EPSG:900913");
    var ol_osmap = new OpenLayers.Layer.OSM("Street Map");
    map.addLayers([ol_osmap]);

    markers = new OpenLayers.Layer.Markers("Markers");
    map.addLayer(markers);

    var lonlat = new OpenLayers.LonLat(10.159, 51.480).transform(proj4326, projmerc);
    map.setCenter(lonlat);
    map.zoomTo(6);

    var click = new OpenLayers.Control.Click();
    map.addControl(click);
    click.activate();


    // 
    // function loads coords for a given adress from noatim, the opne street maps address jammer
    //
    function findLocation() {
        var mrklyr = map.getLayersByName('Markers')[0];
        mrklyr.clearMarkers();
        $('#CoPlaBottom_txbx_lat').val('');
        $('#CoPlaBottom_txbx_lon').val('');

        // var QueUrl = 'http://nominatim.openstreetmap.org/search?q=+Merianstraße,+Salzburg,+at&format=json&polygon=1&addressdetails=1';
        var QueUrl = prepNoatim();

        $.getJSON(QueUrl, function (data) {

            if (typeof data[0] === 'undefined') {
                var lonlat = new OpenLayers.LonLat(10.159, 51.480).transform(proj4326, projmerc);
                map.setCenter(lonlat);
                map.zoomTo(6);

                $('#CoPlaBottom_txbx_street').val('');
                return;
            };
            var GcLon = data[0]['lon'];
            var GcLat = data[0]['lat'];

            var lonlat = new OpenLayers.LonLat(GcLon, GcLat).transform(proj4326, projmerc);
            map.setCenter(lonlat);
            map.zoomTo(15);

            var Items = '';
            Items += 'Lat :  ' + data[0]['lat'] + '\n';
            Items += 'Lon :  ' + data[0]['lon'] + '\n';
            //console.log(Items);
        });
    }


    // 
    // get the coordinates from ui and center map to it
    //
    function centerMap() {
        var latGiven = $('#CoPlaBottom_txbx_lat').val();
        var lonGiven = $('#CoPlaBottom_txbx_lon').val();

        //console.log('latitude  : ' + latGiven);
        //console.log('longitude : ' + lonGiven);

        latGiven = parseFloat(latGiven);
        if (isNaN(latGiven)) {
            alert("Längengrad ist nicht korrekt! Der Punkt '.' dient als Dezimaltrenner.");
            return;
        }

        lonGiven = parseFloat(lonGiven);
        if (isNaN(lonGiven)) {
            alert("Breitengrad ist nicht korrekt! Der Punkt '.' dient als Dezimaltrenner.");
            return;
        }

        var lonlat = new OpenLayers.LonLat(lonGiven, latGiven).transform(proj4326, projmerc);
        map.setCenter(lonlat);
        map.zoomTo(15);
    }

    // 
    // get the post-code and coordinates for given country-code and placename  12.09.2013
    //
    function getPostCodes() {
        var mrklyr = map.getLayersByName('Markers')[0];
        mrklyr.clearMarkers();
        var city = $('#CoPlaBottom_txbx_city_map').val();
        var ctry = $('#CoPlaBottom_sel_country_map option:selected').val();

        // var QueUrl = 'http://nominatim.openstreetmap.org/search?q=+Merianstraße,+Salzburg,+at&format=json&polygon=1&addressdetails=1';
        var QueUrl = '../ajax/dataSource__countryPostCode.aspx?city=' + city + '&ctry=' + ctry;

        $.getJSON(QueUrl, function (data) {

            if (typeof data.cities[0] === 'undefined') {
                var lonlat = new OpenLayers.LonLat(10.159, 51.480).transform(proj4326, projmerc);
                map.setCenter(lonlat);
                map.zoomTo(6);

                $('#CoPlaBottom_txbx_street').val('');
                return;
            };

            // center map to the first postcodearea we have in the list
            var GcLon = data.cities[0]['lon'].replace(',', '.');
            var GcLat = data.cities[0]['lat'].replace(',', '.');
            // alert(GcLon + ' , ' + GcLat );

            var lonlat = new OpenLayers.LonLat(GcLon, GcLat).transform(proj4326, projmerc);
            map.setCenter(lonlat);
            map.zoomTo(15);

            var postcodeselect = $("#CoPlaBottom_sel_lctn");
            postcodeselect.empty()
            for (var i = 0; i < data.cities.length; i++) {
                var otionTxt = '';
                otionTxt += data.cities[i]['postalCode'] + ' ';
                otionTxt += data.cities[i]['placeName'];
                locationId = data.cities[i]['mngId'];
                postcodeselect.append(new Option(otionTxt, locationId));
            }
            postcodeselect.selectedIndex = 0;

            // update the textfields that will be used by server to store the location-data
            $("#CoPlaBottom_txbx_location_id").val(data.cities[0]['mngId']);
            $("#CoPlaBottom_txbx_location_name").val(data.cities[0]['postalCode'] + ' ' + data.cities[0]['placeName'] );


            // var Items = '';
            // Items += 'Lat :  ' + data[0]['lat'] + '\n';
            // Items += 'Lon :  ' + data[0]['lon'] + '\n';
            // console.log(Items);


        });
    }

    
    // bind the geo-location button event to the image
    $('#CoPlaBottom_img_findLocation').click(function (event) {
        findLocation();
    });

    // 23.06.2013 added button to center map at the coords typed in the textboxes
    $('#CoPlaBottom_img_centerMap').click(function (event) {
        centerMap();
    });

    // 12.09.2013 added button to get the postcodes of a given city
    $('#CoPlaBottom_img_findPostcode').click(function (event) {
        getPostCodes();
    });

    // initialy we have the postcode and the city-name : center map by these data
    findLocation();
}



// 
// prepare noatim-url for geocoding
//
// 13.09.2013   using country-dropdown instead of hidden textbox 
//
//    //    //    //    //    //    //    //    //    //    //    //    //    //    //    //    //    //    //    //    //    //    //    //    //
function prepNoatim() {
    // QueUrl = 'http://nominatim.openstreetmap.org/search?q=+Merianstraße,+Salzburg,+au&format=json&polygon=1&addressdetails=1';
    var QueUrl = 'http://nominatim.openstreetmap.org/search?q=+@@STREET@@,+@@POSTCODE@@,+@@COUNTRYCODE@@&format=json&polygon=1&addressdetails=1';

    // get the input to prepare geocoding
    var street = $('#CoPlaBottom_txbx_street').val();
    // var countrycode = $('#CoPlaBottom_lbl_countrycode').text();
    var countrycode = $('#CoPlaBottom_sel_country_map option:selected').val();

    var city = $('#CoPlaBottom_sel_lctn :selected').text();

    // get the postcode from the selected item
    // var postcode = city.split(' ')[0].toLowerCase();

    // construction
    QueUrl = QueUrl.replace('@@STREET@@', street);
    // QueUrl = QueUrl.replace('@@POSTCODE@@', postcode);
    QueUrl = QueUrl.replace('@@POSTCODE@@', city);
    QueUrl = QueUrl.replace('@@COUNTRYCODE@@', countrycode);

    return QueUrl;
};

