<%@ Page Title="Starseite nejoba" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="Search_Rubric.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <style type="text/css">
        body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background-color:transparent;
        }
    </style>
    <script src="<%# ResolveUrl("~/js/MatrixManager.js") %>" type="text/javascript"></script>
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <div class="row"><br /></div>

    <div class="row">
        <div class="accordion" id="Div1">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <h4>
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >
                            Rubrik aussuchen
                        </a>
                    </h4>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
<strong>
Suche nach Rubriken ermöglicht es Beiträge zu finden die einer bestimmten Rubrik zugeordnet wurden. Unter “Rubrik wählen” gibt es drei Themenschwerpunkte : “Wirtschaft”, “Freizeit” und “Gesellschaft”. Diese sind untergliedert in verschiedenen Hauptrubriken. Wenn eine Hauptrubrik angeklickt wird öffnet nejoba eine Bereich um Untzerrubriken auszuwählen. Dabei gilt immer der zuletzt angeklickte Punkt. Wenn du einen übergeordnete Rubrik auswählst werden von nejoba auch alle Unterrubriken angezeigt, die zu diesem Punkt gehören.
<br /><br />
Unten findest du wie gewohnt den Button “Ort wechseln” um nach Region oder Stadt zu filtern. Es ist möglich Ortsunabhängig zu suchen (“Land: Alle vorhandenen”), Einträge eines Landes anzeigen zu lassen oder in der Umgebung einer Stadt zu suchen.
<br /><br />
Darunter kannst du mit dem Button “Liste” die Liste aller passenden Einträge anzeigen lassen. Mit “Karte” zeigt nejoba die alle passenden Einträge für die eine geographische Markierung festgelegt wurde.
<br /><br />
</strong>
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
    <div class="row"><br /></div>

    <div class="row">
        <div class="accordion" id="accordion_useraction">
            <div class="accordion-group">
                <!-- $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ -->
                <div class="accordion-heading">
                    <h4><a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion_useraction" href="#collapseSelctRubric" >Rubrik wählen</a></h4>
                </div>
                <div id="collapseSelctRubric" class="accordion-body collapse in">
                    <div class="accordion-inner">
                        <div id="dsplydiv_rubric">
                            <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                            <h4>
                                <ul class="nav nav-tabs" id="rubricTabs">
                                    <li class="active"><a href="#economy" data-toggle="tab">Wirtschaft</a></li>
                                    <li><a href="#leisure" data-toggle="tab">Freizeit</a></li>
                                    <li><a href="#society" data-toggle="tab">Gesellschaft</a></li>
                                </ul>
                            </h4>
                            <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                            <div class="tab-content">
                                <div class="tab-pane active" id="economy">
                                    <div class="row" >
                                        <div class="span1"></div>
                                        <div class="span10 well label-important" style="color:White;height:150px;">
                                            <h4>
                                                <asp:Label ID="Label23" runat="server" Text="Wirtschaft"></asp:Label>
                                            </h4>
                                            <p>
                                                <asp:Label ID="Label24" runat="server" Text="Informiere dich regional über Unternehmen, finde einen Job über die Job-Börse oder durchstöbere die Kleinanzeigen."></asp:Label>
                                                <br />
                                                <asp:Label ID="Label25" runat="server" Text="Die folgenden Rubriken stehe auf nejoba zur Verfügung. Du kannst dich informieren oder selbst einen Beitrag hinzufügen. Wähle was dich interessiert."></asp:Label>
                                                <br />
                                            </p>
                                        </div>
                                        <div class="span1"></div>
                                    </div>
                                    <div class="row">
                                        <div class="span1"></div>
                                        <div class="span10">
                                            <div id ="div_business" class="span4 well label-important" style="color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_BUSINESS" runat="server" Text="Branchenbuch" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label26" runat="server" Text="Eine Sammlung von Unternehmen in deiner Stadt....... "></asp:Label>
                                                </p>
                                            </div>
                                            <div id ="div_annonce" class="span4 well label-important" style="color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_ANNONCE" runat="server" Text="Kleinanzeigen" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label28" runat="server" Text="Verkaufen oder kaufen. Der regionale private Marktplatz"></asp:Label>
                                                </p>
                                            </div>
                                            <div id ="div_shareconomeny" class="span4 well label-important" style="color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_SWAP" runat="server" Text="Tauschen und Schenken" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label2" runat="server" Text="Die regionale Tausch- und Schenkbörse. Wirtschaft ohne Geld."></asp:Label>
                                                </p>
                                            </div>
                                        </div>
                                        <div class="span1"></div>
                                    </div>
                                    <div class="row">
                                        <div class="span1"></div>
                                        <div class="span10">
                                            <div id ="div_startup" class="span4 well label-important" style="color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_STARTUP" runat="server" Text="Gründungen und Neueröffnungen" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label3" runat="server" Text="Neue Unternehmen stellen sich vor"></asp:Label>
                                                </p>
                                            </div>
                                            <div id ="div_jobmarket" class="span4 well label-important" style="color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hylnk_jobmarket" runat="server" Text="Job-Börse" NavigateUrl="~/wbf_functs/jobs_search.aspx" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label30" runat="server" Text="Die Börse für Job-Börse. Job ausschreiben oder finden von Jobangeboten"></asp:Label>
                                                </p>
                                            </div>
                                            <div class="span12"><br /><br /></div>
                                        </div>
                                        <div class="span1"></div>
                                    </div>
                                </div>
                                <!-- %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 -->
                                <div class="tab-pane" id="leisure">
                                    <div class="row" >
                                        <div class="span1"></div>
                                        <div class="span10 well label-warning" style="color:White;height:150px;">
                                            <h4>
                                                <asp:Label ID="Label27" runat="server" Text="Freizeit"></asp:Label>
                                            </h4>
                                            <p>
                                                <asp:Label ID="Label29" runat="server" Text="Freizeitangebote in deiner Region. Veranstalltungskalender für Konzerte und belibiege andere kulturelle Events."></asp:Label>
                                                <br />
                                                <asp:Label ID="Label31" runat="server" Text="Eine Informationsbörse für Hobbies und Haustierhalter"></asp:Label>
                                                <br />
                                            </p>
                                        </div>
                                        <div class="span1"></div>
                                    </div>
                                    <div class="row">
                                        <div class="span1"></div>
                                        <div class="span10">
                                            <div id ="div_events" class="span4 well label-warning" style="color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_EVENT" runat="server" Text="Veranstaltungskalender" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label33" runat="server" Text="Veranstalltungen: Konzerte, Feste, Aufführungen....."></asp:Label>
                                                </p>
                                            </div>
                                            <div id ="div_poi" class="span4 well label-warning" style="cursor:pointer; color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_LOCATION" runat="server" Text="interessante Orte" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label35" runat="server" Text="Nennenswerte Orte, Treffpunkte, Dienststellen, Bankautomaten......"></asp:Label>
                                                </p>
                                            </div>
                                            <div id ="div_pets" class="span4 well label-warning" style="cursor:pointer; color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_PET" runat="server" Text="Haustiere" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label36" runat="server" Text="Alles zum Thema Haustiere. Entlaufen, zugelaufen, Tipps und Hilfen für Tierhalter"></asp:Label>
                                                </p>
                                            </div>
                                        </div>
                                        <div class="span1"></div>
                                    </div>
                                    <div class="row">
                                        <div class="span1"></div>
                                        <div class="span10">
                                            <div id ="div_hobbies" class="span4 well label-warning" style="cursor:pointer;color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_HOBBY" runat="server" Text="Hobbys" style="text-decoration:underline;color:White;"/>
                                                </h4>
                                                <asp:Label ID="Label37" runat="server" Text="Angebote zur Beschäftigung in der freien Zeit."></asp:Label>
                                            </div>
                                            <div class="span12"><br /><br /></div>
                                        </div>
                                        <div class="span1"></div>
                                    </div>
                                </div>
                                <!-- %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 -->
                                <div class="tab-pane" id="society">
                                    <div class="row" >
                                        <div class="span1"></div>
                                            <div class="span10 well label-success" style="color:White;height:150px;">
                                                <h4>
                                                    <asp:Label ID="Label32" runat="server" Text="Gesellschaft"></asp:Label>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label34" runat="server" Text="Seine Umgebung mitgestalten und aktiv werden. Mitwirkung an der Politik im Wahlkreis."></asp:Label>
                                                    <br />
                                                    <asp:Label ID="Label38" runat="server" Text="Mitarbeit in lokalen Initiativen. Gemeinsam die Umwelt schonen."></asp:Label>
                                                </p>
                                            </div>
                                        <div class="span1"></div>
                                    </div>
                                    <div class="row" >
                                        <div class="span1"></div>
                                        <div class="span10">
                                            <div id ="div_initiative" class="span4 well label-success" style="color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_INITIATIVE" runat="server" Text="Initiativen" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label39" runat="server" Text="Veranstalltungen: Konzerte, Feste, Aufführungen....."></asp:Label>
                                                </p>
                                            </div>
                                            <div id ="div_democracy" class="span4 well label-success" style="cursor:pointer; color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_DEMOCRACY" runat="server" Text="Mitmachdemokratie" style="text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label40" runat="server" Text="Politik gestalten mit der Erststimme in deinem Wahlkreis"></asp:Label>
                                                </p>
                                            </div>
                                            <div id ="div_association" class="span4 well label-success" style="color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_ASSOCIATION" runat="server" Text="Vereine" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label11" runat="server" Text="Menschen mit einem gemeinsamen Ziel."></asp:Label>
                                                </p>
                                            </div>
                                        </div>
                                        <div class="span1"></div>
                                    </div>
                                    <div class="row">
                                        <div class="span1"></div>
                                        <div class="span10">
                                            <div id ="div_family" class="span4 well label-success" style="cursor:pointer; color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_FAMILY" runat="server" Text="Für Familien" style="text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label13" runat="server" Text="Spielplätze, Familienveranstaltungen, Seniorentreffen usw...."></asp:Label>
                                                </p>
                                            </div>
                                            <div id ="div_drive" class="span4 well label-success" style="cursor:pointer; color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_RIDE_SHARING" runat="server" Text="Fahrgemeinschaften" style="text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label41" runat="server" Text="Mitfahren, Fahrzeug teilen, Fahrgemeinschaft gründen"></asp:Label>
                                                </p>
                                            </div>
                                            <div id ="div_flirt" class="span4 well label-success" style="cursor:pointer; color:White;height:120px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyli_select_LONELY_HEARTS_AD" runat="server" Text="Kontaktanzeigen" style="text-decoration:underline;color:White;"/>
                                                </h4>
                                                <p>
                                                    <asp:Label ID="Label6" runat="server" Text="Der regionale Kontaktmarkt für einsame Herzen, Freundschaften und Erotik."></asp:Label>
                                                </p>
                                            </div>
                                            <div class="span12"><br /><br /></div>
                                        </div>
                                        <div class="span1"></div>
                                    </div>
                                </div>
                                <!-- %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 -->
                            </div>
                        </div>
                    <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                        <div id="dsplydiv_subrubric" style="display:none;">
                            <div class="row" >
                                <div class="span12">
                                <div class="well" >
                                    <h3>
                                        <asp:Label ID="Label10" runat="server" Text="Wähle eine Unterrubrik aus"></asp:Label>
                                    </h3>
                                    <div class="span12"><br /></div>
                                    <div id="slct_div_0" style="display:none;">
                                        <br />
                                        <select id="lsbx_0" multiple="multiple" size="7" style="font-size:120%;width:93%;"></select>
                                    </div>
                                    <div id="slct_div_1" style="display:none;">
                                        <br />
                                        <select id="lsbx_1" multiple="multiple" size="7" style="font-size:120%;width:93%;"></select>
                                    </div>
                                    <div id="slct_div_2" style="display:none;">
                                        <br />
                                        <select id="lsbx_2" multiple="multiple" size="7" style="font-size:120%;width:93%;"></select>
                                    </div>
                                    <div id="slct_div_3" style="display:none;">
                                        <br />
                                        <select id="lsbx_3" multiple="multiple" size="7" style="font-size:120%;width:93%;"></select>
                                    </div>
                                    <div id="slct_div_4" style="display:none;">
                                        <br />
                                        <select id="lsbx_4" multiple="multiple" size="7" style="font-size:120%;width:93%;"></select>
                                    </div>
                                    <br /><br />
                                    <div class="span4"><button id="btn_back_to_rubric" class="btn btn-large btn-danger span8" type="button">Zurück</button></div>
                                    <div class="span3">
                                        <div class="span5">
                                            <h5>
                                                <asp:Label ID="lbl_dspl_rbrc" CssClass="pull-right" runat="server" Text="Rubrik:"></asp:Label>
                                            </h5>
                                        </div>
                                        <div class="span5">
                                            <asp:TextBox ID="txbx_itemname_1" runat="server" Enabled="false" CssClass="spacedTop"></asp:TextBox>
                                        </div>
                                    </div>
                                    <div class="span4"><button id="btn_rubric_choosen" class="btn btn-large btn-success span8 pull-right" type="button">Wählen</button></div>
                                    <br /><br />
                                    <br /><br />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ -->
            </div>
        </div>
    </div>

