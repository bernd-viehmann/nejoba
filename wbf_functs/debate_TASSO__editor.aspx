<%@ Page Title="" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="debate_TASSO__editor.aspx.py" validateRequest="false" EnableEventValidation="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <script src="<%# ResolveUrl("~/style/tinymce/js/tinymce/tinymce.min.js") %>" type="text/javascript"></script>
    <script src="<%# ResolveUrl("~/js/OpenLayers-nejoba.js") %>" type="text/javascript"></script>
    <script src="<%# ResolveUrl("~/js/MatrixManager.js") %>" type="text/javascript"></script>
    <script src="<%# ResolveUrl("~/js/LocationSelect.js") %>" type="text/javascript"></script>

    <style type="text/css">
        /* for bootstrap compatibility */
        img.olTileImage {
            max-width: none;
        }
    </style>
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server"></asp:Content>
<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

<div id="editpart" class="container span10">
    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <!-- # #   Heading                                                                                                                                                                                                     # # # -->
    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div id="div_select_main" class="row-fluid well span10">
        <div class="span2 offset1">
            <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/quatschtuete.png" ToolTip="Beginne ein neues Thema" />
        </div>
        <div class="span8 offset1">
            <h3><asp:Label ID="Label2" runat="server" Text="Neuen Beitrag erstellen" /></h3>
            <asp:Label ID="Label3" runat="server" Text="Hier kannst du einen eigenen Beitrag im Forum veröffentlichen." />
            <a id="show_help" class="btn" href="#guidance" role="button" title="Wie schreibt man etwas ins Forum?" data-placement="bottom" data-toggle="modal" data-original-title="Wie schreibt man etwas ins Forum?"><i class="icon-info-sign"></i></a>
        </div>
    </div>

    <div class="row-fluid well span10">
        <div class="span7 offset1">
            <h4>
                <asp:Label ID="Label1" runat="server" Text="Die Kurzmitteilung" ToolTip="Veröffentliche einen Beitrag im Forum. Eine Kurzmitteilung ist immer erforderlich. Zusätzlich kannst Du ein Dokument anfügen." />
                <br /><br />
                <asp:TextBox ID="txbHeader" runat="server" placeholder="Fasse Dein Thema kurz zusammen..." Rows="4" Width="100%" ToolTip="Die Kurzmitteilung ist erforderlich. Verwende Hashtags zur Gruppierung."></asp:TextBox>
            </h4>
        </div>

        <div class="span3 offset1">
            <br /><br />
            <!--<asp:Button ID="btn_Save_older" runat="server" class="btn btn-large btn-primary pull-right" Text="Beitrag ver&ouml;ffentlichen" onclick="HndlrButtonClick"/>-->
            <button id="btn_showPreview" type="button" class="btn btn-large btn-primary pull-right">Vorschau</button>
        </div>
    </div>


    <div id="div1" class="row-fluid well span10 minimize">
        <div class="accordion" id="accordion2">
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <!-- # #   map for setting the location                                                                                                                                                                                 # # # -->
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="accordion-group">
                <div class="accordion-heading">
                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseLocation">
                    <h4><asp:Label ID="Label10" runat="server" Text="Ort" ToolTip="Bestimme einen Ort auf der Karte. nejoba markiert diesen Beitrag an dieser Stelle." /></h4>
                </a>
                </div>
                <div id="collapseLocation" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <div class="row">
                            <div id="Div4" class="span10 offset1 alert alert-info">
                                <!--
                                <asp:Label ID="Label17" runat="server" Text="<strong>Hinweis: </strong>Alle Beiträge auf nejoba werden einer Postleitzahl zugeordnet. Der Marker beeinflußt das Postleitzahlgebiet <strong>nicht!</strong><br /><br />" />
                                <asp:Label ID="Label18" runat="server" Text="Wenn du keine andere auswählst übernimmt nejoba die Postleitzahl deines Benutzerkontos. <strong>Unter dieser PLZ wird der Beitrag gefunden, egal wo der Marker gesetzt ist.</strong><br /><br />"></asp:Label>
                                <asp:Label ID="Label19" runat="server" Text="Wenn dein Beitrag für eine andere Stadt gilt solltest du also auch die passende Postleitzahl auswählen. Um eine Markierung zu setzen musst du diese in der Karte per Mausklick setzen. Die Suche unterhalb dient nur dazu die Karte zu zentrieren."></asp:Label>
                                -->
                                <asp:Label ID="Label1347" runat="server" Text='<br /><strong style="color: #AA0000; font-size: 17pt">Für die Ortsmarkierung einfach einmal auf die Karte klicken.</strong> <br /><br />Es erscheint dann eine rote Markierung. So kannst du auch Orte wählen für die es keine Postadresse gibt. Zum Beispiel einen Parkplatz als Sammelpunkt für eine Fahrgemeinschaft.<br /><br />' ForeColor="Black" />
                                <asp:Label ID="Label523" runat="server" Text='In der Auswahl für die Postleitzahl bei <strong>"Postleitzahl festlegen"</strong> kannst du festlegen welchem Ort dein Beitrag zugeordnet wird. Du kannst unter <strong>"Stadt suchen"</strong> belibiege Orte wählen.<br />' ForeColor="Black" />
                            </div>
                        </div>

                        <div class="span11">
                            <div id="map" style="height:500px; width:100%;"></div>
                            <div class="row"><br /><br /></div>
                        </div>



                        <ul class="nav nav-tabs">
                            <li class="active"><a href="#regio_tab" data-toggle="tab">Postleitzahl festlegen</a></li>
                            <li><a href="#nationwide_tab" data-toggle="tab">Stadt suchen</a></li>
                            <li><a href="#goggle_map" data-toggle="tab">Koordinaten eintragen</a></li>
                        </ul>

                        <div class="tab-content">
                            <!-- ##### regional postcode-selection ###### -->
                            <div id="regio_tab" class="tab-pane active">
                                <div class="span11"><br /></div>

                                <div class="span3">
                                    <label>
                                        <asp:Label ID="lbl_cntrysel" runat="server" Text="Land" />
                                    </label>
                                </div>
                                <div class="span7">
                                    <asp:DropDownList ID="sel_country" runat="server"  ToolTip="Derzeit ist nejoba nur in deutscher Sprache verfügbar. Daran wird aber gearbeitet.">
                                        <asp:ListItem Text="Deutschland" Value="DE" />
                                        <asp:ListItem Text="Österreich" Value="AT" />
                                        <asp:ListItem Text="Schweiz" Value="CH" />
                                        <asp:ListItem Text="Liechtenstein" Value="LI" />
                                        <asp:ListItem Text="Luxemburg" Value="LU" />
                                        <asp:ListItem Text="Niederlande" Value="NL" />
                                        <asp:ListItem Text="Belgien" Value="BE" />
                                    </asp:DropDownList>
                                </div>






                                <div class="span3"><label>
                                    <asp:Label ID="lbl_city2" runat="server" Text="Stadt" /></label>
                                </div>

                                <div class="span7 input-append">
                                    <input id="txbx_city" class="typeahead" type="text" />
                                    <button id="img_findPostcode" class="btn btn-success" type="button" >Suchen</button>
                                </div>

                                <div class="span3"><label><asp:Label ID="lbl_city" runat="server" Text="Postleitzahl" /></label></div>
                                <div class="span7"><asp:DropDownList ID="sel_lctn" runat="server" EnableViewState="True" /></div>

                                <div class="span3"><label><asp:Label ID="lbl_street" runat="server" Text="Straße" /></label></div>
                                <div class="span7"><asp:TextBox ID="txbx_street" runat="server" ToolTip="Bitte nur den Namen der Strasse eingeben. Hausnummer weglassen!"></asp:TextBox></div>

                                <div class="span2 offset1"><asp:Image ID="img_findLocation"       runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_search_loc.png"          ToolTip="Karte zentrieren." /></div>
                            </div>


                            <div id="nationwide_tab" class="tab-pane">
                            <!-- ##### nationwide postcode-selection ###### -->

                                <div class="row"><br /></div>


                                <div class="row">
                                    <div class="span2 offset1"><asp:Image ID="ccc" runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_search_loc.png"          ToolTip="Stadt wählen " /></div>
                                </div>

                                <div class="row"><br /><br /></div>

                                <div style="display:none;">
                                    <div class="row">
                                        <div class="span3 offset1"><label><asp:Label ID="lbl_streetByPostcode" runat="server" Text="Straße" /></label></div>
                                        <div class="span4"><asp:TextBox ID="txbx_streetByPostcode" runat="server" ToolTip="Bitte nur den Namen der Strasse eingeben. Hausnummer weglassen!"></asp:TextBox></div>
                                    </div>

                                    <div class="row">
                                        <div class="span2 offset1"><asp:Image ID="img_findAdressForPostcode" runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_search_loc.png"          ToolTip="Adresse suchen." /></div>
                                    </div>
                                </div>
                            </div>

                            <div id="goggle_map" class="tab-pane">
                                <div class="row">
                                    <div id="Div3" class="span10 offset1 alert alert-info">
                                        <asp:Label ID="Label14" runat="server" Text="Du kannst hier den Kartendienst von Google aufrufen falls du mit der eingebauten Suche nicht zurecht kommst.<br /><br />" />
                                        <asp:Label ID="Label15" runat="server" Text="Wenn du die Koordinaten kennst trage sie in die Felder ein. Ansonsten werden hier die Positionsdaten vom Marker eingetragen, den du in der Karte mit einem einzelnen Klick gesetzt hast.<br/><br/>"></asp:Label>
                                        <asp:Label ID="Label16" runat="server" Text="<strong>Das Dezimaltrennzeichen ist hier der Punkt (.) und nicht das Komma-Zeichen (,).</strong>"></asp:Label>
                                    </div>
                                </div>

                                <div class="row"><br /></div>

                                <div class="row img-polaroid">
                                    <div class="span3 offset1"></div>
                                    <div class="span4"><asp:HyperLink ID="hyli_mapcoordinates" runat="server" Text="GoogleMaps nutzen" NavigateUrl="http://www.mapcoordinates.net/" ImageUrl="../style/pic/Google_maps_logo.png" Target="_blank" ToolTip="Breiten- und Längengrad per 'Cut and Paste' in die Textfelder" /></div>
                                </div>

                                <div class="row"><br /><br /></div>

                                <div class="row">
                                    <div class="span3 offset1"><label><asp:Label ID="lbl_lat" runat="server" Text="Breitengrad" /></label></div>
                                    <div class="span4"><asp:TextBox ID="txbx_lat" runat="server" ToolTip="Wenn du die Koordinaten kennst targe diese ein. Beachte das ein PUNKT (.) anstatt einem Komma als dezimales Trennzeichen benutzt werden muss"></asp:TextBox></div>
                                </div>

                                <div class="row">
                                    <div class="span3 offset1"><label><asp:Label ID="lbl_lon" runat="server" Text="Längengrad" /></label></div>
                                    <div class="span4"><asp:TextBox ID="txbx_lon" runat="server" ToolTip="Wenn du die Koordinaten kennst targe diese ein. Beachte das ein PUNKT (.) anstatt einem Komma als dezimales Trennzeichen benutzt werden muss"></asp:TextBox></div>
                                </div>

                                <div class="row">
                                    <div class="span3 offset1"><label><asp:Label ID="lbl_centerMapAgain" runat="server" Text="Karte neu zentrieren." ToolTip="Die Mitte der Karte wird anhand der Koordinaten gesetzt." /></label></div>
                                    <div class="span4"><asp:Image ID="img_centerMap" runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_search_loc.png" ToolTip="Karte neu zentrieren." /></div>
                                </div>
                                    
                                <br />
                                    
                            </div>
                        </div>

















                    </div>
                </div>
            </div>


            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <!-- # #   upload a photo to the webserver it should be deleted automatically                                                                                                                                         # # # -->
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="accordion-group">
                <div class="accordion-heading">
                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseUpload">
                    <h4><asp:Label ID="Label5" runat="server" Text="Bild hochladen" ToolTip="Du kannst ein Bild zu Deiner Anzeige hochladen" /></h4>
                </a>
                </div>
                <div id="collapseUpload" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <div id="loadfile" class="span11">
                            <asp:FileUpload ID="FileUpload1" runat="server" />
                        </div>
                    </div>
                </div>
            </div>




            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <!-- # #   the body of a message                                                                                                                                                                                    # # # -->
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="accordion-group">
                <div class="accordion-heading">
                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseBody">
                    <h4><asp:Label ID="LabelBody" runat="server" Text="Beschreibung" ToolTip="Hier kannst du eine genau Beschreibung eingeben. Es ist möglich Bilder und Videos einzubinden." /></h4>
                </a>
                </div>
                <div id="collapseBody" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <div id="area_edit" class="span11">
                            <h4>
                                <asp:Label ID="lbl_hint" runat="server" Text="Dein Dokument" ToolTip="Das Dokument ist mit der Kurzmeldung verknüpft. Es ist nicht zwingend erforderlich."></asp:Label>
                                <a id="shwHelp2" class="btn" href="#guidance2" role="button" title="Wie schreibt man etwas ins Forum?" data-placement="bottom" data-toggle="modal" data-original-title="Wie schreibt man etwas ins Forum?"><i class="icon-info-sign"></i></a>
                            </h4>
                            <asp:TextBox runat="server" ID="txtMain" TextMode="MultiLine" Rows="27" style="width:92%"></asp:TextBox>
                        </div>
                    </div>
                </div>
            </div>









            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <!-- # #   additional attributes select a start- and end-date                                                                                                                                                          # # # -->
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="accordion-group">
                <div class="accordion-heading">
                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseOne">
                    <h4><asp:Label ID="Label4" runat="server" Text="Termin" ToolTip="Dein Beitrag kann mit einer Zeitangabe verknüpft werden. Sinnvoll ist das beispielsweise für Veranstaltungen. Auf nejoba kann ein Nutzer die Suche auf einen bestimmten Tag beschränken. Dann werden ihm nur Beiträge angezeigt, die mit einem passenden Termin verknüpft sind." /></h4>
                </a>
                </div>
                <div id="collapseOne" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <div class="span11"></div>
                        <div class="span2">
                            <label><asp:Label ID="lbl_date" runat="server" Text="Start-Termin" /></label>
                            <asp:TextBox ID="txbx_timeFrom" runat="server" ToolTip="Trage hier den Tag der Veranstalltung ein. Wenn die Veranstalltung mehrere Tage dauert ist dies der erste Tag."></asp:TextBox>
                        </div>
                        <div class="span2 offset1">
                            <label><asp:Label ID="Label6" runat="server" Text="End-Termin" /></label>
                            <asp:TextBox ID="txbx_timeTo" runat="server" ToolTip="Wenn die Veranstaltung mehrere Tage dauert, wird hier der Schlusstag eingetragen. WICHTIG: Wenn der Termin nicht über mehrere Tage andauert lass dieses Feld leer."></asp:TextBox>
                        </div>
                    </div>
                </div>
            </div>


            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <!-- # #   define rubric of announcment                                                                                                                                                                                # # # -->
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="accordion-group">
                <div class="accordion-heading">
                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseTwo">
                    <h4><asp:Label ID="Label8" runat="server" Text="Rubrik" ToolTip="Dein Beitrag in einer der nejoba-Rubriken eingliedern." /></h4>
                </a>
                </div>
                <div id="collapseTwo" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <div class="span12">
                            <div class="span5">
                                <h5>
                                    <asp:HyperLink ID="hyli_selectEvent" runat="server" class="well" Text="Termine" Width="80%" ToolTip="Termine und Veranstaltungen suchen " />
                                </h5>
                                <h5>
                                    <asp:HyperLink ID="hyli_selectLocation" runat="server" class="well" Text="Orte" Width="80%" ToolTip="points of interest " />
                                </h5>
                            </div>

                            <div class="span5">
                                <h5>
                                    <asp:HyperLink ID="hyli_selectAnnonceType" runat="server" class="well" Text="Kleinanzeigen" Width="80%" ToolTip="Kaufen, Tauschen, Schenken und Verleihen in der Nachbarschaft " />
                                </h5>
                                <h5>
                                    <asp:HyperLink ID="hyli_selectInitiatives" runat="server" class="well" Text="Initiativen" Width="80%" ToolTip="Aktive Nachbarn und gesellschaftliche Initiativen " />
                                </h5>
                            </div>

                            <div class="span11 offset1"><br /></div>

                            <div class="span2 offset1">
                                <select id="lsbx_0" multiple="multiple" size="13" style="width:99%;"></select>
                            </div>
                            <div class="span2">
                                <select id="lsbx_1" multiple="multiple" size="13" style="width:99%;"></select>
                            </div>
                            <div class="span2">
                                <select id="lsbx_2" multiple="multiple" size="13" style="width:99%;"></select>
                            </div>
                            <div class="span2">
                                <select id="lsbx_3" multiple="multiple" size="13" style="width:99%;"></select>
                            </div>
                            <div class="span2">
                                <select id="lsbx_4" multiple="multiple" size="13" style="width:99%;"></select>
                            </div>
                            <div class="span2 offset1">
                                <br />
                                <asp:TextBox ID="txbx_itemname" runat="server" ToolTip="Name of Item" Enabled="false" />
                            </div>
                        </div>
                        <div class="span11 offset1"></div>
                    </div>
                </div>
            </div>



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
            <h4>Anleitung: Einen Beitrag veröffentlichen.</h4>
        </div>
        <div class="modal-body">
        <iframe width="480" height="360" src="//www.youtube.com/embed/Kkg3GQm7Hdc" frameborder="0" allowfullscreen></iframe>
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


    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   modal dialog with a short guidance how to use this webform                                                                        @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <div id="guidance2" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="linkreuseLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h4>Anleitung: Fortgeschrittene Beiträge</h4>
        </div>
        <div class="modal-body">
        <iframe width="480" height="360" src="//www.youtube.com/embed/otCK2HGi4t0" frameborder="0" allowfullscreen></iframe>
        <br /><br />
        <asp:HyperLink ID="HyperLk1" runat="server" NavigateUrl="../wbf_help/help_debates.aspx" Target="_blank">Zur Bedienungsanleitung</asp:HyperLink>
        <br /><br />
        <asp:HyperLink ID="HyperLk3" runat="server" NavigateUrl="http://www.youtube.com/user/nejobavideo" Target="_blank">Videos zum Thema nejoba auf YouTube</asp:HyperLink>
        <br /><br />
        <asp:HyperLink ID="HyperLk4" runat="server" NavigateUrl="https://www.facebook.com/nejoba" Target="_blank">Unser Benutzerforum auf facebook.</asp:HyperLink>
        </div>
        
        <div class="modal-footer">
            <button class="btn" data-dismiss="modal" aria-hidden="true">Fertig</button>
        </div>
    </div>
