<%@ Page Title="nejoba - Ort festlegen" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="Default.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <style type="text/css">
        body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background-color:transparent;
            /*
            background-image: url(./style/pic/maindefaultwallpaper3.jpg);
            */
        }
    </style>
    <script src="<%# ResolveUrl("~/js/MatrixManager.js") %>" type="text/javascript"></script>
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div id="dsplydiv_mainUnHide">

        <div class="row"><br /></div>

        <div class="row">
            <div class="accordion" id="Div1">
                <div class="accordion-group">
                    <div class="accordion-heading">
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >
                            <h4>Was ist nejoba ?</h4>
                        </a>
                    </div>
                    <div id="collapseHeader" class="accordion-body collapse">
                        <div class="accordion-inner">
                            

<br />
<strong>nejoba ist die Plattform für regionale Informationen. Microblogging für eine Stadt. Jedes Postleitzahlgebiet hat hier einen eigenen Blog. Dieser Stadt-Blog wird von allen Nachbarn geteilt.
<br /><br />
Das Ergebnis ist eine neue Form regionaler Vernetzung.
<br /><br />
<iframe width="480" height="360" src="//www.youtube.com/embed/42sYJAE6VbI?rel=0" frameborder="0" allowfullscreen></iframe>
<br /><br />
Geschäftsleute können auf Angebote hinweisen, Musiker können Konzerttermine veröffentlichen, Nachbarn kommunizieren zu regionalen Themen oder es bilden sich Gemeinschaften über Interessen.
<br /><br />
nejoba bietet mehrere Funktionen zur kommunalen Kommunikation</strong>
<br />
<br />
<br />
<strong>1. Eine Job-Börse</strong>
<br />
Auf nejoba kann man seine Nachbarn um Hilfe bitten. Jeder der Hilfe gebrauchen kann macht auf nejoba eine Jobausschreibung. So finden sich regional Leute zusammen die einander helfen können.
<br />
<br />
<strong>2. Regionale Hashtags</strong>
<br />
Beiträge lassen sich bestimmten Suchbegriffen zuordnen. Die Besonderheit auf nejoba: Solche Hashtags gelten regional. Man findet so alles zu einem Thema in einer bestimmten Region. 
<br />
Die regionalen Hashtags vernetzen Menschen einer Stadt über ihre Interessen.
<br />
<br />
<strong>3. Vordefinierte Rubriken</strong>
<br />
Vergleichbar zu den Bereichen bei Kleinanzeigen bietet nejoba über seine Rubriken vordefinierte Themen an. So lassen sich Kleinanzeigen schalten, Kontakte knüpfen oder Initiativen gründen.
<br />
<br />
<strong>4. Termine </strong>
<br />
Die Beiträge im Forum können mit einem Datum verknüpft werden. So lassen sich Termine einer Region auf nejoba veröffentlichen. Messen, Konzerte, Feste oder andere Veranstaltungen. Mit nejoba haben die Anwohner immer im Blick was in der Stadt abgeht.
<br />
<br />
<strong>5. Eine interaktive Karte</strong>
<br />
Beiträge im Forum lassen sich auf einer Karte markieren. Auf diese Weise können Veranstalltungsorte in Verbindung mit einem Datum eingetragen werden. Auf nejoba sieht man dann mit einem Blick was an einem bestimmten Tag wo in der eigenen Stadt los ist.
<br />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="span12">
                <div class="span1"></div>
                <div class=" span10" style="background-color:White;">
                    <asp:Image ID="Image1" runat="server" ImageUrl="~/style/pic/mainhead_pict_nejoba.jpg" ImageAlign="Middle" />
                </div>
                <div class="span1"></div>
            </div>
        </div>



        <div class="row">
            <div class="accordion" id="Div2">
                <div class="accordion-group">
                    <div class="accordion-heading">
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHowTo" >
                            <h4>Ort festlegen</h4>
                        </a>
                    </div>
                    <div id="collapseHowTo" class="accordion-body collapse">
                        <div class="accordion-inner">
                            