<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->
<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->
    <div class="row"><br /><br /><br /></div>
    <!-- div_slct_loctn ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <!-- div_slct_loctn ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div class="row" id="div_slct_loctn" runat="server">
        <div class="span12 well">

            <div class="span3"></div>

            <div class="span6">
                <!-- CHOOSE COUNTRY ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <h5><asp:Label ID="lbl_country" runat="server" class="spacedTop span3" Text="Land" /></h5>
                        <asp:DropDownList ID="sel_country" runat="server" class="span7 pull-right"  ToolTip="Liste der derzeit verfügbaren Länder. Es muss natürlich zu Stadt oder Postleitzahl passen." />
                        <div id="nocountryselected" class="row alert alert-danger" style="display:none;">
                            <strong><asp:Label ID="lbl_missing_country_selection" runat="server" Text="<br /><br />Fehler : Es wurde kein Land ausgewählt! Stadt / PLZ hängen mit dem Land zusammen."></asp:Label></strong>
                        </div>
                    </div>
                </div>

                <!-- CHOOSE CITY ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <h5><asp:Label ID="lbl_city" runat="server" class="spacedTop span3" Text="Stadt / PLZ" ToolTip="Name oder Postleitzahl der gewünschten Daten" /></h5>
                        <asp:TextBox ID="txbx_city" runat="server" class="typeahead span7 pull-right" EnableViewState="false" autocomplete="off" ToolTip="Gib hier den Namen der gesuchten Stadt ein. Denk bitte daran das passende Land auszuwählen."/>
                    </div>
                </div>

                <div class="row"><br /><br /></div>

                <!-- BUTTONS TO GO FORWARD ### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <a id="cancle_slct_loctn" class="span6 btn btn-large btn-danger" data-toggle="tooltip" title="Ortsauswahl abbrechen"><i class="icon-circle-arrow-left icon-black"></i> Abbrechen</a>
                        <asp:LinkButton id="btn_select_slct_loctn" runat="server" class="span6 btn btn-large btn-success pull-right" OnClick="HandlBtnClick" OnClientClick="return checkForCountry();" ><i class="icon-road icon-black"></i> Weiter</asp:LinkButton>
                    </div>
                </div>
                <div class="row"><br /></div>

            </div>
        </div>
    </div>
    <!-- div_show_loctn ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <!-- div_show_loctn ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div class="row" id="div_show_loctn" runat="server">
        <div class="span12 well">
            <div class="span3"></div>
            <div class="span6">
                <!-- CHOOSE RUBRIC ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <h5><asp:Label ID="lbl__show_loctn_itemOfRubric" runat="server" class="spacedTop span3" Text="Rubrik" /></h5>
                        <asp:TextBox ID="txbx_itemname" runat="server" class="span7 pull-right" ToolTip="Die Rubrik muss oben per Mausklick ausgewählt werden." EnableViewState="false" disabled="disabled"></asp:TextBox>
                    </div>
                </div>
                <!-- LOCATION ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <h5><asp:Label ID="lbl_show_loctn_city" runat="server" class="spacedTop span3" Text="Ort" ToolTip="Momentanes Postleitzahlgebiet oder Stadt" /></h5>
                        <asp:TextBox ID="txbx_location" runat="server" class="span7 pull-right" EnableViewState="false" disabled="disabled" ToolTip="Das momentan eingestellte Postleitzahlgebiet." />
                    </div>
                </div>
                <div class="row">
                    <div class="span8 offset1">
                        <a id="button_opnloc_srch" class="span6 btn btn-large btn-warning pull-right" data-toggle="tooltip" title="Ändere den Ort der dir angezeigt wird"><i class="icon-road icon-black"></i> Ort wechseln</a>
                    </div>
                </div>
                <div class="row"><br /><br /></div>

                <!-- BUTTONS TO GO FORWARD ### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <asp:LinkButton id="btn_show_loctn_list" runat="server" class="span6 btn btn-large btn-success" OnClick="HandlBtnClick" ><i class="icon-th-list icon-black"></i> Liste</asp:LinkButton>
                        <asp:LinkButton id="btn_show_loctn_map"  runat="server" class="span6 btn btn-large btn-success pull-right" OnClick="HandlBtnClick" ><i class="icon-map-marker icon-black"></i> Karte</asp:LinkButton>
                    </div>
                </div>
                <div class="row"><br /></div>
            </div>
            <div class="span3"></div>
        </div>
    </div>
    <div class="row"><br /><br /></div>
