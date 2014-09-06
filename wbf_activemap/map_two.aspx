<%@ Page Title="nejoba Netzwerk-Karte" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="map_two.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <script src="<%# ResolveUrl("~/style/OpenLayers/lib/OpenLayers.js") %>" type="text/javascript" ></script>
    <script src="<%# ResolveUrl("~/js/neJOBaBrowserBrain.js") %>" type="text/javascript"></script>

    <style type="text/css">
        /* for bootstrap compatibility */
        img.olTileImage {
            max-width: none;
        }
        /* for bootstrap compatibility */

        body {
            margin: 0;
            padding-top: 0px;
            padding-bottom: 10px;
        }
        
        #map 
        {
            position:relative;
            width: 99%;
            height: 735px;
            top:21px;
            left:33px;
            padding: 0.5em 0.5em 0.5em 0.5em;
        }
        
        #butn {
            position: absolute;
            top: 13px;
            left: 53px;
            width: 64px;
            z-index:1000;
            background-color:transparent;
            zoom: 1;
            filter: alpha(opacity=47);
            opacity: 0.47;
        }        
        #butn:hover{
            filter: alpha(opacity=100);
            opacity: 1.0;
        }
        
        #loadingGif {
            position: absolute;
            z-index:1000;
            top:300px;
            left: 50%;
            margin-left: -50px;
        }

    </style>