<h5>Ort festlegen</h5>
<br />
Die Beiträge auf nejoba beziehen sich immer auf ein Postleitzahlgebiet. Unten kannst du festlegen welchen Ort du angezeigt bekommen möchtest. Diese Auswahl ist dann in allen Funktionen von nejoba gültig.
<br /><br />
Wenn du für Land die Einstellung ‘alle vorhandenen’ nutzt werden die Beiträge unabhängig vom Ort angezeigt. Du kannst aber auch nach einem bestimmten Land filtern. Lasse dann einfach das Feld für die Stadt bzw. Postleitzahl leer.
<br /><br />
Wenn du einen bestimmten Ort angezeigt bekommen möchtest muss du das dazu gehörende Land auswählen und den Namen der Stadt oder die Postleitzahl eingeben.
<br /><br />
nejoba zeigt auch immer die benachbarten Postleitzahlgebiete an. So findest du auch Beiträge aus deiner näheren Umgebung.
<br /><br />
<h5>
Dein Leben spielt sich vor deiner Haustüre ab. nejoba verbindet dich mit deinen Nachbarn <br /><br />
</h5>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row"><br /></div>

        <div class="row">
            <div class="span12 well">
                <div id ="location_choose" >
                    <div class="">
                        <div class="span3"></div>
                        <div class="span6">
                            <br />
                            <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                            <div class="row">
                                <div class="span6">
                                    <h5>
                                        <asp:Label ID="Label1" runat="server" Text="Land:"></asp:Label>
                                    </h5>
                                </div>
                                <div class="span6">
                                    <asp:DropDownList ID="sel_country" runat="server"  ToolTip="Liste der derzeit verfügbaren Länder. Es muss natürlich zu Stadt oder Postleitzahl passen." />
                                </div>
                                <div id="nocountryselected" class="alert alert-danger" style="display:none;">
                                    <strong><asp:Label ID="lbl_missing_country_selection" runat="server" Text="Fehler : Es wurde kein Land ausgewählt!! Die Stadt/PLZ muss im jeweiligen Land liegen !!"></asp:Label></strong>
                                </div>
                            </div>
                            <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                            <div class="row">
                                <div class="span6">
                                    <h5>
                                        <asp:Label ID="Label7" runat="server" Text="Stadt oder Postleitzahl:"></asp:Label>
                                    </h5>
                                </div>
                                <div class="span6">
                                    <asp:TextBox ID="txbx_city" class="typeahead" runat="server" EnableViewState="false" autocomplete="off" ToolTip="Gib hier den Namen der gesuchten Stadt ein. Denk bitte daran das passende Land auszuwählen."/>
                                </div>
                            </div>
                            <br /><br />


                            <div class="row">
                            </div>
                            <br /><br />


                        </div>
                        <div class="span3"></div>
                    </div>
                </div>
                <div class="row">
                </div>
            </div>

            <!-- ##################################################################################################################################### -->

            <div class="spam12 well">
            
                <div class="span5">
                    <h5><asp:Label ID="Label4" runat="server" Text="Das Micro-Blog"></asp:Label></h5>

                    <asp:LinkButton ID="hyLnk_openBlgLst" runat="server" class="btn btn-large btn-primary" style="width:100%;" data-toggle="tooltip" title="Die Listenansicht des regionalen Micro-Blogs" OnClick="HandlBtnClick" OnClientClick="return checkForCountry();"><i class="icon-list icon-black"></i> Liste des Forums</asp:LinkButton>
                    <br /><br />
                    <asp:LinkButton ID="hyLnk_openMap" runat="server" class="btn btn-large btn-primary" style="width:100%;" data-toggle="tooltip" title="Die Kartenansicht des regionalen Micro-Blogs" OnClick="HandlBtnClick" OnClientClick="return checkForCountry();"><i class="icon-globe icon-black"></i> Kartensicht</asp:LinkButton>
                    <br /><br />
                    <asp:LinkButton ID="hyLnk_openBlog" runat="server" class="btn btn-large btn-primary" style="width:100%;" data-toggle="tooltip" title="Regionaler Micro-Blog : Funktionen" OnClick="HandlBtnClick" OnClientClick="return checkForCountry();"><i class="icon-bullhorn icon-black"></i> Nachbarforum</asp:LinkButton>
                    <br /><br />
                </div>
            
                <div class="span5 offset1">
                    <h5><asp:Label ID="Label2" runat="server" Text="Der regionale Arbeitsmarkt"></asp:Label></h5>

                    <asp:LinkButton ID="hyLnk_listOfJobs" runat="server" class="btn btn-large btn-success" style="width:100%;" data-toggle="tooltip" title="Arbeitsangebote als Liste anzeigen" OnClick="HandlBtnClick" OnClientClick="return checkForCountry();"><i class="icon-list icon-black"></i> Liste der Arbeit</asp:LinkButton>
                    <br /><br />
                    <asp:LinkButton ID="hyLnk_openJobs" runat="server" class="btn btn-large btn-success" style="width:100%;" data-toggle="tooltip" title="Funktionen zur Nachbarhilfe" OnClick="HandlBtnClick" OnClientClick="return checkForCountry();"><i class="icon-briefcase icon-black"></i> Nachbarhilfe</asp:LinkButton>
                    <br /><br />
                    
                </div>
            </div>
        </div>


    </div>

    <!-- do not delete dummies needed from server-processing -->
    <div id="div_slct_loctn" runat="server"></div>
    <div id="div_show_loctn" runat="server"></div>

    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->

    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   modal dialog that shows the link which can be used external                                                                       @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <div id="shortdescription" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="linkreuseLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h4>Wie geht Nachbarschaft im Internet?</h4>
        </div>
        <div class="modal-body">
        <strong>
            <iframe width="420" height="315" src="//www.youtube.com/embed/rc5B737Q6LE?rel=0" frameborder="0" allowfullscreen></iframe>
            <p>
            Wie wäre eine öffentliche Pinnwand deiner Stadt? Ein schwarzes Brett für deinen Heimatort? Fragen stellen, Angebote machen und Informationen weitergeben. Von jedem für jeden?
            </p>
            <br />
            <p>
            Willkommen bei nejoba, dem neuen Info-Punkt für deine Stadt im Netz. 
            </p>
        </strong>
        <ul>
            <li>Veröffentliche Texte, Bilder und Videos</li>
            <li>Markiere interessante Orte auf der Karte</li>
            <li>Lege Termine für Veranstaltungen fest</li>
            <li>Gruppiere Themen mit Hashtags</li>
            <li>Verlinke auf Webseiten aus deiner Region</li>
        </ul>
        <br />
        <h5>Wofür kann man das gebrauchen?</h5>

        <p>Einige Beispiele:</p>

        <p><strong>Du brauchst jemanden der dir beim Umzug hilft? </strong><br/>Frag doch erstmal deine Nachbarn.</p>
        <p><strong>Du willst auf eine Veranstaltung hinweisen? </strong><br/>Lege einen Termin fest und markiere den Veranstaltungsort auf der Karte.</p>
        <p><strong>Du möchtest über das letzte Fußballspiel der Regionalliga berichten? </strong><br/>Veröffentliche ein Fotoalbum im regionalen Forum.</p>
        <p><strong>Du möchtest deine Firma vorstellen oder Sonderangebote anbieten? </strong><br/>Die Plattform ist auch für kommerzielle Nutzung offen.</p>
        <p><strong>Möchtest Du eine Initiative organisieren? </strong><br/>Nutze die regionalen Hashtags und informiere über Treffen und Aktionen.</p>
        <p><strong>Du suchst Alltagshilfen für deine Großeltern? </strong><br/>Suche nach Pflegekräften aus deiner Region.</p>
        <p><strong>Deine Katze ist weggelaufen? </strong><br/>Veröffentliche eine Suchanzeige mit ihrem Foto und deiner Handy-Nummer.</p>
        <p><strong>Du suchst Zeugen für einen Unfall? </strong><br/>Markiere den Unfallort und beschreibe was passiert ist.</p>
        <p><strong>Du willst ein Straßenfest organisieren? </strong><br/>Informiere die Anwohner über das Forum.</p>
        <p><strong>Willst du eine Fahrgemeinschaft gründen? </strong><br/>Zeige auf der Karte wohin es gehen soll und suche nach Leuten mit dem gleichen Ziel.</p>
        <br />
        <p>was auch immer.........nejoba nützt.</p>
        <br /><br />
        <strong>
            Nachbarn vernetzen sich. Wir machen das Internet regional. 
            <br />
            Mit nejoba entsteht die Nachbarschaft 2.0. 
        </strong>
        <p></p>
        <br /><br />
        <asp:HyperLink ID="HyperLink1" runat="server" NavigateUrl="wbf_help/help_debates.aspx" Target="_blank">Zur Bedienungsanleitung</asp:HyperLink>
        <br /><br />
        <asp:HyperLink ID="HyperLink_YouTube" runat="server" NavigateUrl="http://www.youtube.com/user/nejobavideo" Target="_blank">Videos zum Thema nejoba auf YouTube</asp:HyperLink>
        <br /><br />
        <asp:HyperLink ID="HyperLink_facebook" runat="server" NavigateUrl="https://www.facebook.com/nejoba" Target="_blank">Unser Benutzerforum auf facebook.</asp:HyperLink>
        </div>
        
        <div class="modal-footer">
            <button class="btn btn-success" data-dismiss="modal" aria-hidden="true">Fertig</button>
        </div>
    </div>

    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->


    <div style="display:none;">
        <asp:Label ID="timeIsNow" runat="server" ></asp:Label> 
        <asp:TextBox ID="txbx_selected_function" runat="server"></asp:TextBox>

        <!-- the hidden textbox stores the tag for a rubric -->
        <asp:TextBox ID="txbx_tagforitem" runat="server" />

        <!-- the hidden textboxes stores the name id of the hometown of user -->
        <asp:TextBox ID="txbx_location_id" runat="server" />
        <asp:TextBox ID="txbx_location_name" runat="server" />

        <asp:TextBox ID="txbx_location" runat="server" />


        <!-- the div will contain the source-data for the item-type-selection -->
        <div id="date_event_div" runat="server"></div>
        <div id="location_div" runat="server"></div>
        <div id="annonce_div" runat="server"></div>
        <div id="initiative_div" runat="server"></div>
        <div id="business_div" runat="server"></div>
    </div>

    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->


