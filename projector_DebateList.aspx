<%@ Page Title="Das nejoba Nachbarforum " Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="projector_DebateList.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <script src="<%# ResolveUrl("~/js/OpenLayers-nejoba.js") %>" type="text/javascript"></script>
    <script src="<%# ResolveUrl("~/js/neJOBaBrowserBrain.js") %>" type="text/javascript"></script>
    <script src="<%# ResolveUrl("~/js/MatrixManager.js") %>" type="text/javascript"></script>

    <style type="text/css">

    </style>

</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div class="row">
        <div class="span4 btn-toolbar pull-left">
            <div class="btn-group">
                <!-- <a id="back_to_start"    class="btn" href="#"><i class="icon-backward"></i></a> -->
                <a id="back_in_list"        class="btn" title="Zurück blättern" data-placement="bottom" data-toggle="tooltip" data-original-title="Zurück"><i class="icon-step-backward"></i></a>
                <a id="open_modal"          class="btn" href="#srchDialg" role="button" data-toggle="modal" title="Suchen" data-placement="bottom" data-original-title="Suchen"><i class="icon-search"></i></a>
                <a id="foreward_in_list"    class="btn disabled" role="button" data-toggle="modal"title="Vorwärts blättern" data-placement="bottom" data-toggle="tooltip" data-original-title="Weiter"><i class="icon-step-forward"></i></a>
                <a id="show_bookmark" class="btn" href="#linkreuse" role="button" title="externen Link erhalten" data-placement="bottom" data-toggle="modal" data-original-title="Link wiederverwenden"><i class="icon-bookmark"></i></a>
                <a id="open_map"            class="btn" title="Zur Karte (mit Suchparametern)" data-placement="bottom" data-toggle="tooltip" data-original-title="Zur Kartenansicht"><i class="icon-globe"></i></a>
                <a id="show_help"           class="btn" href="#guidance" role="button" title="Anleitung" data-placement="bottom" data-toggle="modal" data-original-title="Anleitung"><i class="icon-info-sign"></i></a>
            </div>
        </div>
        <div class="span8"></div>
    </div>

    <div class="row" id="div_projection_of_data">
        <div id="canvasforlist" class="span11 offset1"></div>
    </div>




    <!--    rubricChooser   ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> 
    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div id="rubricChooser" style="display:none;">
        <!--    dsplydiv_rubric ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> 
        <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
        <div id="dsplydiv_rubric" class="well">
            <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
            <h4>
                <ul class="nav nav-tabs" id="rubricTabs">
                    <li class="active"><a href="#economy" data-toggle="tab">Wirtschaft</a></li>
                    <li><a href="#leisure" data-toggle="tab">Freizeit</a></li>
                    <li><a href="#society" data-toggle="tab">Gesellschaft</a></li>
                </ul>
            </h4>
            <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> <!-- ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
            <div class="tab-content" id="rubricTabDef" >
                <div class="tab-pane active" id="economy">
                    <div class="row" >
                        <div class="span1"></div>
                        <div class="span10 well label-important" style="color:White;height:150px;">
                            <h4>
                                <asp:Label ID="Label1" runat="server" Text="Wirtschaft"></asp:Label>
                            </h4>
                            <p>
                                <asp:Label ID="Label3" runat="server" Text="Informiere dich regional über Unternehmen, finde einen Job über die Job-Börse oder durchstöbere die Kleinanzeigen."></asp:Label>
                                <br />
                                <asp:Label ID="Label14" runat="server" Text="Die folgenden Rubriken stehe auf nejoba zur Verfügung. Du kannst dich informieren oder selbst einen Beitrag hinzufügen. Wähle was dich interessiert."></asp:Label>
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
                                    <asp:Label ID="Label3business" runat="server" Text="Eine Sammlung von Unternehmen in deiner Stadt....... "></asp:Label>
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
                                    <asp:Label ID="Label18" runat="server" Text="Die regionale Tausch- und Schenkbörse. Wirtschaft ohne Geld."></asp:Label>
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
                                    <asp:Label ID="Label19" runat="server" Text="Neue Unternehmen stellen sich vor"></asp:Label>
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
                                    <asp:Label ID="Label4726" runat="server" Text="Menschen mit einem gemeinsamen Ziel."></asp:Label>
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
                                    <asp:Label ID="Label4727" runat="server" Text="Spielplätze, Familienveranstaltungen, Seniorentreffen usw...."></asp:Label>
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
                                    <asp:Label ID="Label4728" runat="server" Text="Der regionale Kontaktmarkt für einsame Herzen, Freundschaften und Erotik."></asp:Label>
                                </p>
                            </div>
                            <div class="span12"><br /><br /></div>
                        </div>
                        <div class="span1"></div>
                    </div>
                </div>
            </div>
            <!-- %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%% -->
            <!-- %%%%%%%%%%%%%%%  bottom of the dsplydiv_rubric   add hidden cancle button for projection-webforms                               %%%%%%%%%%%%%%% -->
            <div id="cancleProjector">
                <button id="btn_cancle_rubric" class="btn btn-large btn-danger span3" type="button">Abbrechen</button>
                <div class="span7"></div>
            </div>
            <div class="row"><br /></div>
            <!-- %%%%%%%%%%%%%%%                                                                                                                 %%%%%%%%%%%%%%% -->
            <!-- %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%% -->
        </div>




        <!-- dsplydiv_subrubric ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> 
        <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
        <div id="dsplydiv_subrubric" style="display:none;">
            <div class="row well" id="listboxstairway">
                <div class="span12">
                    <h3>
                        <asp:Label ID="Label477729" runat="server" Text="Wähle eine Unterrubrik aus"></asp:Label>
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
                    <button id="btn_back_to_rubric" class="btn btn-large btn-danger span3" type="button">Zurück</button>
                    <div id="div_for_projector">
                        <div class="span2">
                            <h5>
                                <asp:Label ID="lbl_dspl_rbrc" CssClass="pull-right" runat="server" Text="gewählte Rubrik:"></asp:Label>
                            </h5>
                        </div>
                        <div class="span2">
                            <asp:TextBox ID="txbx_itemname" runat="server" Enabled="false"></asp:TextBox>
                        </div>
                    </div>
                    <button id="btn_rubric_finished" class="btn btn-large btn-success span3 pull-right" type="button">Wählen</button>
                    <div class="row"><br /><br /></div>
                </div>
            </div>
        </div>
    </div>

    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> 
    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div id="srchDialg" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
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
                        <h5>
                            <asp:Label ID="Label6" runat="server" Text="Ort festlegen"></asp:Label>
                            <br />
                            <small>Gilt nur für aktuelle Sicht!</small>
                            <hr />
                        </h5>
                        
                        <h5>
                            <asp:Label ID="Label21" class="span4" runat="server" Text="Land" />
                            <asp:DropDownList ID="sel_country" class="span6 offset1" runat="server" EnableViewState="false" />
                        </h5>

                        <h5>
                            <asp:Label ID="Label26" class="span4" runat="server" Text="Stadt" />
                            <asp:TextBox ID="txbx_city" class="typeahead span6 offset1" runat="server" EnableViewState="false" autocomplete="off" disabled/>
                        </h5>

                        <h5>
                            <asp:Label ID="lblPstCode" class="span4" runat="server" Text="Postleitzahl" />
                            <asp:TextBox ID="txbx_postCode" class="span6 offset1" runat="server" EnableViewState="false" disabled/>
                        </h5>

                        <div>
                            <hr />
                            <strong><asp:Label ID="Label15" runat="server" Text="nejoba macht glücklich :-)<br /><br />" /></strong>
                        </div>
                    </div>

                    <div id="tab_Termin" class="tab-pane">
                        <h5>
                            <asp:Label ID="Label5" runat="server" Text="Termine"></asp:Label>
                        </h5>
                        <hr />
                        <h5>
                            <asp:Label ID="lbl_date" class="span4" runat="server" Text="Start-Termin" />
                            <asp:TextBox ID="txbx_timeFrom" class="span6 offset1" runat="server" autocomplete="off" EnableViewState="false" ToolTip="Trage hier den Tag der Veranstalltung ein. Wenn die Veranstalltung mehrere Tage dauert ist dies der erste Tag."></asp:TextBox>
                        </h5>


                        <h5>
                            <asp:Label ID="Label22" class="span4" runat="server" Text="End-Termin" />
                            <asp:TextBox ID="txbx_timeTo" class="span6 offset1" runat="server" autocomplete="off" EnableViewState="false" ToolTip="Wenn die Veranstaltung mehrere Tage dauert, wird hier der Schlusstag eingetragen. WICHTIG: Wenn der Termin nicht über mehrere Tage andauert lass dieses Feld leer."></asp:TextBox>
                        </h5>

                        <br />
                        <div>
                            <hr />
                            <asp:Label ID="Label10" runat="server" Text="Ein Beitrag läßt sich in nejoba mit einem Start- und Endtermin verknüpfen.<br />" />
                            <asp:Label ID="Label11" runat="server" Text="Auf diese Weise entsteht eine Datenbank mit der Info wann welche Veranstallungen stattfinden.<br /><br />" />
                            <strong><asp:Label ID="Label12" runat="server" Text="nejoba zeigt Dir was abgeht in deiner Stadt<br /><br />" /></strong>
                        </div>
                    </div>

                    <div id="tab_Thema" class="tab-pane">
                        <h5>
                            <asp:Label ID="Label4" runat="server" Text="regionale Themen (Hashtags)"></asp:Label>
                            <hr />
                        </h5>
                        <h5>
                            <asp:Label ID="lbl_hashtag" class="span4" runat="server" Text="Hashtag" />
                            <asp:TextBox ID="txbx_hashtag" class="span6 offset1 typeahead" runat="server" EnableViewState="false" autocomplete="off" />
                        </h5>
                        <br />
                        <div>
                            <hr />
                            <asp:Label ID="Label8" runat="server" Text="Regionale Themen sind Hashtags in nejoba. Es werden Stichwörter mit einem '#' markiert. So entsteht eine regionale Themengruppe.<br />" />
                            <strong><asp:Label ID="Label16" runat="server" Text="nejoba hat eine Antwort<br /><br />" /></strong>
                        </div>
                    </div>

                    <div id="tab_Rubrik" class="tab-pane">
                        <h5><asp:Label ID="Label2" runat="server" Text="nejoba Rubriken"></asp:Label></h5>
                        <div>
                            <asp:Label ID="Label_2" runat="server" Text="Die Rubriken funktionieren wie man es von den Kleinanzeigen in Zeitungen kennt.<br/>Der Clou : Wenn du eine Oberrubrik wählst findet nejoba auch alle untergeordneten Rubriken.<br /><br />" />
                            
                        </div>
                        <h5>
                            <asp:Label ID="Label13" class="span4 offset1" runat="server" Text="Einsortieren: " />
                            <button id="btn_selectRubric" type="button" class="span4 offset1 btn btn-success" >Rubrick wählen</button>
                            <!--<asp:Image ID="imgOLD_selectRubric" runat="server"  style="cursor: pointer;" ImageUrl="~/style/pic/64_call_forum.png" ToolTip="Beiträge aus Rubriken suchen"  />-->
                        </h5>
                        <div class="span10 offset1"><br /></strong></div>
                        <h5>
                            <asp:Label ID="Label9" class="span4 offset1" runat="server" Text="Gewählt: " />
                            <asp:TextBox ID="txbx_itemname_2" runat="server" class="span4 offset1" EnableViewState="false" ToolTip="Die gewählte Rubrik" Enabled="false" />
                        </h5>
                        <div class="span10"><strong><asp:Label ID="Label17" runat="server" Text="nejoba verbindet Menschen<br /><br />" /></strong></div>
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


    <!-- link-reuse-dlg     ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> 
    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div id="linkreuse" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="linkreuseLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h3 id="reuseLabel">Link zur Wiederverwendung</h3>
        </div>
        <div class="modal-body">
            <p>Der folgende Link dient dazu deine gefilterte Ansicht wiederzuverwenden. Er öffnet also die Karte mit den jetzt gültigen Suchkriterien.</p>
            <br />
            <div><a id="extLinkDisplay"></a></div>
            <br />
            <a id="post_on_diaspora" ><img class="btn" src="style/pic/diaspora_icon_64x64.png" alt="Teilen auf diaspora" style="height:48px; width:48px; background-image: none; background:#DAD7D0;" data-toggle="tooltip" title="Teilen auf *diaspora"/></a>
            <a id="post_on_googleplus" ><img class="btn" src="style/pic/social_googleplus_64.jpg" alt="Teilen auf facebook" style="height:48px; width:48px; background-image: none; background:#DAD7D0;" data-toggle="tooltip" title="Teilen auf google+"/></a>
            <a id="post_on_twitter" ><img class="btn" src="style/pic/social_twitter_64.jpg" alt="Teilen auf facebook" style="height:48px; width:48px; background-image: none; background:#DAD7D0;" data-toggle="tooltip" title="Teilen auf twitter"/></a>
            <a id="post_on_facebook" ><img class="btn" src="style/pic/social_facebook_64.jpg" alt="Teilen auf facebook" style="height:48px; width:48px; background-image: none; background:#DAD7D0;" data-toggle="tooltip" title="Teilen auf facebook"/></a>
            <a id="post_on_clipboard" ><img class="btn" src="style/pic/social_clipboard_64.jpg" alt="Teilen auf facebook" style="height:48px; width:48px; background-image: none; background:#DAD7D0;" data-toggle="tooltip" title="In das Clipboard kopieren"/></a>
            <br />
        </div>
        <div class="modal-footer">
            <button class="btn" data-dismiss="modal" aria-hidden="true">Fertig</button>
        </div>
    </div>



    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> 
    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div id="loadNwait" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
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


    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> 
    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div id="noDataFound" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h3 id="H3">
                <asp:Label ID="Label20" runat="server" Text="Nichts gefunden."></asp:Label>
            </h3>
        </div>
        <div class="modal-body">
            <img src="http://www.nejoba.net/njb_02/style/pic/noDataFound.png" />
        </div>
        <div class="modal-footer">
            <asp:Label ID="Label23" runat="server" Text="Es konnten keine Daten gefunden werden,<br /> die zu den verwendeten Suchparametern passen würden.<br />Diese Tatsache ist für alle Beteiligte zutiefst unbefriedigend.<br />Vielleicht hilft dir die Antwort   "></asp:Label>
            <a href="http://de.wikipedia.org/wiki/42_%28Antwort%29" target="_blank" ><strong>42</strong></a> 
            <br />
            <button class="btn" data-dismiss="modal" aria-hidden="true">Fertig</button>
        </div>
    </div>


    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> 
    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div id="endOfDataReached" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h3 id="H4">
                <asp:Label ID="Label24" runat="server" Text="Keine weiteren Daten."></asp:Label>
            </h3>
        </div>
        <div class="modal-body">
            <img src="style/pic/noDataFound.png" />
        </div>
        <div class="modal-footer">
            <asp:Label ID="Label25" runat="server" Text="Weitere Veröffentlichungen gibt es nicht."></asp:Label>
            <button class="btn" data-dismiss="modal" aria-hidden="true">Fertig</button>
        </div>
    </div>


    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> 
    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div id="guidance" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="linkreuseLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h4>Anleitung: Wie Wie finde ich etwas im Nachbarforum?</h4>
        </div>
        <div class="modal-body">
        <br />
        <iframe width="480" height="360" src="//www.youtube.com/embed/m5Kg7KOVaYU" frameborder="0" allowfullscreen></iframe>
        <br /><br />
        <asp:HyperLink ID="HyperLink2" runat="server" NavigateUrl="./wbf_help/help_debates.aspx" Target="_blank">Zur Bedienungsanleitung</asp:HyperLink>
        <br /><br />
        <asp:HyperLink ID="HyperLink5" runat="server" NavigateUrl="http://www.youtube.com/user/nejobavideo" Target="_blank">Videos zum Thema nejoba auf YouTube</asp:HyperLink>
        <br /><br />
        <asp:HyperLink ID="HyperLink3" runat="server" NavigateUrl="https://www.facebook.com/nejoba" Target="_blank">Unser Benutzerforum auf facebook.</asp:HyperLink>
        </div>
        
        <div class="modal-footer">
            <button class="btn" data-dismiss="modal" aria-hidden="true">Fertig</button>
        </div>
    </div>


    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########--> 
    <!--                    ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div style="display:none;">
        <!-- hidden text that is needed for the error-messages-->
        <asp:Label ID="lbl_error_text" runat="server" Text="error_text !"></asp:Label>

        <!-- the country-code of the user is used by javascript to make the geocoding by noatim -->
        <asp:Label ID="lbl_countrycode" runat="server" Text="de"></asp:Label>

        <!-- the user_id of the looged-in user. empty if nobody is logged in -->
        <asp:Label ID="lbl_userId" runat="server" Text=""></asp:Label>

        <!-- the hidden textbox stores the tag for a rubric -->
        <asp:TextBox ID="txbx_tagforitem" runat="server" EnableViewState="false"/>

        <!-- this lable is read by javascript to figure out what display-url will be used -->
        <asp:Label ID="lbl_display_url" runat="server" Text="de"></asp:Label>

        <div id="template">
            <div class="row">
                <div class="span12">
                    <h5>
                        <a href="§§URL_LINK_TARGET§§" target="_blank">§§URL_LINK_TEXT§§</a>
                    </h5>
                </div>
            </div>
            <div class="row">
                <div class="span12">
                    <div class="span4">
                        <strong>Ersteller: </strong>§§NICKNAME§§<br />
                        <strong>erstellt am: </strong>§§CREATIONTIME§§<br />
                    </div>
                    <div class="span4">
                        <strong>vom: </strong>§§DATE_FROM§§<br />
                        <strong>bis: </strong>§§DATE_TILL§§<br />
                    </div>
                    <div class="span4">
                        <strong>Ort: </strong>§§LOCATIONNAME§§<br />
                    </div>
                </div> 
            </div>
        </div>
    </div>




    <script type="text/javascript">
        // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        // start webform js stuff
        // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        $(document).ready(function () {
            var displayUrl = $('#CoPlaBottom_lbl_display_url').text();      // define the url that will be used to dispaly the details in javascript
            projector = new DebateProjector(displayUrl);                    // the map-projector handles the map via openlayers
            lstExtr = new ListExtractor('list', 2500, 20);                  // list-extractor manages the AJAX-load of data. initialie it loads some stuff from the server
            //lstExtr = new ListExtractor('list', 4, 2);                    // list-extractor manages the AJAX-load of data. initialie it loads some stuff from the server

            // datepicker from jquery_ui
            $("#CoPlaBottom_txbx_timeFrom").datepicker($.datepicker.regional["de"]);
            $("#CoPlaBottom_txbx_timeTo").datepicker($.datepicker.regional["de"]);

            // click function for start display with the map-projector
            $('#startSearch').click(function () {
                $('#srchDialg').modal('hide');
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

            $('.btn').tooltip();                        // add tooltips to the buttons

            // open a new tab with the map-view. current search parameter are transmitted
            $('#open_map').click(function () {
                lstExtr.getUrlParams();
                var param = lstExtr.prepareUrl();
                // alert(param);
                var url = './projector_DebateMap.aspx' + param;
                var win = window.open(url, '_blank');
                win.focus();
            });

            //open the bookmark-dialog. also helpfull for social networx
            $('#show_bookmark').click(function () {
                lstExtr.showBookmark();
            });

            //
            //  16.09.2013 bervie
            //
            // if a country is set the textfields should not be disabeled. a user is logged in !
            //
            var c = document.getElementById("CoPlaBottom_sel_country");
            if ('0' != c.options[c.selectedIndex].value) {
                // alert('c.options[c.selectedIndex].value : ' + c.options[c.selectedIndex].value);
                $("#CoPlaBottom_txbx_postCode").removeAttr('disabled');
                $("#CoPlaBottom_txbx_city").removeAttr('disabled');
                return;
            }



//            $('#btn_selectRubric').click(function () {
//                $('select[id*="lsbx_"]').html('');           // clean-up the rubric-matrix-manager select boxes
//                $('#srchDialg').modal('hide');
//                $('#canvasforlist').hide(500);
//                $('#rubricChooser').show(500);
//            });


//            // click function for rubric is selected
//            $('#btn_select_rubrik').click(function () {
//                $('#rubricChooser').hide(500);
//                $('#canvasforlist').show(500);
//                $('#srchDialg').modal('show');
//            });



        });

    </script>
</asp:Content>
