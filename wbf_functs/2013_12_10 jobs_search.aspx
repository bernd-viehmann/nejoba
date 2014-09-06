<%@ Page Title="Suche Arbeitsangebote" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="True" CodeFile="2013_12_10 jobs_search.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server"></asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server"></asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="row">
        <div class="accordion" id="Div1">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >
                        <h4>Arbeit suchen</h4>
                    </a>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <h5>
                            <asp:Label ID="Label1" runat="server" Text="Finde Jobausschreibungen deiner Nachbarn."></asp:Label>
                        </h5>
                        <br />
                        <asp:Label ID="Label10" runat="server" Text="W&auml;hle oben die T&auml;tigkeit aus, die du suchst. Wenn du unter Arbeitsbereich 'Bitte wählen' anklickst, werden alle Angebote angezeigt.<br/><br/>Zusätzlich ist zumindest die Postleitzahl erforderlich. Dabei werden auch umliegende Orte berücksichtigt.<br/><br/>Dann klicke auf 'Arbeit suchen'. " />
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
                <asp:Image ID="Image2" runat="server" ImageUrl="~/style/pic/jobmarket_head.jpg" ImageAlign="Middle" />
            </div>
            <div class="span1"></div>
        </div>
    </div>

    <div class="row"><br /><br /></div>

    <div class="row">
        <div class="accordion" id="accordion_useraction">
            <div class="accordion-group">
                <!-- $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ -->

                <div class="accordion-heading">
                    <h4><a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion_useraction" href="#collapseSelctJobType" >Arbeitbereich filtern</a></h4>
                </div>
                <div id="collapseSelctJobType" class="accordion-body collapse in">
                    <div class="accordion-inner">
                        <div id="dsplydiv_rubric">
                        <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                        <h4>
                            <ul class="nav nav-tabs" id="rubricTabs">
                                <li class="active"><a href="#social" data-toggle="tab">Soziales</a></li>
                                <li><a href="#mobility" data-toggle="tab">Mobilität</a></li>
                                <li><a href="#work" data-toggle="tab">Bauen und denken</a></li>
                                <li><a href="#miscellaneous" data-toggle="tab">Sonstiges</a></li>
                            </ul>
                        </h4>
                        <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                        <div class="tab-content">
                            <div class="tab-pane active" id="social">
                                <div class="row">
                                    <div class="span1"></div>
                                    <div class="span10">
                                        <div id ="div_business" class="span4 well label-info" style="color:White;height:157px;">
                                            <h4>
                                                <asp:HyperLink ID="hyLink_human2human" runat="server" Text="Menschen" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                            </h4>
                                            <br />
                                            <div class="span6">Betreuung<br />Altenpflege<br /></div>
                                            <div class="span5">Krankenpflege<br/>Geselligkeit<br />Behinderte<br /></div>
                                        </div>
                                        <div id ="div_annonce" class="span4 well label-info" style="color:White;height:157px;">
                                            <h4>
                                                <asp:HyperLink ID="hyLink_leisure" runat="server" Text="Freizeit" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                            </h4>
                                            <br />
                                            <div class="span6">Hobbys<br />Interessen<br />Sport<br /></div>
                                            <div class="span5">Musik<br />Kunst<br />Basteln</div>
                                        </div>
                                        <div id ="div_shareconomeny" class="span4 well label-info" style="color:White;height:157px;">
                                            <h4>
                                                <asp:HyperLink ID="hyLink_personalhygiene" runat="server" Text="Körperpflege" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                            </h4>
                                            <br />
                                            <div class="span6">Kosmetik<br />Gesundheit<br />Maniküre<br /></div>
                                            <div class="span5">Pediküre<br />Frisur<br />Hautpflege</div>
                                        </div>
                                    </div>
                                    <div class="span1"></div>
                                </div>
                                <div class="row">
                                    <div class="span1"></div>
                                    <div class="span10">
                                        <div id ="div_startup" class="span4 well label-info" style="color:White;height:157px;">
                                            <h4>
                                                <asp:HyperLink ID="hyLink_children" runat="server" Text="Kinder" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                            </h4>
                                            <br />
                                            <div class="span6">Babysitter<br />Tagesmutter<br />Hausaufgaben<br /></div>
                                            <div class="span5">Nachhilfe<br />Erziehung</div>
                                        </div>
                                        <div id ="div_jobmarket" class="span4 well label-info" style="color:White;height:157px;">
                                            <h4>
                                                <asp:HyperLink ID="hyLink_education" runat="server" Text="Bildung" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                            </h4>
                                            <br />
                                            <div class="span6">Fortbildung<br />Kultur<br />Sprachen<br /></div>
                                            <div class="span5">Musik<br />Literatur<br />Lernen</div>
                                        </div>
                                        <div id ="div5" class="span4 well label-info" style="color:White;height:157px;">
                                            <h4></h4>
                                            <p>
                                                <br />
                                                <br />
                                            </p>
                                        </div>
                                        <div class="span12"><br /><br /></div>
                                    </div>
                                    <div class="span1"></div>
                                </div>
                            </div>
                            <!-- %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 -->
                            <div class="tab-pane" id="mobility">
                                <div class="row">
                                    <div class="span1"></div>
                                    <div class="span10">
                                        <div id ="div_events" class="span4 well label-info" style="color:White;height:157px;">
                                            <h4>
                                                <asp:HyperLink ID="hyLink_bringservice" runat="server" Text="Bringdienste" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                            </h4>
                                            <br />
                                            <div class="span6">Liefern<br />Holen<br />Einkaufen</div>
                                            <div class="span5">Botengänge<br />Fahrdienst</div>
                                        </div>
                                        <div id ="div_poi" class="span4 well label-info" style="cursor:pointer; color:White;height:157px;">
                                            <h4>
                                                <asp:HyperLink ID="hyLink_vehicles" runat="server" Text="Auto und Motorrad" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                            </h4>
                                            <br />
                                            <div class="span6">Arbeiten am Fahrzeug<br />Pflege</div>
                                            <div class="span5">Inspektion<br />Reperatur<br />Lackierung</div>
                                        </div>
                                        <div id ="div_pets" class="span4 well label-info" style="cursor:pointer; color:White;height:157px;">
                                            <h4>
                                                <asp:HyperLink ID="hyLink_transport" runat="server" Text="Transport" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                            </h4>
                                            <br />
                                            <div class="span6">Lieferung<br />Mobilität<br />Umzüge<br /></div>
                                            <div class="span5">Entsorgung<br />Carsharing<br />Mitfahren</div>
                                        </div>
                                    </div>
                                    <div class="span1"></div>
                                </div>
                            </div>
                            <!-- %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 -->
                            <div class="tab-pane" id="work">
                                <div class="row" >
                                    <div class="span1"></div>
                                        <div class="span10">
                                            <div id ="div_initiative" class="span4 well label-info" style="color:White;height:157px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyLink_craft" runat="server" Text="Handwerker gesucht" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <br />
                                                <div class="span6">Renovieren<br />Reperatur<br /></div>
                                                <div class="span5">Bauen<br />Technik</div>
                                            </div>
                                            <div id ="div_democracy" class="span4 well label-info" style="cursor:pointer; color:White;height:157px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyLink_computer" runat="server" Text="PC und Internet" style="text-decoration:underline;color:White;"/>
                                                </h4>
                                                <br />
                                                <div class="span6">Computer und Internet<br />Webdesign</div>
                                                <div class="span5">PC-Service<br />Netzwerk<br />Programmierung</div>
                                            </div>
                                            <div id ="div_association" class="span4 well label-info" style="color:White;height:157px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyLink_homework" runat="server" Text="Heimarbeit" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <br />
                                                <div class="span6">Homeoffice<br />Callcenter<br />Schreibarbeiten</div>
                                                <div class="span5">Produktion<br />Übersetzungen</div>
                                            </div>
                                        </div>
                                        <div class="span1"></div>
                                    </div>
                                    <div class="row">
                                        <div class="span1"></div>
                                        <div class="span10">
                                            <div id ="div_family" class="span4 well label-info" style="cursor:pointer; color:White;height:157px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyLink_office" runat="server" Text="Büroarbeiten" style="text-decoration:underline;color:White;"/>
                                                </h4>
                                                <br />
                                                <div class="span6">Office<br />Schreiben<br />Sekretär(in)</div>
                                                <div class="span5">Finanzen<br />Buchhaltung<br />Steuern</div>
                                            </div>
                                            <div id ="div_drive" class="span4 well label-info" style="cursor:pointer; color:White;height:157px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyLink_home" runat="server" Text="Hausarbeiten" style="text-decoration:underline;color:White;"/>
                                                </h4>
                                                <br />
                                                <div class="span6">Reinigung<br />Fenster putzen</div>
                                                <div class="span5">Wäsche<br />Kochen</div>
                                            </div>
                                            <div id ="div_flirt" class="span4 well label-info" style="cursor:pointer; color:White;height:157px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyLink_garden" runat="server" Text="Gartenarbeiten" style="text-decoration:underline;color:White;"/>
                                                </h4>
                                                <br />
                                                <div class="span6">Gartenpflege<br />Rasen<br />Baumschnitt<br /></div>
                                                <div class="span5">Fällungen<br />Gestalltung</div>
                                            </div>
                                            <div class="span12"><br /><br /></div>
                                        </div>
                                        <div class="span1"></div>
                                    </div>
                                </div>
                                <!-- %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 -->
                            <div class="tab-pane" id="miscellaneous">
                                <div class="row" >
                                    <div class="span1"></div>
                                        <div class="span10">
                                            <div id ="div6" class="span4 well label-info" style="color:White;height:157px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyLink_pets" runat="server" Text="Haustiere" style="cursor:pointer;text-decoration:underline;color:White;"/>
                                                </h4>
                                                <br />
                                                <div class="span6">Gassi<br />Tierpflege<br />Tierpension<br /></div>
                                                <div class="span5">Hundeschule<br />Hufschmied<br />Bereiter</div>
                                            </div>
                                            <div id ="div7" class="span4 well label-info" style="cursor:pointer; color:White;height:157px;">
                                                <h4>
                                                    <asp:HyperLink ID="hyLink_notspecified" runat="server" Text="Sonstiges" style="text-decoration:underline;color:White;"/>
                                                </h4>
                                                <br />
                                                <div class="span6">Alles übrige</div>
                                                <div class="span5"></div>
                                            </div>
                                            <div id ="div8" class="span4 well label-info" style="color:White;height:157px;">
                                            </div>
                                        </div>
                                        <div class="span1"></div>
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























    <div class="row"><br /></div>

