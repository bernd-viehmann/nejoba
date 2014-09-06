<%@ Page Title="" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="debate_article_editor.aspx.py" validateRequest="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">

    <script src="<%# ResolveUrl("~/style/tinymce/jscripts/tiny_mce/tiny_mce.js") %>" type="text/javascript"></script>
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

    <!-- ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  -->
    <div class="row">
        <div ID="MAP_AREA" runat="server" visible="true" class="span11 offset1">
            <div >
                <div id="map" style="height:377px; width:100%;background-color:Gray;"></div>
            </div>
        </div>
    </div>




    <!-- ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  -->
    <div ID="Div1" runat="server" visible="true">

        <div class="row">
            <div class="span11 offset1">
                <asp:CheckBox ID="cxbx_email_abo" runat="server" Text="Abo" ToolTip="Wenn angehakt bekommst du eine Mail wenn ein Standpunkt hinzugefügt wird." AutoPostBack="true" OnCheckedChanged="HndlrButtonClick"/>
                
            </div>
        </div>

        <div class="row">
            <div class="span11 offset1">
                <h3><asp:Label ID="lbl_heading" runat="server" Text="Heading" /></h3>
            </div>
        </div>

        <div class="row">
            <div class="span11 offset1">
                <div class="accordion" id="accordion_info">
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
                                        <asp:Label ID="Label2" runat="server" Text="Ersteller:"></asp:Label>
                                        <br />
                                        <asp:Label ID="Label6" runat="server" Text="Stadt:"></asp:Label>
                                        <br />
                                        <asp:Label ID="Label4" runat="server" Text="Erstellt am:"></asp:Label>
                                        <br /><br />
                                    </div>
                                    <div class="span2">
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
                                    <div class="span2">
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
        </div>
    </div>


    <!-- ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  ####  -->
    <div class="row">
        <div id="divShowThread" runat="server" class="span11 offset1">dataoutputaera not populated</div>
    </div>









        <!-- # #    data-output for the items in the discussion    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->

    <!-- # #    editor for deabtes     # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div ID="YES_WE_CAN" runat="server" visible="true">
        <div class="row">
            <div class="span1"></div>
            <div class="span10">
                <div class="span10">
                    <h4><asp:Label ID="Label1" runat="server" Text="Kommentar"></asp:Label></h4>
                </div>
                <div class="span2">
                    <a id="show_help" class="btn" href="#guidance" role="button" title="Anleitung" data-placement="bottom" data-toggle="modal" data-original-title="Anleitung"><i class="icon-info-sign"></i></a>
                </div>
                <br /><br /><br />
                <p>
                    <br />
                    <asp:TextBox runat="server" ID="txtMain" TextMode="MultiLine" Rows="17" style="width:97%"></asp:TextBox>
                </p>
            </div>
            <div class="span1"></div>
        </div>
        <div class="row">
            <div class="span1"></div>
            <div class="span10">
                <asp:Button ID="btnPublish" runat="server" class="btn btn-large btn-primary pull-right" Text="Kommentar ver&ouml;ffentlichen" onclick="HndlrButtonClick"/>
            </div>
            <div class="span1"></div>
        </div>
    </div>

















    
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   modal dialog with a short guidance how to use this webform                                                                        @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <div id="guidance" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="linkreuseLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h4>Anleitung: Einen Beitrag im Nachbarforum diskutieren.</h4>
        </div>
        <div class="modal-body">
        <br /><br />
        <asp:HyperLink ID="HyperLink2" runat="server" NavigateUrl="../wbf_help/help_debates.aspx" Target="_blank">Zur Bedienungsanleitung</asp:HyperLink>
        <br /><br />
        <asp:HyperLink ID="HyperLink_YouTube" runat="server" NavigateUrl="http://www.youtube.com/user/nejobavideo" Target="_blank">Videos zum Thema nejoba auf YouTube</asp:HyperLink>
        <br /><br />
        <asp:HyperLink ID="HyperLink_facebook" runat="server" NavigateUrl="https://www.facebook.com/nejoba" Target="_blank">Unser Benutzerforum auf facebook.</asp:HyperLink>
        </div>
        
        <div class="modal-footer">
            <button class="btn" data-dismiss="modal" aria-hidden="true">Fertig</button>
        </div>
    </div>



    <div style="visibility:hidden;">
        <asp:Label ID="msg_mailSubject" runat="server" Text="nejoba Debaten  : Es wurde ein neuer Beitrag hinzugef&uuml;gt"></asp:Label>

        <!-- textfileds are used for centering the map -->
        <asp:Label ID="lbl_map_lon" runat="server" Text=""></asp:Label>
        <asp:Label ID="lbl_map_lat" runat="server" Text=""></asp:Label>

        <!-- tags and locations : locations are used by the Item-sve fct. So we have to have a textbox for it !! -->

        <asp:TextBox ID="txbx_tagforitem" runat="server" />                             <!-- the hidden textbox stores the tag for a rubric -->
        <asp:TextBox ID="txbx_itemname" runat="server" />                               <!-- the hidden textbox stores the nice-name of choosen rubric -->
        <asp:TextBox ID="txbx_location_id" runat="server" />                            <!-- the hidden textboxes stores the location-id   of hometown -->
        <asp:TextBox ID="txbx_location_name" runat="server" />                          <!-- the hidden textboxes stores the location-name of hometown -->


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
            $("#CoPlaBottom_txtMain").wysihtml5();
            initMap();
        }); 

    </script>
</asp:Content>