</div>














<div id="inspection" style="display:none;">
    <div class="row alert alert-info span10 well">
        <asp:Label ID="Label1er7" runat="server" Text="<strong>Ein Beitrag auf nejoba kann nicht nachträglich verändert werden.</strong> <br/><br/>Daher kontrolliere bitte hier deine Eingaben und achte auch auf die Eigenschaften wie Ort, Rubrik oder Datumsangaben." />
    </div>

    <div id="canvas"></div>

    <div class="row span10 well">
        <div class="span3 offset1">
            <button id="btn_backToEdit" type="button" class="btn btn-large btn-warning pull-right">Neu bearbeiten</button>
        </div>
        <div class="span3 offset1">
            <asp:Button ID="btn_Save" runat="server" class="btn btn-large btn-success pull-right" Text="Ver&ouml;ffentlichen" onclick="HndlrButtonClick"/>
        </div>
    </div>
</div>
















<!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
<!-- @@                                                                                                                                     @@ -->
<!-- @@   hiddenstuff to be translated to have easy multilanguagesupport                                                                    @@ -->
<!-- @@                                                                                                                                     @@ -->
<!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
<div style="display:none;">
    <!-- the div-text will toggled by the type-select-buttons. used from javascript to choose the corresponding data-container-->
    <div id="toggle_div"></div>

    <!-- hidden text that is needed for the error-messages-->
    <asp:Label ID="lbl_header_needed" runat="server" Text="Eine Betreff-Zeile (Überschrift) ist zwingend erforderlich !"></asp:Label>
    <asp:Label ID="lbl_time_from_invalid_format" runat="server" Text="Deine Eingabe für den Start-Termin ist nicht gültig !"></asp:Label>
    <asp:Label ID="lbl_time_to_invalid_format" runat="server" Text="Deine Eingabe für den End-Termin ist nicht gültig !"></asp:Label>
    <asp:Label ID="lbl_missing_from_date" runat="server" Text="Du hast einen End- aber keinen Start-Termin eingegeben !"></asp:Label>
    <asp:Label ID="lbl_from_date_after_to" runat="server" Text="Datumsangaben haben vertauschte Start- und Endangabe !"></asp:Label>
    <asp:Label ID="lbl_latitude_error" runat="server" Text="Der eingegeben Breitengrad ist ungültig !"></asp:Label>
    <asp:Label ID="lbl_longitude_error" runat="server" Text="Der eingegeben Längengrad ist ungültig !"></asp:Label>
    <asp:Label ID="lbl_need_both_coords" runat="server" Text="Es werden beide Angaben für Längen- und Breitengrad benötigt !"></asp:Label>


    <!-- the country-code of the user is used by javascript to make the geocoding by noatim -->
    <!-- obsolete  13.09.2013  -->
    <asp:Label ID="lbl_countrycode" runat="server" Text=""></asp:Label>

    <!-- the hidden textbox stores the tag for a rubric -->
    <asp:TextBox ID="txbx_tagforitem" runat="server" />

    <!-- the hidden textboxes stores the name id of the hometown of user -->
    <asp:TextBox ID="txbx_location_id" runat="server" />
    <asp:TextBox ID="txbx_location_name" runat="server" />

    <!-- the div will contain the source-data for the item-type-selection -->
    <div id="date_event_div" runat="server"></div>
    <div id="location_div" runat="server"></div>
    <div id="annonce_div" runat="server"></div>
    <div id="initiative_div" runat="server"></div>
    <div id="business_div" runat="server"></div>

    <!-- previewtamplate will be loaded when preview-button was clicked -->
    <!-- the §§STRING§§ parts will be replaces by users input -->
    <div id="template">
        <div class="row span10 well">
            <div class="span11 offset1">
                <h4><asp:Label ID="Labeldsdf17" runat="server" Text="Eingabe kontrollieren" /></h4>
            </div>

            <div class="span11 offset1"><br /></div>

            <div class="span4 offset1">
                §§LOCATIONNAME§§<br />
                §§RUBRICNAME§§<br />
            </div>
            <div class="span4">
                §§DATE_FROM§§<br />
                §§DATE_TILL§§<br />
            </div>
            <div class="span3"></div>

            <div class="span11 offset1"><br /></div>
        </div>

        <div class="row span10">
            <div class="span11 offset1">§§HEADERTXT§§</div>
        </div>

        <div class="row span10">
            <div class="span11 offset1">§§BODYTXT§§</div>
        </div>
    </div>
