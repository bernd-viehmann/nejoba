<%@ Page Title="Suche Arbeitsangebote" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="True" CodeFile="jobs_search.aspx.py" %>

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
<strong>
Auf dieser Seite können Arbeitssuchende nach Aufträgen suchen. nejoba zeigt hier die verfügbaren Jobs an.
<br /><br />
Die angezeigten Daten können gefiltert werden. Wenn du auf den Button mit der Lupe klickst werden die verfügbaren Bereiche als Link angezeigt. Ein Klick filtert das Angebot. Eine andere Möglichkeit ist den gewünschten Bereich in das Textfeld “” einzugeben und danach “neu laden” anzuklicken. Auf diese Weise kannst du zum Beispiel nur Angebote zum Thema “Heimarbeit” sehen.
<br /><br />
Um eine regionale Filterung vorzunehmen klicke auf den Button “Ort wechseln”. Du kannst unter Land “alle vorhandenen” anwählen um ortsunabhängig zu suchen. Oder du wählst nur ein Land um alle Angebote in den Niederlanden zu sehen. Um die Angebote einer Stadt zu finden gibst du zusätzlich zum Land die Postleitzahl oder den Namen der Stadt ein.
<br /><br />
Der grüne Button “neu laden” holt die Daten erneut mit den jeweiligen Filtereinstellungen vom Server. 
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

    <div class="row"><br /><br /></div>


    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div class="row">
        <div class="span4 btn-toolbar pull-left">
            <div class="btn-group">
                <!-- <a id="back_to_start"    class="btn" href="#"><i class="icon-backward"></i></a> -->
                <asp:LinkButton ID="hyLnk_pageOlderJobs" runat="server" OnClick="HandlBtnClick" class="btn" title="Zurück blättern" data-placement="bottom" data-toggle="tooltip" data-original-title="Zurück"><i class="icon-step-backward"></i></asp:LinkButton>
                <a id="open_jbTpSlctn"      class="btn" role="button" title="Suchen" data-placement="bottom" data-original-title="Suchen"><i class="icon-search"></i></a>
                <asp:LinkButton ID="hyLnk_pageNewerJobs" runat="server" OnClick="HandlBtnClick" class="btn" title="Zurück blättern" data-placement="bottom" data-toggle="tooltip" data-original-title="Zurück"><i class="icon-step-forward"></i></asp:LinkButton>
            </div>
        </div>
        <div class="span8"></div>
    </div>










    <div class="accordion-heading">
    <h4><a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion_useraction" href="#collapseSelctJobType" > Arbeitsbereich wählen</a></h4>
    </div>
    <div id="collapseSelctJobType" class="accordion-body collapse">

        <div class="accordion-inner">

    
        <div class="tab-content">

            <!-- r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r -->
            <div class="row">
                <div class="span1"></div>
                <div class="span10">
                    <div id ="div_business" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_human2human" runat="server" OnClick="HandlLnkBtn" Text="Menschen" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Betreuung<br />Altenpflege<br />Einkaufen</div>
                        <div class="span5">Krankenpflege<br/>Geselligkeit<br />Behinderte<br /></div>
                    </div>
                    <div id ="div_annonce" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_leisure" runat="server" OnClick="HandlLnkBtn" Text="Freizeit" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Hobbys<br />Interessen<br />Sport<br /></div>
                        <div class="span5">Musik<br />Kunst<br />Basteln</div>
                    </div>
                    <div id ="div_shareconomeny" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_personalhygiene" runat="server" OnClick="HandlLnkBtn" Text="Körperpflege" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Kosmetik<br />Gesundheit<br />Maniküre<br /></div>
                        <div class="span5">Pediküre<br />Frisur<br />Hautpflege</div>
                    </div>
                    <div id ="div_startup" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_children" runat="server" OnClick="HandlLnkBtn" Text="Kinder" style="cursor:pointer;text-decoration:underline;color:White;"/>
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
                            <asp:LinkButton ID="hyLnk_education" runat="server" OnClick="HandlLnkBtn" Text="Bildung" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Fortbildung<br />Kultur<br />Sprachen<br /></div>
                        <div class="span5">Musik<br />Literatur<br />Lernen</div>
                    </div>
                    <div id ="div_pets" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_transport" runat="server" OnClick="HandlLnkBtn" Text="Transport" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Lieferung<br />Mobilität<br />Umzüge<br /></div>
                        <div class="span5">Entsorgung<br />Carsharing<br />Mitfahren</div>
                    </div>
                    <div id ="div_initiative" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_craft" runat="server" OnClick="HandlLnkBtn" Text="Handwerker" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Renovieren<br />Reperatur<br />Heizung</div>
                        <div class="span5">Bauen<br />Technik<br />Sanitär</div>
                    </div>
                    <div id ="div_democracy" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_computer" runat="server" OnClick="HandlLnkBtn" Text="PC und Internet" style="text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Computer<br />Internet<br />Webdesign</div>
                        <div class="span5">PC-Service<br />Netzwerk<br />Software</div>
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
                                <asp:LinkButton ID="hyLnk_homework" runat="server" OnClick="HandlLnkBtn" Text="Heimarbeit" style="cursor:pointer;text-decoration:underline;color:White;"/>
                            </h4>
                            <br />
                            <div class="span6">Homeoffice<br />Callcenter<br />Schreibarbeiten</div>
                            <div class="span5">Produktion<br />Übersetzungen</div>
                        </div>
                        <div id ="div_family" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                            <h4>
                                <asp:LinkButton ID="hyLnk_office" runat="server" OnClick="HandlLnkBtn" Text="Büroarbeiten" style="text-decoration:underline;color:White;"/>
                            </h4>
                            <br />
                            <div class="span6">Office<br />Schreiben<br />Sekretär(in)</div>
                            <div class="span5">Finanzen<br />Buchhaltung<br />Steuern</div>
                        </div>
                        <div id ="div_drive" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                            <h4>
                                <asp:LinkButton ID="hyLnk_home" runat="server" OnClick="HandlLnkBtn" Text="Hausarbeiten" style="text-decoration:underline;color:White;"/>
                            </h4>
                            <br />
                            <div class="span6">Reinigung<br />Fenster<br />Putzen</div>
                            <div class="span5">Wäsche<br />Kochen<br />Bügeln</div>
                        </div>
                        <div id ="div_flirt" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                            <h4>
                                <asp:LinkButton ID="hyLnk_garden" runat="server" OnClick="HandlLnkBtn" Text="Gartenarbeiten" style="text-decoration:underline;color:White;"/>
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
                                <asp:LinkButton ID="hyLnk_pets" runat="server" OnClick="HandlLnkBtn" Text="Haustiere" style="cursor:pointer;text-decoration:underline;color:White;"/>
                            </h4>
                            <br />
                            <div class="span6">Gassi<br />Tierpflege<br />Tierpension<br /></div>
                            <div class="span5">Hundeschule<br />Hufschmied<br />Bereiter</div>
                        </div>
                        <div id ="div7" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                            <h4>
                                <asp:LinkButton ID="hyLnk_notspecified" runat="server" OnClick="HandlLnkBtn" Text="Sonstiges" style="text-decoration:underline;color:White;"/>
                            </h4>
                            <br />
                            <div class="span11">Alles was nirendwo anders hinein passt</div>
                        </div>
                        <div id ="div8" class="span3 well label-info" style="color:White;height:157px;">
                            <h4>
                                <asp:LinkButton ID="hyLnk_unfiltered" runat="server" OnClick="HandlLnkBtn" Text="Alles" style="text-decoration:underline;color:White;"/>
                            </h4>
                            <br />
                            <div class="span11">Keine Filterung der Daten vornehmen</div>
                            
                        </div>
                        <div id ="div2" class="span3 well label-info" style="color:White;height:157px;">
                        </div>
                    </div>
                    <div class="span1"></div>
                </div>
            </div>
        </div>
    </div>


























    <!-- ############################################################################################################################################ -->
    <!--   repeaer renders stuff from db to the outside world                                                                                         -->
    <!-- ############################################################################################################################################ -->

    <div class="accordion row" id="accordion2">
        <asp:Repeater ID="repJobList" runat="server">
                <ItemTemplate>
                <div class="accordion-group">
                    <div class="accordion-heading row">
                        <div class="span9 offset1">
                            <div class="span10">
                                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href='#<%# Eval("_ID")%>'>
                                    <h5><asp:Label ID="Label4" runat="server" Text='<%# Eval("subject")%>' /></h5>
                                </a>
                            </div>
                            <div class="span2">
                                <asp:HyperLink ID="hyLnk_opnJob" runat="server" class="spacedTop btn btn-info pull-right" Text='Aufrufen' NavigateUrl='<%# Eval("tagZero")%>' Target="_blank" />
                            </div>
                        </div>
                        
                    </div>

                    <div id='<%# Eval("_ID")%>' class="accordion-body collapse">
                        <div class="accordion-inner">
                            <small>
                                <div class="row">
                                    <div class="span5 offset1">
                                        <asp:Label ID='Label6' runat="server"  Text='Benutzer : ' />
                                        <asp:Label ID='lblBody' runat="server"  Text='<%# Eval("nickname")%>' />
                                    </div>
                                    
                                    <div class="span6">
                                        <asp:Label ID='Label8' runat="server"  Text='Standort : ' />
                                        <asp:Label ID='Label9' runat="server"  Text='<%# Eval("locationname")%>' />
                                    </div>
                                </div>
                            </small>
                            <div class="row">
                                <div class="span10 offset1">
                                    <asp:Label ID='Label5' runat="server"  Text='<%# Eval("body")%>' />
                                </div>
                                <div class="span1"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <br />
                </ItemTemplate>
                <SeparatorTemplate></SeparatorTemplate>
        </asp:Repeater>
    </div>

    <!-- ############################################################################################################################################ -->
    <!-- ############################################################################################################################################ -->

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
                <div class="row"><br /></div>
                <!-- BUTTONS TO GO FORWARD ### ########### ########### ########### ########### ########### ########### ########### ########### ########### -->
                <div class="row">
                    <div class="span8 offset1">
                        <div class="span6"></div>
                        <asp:LinkButton id="btn_show_job_list"  runat="server" class="span6 btn btn-large btn-success pull-right" OnClick="HandlBtnClick" ><i class="icon-th-list icon-black"></i> neu laden</asp:LinkButton>
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
        <asp:Label ID="msg_missingLocation" runat="server" Text="Es muss ein bestimmter Ort für deine Suche gewählt werden" ></asp:Label>
        <asp:Label ID="msg_wrong_location" runat="server" Text="Der eingegebene Ort konnte nicht gejunden werden. <br /><br />Bitte klicke auf 'Ort wechseln'. Achte bitte darauf das passende Land auszuwählen." ></asp:Label>
        <asp:Label ID="msg_noLocFound" runat="server" Text="Es wurde keine Stadt oder Postleitzahl gefunden! <br />Hast du das richtige Land ausgew&auml;hlt?" ></asp:Label>
        <asp:Label ID="msg_invalidJobType" runat="server" Text="Der Tätigkeitsbereich ist nicht bekannt. Bitte Eingabe kontrollieren." ></asp:Label>
        <asp:Label ID="msg_noDataFound" runat="server" Text="Es wurden keine Daten gefunden. Bitte versuche es später noch einmal." ></asp:Label>
        <asp:Label ID="msg_no_jobs_found" runat="server" Text="Es wurden keine Jobangebote gefunden. Bitte ändere deine Suchparameter." ></asp:Label>
        
        
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

        $('#open_jbTpSlctn').click( function (){ $('#collapseSelctJobType').collapse('toggle')});

    });
</script>

</asp:Content>

