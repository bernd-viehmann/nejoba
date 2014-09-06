<%@ Page Title="" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="jobs_editor.aspx.py" validateRequest="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <script src="<%# ResolveUrl("~/style/tinymce/js/tinymce/tinymce.min.js") %>" type="text/javascript"></script>
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <div class="row">
        <div class="accordion" id="accordionic_main_root">
            <div class="accordion-group">

                <div class="accordion-heading">
                    <h4>
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >Arbeit vergeben</a>
                    </h4>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
<strong>
nejoba ermöglicht Privatleuten einen Auftrag öffentlich auszuschreiben. So findet man schnell Hilfe aus der Nachbarschaft. Egal ob kleine Gefälligkeit oder umfangreiche Arbeiten wie eine Renovierung: nejoba beinhaltet einen unkomplizierten regionalen Arbeitsmarkt für Privatleute und Gewerbetreibende.
<br /><br />
Zuerst muss eine Mitteilung eingegeben werden. Diese sollte die Art des Jobs mit einem kurzen Text beschreiben. Diese Überschrift erscheint  später in der Jobliste.
<br /><br />
Darunter findest du die Auswahl des Arbeitsbereiches. Du musst hier festlegen in welchen Bereich der angebotene Job fällt. Wenn kein Themengebiet passt wähle einfach den Punkt “Sonstiges”.
<br /><br />
Wenn du einen Job ausgewählt hast bekommst du die Möglichkeit einer genaueren Beschreibung des Auftrages. Hier kannst du deine Kontaktdaten angeben, genauer beschreiben was zu machen ist oder ein Video aus YouTube oder foto aus z.B. facebook einfügen. Weitergehende Angaben hier sind aber nicht unbedingt notwendig sondern freiwillig. Interessierte Auftragnehmer können auch mit dir über nejoba in Kontakt treten wenn du dieses Feld leer lässt.
<br /><br />
Unbedingt erforderlich ist die Angabe eines Ortes. Hier musst du festlegen wo der Job zu erledigen ist. Solltest du noch nichts angegeben haben klicke auf “Ort wechseln” und gib den Namen der Stadt oder besser (weil genauer) die Postleitzahl an. 
<br /><br />
Wenn alle Eingaben gemacht sind klicke auf den grünen Knopf “Speichern”.
<br /><br />
nejoba ist derzeit noch im Test. Solange erscheinen ausgeschriebene Jobs sofort in der Liste unter “Arbeit suchen”. Später werden neu erstellte Jobangebote zunächst nur den Premium-Nutzern angezeigt. Die Veröffentlichung für alle erfolgt dann erst zeitversetzt.
<br /><br />
Wenn jemand innerhalb nejoba auf deine Ausschreibung antwortet bekommst du eine Email-Benachrichtigung. Zusätzlich bietet nejoba dir die Möglichkeit mit den Interessente zu diskutieren. Rufe dazu die Seite “Deine Angebote” unter dem Hauptpunkt “Dein Bereich”.
<br /><br />
Alle eingegebenen Daten auf nejoba unterliegen der creative-commons Lizens. Mit dem Anlegen eines Benutzerkontos hat der Anwender seine Zustimmung dazu erteilt.
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
                <asp:Image ID="Image2" runat="server" ImageUrl="~/style/pic/jobmarket_head.jpg" ImageAlign="Middle" />
            </div>
            <div class="span1"></div>
        </div>
    </div>

    <div class="row"><br /></div>

    <div class="row well">
        <div class="span10 offset1">
            <h4>
                <asp:Label ID="lbl_header_hint" runat="server" Text="Mitteilung für die Anzeige (max. 200 Zeichen )" ToolTip="Beschreibe was zu tun ist." />
                <br /><br />
                <asp:TextBox ID="txbHeader" runat="server" Width="100%" ToolTip="Das Feld muss ausgefüllt werden."></asp:TextBox>
            </h4>
        </div>
        <div class="span1"></div>
    </div>

    <div class="row">
        <div class="accordion" id="accordion_useraction">
            <div class="accordion-group">
                <!-- $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ -->
                <div class="accordion-heading">
                    <h4><a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion_useraction" href="#collapseSelctJobType" >Wähle einen Arbeitsbereich </a></h4>
                </div>
                <div id="collapseSelctJobType" class="accordion-body collapse in">
        <div class="accordion-inner">

        <div class="tab-content">

            <!-- r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r -->
            <div class="row">
                <div class="span1"></div>
                <div class="span10">
                    <div id ="div_business" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:HyperLink ID="hyLink_human2human" runat="server" Text="Menschen" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Betreuung<br />Altenpflege<br />Einkaufen</div>
                        <div class="span5">Krankenpflege<br/>Geselligkeit<br />Behinderte</div>
                    </div>
                    <div id ="div_annonce" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:HyperLink ID="hyLink_leisure" runat="server" Text="Freizeit" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Hobbys<br />Interessen<br />Sport<br /></div>
                        <div class="span5">Musik<br />Kunst<br />Basteln</div>
                    </div>
                    <div id ="div_shareconomeny" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:HyperLink ID="hyLink_personalhygiene" runat="server" Text="Körperpflege" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Kosmetik<br />Gesundheit<br />Maniküre<br /></div>
                        <div class="span5">Pediküre<br />Frisur<br />Hautpflege</div>
                    </div>
                    <div id ="div_startup" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:HyperLink ID="hyLink_children" runat="server" Text="Kinder" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Babysitter<br />Tagesmutter<br />Bildung</div>
                        <div class="span5">Nachhilfe<br />Erziehung<br />Hausaufgaben</div>
                    </div>
                </div>
                <div class="span1"></div>
            </div>

            <!-- r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r -->
            <div class="row">
                <div class="span1"></div>
                <div class="span10">
                    <div id ="div_jobmarket" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:HyperLink ID="hyLink_education" runat="server" Text="Bildung" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Fortbildung<br />Kultur<br />Sprachen<br /></div>
                        <div class="span5">Musik<br />Literatur<br />Lernen</div>
                    </div>
                    <div id ="div_pets" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                        <h4>
                            <asp:HyperLink ID="hyLink_transport" runat="server" Text="Transport" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Lieferung<br />Mobilität<br />Umzüge<br /></div>
                        <div class="span5">Entsorgung<br />Carsharing<br />Mitfahren</div>
                    </div>
                    <div id ="div_initiative" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:HyperLink ID="hyLink_craft" runat="server" Text="Handwerker" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Renovieren<br />Reparatur<br />Heizung</div>
                        <div class="span5">Bauen<br />Technik<br />Sanitär</div>
                    </div>
                    <div id ="div_democracy" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                        <h4>
                            <asp:HyperLink ID="hyLink_computer" runat="server" Text="PC und Internet" style="text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Computer<br />Internet<br />Webdesign</div>
                        <div class="span5">PC-Service<br />Netzwerk<br />Programmierung</div>
                    </div>
                </div>
                <div class="span1"></div>
            </div>

            <!-- r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r -->
            <div class="row" >
                <div class="span1"></div>
                    <div class="span10">
                        <div id ="div_association" class="span3 well label-info" style="color:White;height:157px;">
                            <h4>
                                <asp:HyperLink ID="hyLink_homework" runat="server" Text="Heimarbeit" style="cursor:pointer;text-decoration:underline;color:White;"/>
                            </h4>
                            <br />
                            <div class="span6">Homeoffice<br />Callcenter<br />Fertigung</div>
                            <div class="span5">Produktion<br />Übersetzungen<br />Schreiben</div>
                        </div>
                        <div id ="div_family" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                            <h4>
                                <asp:HyperLink ID="hyLink_office" runat="server" Text="Büroarbeiten" style="text-decoration:underline;color:White;"/>
                            </h4>
                            <br />
                            <div class="span6">Office<br />Schreiben<br />Sekretär(in)</div>
                            <div class="span5">Finanzen<br />Buchhaltung<br />Steuern</div>
                        </div>
                        <div id ="div_drive" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                            <h4>
                                <asp:HyperLink ID="hyLink_home" runat="server" Text="Hausarbeiten" style="text-decoration:underline;color:White;"/>
                            </h4>
                            <br />
                            <div class="span6">Reinigung<br />Fenster<br />Putzen</div>
                            <div class="span5">Wäsche<br />Kochen<br />Bügeln</div>
                        </div>
                        <div id ="div_flirt" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                            <h4>
                                <asp:HyperLink ID="hyLink_garden" runat="server" Text="Gartenarbeiten" style="text-decoration:underline;color:White;"/>
                            </h4>
                            <br />
                            <div class="span6">Gartenpflege<br />Rasen<br />Baumschnitt<br /></div>
                            <div class="span5">Fällungen<br />Gestalltung<br />Bewässerung</div>
                        </div>

                    </div>
                    <div class="span1"></div>
                </div>

                <!-- r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r -->
                <div class="row" >
                    <div class="span1"></div>
                    <div class="span10">
                        <div id ="div6" class="span3 well label-info" style="color:White;height:157px;">
                            <h4>
                                <asp:HyperLink ID="hyLink_pets" runat="server" Text="Haustiere" style="cursor:pointer;text-decoration:underline;color:White;"/>
                            </h4>
                            <br />
                            <div class="span6">Gassi<br />Tierpflege<br />Tierpension<br /></div>
                            <div class="span5">Hundeschule<br />Hufschmied<br />Bereiter</div>
                        </div>
                        <div id ="div7" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                            <h4>
                                <asp:HyperLink ID="hyLink_notspecified" runat="server" Text="Sonstiges" style="text-decoration:underline;color:White;"/>
                            </h4>
                            <br />
                            <div class="span6">Alles übrige</div>
                            <div class="span5"></div>
                        </div>
                        <div id ="div8" class="span3 well label-info" style="color:White;height:157px;">
                        </div>
                        <div id ="div2" class="span3 well label-info" style="color:White;height:157px;">
                        </div>
                    </div>
                    <div class="span1"></div>
                </div>
            </div>
        </div>

                </div>
                <!-- $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ -->
                <div class="accordion-heading">
                    <h4>                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion_useraction" href="#collapseEditor" >Dokument</a></h4>
                </div>
                <div id="collapseEditor" class="accordion-body collapse">
                    <div class="accordion-inner">

                        <div id="divEditArea" runat="server">
                            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
                            <h5><asp:Label ID="lbl_hint" runat="server" Text="Genauere Beschreibung (optional)"></asp:Label></h5>
                            <asp:TextBox runat="server" ID="txtMain" TextMode="MultiLine" Rows="15" style="width:100%"></asp:TextBox>
                        </div>
                    </div>
                </div>
                <!-- $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ -->
            </div>
        </div>
    </div>