</div>




























<script type="text/javascript">
    var map, vectors, controls;

    function ResolveUrl(url) {
        if (url.indexOf("~/") == 0) {
            url = baseUrl + url.substring(2);
        }
        return url;
    }


    $(document).ready(function () {


        // $("#CoPlaBottom_txtMain").wysihtml5();                                        // bootstrap free editor
        $("#CoPlaBottom_txbx_timeFrom").datepicker($.datepicker.regional["de"]);
        $("#CoPlaBottom_txbx_timeTo").datepicker($.datepicker.regional["de"]);

        /*
         * HTML-editor initialization
         *
         */
        tinymce.init({
        selector: "textarea",
        plugins: [
        "advlist autolink lists link image charmap print preview anchor",
        "searchreplace visualblocks code fullscreen",
        "insertdatetime media table contextmenu paste "
        ],
        toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image",
        language: 'de'
        });

        /*
        *  handle autocomplete for cities
        *
        */
//        cityListFromServer = []                 // used as datasource for the bootstrap-typeahead 'txbx_city'
//        $('#txbx_city').typeahead({
//            source: function (query, process) {
//                var ajxurl = nejobaUrl('../ajax/dataSource__city.aspx?')

//                if (cityListFromServer.length == 0) {
//                    return $.get(ajxurl, { query: query }, function (data) {
//                        cityListFromServer = JSON.parse(data).options;
//                        return process(cityListFromServer);
//                    });
//                }
//                else {
//                    if (cityListFromServer[0].slice(0, 4).toLowerCase() == query.slice(0, 4).toLowerCase()) {
//                        return cityListFromServer;
//                    }
//                    else {
//                        return $.get(ajxurl, { query: query }, function (data) {
//                            cityListFromServer = JSON.parse(data).options;
//                            return process(cityListFromServer);
//                        });
//                    }
//                }
//            },
//            minLength: 4,
//            items: 5
//        });


        // get the selected location via javascript
        $("#CoPlaBottom_sel_lctn").change(function () {
            var valOfSel = $('#CoPlaBottom_sel_lctn option:selected').val();
            var txtOfSel = $('#CoPlaBottom_sel_lctn option:selected').text();

            // alert("location-ID : " + valOfSel + ' ; placename : ' + txtOfSel);

            $("#CoPlaBottom_txbx_location_id").val(valOfSel);
            $("#CoPlaBottom_txbx_location_name").val(txtOfSel);
        });


        initMap();

        // prepare the matrix
        console.log("Handler for doc.ready() was called !");
        mgr = new MtrxMngr();


        // open review-part after edit was finished
        $("#btn_showPreview").click(function () {
            // alert("click-Handler for #btn_showPreview called.");
            var tmpltTxt = $("#template").html()
            tmpltTxt = tmpltTxt.replace("§§LOCATIONNAME§§", '<strong>Ort: </strong>' + $("#CoPlaBottom_sel_lctn option:selected").text().trim());

            var rubric = $("#CoPlaBottom_txbx_itemname").val().trim();
            var dateFrom = $("#CoPlaBottom_txbx_timeFrom").val().trim();
            var dateTo = $("#CoPlaBottom_txbx_timeTo").val().trim();
            var header = $("#CoPlaBottom_txbHeader").val().trim();
            var docum = tinyMCE.activeEditor.getContent().trim();
            length

            if (rubric.length > 0) { tmpltTxt = tmpltTxt.replace("§§RUBRICNAME§§", '<strong>Rubrik: </strong>' + rubric) }
            else { tmpltTxt = tmpltTxt.replace( "§§RUBRICNAME§§", "" ) };

            if (dateFrom.length > 0) { tmpltTxt = tmpltTxt.replace("§§DATE_FROM§§", '<strong>Start-Termin: </strong>' + dateFrom) }
            else { tmpltTxt = tmpltTxt.replace( "§§DATE_FROM§§", "" ) };

            if (dateTo.length > 0) { tmpltTxt = tmpltTxt.replace("§§DATE_TILL§§", '<strong>End-Termin: </strong>' + dateTo) }
            else { tmpltTxt = tmpltTxt.replace( "§§DATE_TILL§§", "" ) };

            if (header.length > 0) { tmpltTxt = tmpltTxt.replace("§§HEADERTXT§§", '<strong>Kurznachricht: </strong><br/><h2>' + header + '</h2><br /><hr /><br />') }
            else { tmpltTxt = tmpltTxt.replace( "§§HEADERTXT§§", "" ) };

            if (docum.length > 0) { tmpltTxt = tmpltTxt.replace("§§BODYTXT§§", '<strong>Dokument: </strong><br/>' + docum) }
            else { tmpltTxt = tmpltTxt.replace( "§§BODYTXT§§", "" ) };


            $("#messagebox").hide();
            $("#canvas").html(tmpltTxt);
            $("#editpart").hide();
            $("#inspection").show();
        });

        // if user wants to change something in the review this button is clicked
        $("#btn_backToEdit").click(function () {
            // alert("click-Handler for #btn_backToEdit called.");

            $("#canvas").html('');
            $("#inspection").hide();
            $("#editpart").show();
        });
    });
</script>

</asp:Content>

