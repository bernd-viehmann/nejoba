<%@ Page Title="" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="show_for_stranger.aspx.py" validateRequest="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <script src="<%# ResolveUrl("~/js/OpenLayers-nejoba.js") %>" type="text/javascript"></script>
    <style type="text/css">
        /* for bootstrap compatibility */
        img.olTileImage {
            max-width: none;
        }
    </style>
</asp:Content>


<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>


<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <div class="row">
        <!-- display the main-object (must be loaded from thre database) in a div-container -->
        <div ID="MAP_AREA" class="span11 offset1" runat="server" visible="true">
            <div id="map" style="height:250px; width:100%;background-color:Gray;"></div>
            <br />                
        </div>
    </div>

<!--
    <div class="row">
        <div ID="SetUpFiltering" runat="server" visible="true">
            <div class="span11 offset1" >
                <h3><asp:Label ID="lbl_heading" runat="server" Text="Heading" /></h3>
            </div>
        </div>
    </div>
-->
    <!-- ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  -->
    <div class="row">
        <div class="accordion span11 offset1" id="accordion_info">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion-heading" href="#collapseOne">
                        <strong><asp:Label ID="Label5" runat="server" Text="Info"></asp:Label></strong>
                    </a>
                </div>
                <small>
                    <div id="collapseOne" class="accordion-body collapse">
                        <div class="accordion-inner">
                            <div class="span1">
                                <asp:Label ID="Label1" runat="server" Text="Ersteller:"></asp:Label>
                                <br />
                                <asp:Label ID="Label6" runat="server" Text="Stadt:"></asp:Label>
                                <br />
                                <asp:Label ID="Label2" runat="server" Text="Erstellt am:"></asp:Label>
                                <br /><br />
                            </div>
                            <div class="span4">
                                <asp:Label ID="lbl_nickname" runat="server"/>
                                <br />
                                <asp:Label ID="lbl_city" runat="server"/>
                                <br />
                                <asp:Label ID="lbl_creationTime" runat="server"/>
                                <br /><br />
                            </div>
                            <div class="span1">
                                <asp:Label ID="lbl_FromDate_lable" runat="server" Text="Start-Termin:"></asp:Label>
                                <br />
                                <asp:Label ID="lbl_TillDate_lable" runat="server" Text="End-Termin:"></asp:Label>
                                <br /><br />
                            </div>
                            <div class="span4">
                                <asp:Label ID="lbl_FromDate" runat="server"/>
                                <br />
                                <asp:Label ID="lbl_TillDate" runat="server"/>
                                <br /><br />
                            </div>
                        </div>
                    </div>
                </small>
            </div>
        </div>
    </div>

    <!-- ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  -->
    <div class="row">
        <div id="divShowMain" class="span11 offset1" runat="server" visible="true">
        Dataoutputarea
        </div>
    </div>

    <div class="row">
        <div class="accordion span11 offset1" id="accordeon_member">
                <div class="accordion-group">
                <div class="accordion-heading">
                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordeon_member" href="#collapseTwo">
                        <strong><asp:Label ID="lbl_notLoggedIn" runat="server" Text="Benutzerkonto"></asp:Label></strong>
                    </a>
                </div>
                <div id="collapseTwo" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <small>
                            <asp:Label ID="Label132" runat="server" Text="Um nejoba vollständig nutzen zu können brauchst du ein eigenes Benutzerkonto. Drücke auf den Knopf falls du noch kein eigenes Konto hast."></asp:Label>
                            <br />
                            <asp:HyperLink ID="HyperLink1" runat="server" class="btn" NavigateUrl="~/wbf_activemap/create_map_user.aspx">
                                <i class="icon-user"></i>
                            </asp:HyperLink>
                            <br />
                            <asp:Label ID="Label234" runat="server" Text="Solltest du schon ein Konto eingerichtet haben logge dich bitte oben rechts mit deiner Mail-Adresse und deinem Passwort ein."></asp:Label>
                        </small>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div style="visibility:hidden;">
        <!-- textfileds are used for centering the map -->
        <asp:Label ID="lbl_map_lon" runat="server" Text=""></asp:Label>
        <asp:Label ID="lbl_map_lat" runat="server" Text=""></asp:Label>
    </div>

    <script type="text/javascript">
        function ResolveUrl(url) {
            if (url.indexOf("~/") == 0) {
                url = baseUrl + url.substring(2);
            }
            return url;
        }

        function initMap() {

            // get the coordinates from server
            var lableTxtLon = $("#CoPlaBottom_lbl_map_lon").text();
            var lableTxtLat = $("#CoPlaBottom_lbl_map_lat").text();

            if ((lableTxtLon.length > 0) && (lableTxtLat.length > 0)) {
                map = new OpenLayers.Map('map');
                var proj4326 = new OpenLayers.Projection("EPSG:4326");
                var projmerc = new OpenLayers.Projection("EPSG:900913");
                var ol_osmap = new OpenLayers.Layer.OSM("Street Map");
                map.addLayers([ol_osmap]);

                markers = new OpenLayers.Layer.Markers("Markers");
                map.addLayer(markers);

                // marker
                var size = new OpenLayers.Size(21, 25);
                var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
                var icon = new OpenLayers.Icon('http://www.openlayers.org/dev/img/marker.png', size, offset);

                // get coords from the server 
                LonCntr = parseFloat(lableTxtLon);
                LatCntr = parseFloat(lableTxtLat);
                var lonlat = new OpenLayers.LonLat(LonCntr, LatCntr).transform(proj4326, projmerc);
                markers.addMarker(new OpenLayers.Marker(lonlat, icon));
                map.setCenter(lonlat);
                map.zoomTo(15);
            }
            else {
                // no coords: do not show the map
                return;
            }
        }

        $(document).ready(function () {
            initMap();
        });
    </script>
</asp:Content>