<script type="text/javascript">

    $(document).ready(function () {

        $("#btn_select_rubrcfinished").click(function (event) {
            $("#dsplydiv_selectrubric").hide();
            $("#dsplydiv_location").show();
            $("#dsplydiv_read_or_create").show();
        });

        //
        // handler for the buttons opening the next-div after location-select
        //
        $("a[id*='dspNxtOptn_']").click(function (event) {
            var slctVl = $("#CoPlaBottom_sel_country").val();
            var city = $("#CoPlaBottom_txbx_city").val().trim();

            if ((city.length > 0) && (slctVl == '0')) {
                // alert('also SO geht das nicht !');
                $('#nocountryselected').show();
                $('#callfiltered').hide();
                $('#callunfiltered').hide();
                return;
            }

            $('#nocountryselected').hide();

            if (this.id == "dspNxtOptn_filtered") {
                $('#callfiltered').show();
                $('#callunfiltered').hide();
            }
            else {
                $('#callunfiltered').show();
                $('#callfiltered').hide();
            }
        });

        // --------------------------------------------------------------------------------------------------------------------------------------
        // -- 
        // -- add the click-event-handler for the selects 
        // -- 
        // --------------------------------------------------------------------------------------------------------------------------------------
        $("select[id*='lsbx_']").click(function (event) { matrix.handleSelection(event); });
    });
</script>



</asp:Content>