</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   the main map that shows the world with the eyes of nejoba                                                                         @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <div id="map" class="row span12">
        <span id="loadingGif" style="display:none;">
            <asp:Image ID="Image1" runat="server" ImageUrl="~/style/pic/ajax-loader.gif" />
        </span>

        <div id="butn">
            <div class="btn-toolbar">
                <div class="btn-group">
                    <!-- <a id="back_to_start"    class="btn" href="#"><i class="icon-backward"></i></a> -->
                    <a id="back_in_list"     class="btn" title="" data-placement="bottom" data-toggle="tooltip" data-original-title="Zurück"><i class="icon-step-backward"></i></a>
                    <a id="open_modal"       class="btn" href="#myModal" role="button" data-toggle="modal" title="" data-placement="bottom" data-original-title="Suchen"><i class="icon-search"></i></a>
                    <a id="foreward_in_list" class="btn disabled" role="button" data-toggle="modal"title="" data-placement="bottom" data-toggle="tooltip" data-original-title="Weiter"><i class="icon-step-forward"></i></a>
                    <!-- <a id="foreward_to_end"  class="btn" href="#"><i class="icon-forward"></i></a> -->
                    <a id="divider"          class="btn disabled" role="button" data-toggle="modal" ></a>
                    <a id="open_list"        class="btn" title="" data-placement="bottom" data-toggle="tooltip" data-original-title="Zur Listenansicht"><i class="icon-list"></i></a>
                    <a id="show_bookmark"    class="btn" href="#linkreuse" role="button title="" data-placement="bottom" data-toggle="modal" data-original-title="Link wiederverwenden"><i class="icon-bookmark"></i></a>
                    <a id="show_help"        class="btn" href="#shortdescription" role="button title="" data-placement="bottom" data-toggle="modal" data-original-title="Was ist nejoba?"><i class="icon-question-sign"></i></a>
                </div>
            </div>
        </div>
    </div>


    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   the modal dialog that is used to set the search-parameters                                                                        @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <div id="myModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h4><asp:Label ID="Label7" runat="server" Text="erweiterte Suche " /></h4>
                    
        </div>
        <div class="modal-body">
            <div class="tabbable">
                <ul class="nav nav-tabs">
                    <li class="active"><a href="#tab_Ort" data-toggle="tab">Ort</a></li>
                    <li><a href="#tab_Termin" data-toggle="tab">Termin</a></li>
                    <li><a href="#tab_Thema" data-toggle="tab">Thema</a></li>
                    <li><a href="#tab_Rubrik" data-toggle="tab">Rubrik</a></li>
                </ul>
                <div class="tab-content">
                    <div id="tab_Ort" class="tab-pane active">
                        <h5><asp:Label ID="Label6" runat="server" Text="Ort bestimmen (Postleitzahlgebiet)"></asp:Label></h5>
                        <hr />
                        <div class="span3 offset1">
                            <h5><asp:Label ID="Label21" runat="server" Text="Land" /></h5>
                            <asp:DropDownList ID="sel_country" runat="server" EnableViewState="false">
                                <asp:ListItem Selected="True" Text="bitte wählen....." Value="0" />
                                <asp:ListItem Text="Deutschland" Value="DE" />
                                <asp:ListItem Text="Österreich" Value="AT" />
                                <asp:ListItem Text="Schweiz" Value="CH" />
                                <asp:ListItem Text="Lichtenstein" Value="LI" />
                                <asp:ListItem Text="Belgien" Value="BE" />
                                <asp:ListItem Text="Niederlande" Value="NL" />
                            </asp:DropDownList>
                        </div>
                        <div class="span3 offset1">
                            <h5><asp:Label ID="lblPstCode" runat="server" Text="Postleitzahl" /></h5>
                            <asp:TextBox ID="txbx_postCode" runat="server" EnableViewState="false"/>
                        </div>
                        <br />
                        <div class="span5">
                            <hr />
                            <asp:Label ID="Label14" runat="server" Text="Wenn du nur ein Land angibst werden die neuesten Einträge für das Land angezeigt. Nejoba ist aber für deine Region gedacht.<br /><br />" />
                            <asp:Label ID="Label13" runat="server" Text="Die Daten werden hier nach Postleitzahlgebieten organisiert. Um also alles aus Deiner Stadt anzuzeigen benenne die Postleitzahl Deines Ortes.<br /><br />" />
                            <strong><asp:Label ID="Label15" runat="server" Text="nejoba macht glücklich :-)<br /><br />" /></strong>
                        </div>
                    </div>

                    <div id="tab_Termin" class="tab-pane">
                        <h5><asp:Label ID="Label5" runat="server" Text="Termine"></asp:Label></h5>
                        <hr />
                        <div class="span3 offset1">
                            <h5><asp:Label ID="lbl_date" runat="server" Text="Start-Termin" /></h5>
                            <asp:TextBox ID="txbx_timeFrom" runat="server" EnableViewState="false" ToolTip="Trage hier den Tag der Veranstalltung ein. Wenn die Veranstalltung mehrere Tage dauert ist dies der erste Tag."></asp:TextBox>
                        </div>
                        <div class="span3 offset1">
                            <h5><asp:Label ID="Label22" runat="server" Text="End-Termin" /></h5>
                            <asp:TextBox ID="txbx_timeTo" runat="server" EnableViewState="false" ToolTip="Wenn die Veranstaltung mehrere Tage dauert, wird hier der Schlusstag eingetragen. WICHTIG: Wenn der Termin nicht über mehrere Tage andauert lass dieses Feld leer."></asp:TextBox>
                        </div>
                        <br />
                        <div class="span5">
                            <hr />
                            <asp:Label ID="Label10" runat="server" Text="Ein Beitrag läßt sich in nejoba mit einem Start- und Endtermin verknüpfen.<br /><br />" />
                            <asp:Label ID="Label11" runat="server" Text="Auf diese Weise entsteht eine Datenbank mit der Info wann welche Veranstallungen stattfinden.<br /><br />" />
                            <strong><asp:Label ID="Label12" runat="server" Text="nejoba zeigt Dir was abgeht in deiner Stadt<br /><br />" /></strong>
                        </div>
                    </div>

                    <div id="tab_Thema" class="tab-pane">
                        <h5><asp:Label ID="Label4" runat="server" Text="regionale Themen (Hashtags)"></asp:Label></h5>
                        <hr />
                        <div class="span3 offset1">
                            <h5><asp:Label ID="lbl_hashtag" runat="server" Text="Hashtag" /></h5>
                            <asp:TextBox ID="txbx_hashtag" runat="server" EnableViewState="false" ToolTip="Trage hier den Tag der Veranstalltung ein. Wenn die Veranstalltung mehrere Tage dauert ist dies der erste Tag."></asp:TextBox>
                        </div>
                        <br />
                        <div class="span5">
                            <hr />
                            <asp:Label ID="Label8" runat="server" Text="Regionale Themen sind Hashtags in nejoba. Es werden Stichwörter mit einem '#' markiert. So entsteht eine regionale Themengruppe.<br /><br />" />
                            <asp:Label ID="Label9" runat="server" Text="Der Clou bei nejoba ist das ein Hashtag immer nur auf ein Postleitzahlgebiet beschränkt ist. So bilden sich regionale Themen.<br /><br />" />
                            <strong><asp:Label ID="Label16" runat="server" Text="nejoba hat immer eine Antwort<br /><br />" /></strong>
                        </div>


                    </div>
                    <div id="tab_Rubrik" class="tab-pane">
                        <h5><asp:Label ID="Label1" runat="server" Text="nejoba Rubriken"></asp:Label></h5>
                        <br />
                        <div class="span5">
                            <asp:Label ID="Label_2" runat="server" Text="Die Rubriken funktionieren wie man es von den Kleinanzeigen in Zeitungen kennt. Nejoba bietet unterschiedliche Rubrik-Gruppen für unterschiedliche Themen.<br/><br/>Der Clou an der Sache: Wenn du eine Gruppe auswählst findet nejoba auch alle Untergruppen oder Unterbegriffe, die zu der von dir gewählten Gruppe gehören.<br />" />
                            <asp:Label ID="Label_3" runat="server" Text="Um eine Rubrik auszuwählen drücke den Knopf. Es öffnet sich ein extra Fenster in dem du eine auswählen kannst.<br/><br/>" />
                            <strong><asp:Label ID="Label17" runat="server" Text="nejoba verbindet Menschen<br /><br />" /></strong>
                            <br />
                            <asp:TextBox ID="txbx_itemname" runat="server" EnableViewState="false" ToolTip="Die gewählte Rubrik" Enabled="false" />
                            <asp:Image ID="img_selectRubric" runat="server" class="pull-right" style="cursor: pointer;" ImageUrl="~/style/pic/64_call_forum.png" ToolTip="Beiträge aus Rubriken suchen"  />
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal-footer">
            <button id='deleteSearch' class="btn" type="button" >Löschen</button>
            <button class="btn" data-dismiss="modal" aria-hidden="true" type="button" >Abbrechen</button>
            <button id='startSearch' class="btn btn-primary" type="button" >Suchen</button>
        </div>
    </div>
    <!-- Modal HELP dialog ends here -------------------------------------------------------------------------------------------------------------------- -->




    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   modal dialog that shows the link which can be used external                                                                       @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <div id="linkreuse" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h3 id="myModalLabel">Link zur Wiederverwendung</h3>
        </div>
        <div class="modal-body">
            <p>Der folgende Link dient dazu deine gefilterte Ansicht wiederzuverwenden. Er öffnet also die Karte mit den Suchkriterien die Du jetzt eingestellt hast.</p>
            <br />
            <div></div>
            <p>Am einfachsten klickst Du auf die rechte Maustaste und setzt so ein Lesezeichen. Der Link kann auch dazu benutzt werden in sozialen Neten wie facebook und twitter verwendet zu werden.</p>
        </div>
        <div class="modal-footer">
            <button class="btn" data-dismiss="modal" aria-hidden="true">Fertig</button>
        </div>
    </div>









    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   modal dialog that shows the link which can be used external                                                                       @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <div id="shortdescription" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="linkreuseLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h3 id="H1">Was ist nejoba eigentlich? Kurze Erklärung</h3>
        </div>
        <div class="modal-body">
            <p>Nejoba ist eine Plattform die helfen soll Nachbarschaften über das Internet zu vernetzen.</p>
            <br />
            <div>
                <a id="A1"></a>

            </div>
            <br />
            <br />
            <p>Dabei ist nejoba offen für alle.</p>
        </div>
        <div class="modal-footer">
            <button class="btn" data-dismiss="modal" aria-hidden="true">Fertig</button>
        </div>
    </div>







    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   this is the rubric selector working with javascript                                                                       @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <div id="ruricon" class="row span12" style="display:none;">
        <div class="span12 offset1">
            <br /><br /><br /><br />
            <h4><asp:Label ID="Label19" runat="server" Text="Beiträge in Rubriken suchen" /></h4>
        </div>

        <div class="span11 offset1"><br /><br /><br /></div>

        <div class="span2 offset1">
            <asp:Image ID="img_selectInitiatives" runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_users_initiatives.png" ToolTip="Rubriken: Initiative oder gesellschaftliche Aktion eintragen"  />
            <asp:Label ID="Label2" runat="server" Text="Gemeinschaften" ToolTip="Initiativen oder gesellschaftliche Initiativen von Vereinen und Organisationen"/>
            <br />
            <asp:Image ID="img_selectEvent"       runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_calendar.png"   ToolTip="Rubriken: Art eines Events oder Termins festlegen" ImageAlign="AbsMiddle" />
            <asp:Label ID="Label3" runat="server" Text="Termine" ToolTip="Zum Beispiel Events, Konzerte oder andere Veranstaltungen" />
            <br />
        </div>
        <div class="span2 offset1">
            <asp:Image ID="img_selectLocation"    runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_POI.png"               ToolTip="Diese Rubrik beinhaltet Typen von Orten.  Zum Beispiel Gewerbestandorte, Sehenswürdigkeiten, kulturelle Gebäude oder Aussichtspunkte" />
            <asp:Label ID="lbl_selloc" runat="server" Text="Orte" ToolTip="Diese Rubrik beinhaltet Typen von Orten. Zum Beispiel Gewerbestandorte, Sehenswürdigkeiten, kulturelle Gebäude oder Aussichtspunkte"/>
            <br />
            <asp:Image ID="img_selectBusiness"    runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_branchenbuch.png"      ToolTip="Das nejoba Branchenbuch ist ein regionales Verzeichniss für Firmen und Kleinunternehmer" />
            <asp:Label ID="lbl_selbusiness" runat="server" Text="Branchen" ToolTip="Das nejoba Branchenbuch ist ein regionales Verzeichniss für Firmen und Kleinunternehmer"/>
            <br />
        </div>
        <div class="span2 offset1">
            <asp:Image ID="img_selectAnnonceType" runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_call_list.png"         ToolTip="Rubriken: Eine Anzeige oder allgemeine Veröffentlichung" />
            <asp:Label ID="Label18" runat="server" Text="Anzeigen" ToolTip="Kaufen, verkaufen, Kontaktbörse oder allgemeine Anfragen"/>
            <br />
        </div>
        <div class="span11 offset1"><br /></div>

        <div class="span2 offset1">
            <select id="lsbx_0" multiple="multiple" size="13" style="width:96%;"></select>
        </div>
        <div class="span2">
            <select id="lsbx_1" multiple="multiple" size="13" style="width:96%;"></select>
        </div>
        <div class="span2">
            <select id="lsbx_2" multiple="multiple" size="13" style="width:96%;"></select>
        </div>
        <div class="span2">
            <select id="lsbx_3" multiple="multiple" size="13" style="width:96%;"></select>
        </div>
        <div class="span2">
            <select id="lsbx_4" multiple="multiple" size="13" style="width:96%;"></select>
        </div>
        
        <div class="span11 offset1"><br />
            <input id="btn_select_rubrik" class="btn btn-primary pull-right" type="button" value="Auswählen" />
        </div>
    </div>







    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   hidden area                                                                                                                       @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <div style="visibility:hidden; height:0px;">
        <!-- hidden text that is needed for the error-messages-->
        <asp:Label ID="lbl_error_text" runat="server" Text="error_text !"></asp:Label>

        <!-- the country-code of the user is used by javascript to make the geocoding by noatim -->
        <asp:Label ID="lbl_countrycode" runat="server" Text="de"></asp:Label>

        <!-- the hidden textbox stores the tag for a rubric -->
        <asp:TextBox ID="txbx_tagforitem" runat="server" EnableViewState="false"/>

        <!-- this lable is read by javascript to figure out what display-url will be used -->
        <asp:Label ID="lbl_display_url" runat="server" Text="de"></asp:Label>

        <!-- the div will contain the source-data for the item-type-selection -->
        <div id="date_event_div" runat="server"></div>
        <div id="location_div" runat="server"></div>
        <div id="annonce_div" runat="server"></div>
        <div id="initiative_div" runat="server"></div>
        <div id="business_div" runat="server"></div>

    </div>

    <script type="text/javascript">
        // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        // start webform js stuff
        // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        $(document).ready(function () {

            // datepicker from jquery_ui
            $("#CoPlaBottom_txbx_timeFrom").datepicker($.datepicker.regional["de"]);
            $("#CoPlaBottom_txbx_timeTo").datepicker($.datepicker.regional["de"]);

            // click function for select-rubric
            $('#CoPlaBottom_img_selectRubric').click(function () {
                $('#myModal').modal('hide');
                $('#map').hide(500);
                $('#ruricon').show(500);
            });

            // click function for rubric is selected
            $('#btn_select_rubrik').click(function () {
                $('#ruricon').hide(500);
                $('#map').show(500);
                $('#myModal').modal('show');
            });

            // click function for start display with the map-projector
            $('#startSearch').click(function () {
                $('#myModal').modal('hide');
                // start the marker-positioning
                console.log('start customized search');
                lstExtr.loadInitial();
                lstExtr.clientPageSend();
            });

            // click function for deleting all setings in the modal search-parameter-dialog
            $('#deleteSearch').click(function () {
                lstExtr.clearSearchDialog();
                return false;
            });

            var displayUrl = $('#CoPlaBottom_lbl_display_url').text();      // define the url that will be used to dispaly the details in javascript
            projector = new MapProjector(displayUrl);                       // the map-projector handles the map via openlayers
            // lstExtr = new ListExtractor('map', 3000, 300);               // list-extractor manages the AJAX-load of data. initialie it loads some stuff from the server
            lstExtr = new ListExtractor('map', 2500, 5 );                   // list-extractor manages the AJAX-load of data. initialie it loads some stuff from the server
            mtrx = new MtrxMngr();                                          // manager for the item-typ-selector

            // handle "open List" clicked
            $('.btn').tooltip();
            $('#open_list').click(function () {
                lstExtr.getUrlParams();
                var param = lstExtr.prepareUrl();
                // alert(param);
                var url = '../wbf_functs/debate_projector.aspx' + param;
                var win = window.open(url, '_blank');
                win.focus();
            });

        });

    </script>
</asp:Content>