<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->
<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->
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
                            <strong><asp:Label ID="lbl_missing_country_selection" runat="server" Text="Fehler : Es wurde kein Land ausgewählt! Stadt / PLZ hängen mit dem Land zusammen."></asp:Label></strong>
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
                
                <!-- OBSOLETE       ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <!--
                <div class="row">
                    <div class="span8 offset1">
                        <h5><asp:Label ID="lbl__show_loctn_genre" runat="server" class="spacedTop span3" Text="Bereich" /></h5>
                        <asp:DropDownList ID="sel_type" runat="server" autocomplete="off" class="typeahead span7 pull-right" ToolTip="nejoba macht Hashtags zu regionalen Themen." EnableViewState="false" ></asp:DropDownList>
                    </div>
                </div>
                -->

                <!-- CHOOSE JOBTYPE ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <h5><asp:Label ID="Label2" runat="server" class="spacedTop span3" Text="Tätigkeit" /></h5>
                        <asp:TextBox ID="txbx_jobName" runat="server" class="span7 pull-right typeahead" ToolTip="Wähle einen Job-Typen. Wenn du nichts (oder einen '*') eingibst wird alles angezeigt" autocomplete="off" data-provide="typeahead"/>
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
                        <div class="span6"></div>
                        <asp:LinkButton id="btn_show_job_list"  runat="server" class="span6 btn btn-large btn-success pull-right" OnClick="HandlBtnClick" ><i class="icon-th-list icon-black"></i> Job-Liste</asp:LinkButton>
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

    <div class="thehidden">
        <!-- hidden textfields used for statusmessages from the server (easier internationalization of the text -->
        <asp:Label ID="msg_missingLocation" runat="server" Text="Bestimme einen Ort für deine Suche" ></asp:Label>
        <asp:Label ID="msg_noLocFound" runat="server" Text="Es wurde keine Stadt oder Postleitzahl gefunden! <br />Hast du das richtige Land ausgew&auml;hlt?" ></asp:Label>
        <asp:Label ID="msg_invalidJobType" runat="server" Text="Der Tätigkeitsbereich ist nicht bekannt. Bitte Eingabe kontrollieren." ></asp:Label>
        
        <div id="div_jobtypedefinition" runat="server">
[{   "linkName": "CoPlaBottom_hyLink_human2human",
     "hashtag": "§*JTD01_human2human",
     "ui_name": "Menschen"},
    {"linkName": "CoPlaBottom_hyLink_leisure",
     "hashtag": "§*JTD01_leisure",
     "ui_name": "Freizeit"    },
    {"linkName": "CoPlaBottom_hyLink_personalhygiene",
     "hashtag": "§*JTD01_personalhygiene",
     "ui_name": "Körperpflege"},
    {"linkName": "CoPlaBottom_hyLink_children",
     "hashtag": "§*JTD01_children",
     "ui_name": "Kinder"},
    {"linkName": "CoPlaBottom_hyLink_education",
     "hashtag": "§*JTD01_education",
     "ui_name": "Bildung"},
    {"linkName": "CoPlaBottom_hyLink_bringservice",
     "hashtag": "§*JTD01_bringservice",
     "ui_name": "Bringdienste"},
    {"linkName": "CoPlaBottom_hyLink_vehicles",
     "hashtag": "§*JTD01_vehicles",
     "ui_name": "Auto und Motorrad"},
    {"linkName": "CoPlaBottom_hyLink_transport",
     "hashtag": "§*JTD01_transport",
     "ui_name": "Transport"},
    {"linkName": "CoPlaBottom_hyLink_craft",
     "hashtag": "§*JTD01_craft",
     "ui_name": "Handwerker gesucht"},
    {"linkName": "CoPlaBottom_hyLink_computer",
     "hashtag": "§*JTD01_computer",
     "ui_name": "PC und Internet"},
    {"linkName": "CoPlaBottom_hyLink_homework",
     "hashtag": "§*JTD01_homework",
     "ui_name": "Heimarbeit"},
    {"linkName": "CoPlaBottom_hyLink_office",
     "hashtag": "§*JTD01_office",
     "ui_name": "Büroarbeit"},
    {"linkName": "CoPlaBottom_hyLink_home",
     "hashtag": "§*JTD01_home",
     "ui_name": "Hausarbeit"},
    {"linkName": "CoPlaBottom_hyLink_garden",
     "hashtag": "§*JTD01_garden",
     "ui_name": "Gartenarbeit"},
    {"linkName": "CoPlaBottom_hyLink_pets",
     "hashtag": "§*JTD01_pets",
     "ui_name": "Haustiere"},
    {"linkName": "CoPlaBottom_hyLink_notspecified",
     "hashtag": "§*JTD01_notspecified",
     "ui_name": "Sonstiges"}
]
        </div>
        <asp:TextBox ID="txbx_jobType" runat="server" />    <!-- controll is filled by javascript to store the type of job to save !! -->
    </div>




<!-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -->
<!-- -- JavaScript we need to handle the clicks in the job-type matrix here                                                     -->
<!-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -->
<script type="text/javascript">

    // ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    // ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    $(document).ready(function () {

        /*
        * maschine to receive the links klicked in the jobtype-matrix
        */
        var JbTpSrc = $('#CoPlaBottom_div_jobtypedefinition').html();
        var JbTypes = JSON.parse(JbTpSrc);
        $("a[id*='CoPlaBottom_hyLink_']").click(function () {
            for (var i = 0; i < JbTypes.length; i++) {
                var item = JbTypes[i];
                if (item['linkName'] == this.id) {
                    // alert(item['ui_name'])
                    $('#CoPlaBottom_txbx_jobType').val(item['hashtag']);
                    $('#CoPlaBottom_txbx_jobName').val(item['ui_name']);
                    $('#CoPlaBottom_txbx_jobName2').val(item['ui_name']);
                }
            }
            $('#collapseSelctJobType').collapse('hide');
        });

        /*
        * create a typeahead for the jobtype
        *
        */
        var jobTypeAhead = [];
        for (var i = 0; i < JbTypes.length; i++) {
            var item = JbTypes[i];
            jobTypeAhead[i] = item['ui_name'];
        }

        $('#CoPlaBottom_txbx_jobName').typeahead({ source: jobTypeAhead });

    });
</script>

</asp:Content>