<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->
    <div class="row"><br /><br /></div>


    <!-- div_slct_loctn ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div class="row" id="div_slct_loctn" runat="server">
        <div class="span6 offset3">
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



    <!-- div_show_loctn ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div class="row" id="div_show_loctn" runat="server">
        <div class="span6 offset3">
            <!-- CHOOSE JOBTYPE ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
            <div class="row">
                <div class="span8 offset1">
                    <h5><asp:Label ID="lbl__show_loctn_itemOfRubric" runat="server" class="spacedTop span3" Text="Tätigkeit" /></h5>
                    <asp:TextBox ID="txbx_jobName_show" runat="server" class="span7 pull-right well" ToolTip="Die Rubrik muss oben per Mausklick ausgewählt werden." disabled="disabled" />
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
                    <asp:LinkButton id="btn_Save"  runat="server" class="span6 btn btn-large btn-success pull-right" OnClick="HandlBtnClick" ><i class="icon-check icon-black"></i> Speichern</asp:LinkButton>
                </div>
            </div>
            <div class="row"><br /></div>
        </div>
    </div>


    <div class="row"><br /><br /></div>
<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->
<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->

    <div class="span12"><br /><br /></div>

    <div class="thehidden">
        <!-- hidden textfields used for statusmessages from the server (easier internationalization of the text -->
        <asp:Label ID="msg_slectJobType" runat="server" Text="Bitte w&auml;hle einen Arbeitsbereich für Deine Anfrage aus" ></asp:Label>
        <asp:Label ID="msg_defineHeader" runat="server" Text="Du hast keine &Uuml;berschrift angegeben" ></asp:Label>
        <asp:Label ID="msg_defineJobDescription" runat="server" Text="Es fehlt noch die Beschreibung der Arbeit" ></asp:Label>
        <asp:Label ID="msg_missingLocation" runat="server" Text="Bitte gib einen Ort ein. Klicke dazu auf 'Ort wechseln'." ></asp:Label>
        <asp:Label ID="msg_wrong_location" runat="server" Text="Der angegebene Ort wurde nicht in der Datenbank gefunden.<br />Bitte checke noch einmal deine Eingaben" ></asp:Label>

        <asp:Label ID="msg_errorfooter" runat="server" Text="<br /><br />Zwingend müssen für ein Jobangebot wenigstens die Mitteilung, der Arbeitsbereich und der Ort angegeben werden. " ></asp:Label>

        <!-- hidden text-boxes with the job-stuff -->
        <asp:TextBox ID="txbx_tagforitem" runat="server" />            <!-- controll is filled by javascript to store the type of job to save !! -->
        <asp:TextBox ID="txbx_jobName" runat="server" />            <!-- controll is filled by javascript to store the name of jobtype used for ui -->

        <!-- hidden textboxes for storing the location -->
        <asp:TextBox ID="txbx_location_id" runat="server" />        <!-- the hidden textboxes stores the location-id   of hometown -->
        <asp:TextBox ID="txbx_location_name" runat="server" />      <!-- the hidden textboxes stores the location-name of hometown -->

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
    </div>





    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<script type="text/javascript">
    /*
     * resolve_url helper for relative urls
     *
     */
    function ResolveUrl(url) {
        if (url.indexOf("~/") == 0) {
            url = baseUrl + url.substring(2);
        }
        return url;
    }

    /*
     * init the js-editor
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

    $(document).ready(function () {
        // put the last choosen jobtype into the UI
        $('#CoPlaBottom_txbx_jobName_show').val($('#CoPlaBottom_txbx_jobName').val());

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
                    $('#CoPlaBottom_txbx_tagforitem').val(item['hashtag']);
                    $('#CoPlaBottom_txbx_jobName').val(item['ui_name']);
                    $('#CoPlaBottom_txbx_jobName_show').val(item['ui_name']);

                    $('#collapseSelctJobType').collapse('hide');
                    $('#collapseEditor').collapse('show');

                }
            }
        });
    });

</script>
    
    

</asp:Content>

