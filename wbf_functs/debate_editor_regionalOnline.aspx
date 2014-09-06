<%@ Page Title="" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="debate_editor_regionalOnline.aspx.py" validateRequest="false"%>

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


<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
<div class="container span10">
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

        <div class="span2 offset1">
            <br /><br />
            <asp:Button ID="btn_Save" runat="server" class="btn btn-large btn-primary pull-right" Text="Beitrag ver&ouml;ffentlichen" onclick="HndlrButtonClick"/>
        </div>
    </div>


    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <!-- # #   EDIT area. cuurently using tinyMCE                                                                                                                                                                          # # # -->
    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div class="row-fluid well span10">
        <div id="area_edit" class="span11 offset1">
            <h4>
                <asp:Label ID="lbl_hint" runat="server" Text="Dein Dokument" ToolTip="Das Dokument ist mit der Kurzmeldung verknüpft. Es ist nicht zwingend erforderlich."></asp:Label>
                <a id="shwHelp2" class="btn" href="#guidance2" role="button" title="Wie schreibt man etwas ins Forum?" data-placement="bottom" data-toggle="modal" data-original-title="Wie schreibt man etwas ins Forum?"><i class="icon-info-sign"></i></a>
            </h4>
            <asp:TextBox runat="server" ID="txtMain" TextMode="MultiLine" Rows="27" style="width:92%"></asp:TextBox>
        </div>
    </div>

    <div id="div1" class="row-fluid well span10 minimize">
        <div class="accordion" id="accordion2">
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <!-- # #   additional attributes select a start- and end-date                                                                                                                                                          # # # -->
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="accordion-group">
                <div class="accordion-heading">
                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseOne">
                    <h4><asp:Label ID="Label4" runat="server" Text="Einen Termin festlegen" ToolTip="Dein Beitrag kann mit einer Zeitangabe verknüpft werden. Sinnvoll ist das beispielsweise für Veranstaltungen. Auf nejoba kann ein Nutzer die Suche auf einen bestimmten Tag beschränken. Dann werden ihm nur Beiträge angezeigt, die mit einem passenden Termin verknüpft sind." /></h4>
                </a>
                </div>
                <div id="collapseOne" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <div class="span11 offset1"></div>
                        <div class="span3 offset1">
                            <label><asp:Label ID="lbl_date" runat="server" Text="Start-Termin" /></label>
                            <asp:TextBox ID="txbx_timeFrom" runat="server" ToolTip="Trage hier den Tag der Veranstalltung ein. Wenn die Veranstalltung mehrere Tage dauert ist dies der erste Tag."></asp:TextBox>
                        </div>
                        <div class="span3 offset1">
                            <label><asp:Label ID="Label6" runat="server" Text="End-Termin" /></label>
                            <asp:TextBox ID="txbx_timeTo" runat="server" ToolTip="Wenn die Veranstaltung mehrere Tage dauert, wird hier der Schlusstag eingetragen. WICHTIG: Wenn der Termin nicht über mehrere Tage andauert lass dieses Feld leer."></asp:TextBox>
                        </div>
                        <div class="span11 offset1"></div>
                    </div>
                </div>
            </div>


            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <!-- # #   define rubric of announcment                                                                                                                                                                                # # # -->
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="accordion-group">
                <div class="accordion-heading">
                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseTwo">
                    <h4><asp:Label ID="Label8" runat="server" Text="Einer Rubrik zuordnen" ToolTip="Dein Beitrag in einer der nejoba-Rubriken eingliedern." /></h4>
                </a>
                </div>
                <div id="collapseTwo" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <div class="span12"></div>
                        <div class="span3 offset1">
                            <asp:Image ID="img_selectInitiatives" runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_users_initiatives.png" ToolTip="Rubriken: Initiative oder gesellschaftliche Aktion eintragen"  />
                            <asp:Label ID="Label9" runat="server" Text="Initiativen" ToolTip="Initiativen oder gesellschaftliche Initiativen von Vereinen und Organisationen"/>
                            <br />
                            <asp:Image ID="img_selectEvent"       runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_calendar.png"   ToolTip="Rubriken: Art eines Events oder Termins festlegen" ImageAlign="AbsMiddle" />
                            <asp:Label ID="Label7" runat="server" Text="Termine" ToolTip="Zum Beispiel Events, Konzerte oder andere Veranstaltungen" />
                            <br />
                        </div>
                        <div class="span3">
                            <asp:Image ID="img_selectLocation"    runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_POI.png"               ToolTip="Diese Rubrik beinhaltet Typen von Orten.  Zum Beispiel Gewerbestandorte, Sehenswürdigkeiten, kulturelle Gebäude oder Aussichtspunkte" />
                            <asp:Label ID="lbl_selloc" runat="server" Text="Orte" ToolTip="Diese Rubrik beinhaltet Typen von Orten. Zum Beispiel Gewerbestandorte, Sehenswürdigkeiten, kulturelle Gebäude oder Aussichtspunkte"/>
                            <br />
                            <asp:Image ID="img_selectBusiness"    runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_branchenbuch.png"      ToolTip="Das nejoba Branchenbuch ist ein regionales Verzeichniss für Firmen und Kleinunternehmer" />
                            <asp:Label ID="lbl_selbusiness" runat="server" Text="Branchen" ToolTip="Das nejoba Branchenbuch ist ein regionales Verzeichniss für Firmen und Kleinunternehmer"/>
                            <br />
                        </div>
                        <div class="span3">
                            <asp:Image ID="img_selectAnnonceType" runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_call_list.png"         ToolTip="Rubriken: Eine Anzeige oder allgemeine Veröffentlichung" />
                            <asp:Label ID="Label11" runat="server" Text="Anzeigen" ToolTip="Kaufen, verkaufen, Kontaktbörse oder allgemeine Anfragen"/>
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
                        <div class="span2 offset1">
                            <br />
                            <asp:TextBox ID="txbx_itemname" runat="server" ToolTip="Name of Item" Enabled="false" />
                        </div>
                        <div class="span11 offset1"></div>
                    </div>
                </div>
            </div>


            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <!-- # #   map for setting the location                                                                                                                                                                                 # # # -->
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="accordion-group">
                <div class="accordion-heading">
                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseThree">
                    <h4><asp:Label ID="Label10" runat="server" Text="Markierung für die Karte hinzufügen" ToolTip="Bestimme einen Ort auf der Karte. nejoba markiert diesen Beitrag an dieser Stelle." /></h4>
                </a>
                </div>
                <div id="collapseThree" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <div class="span11 offset1"></div>
                        <div class="span2 offset1">
                            <label><asp:Label ID="lbl_city" runat="server" Text="Ort" /></label>
                            <asp:DropDownList ID="sel_lctn" runat="server" EnableViewState="True" />
                            <label><asp:Label ID="lbl_street" runat="server" Text="Straße" /></label>
                            <asp:TextBox ID="txbx_street" runat="server" ToolTip="Bitte nur den Namen der Strasse eingeben. Hausnummer weglassen!"></asp:TextBox>
                            <asp:Image ID="img_findLocation"       runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_search_loc.png"          ToolTip="Karte anhand der Adressdaten zentrieren." />
                            <br />
                            <asp:HyperLink ID="hyli_mapcoordinates" runat="server" Text="GoogleMaps nutzen" NavigateUrl="http://www.mapcoordinates.net/" Target="_blank" ToolTip="Breiten- und Längengrad per 'Cut and Paste' in die Textfelder" />
                            <br /><br /><br />

                            <label><asp:Label ID="lbl_lat" runat="server" Text="Breitengrad" /></label>
                            <asp:TextBox ID="txbx_lat" runat="server" ToolTip="Wenn das Feld leer bleibt wird die Markierung zufällig im Postleitzahlgebiet gesetzt. Wenn du die Koordinaten kennst targe diese ein. Beachte das ein PUNKT (.) anstatt einem Komma als dezimales Trennzeichen benutzt werden muss"></asp:TextBox>
                            <label><asp:Label ID="lbl_lon" runat="server" Text="Längengrad" /></label>
                            <asp:TextBox ID="txbx_lon" runat="server" ToolTip="Wenn das Feld leer bleibt wird die Markierung zufällig im Postleitzahlgebiet gesetzt. Wenn du die Koordinaten kennst targe diese ein. Beachte das ein PUNKT (.) anstatt einem Komma als dezimales Trennzeichen benutzt werden muss"></asp:TextBox>
                            <asp:Image ID="img_centerMap" runat="server" style="cursor: pointer;" ImageUrl="~/style/pic/64_search_loc.png" ToolTip="Karte neu zentrieren." />
                            <br />
                            <label><asp:Label ID="lbl_centerMapAgain" runat="server" Text="Karte neu zentrieren." ToolTip="Die Mitte der Karte wird anhand der Koordinaten gesetzt." /></label>
                        </div>
                        <div class="span7 offset1">
                            <div id="map" style="height:500px; width:100%;"></div>                
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>






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
        <asp:Label ID="lbl_countrycode" runat="server" Text=""></asp:Label>

        <!-- the hidden textbox stores the tag for a rubric -->
        <asp:TextBox ID="txbx_tagforitem" runat="server" />

        <!-- the div will contain the source-data for the item-type-selection -->
        <div id="date_event_div" runat="server"></div>
        <div id="location_div" runat="server"></div>
        <div id="annonce_div" runat="server"></div>
        <div id="initiative_div" runat="server"></div>
        <div id="business_div" runat="server"></div>

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
        $("#CoPlaBottom_txbx_timeTo"  ).datepicker($.datepicker.regional["de"]);
        
        tinymce.init({
            selector: "textarea",
            plugins: [
                "advlist autolink lists link image charmap print preview anchor",
                "searchreplace visualblocks code fullscreen",
                "insertdatetime media table contextmenu paste "
            ],
            toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image",
            language : 'de'
        });


//        tinyMCE.init({
//            // General options
//            mode: "textareas",
//            theme: "advanced",
//            plugins: "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",

//            // Theme options
//            theme_advanced_buttons1: "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,formatselect,fontselect,fontsizeselect,|,print,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo",
//            theme_advanced_buttons2: "link,unlink,anchor,image,cleanup,help,|,charmap,emotions,iespell,media,advhr,|,insertdate,inserttime,preview,|,forecolor,backcolor,|,tablecontrols",
//            theme_advanced_toolbar_location: "top",
//            theme_advanced_toolbar_align: "left",
//            theme_advanced_statusbar_location: "bottom",
//            theme_advanced_resizing: true,

//            // Skin options
//            skin: "o2k7",
//            skin_variant: "silver",

//            // Example content CSS (should be your site CSS)
//            content_css: ResolveUrl("http://ajax.aspnetcdn.com/ajax/bootstrap/2.3.2/css/bootstrap.min.css"),

//            // Drop lists for link/image/media/template dialogs
//            template_external_list_url: "js/template_list.js",
//            language : 'de_DE',
//        });

        initMap();

        // prepare the matrix
        console.log("Handler for doc.ready() was called !");
        mgr = new MtrxMngr();
    });


</script>
</asp:Content>