<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->
<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->



    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   modal dialog that shows the wiat till data is loaded message                                                                      @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <div id="loadNwait" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="loadNWaitLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h3 id="H2">
                <asp:Label ID="lblWaitTop" runat="server" Text="Die Daten werden geladen."></asp:Label>
            </h3>
        </div>
        <div class="modal-body">
            <img src="http://www.nejoba.net/njb_02/style/pic/searching.gif" />
        </div>
        <div class="modal-footer">
            <asp:Label ID="lblWaitASecond" runat="server" Text="Entschleunige Dich :-)"></asp:Label>
        </div>
    </div>



<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div id="dsplydiv_location" class="row span12" style="display:none;">
    </div>

<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->

    <div id="dsplydiv_read_or_create" class="row span12" style="display:none;">
        <div class="span12"><br /></div>
    </div>

<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->




<div style="display:none;">
    <asp:Label ID="timeIsNow" runat="server" ></asp:Label> 
    <asp:TextBox ID="txbx_selected_function" runat="server"></asp:TextBox>

    <!-- the hidden textboxes stores the name id of the hometown of user -->
    <asp:TextBox ID="txbx_location_id" runat="server" />
    <asp:TextBox ID="txbx_location_name" runat="server" />

    <!-- the hidden textbox stores the tag for a rubric -->
    <asp:TextBox ID="txbx_tagforitem" runat="server" />

    <!-- used for remembering the text in a disabeled edit -->
    <asp:TextBox ID="txbx_itemname_2" runat="server" />


    <!-- the div will contain the source-data for the item-type-selection -->
    <div id="date_event_div" runat="server"></div>
    <div id="location_div" runat="server"></div>
    <div id="annonce_div" runat="server"></div>
    <div id="initiative_div" runat="server"></div>
    <div id="business_div" runat="server"></div>
</div>



<script type="text/javascript">
    $(document).ready(function () {
//        // --------------------------------------------------------------------------------------------------------------------------------------
//        // -- 
//        // -- auto-complete for the city-name 
//        // -- 
//        // --------------------------------------------------------------------------------------------------------------------------------------
//        cityListFromServer = []                 // used as datasource for the bootstrap-typeahead 'txbx_city'

//        $('#CoPlaBottom_txbx_city').typeahead({
//            source: function (query, process) {
//                var ajxurl = nejobaUrl('./ajax/dataSource__city.aspx?')

//                console.log('length citylistfromserver:' + cityListFromServer.length);

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
//            items: 7
//        });
        /*
        * click-handler for chose a rubric
        * 
        *  button has no special function. just closes the carussel
        */
        $("#btn_rubric_choosen").click(function () {
            $("#collapseSelctRubric").collapse('hide');
        });


    });
</script>



</asp:Content>
