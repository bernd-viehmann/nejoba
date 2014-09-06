<%@ Page Title="Jobs auf nejoba" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="job_market.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">


<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->


    <div class="row"><br /></div>

    <div class="row">
        <div class="accordion" id="Div1">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <h4>
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >
                            Job-Börse
                        </a>
                    </h4>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
                            

<br />
<h5>Die Job-Börse auf nejoba: Der private Arbeitsmarkt. </h5>
<br />

Der Arbeitsmarkt ist in zwei Funktionen gegliedert:
<br /><br />
<strong>1. Arbeit vergeben</strong>
<br /><br />
Ein Angebot ist bei der Job-Börse vergleichbar mit der Ausschreibung einer Behörde. Hier erstellt man eine Stellenanzeigen auf nejoba. 
<br />
Jemand hat etwas zu tun (zum Beispiel seinen Rasen mähen) und sucht dafür einen Menschen, der diese Aufgabe für ihn übernimmt.
<br /> 
Er veröffentlicht hier diese Aufgabe als ein Angebot in der Job-Börse. 
<br /><br />

<strong>2. Arbeit suchen</strong>
<br /><br />
Eine Nachfrage ist ist auf nejoba die Suche nach Arbeit. Wenn jemand seinen Nachbarn helfen möchte oder eine Arbeit sucht ruft er die Funktion “Arbeit suchen” auf.
<br />
Hier findet er die Arbeitsangebote in seiner Region. Nejoba ermöglicht nun die Kontaktaufnahme mit dem Auftraggeber. 
<br /><br />

<strong>Verhandlung der Bedingungen</strong>
<br /><br />
Auf nejoba erscheinen die Arbeitsangebote sortiert nach Regionen als Liste. Die einzelnen Angebote können angeklickt werden um mit dem Auftraggeber in Kontakt zu treten. nejoba bietet die Möglichkeit eines privaten Dialoges zwischen Auftraggeber und Dienstleister. 
So können die Bedingungen anonym auf der Plattform ausgehandelt werden.
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

<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div id="fnctnselect" class="row-fluid">
        <div class="span10 offset1">
                <div class="span3">
                <asp:ImageButton ID="btn_offerJob" class="btn img-polaroid" runat="server" Text="Arbeit vergeben und Hilfe nachfragen" OnClientClick="return showJobMatrix('offer_job');" ImageUrl="style/pic/searchHelp.png" ToolTip="Klicke um eine Arbeit zu vergeben"  />
                <h4>
                    <asp:Label ID="Labelds1" runat="server" Text="Arbeit vergeben" class="muted"></asp:Label>
                </h4>

                <br /><br />

                <asp:ImageButton ID="btn_searchJob" class="btn img-polaroid" runat="server" Text="Arbeit suchen und helfen" OnClientClick="return showJobMatrix('search_job');" ImageUrl="style/pic/searchJob.png" ToolTip="Klicke um einen Job zu finden"  />
                <h4>
                    <asp:Label ID="Label2" runat="server" Text="Arbeit suchen" class="muted"></asp:Label>
                </h4>
            </div>

            <div class="span7 offset1">
                <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/jobmarket_wallpaper.png" />
            </div>
        </div>
    </div>



    <!-- *********************           ********************************************************************************************************* -->

    <div id="jobtypetable" style="display:none;">

        <div class="row-fluid">
            <div class="span1"></div>
            <div class="span10 well">
                <h4>Arbeitsbereiche auf nejoba</h4>
                <p>
                    <br />
                    Du findest in der Job-Börse eine grobe Einteilung in verschiedene Arbeitsbereiche. 
                    <br />
                    Diese Unschärfe ist gewollt. Von Festanstellungen über gewerbliche Aufträge bis hin zu Gefälligkeiten erleichtert dies die Zuordnung.
                
                </p>
            </div>
            <div class="span1"></div>
        </div>



        <!-- r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r -->
        <div class="row-fluid">
            <div class="span1"></div>
            <div class="span10">
                <div id ="div_business" class="span3 well label-info" style="color:White;height:157px;">
                    <h4>
                        <asp:LinkButton ID="hyLnk_human2human" runat="server" Text="Menschen" OnClick="HndlrHyLnkClick" style="cursor:pointer;text-decoration:underline;color:White;"/>
                    </h4>
                    <br />
                    <div class="span6">Betreuung<br />Altenpflege<br />Einkaufen</div>
                    <div class="span5">Krankenpflege<br/>Geselligkeit<br />Behinderte<br /></div>
                </div>
                <div id ="div_annonce" class="span3 well label-info" style="color:White;height:157px;">
                    <h4>
                        <asp:LinkButton ID="hyLnk_leisure" runat="server" Text="Freizeit" OnClick="HndlrHyLnkClick" style="cursor:pointer;text-decoration:underline;color:White;"/>
                    </h4>
                    <br />
                    <div class="span6">Hobbys<br />Interessen<br />Sport<br /></div>
                    <div class="span5">Musik<br />Kunst<br />Basteln</div>
                </div>
                <div id ="div_shareconomeny" class="span3 well label-info" style="color:White;height:157px;">
                    <h4>
                        <asp:LinkButton ID="hyLnk_personalhygiene" runat="server" Text="Körperpflege" OnClick="HndlrHyLnkClick" style="cursor:pointer;text-decoration:underline;color:White;"/>
                    </h4>
                    <br />
                    <div class="span6">Kosmetik<br />Gesundheit<br />Maniküre<br /></div>
                    <div class="span5">Pediküre<br />Frisur<br />Hautpflege</div>
                </div>
                <div id ="div_startup" class="span3 well label-info" style="color:White;height:157px;">
                    <h4>
                        <asp:LinkButton ID="hyLnk_children" runat="server" Text="Kinder" OnClick="HndlrHyLnkClick" style="cursor:pointer;text-decoration:underline;color:White;"/>
                    </h4>
                    <br />
                    <div class="span6">Babysitter<br />Tagesmutter<br />Bildung</div>
                    <div class="span5">Nachhilfe<br />Erziehung<br />Hausaufgaben</div>
                </div>
            </div>
            <div class="span1"></div>
        </div>

        <!-- r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r -->
        <div class="row-fluid">
            <div class="span1"></div>
            <div class="span10">
                <div id ="div_jobmarket" class="span3 well label-info" style="color:White;height:157px;">
                    <h4>
                        <asp:LinkButton ID="hyLnk_education" runat="server" Text="Bildung" OnClick="HndlrHyLnkClick" style="cursor:pointer;text-decoration:underline;color:White;"/>
                    </h4>
                    <br />
                    <div class="span6">Fortbildung<br />Kultur<br />Sprachen<br /></div>
                    <div class="span5">Musik<br />Literatur<br />Lernen</div>
                </div>
                <div id ="div_pets" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                    <h4>
                        <asp:LinkButton ID="hyLnk_transport" runat="server" Text="Transport" OnClick="HndlrHyLnkClick" style="cursor:pointer;text-decoration:underline;color:White;"/>
                    </h4>
                    <br />
                    <div class="span6">Lieferung<br />Mobilität<br />Umzüge<br /></div>
                    <div class="span5">Entsorgung<br />Carsharing<br />Mitfahren</div>
                </div>
                <div id ="div_initiative" class="span3 well label-info" style="color:White;height:157px;">
                    <h4>
                        <asp:LinkButton ID="hyLnk_craft" runat="server" Text="Handwerker" OnClick="HndlrHyLnkClick" style="cursor:pointer;text-decoration:underline;color:White;"/>
                    </h4>
                    <br />
                    <div class="span6">Renovieren<br />Reperatur<br />Heizung</div>
                    <div class="span5">Bauen<br />Technik<br />Sanitär</div>
                </div>
                <div id ="div_democracy" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                    <h4>
                        <asp:LinkButton ID="hyLnk_computer" runat="server" Text="PC und Internet" OnClick="HndlrHyLnkClick" style="text-decoration:underline;color:White;"/>
                    </h4>
                    <br />
                    <div class="span6">Computer<br />Internet<br />Webdesign</div>
                    <div class="span5">PC-Service<br />Netzwerk<br />Software</div>
                </div>
            </div>
            <div class="span1"></div>
        </div>

        <!-- r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r -->
        <div class="row-fluid" >
            <div class="span1"></div>
                <div class="span10">
                    <div id ="div_association" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_homework" runat="server" Text="Heimarbeit" OnClick="HndlrHyLnkClick" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Homeoffice<br />Callcenter<br />Fertigung</div>
                        <div class="span5">Produktion<br />Übersetzungen<br />Schreiben</div>
                    </div>
                    <div id ="div_family" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_office" runat="server" Text="Büroarbeiten" OnClick="HndlrHyLnkClick" style="text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Office<br />Schreiben<br />Sekretär(in)</div>
                        <div class="span5">Finanzen<br />Buchhaltung<br />Steuern</div>
                    </div>
                    <div id ="div_drive" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_home" runat="server" Text="Hausarbeiten" OnClick="HndlrHyLnkClick" style="text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Reinigung<br />Fenster<br />Putzen</div>
                        <div class="span5">Wäsche<br />Kochen<br />Bügeln</div>
                    </div>
                    <div id ="div_flirt" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_garden" runat="server" Text="Gartenarbeiten" OnClick="HndlrHyLnkClick" style="text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Gartenpflege<br />Rasen<br />Baumschnitt<br /></div>
                        <div class="span5">Fällungen<br />Gestalltung<br />Bewässerung</div>
                    </div>

                </div>
                <div class="span1"></div>
            </div>

            <!-- r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r -->
            <div class="row-fluid" >
                <div class="span1"></div>
                <div class="span10">
                    <div id ="div6" class="span3 well label-info" style="color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_pets" runat="server" Text="Haustiere" OnClick="HndlrHyLnkClick" style="cursor:pointer;text-decoration:underline;color:White;"/>
                        </h4>
                        <br />
                        <div class="span6">Gassi<br />Tierpflege<br />Tierpension<br /></div>
                        <div class="span5">Hundeschule<br />Hufschmied<br />Bereiter</div>
                    </div>
                    <div id ="div7" class="span3 well label-info" style="cursor:pointer; color:White;height:157px;">
                        <h4>
                            <asp:LinkButton ID="hyLnk_notspecified" runat="server" Text="Sonstiges"  OnClick="HndlrHyLnkClick" style="text-decoration:underline;color:White;"/>
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

            <div class="row-fluid">
                <div class="span10 offset1">

                    <a id="btn_cancle_slct_job" class="span3 btn btn-large btn-danger" data-toggle="tooltip" title="Ortsauswahl abbrechen" onclick="return showJobMatrix('cancle');" ><i class="icon-circle-arrow-left icon-black"></i> Abbrechen</a>

                    <div class="span3"></div>
                    <div class="span3"></div>
                    
                    <asp:LinkButton id="hyLnk_go" runat="server" class="span3 btn btn-large btn-success" OnClick="HndlrButtonClick" ><i class="icon-road icon-black"></i> Weiter</asp:LinkButton>
                </div>
            </div>
        </div>




    <!-- %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 -->
    <!-- %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 -->
    <!-- %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 %%%%%%%%%%%%%%%                 -->













    <div class="row hidden">
        <!-- function type defines if job_search or job_create was clicked -->
        <asp:TextBox ID="txbx_functn_type" runat="server"></asp:TextBox>
        <asp:Label ID="timeIsNow" runat="server" ></asp:Label> 
    </div>









<script type="text/javascript">
// ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

// ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    function showJobMatrix(param) {
        $('#CoPlaBottom_txbx_functn_type').val(param);
        $('#fnctnselect').animate({
            opacity: 1,
            left: "+=50",
            height: "toggle"
        }, 333, function () {
            // Animation complete.
            // later
        });

        $('#jobtypetable').animate({
            opacity: 1,
            left: "+=50",
            height: "toggle"
        }, 333, function () {
            // Animation complete.
            // later
        });
        return false;
    }
</script>

</asp:Content>

