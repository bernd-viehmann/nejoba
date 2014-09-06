<%@ Page Title="" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="debate_editor.aspx.py" validateRequest="false" EnableEventValidation="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <script src="<%# ResolveUrl("~/style/tinymce/js/tinymce/tinymce.min.js") %>" type="text/javascript"></script>
    <script src="<%# ResolveUrl("~/js/OpenLayers-nejoba.js") %>" type="text/javascript"></script>
    <script src="<%# ResolveUrl("~/js/LocationSelect.js") %>" type="text/javascript"></script>

    <script src="<%# ResolveUrl("~/js/MatrixManager.js") %>" type="text/javascript"></script>

    <style type="text/css">
        /* for bootstrap compatibility */
        img.olTileImage {
            max-width: none;
        }
    </style>
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server"></asp:Content>
<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <div id="editpart">
        <div class="row">
            <div class="accordion" id="Div1">
                <div class="accordion-group">
                    <div class="accordion-heading">
                        <h4>
                            <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseRemark" >
                                Beitrag für das Nachbarforum erstellen
                            </a>
                        </h4>
                    </div>
                    <div id="collapseRemark" class="accordion-body collapse">
                        <div class="accordion-inner">
<strong>
Diese Seite ermöglicht dir die Eingabe eines neuen Beitrages im Nachbarforum.
<br /><br />
Ein einfacher Beitrag besteht aus einer Mitteilung an einem Ort. Du gibst einen kurzen Text für die Überschrift an und wählst aus für welchen Ort ( oder genauer : Postleitzahlgebiet ) dein Text bestimmt ist.
<br /><br />
Danach klicke auf “Vorschau”. Hier kannst du deine Eingaben noch einmal kontrollieren. Um den Beitrag ins Forum zu stellen klicke hier auf “Veröffentlichen”. 
<br /><br />
Danach ist dieser Beitrag auf der Liste im Nachbarforum öffentlich. Hier haben die nejoba-User nun die Möglichkeit ihn zu lesen und im Forum zu diskutieren.
<br /><br />
nejoba unterstützt Hashtags die hier immer einen regionalen Bezug haben. Auf diese können sich über nejoba Nachbarn über ihre Interessen vernetzen. Sie nutzen die Tags als regionales Thema. 
<br /><br />
Des weiteren können Beiträge mit zusätzlichen Informationen wie einem detaillierten Dokument, einem Termin, einer Rubrik oder einem Ort versehen werden. Darüber realisiert nejoba einen Veranstaltungskalender, eine Plattform für regionale Kleinanzeigen und eine Karte mit interessanten Orten.
<br /><br />
Folgende Attribute sind verfügbar:
<br /><br />

<ul>
    <li>
    Dokument erstellen  
    <br />
    Ein Dokument ist ein Webseite die mit einer Kurzmitteilung verknüpft ist. Es können neben der Gestaltung des Textes zusätzliche Elemente eingefügt werden. Dazu zählen Weblinks, Bilder oder Videos.
    <br /><br />
    </li>

    <li>Termin bestimmen  
    <br />
    Eine Mitteilung kann mit einem Start- und Endtermin versehen werden. Auf diese Weise lassen sich auf nejoba Veranstaltungen aller Art an einem bestimmten Termin auffinden.
    <br /><br />
    </li>

    <li>
    Rubrik zuordnen  
    <br />
    Rubriken sind vorgegeben Themengebiete. Die Filterung funktioniert rekursiv. Das bedeutet: Wenn eine übergeordnete Kategorie gesucht wird findet nejoba auch die untergeordneten Bereiche. So realisiert nejoba Rubriken für Anzeigen oder zur thematischen Vernetzung.
    <br /><br />
    </li>

    <li>
    Ort markieren  
    <br />
    Ein Beitrag kann mit einer geographischen Koordinate kombiniert werden. So können Veranstaltungsorte, Sehenswürdigkeiten, Ladenlokale, Pfundstellen oder Treffpunkte auf einer Karte visualisiert werden.
    <br /><br />
    </li>

</ul>
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

        <div class="row well">
            <div class="span10 offset1">
                <h4>
                    <asp:Label ID="Label1" runat="server" Text="Mitteilung für die Anzeigen (max. 200 Zeichen )" ToolTip="Veröffentliche einen Beitrag im Forum. Eine Kurzmitteilung ist immer erforderlich. Zusätzlich kannst Du ein Dokument anfügen." />
                    <br /><br />
                    <asp:TextBox ID="txbHeader" runat="server" Width="100%" ToolTip="Die Kurzmitteilung ist erforderlich. Verwende Hashtags zur thematischen Gruppierung."></asp:TextBox>
                </h4>
            </div>
            <div class="span1"></div>
        </div>

        <div class="row">
            <div class="span12">
                <div class="accordion" id="accordion2">
                    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
                    <!-- # #   main-text attributes                                                                                                                                                         # # # -->
                    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
                    <div class="accordion-group">
                        <div class="accordion-heading">
                            <h4>
                                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseZero">
                                    <asp:Label ID="Label5" runat="server" Text="Dokument erstellen" ToolTip="Ein Beitrag beinhaltet mindestens eine Kurzmitteilung. Zusätzlich kann eine detailiertere Beschreibung dazu gehören." />
                                </a>
                            </h4>
                        </div>
                        <div id="collapseZero" class="accordion-body collapse">
                            <div id="area_edit" class="accordion-inner">
                                <div class="row">
                                    <div class="span10 offset1">
                                        <h4>
                                            <br />
                                            <asp:Label ID="lbl_hint" runat="server" Text="Dein Dokument" ToolTip="Das Dokument ist mit der Kurzmeldung verknüpft. Es ist nicht zwingend erforderlich."></asp:Label>
                                            <a id="shwHelp2" class="btn" href="#guidance2" role="button" title="Wie schreibt man etwas ins Forum?" data-placement="bottom" data-toggle="modal" data-original-title="Wie schreibt man etwas ins Forum?"><i class="icon-info-sign"></i></a>
                                        </h4>
                                        <asp:TextBox runat="server" ID="txtMain" TextMode="MultiLine" Rows="13" style="width:92%"></asp:TextBox>
                                    </div>
                                    <div class="span1"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
                    <!-- # #   additional attributes select a start- and end-date                                                                                                                                                          # # # -->
                    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
                    <div class="accordion-group">
                        <div class="accordion-heading">
                        <h4>
                            <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseOne">
                                <asp:Label ID="Label4" runat="server" Text="Termin bestimmen" ToolTip="Lege für deinen Beitrag ein Datum fest. Zum Beispiel wann eine Veranstalltung stattfindet." />
                            </a>
                        </h4>
                        </div>
                        <div id="collapseOne" class="accordion-body collapse">
                            <div class="accordion-inner">
                                <div class="row">
                                    <br /><br />
                                    <div class="span11">
                                        <strong>
                                            Wenn du eine Veranstalltung oder einen Termin festlegen willst genügt es nur das Start-Datum festzulegen.
                                            <br />
                                            Das End-Datum dient dazu einen Zeitbereich zu definieren. So kannst z.B. eine Konzert-Tournee oder eine mehrtägige Ausstellung auf nejoba dargestellt werden.
                                            <br />
                                        </strong>
                                    </div>
                                </div>

                                <div class="row"><br /><br /><br /></div>

                                <div class="row">
                                    <div class="span3 offset1">
                                        <h5>
                                            <asp:Label ID="Label9" runat="server" Text="Start-Datum :" ></asp:Label>
                                        </h5>
                                    </div>
                                    <div class="span8">
                                        <asp:TextBox ID="txbx_timeFrom" runat="server" autocomplete="off" EnableViewState="false" ToolTip="Trage dein gesuchtes Datum ein. Wenn die Veranstalltung mehrere Tage dauert ist dies der erste Tag."></asp:TextBox>
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="span3 offset1">
                                        <h5>
                                            <asp:Label ID="Label7" runat="server" Text="End-Datum:"></asp:Label>
                                        </h5>
                                    </div>
                                    <div class="span8">
                                        <asp:TextBox ID="txbx_timeTo" runat="server" autocomplete="off" EnableViewState="false" ToolTip="Wenn du ein Datum einsetzt sucht nejoba alle Termine, die in diesem Bereich liegen. Lass es einfach leer wenn du nur nach einem bestimmten Tag suchst."></asp:TextBox>
                                    </div>
                                </div>
                                <div class="row"><br /><br /></div>
                            </div>
                        </div>
                    </div>


                    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
                    <!-- # #   define rubric of announcment                                                                                                                                                                                # # # -->
                    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
                    <div class="accordion-group">
                        <div class="accordion-heading">
                            <h4>
                                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseTwo">
                                    <asp:Label ID="Label8" runat="server" Text="Rubrik zuordnen" ToolTip="Dein Beitrag in einer der vorgegebenen Rubriken eingliedern." />
                                </a>
                            </h4>
                        </div>
                        <div id="collapseTwo" class="accordion-body collapse">
                            <div class="accordion-inner">
                                <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ --><!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ --><!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ --><!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ --><!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
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
                                                        <asp:Label ID="Label24" runat="server" Text="Informiere dich regional über Unternehmen oder durchstöbere die Kleinanzeigen."></asp:Label>
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
                                                    <div id ="div_emptienes01" class="span4 well label-important" style="color:White;height:120px;">
                                                    </div>
                                                    <div id ="div_emptienes02" class="span4 well label-important" style="color:White;height:120px;">
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
                                                    <div id ="div_leer001" class="span4 well label-warning" style="cursor:pointer;color:White;height:120px;">
                                                    </div>
                                                    <div id ="div_leer002" class="span4 well label-warning" style="cursor:pointer;color:White;height:120px;">
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
                                        <div class="span11 offset1">
                                            <h4>
                                                <asp:Label ID="Label28547" runat="server" Text="Wähle eine Unterrubrik aus"></asp:Label>
                                            </h4>

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
                                            <div class="span12"><br /></div>


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
                                        </div>
                                    </div>

                                    <div class="row"><br /></div>
                                </div>

                                <div id="div_for_projector">
                                    <div class="row">
                                    </div>

                                <button id="btn_rubric_finished" class="btn btn-large btn-success span3 pull-right" type="button" style="visibility:hidden">Wählen</button>
                                
                                </div>

                                <div class="row"><br /><br /></div>

                            </div>
                        </div>
                    </div>
                    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ --><!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ --><!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ --><!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ --><!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->

                    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
                    <!-- # #   map for setting the location                                                                                                                                                                                 # # # -->
                    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
                    <div class="accordion-group">
                        <div class="accordion-heading">
                            <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseThree">
                                <h4><asp:Label ID="Label10" runat="server" Text="Ort markieren" ToolTip="Markiere einen Punkt auf der Karte. Wo ist der Veranstalltungsort. Was ist das Ziel deiner Fahrgemeinschaft." /></h4>
                            </a>
                        </div>
                        <div id="collapseThree" class="accordion-body collapse">
                            <div class="accordion-inner">
                                <div class="row">
                                    <div class="span1"></div>
                                    <div id="Div_help" class="span10 alert alert-info">
                                        <asp:Label ID="Label1347" runat="server" Text='<br /><strong style="color: #AA0000; font-size: 17pt">Für die Ortsmarkierung einfach einmal auf die Karte klicken.</strong> <br /><br />Es erscheint dann eine rote Markierung. So kannst du auch Orte wählen für die es keine Postadresse gibt. Zum Beispiel einen Parkplatz als Sammelpunkt für eine Fahrgemeinschaft.<br /><br />' ForeColor="Black" />
                                        <asp:Label ID="Label523" runat="server" Text='In der Auswahl für die Postleitzahl bei <strong>"Postleitzahl festlegen"</strong> kannst du festlegen welchem Ort dein Beitrag zugeordnet wird. Du kannst unter <strong>"Stadt suchen"</strong> belibiege Orte wählen.<br />' ForeColor="Black" />
                                    </div>
                                    <div class="span1"></div>
                                </div>

                                <div class="row">
                                    <div class="span1"></div>
                                    <div class="span10">
                                        <div id="map" style="height:500px; width:100%;"></div>
                                        <div class="row"><br /><br /></div>
                                    </div>
                                    <div class="span1"></div>
                                </div>

                                <div class="row">
                                    <div class="span1"></div>
                                    <div class="span10">
                                        <h4>
                                            <ul class="nav nav-tabs">
                                                <li class="active"><a href="#nationwide_tab" data-toggle="tab">Welche Stadt</a></li>
                                                <li><a href="#regio_tab" data-toggle="tab">Adresssuche</a></li>
                                                <li><a href="#goggle_map" data-toggle="tab">Koordinaten eintragen</a></li>
                                            </ul>
                                        </h4>
                                        <div class="tab-content">

                                            <!-- ##### nationwide postcode-selection ###### -->
                                            <div id="nationwide_tab" class="tab-pane active">
                                                 <div class="row">
                                                    <div id="Div212" class="span10 offset1 alert alert-info">
                                                        <asp:Label ID="Label17" runat="server" Text="<strong>Lege hier fest welche Stadt auf der Karte angezeigt werden soll.</strong><br /><br />" />
                                                        <asp:Label ID="Label18" runat="server" Text="Zuerst das Land auswählen, dann den Namen der Stadt eingeben und auf den Knopf drücken. <br />Die Karte zeigt die Stadt an."></asp:Label>
                                                    </div>
                                                </div>
                                               <div class="row"><br /></div>
                                                <div class="row">
                                                    <div class="span3 offset1"><label><asp:Label ID="lbl_cntrysel" runat="server" Text="Land" /></label></div>
                                                    <div class="span4">
                                                        <asp:DropDownList ID="sel_country_map" runat="server"  ToolTip="Derzeit ist nejoba nur in deutscher Sprache verfügbar. Daran wird aber gearbeitet.">
                                                            <asp:ListItem Text="Deutschland" Value="DE" />
                                                            <asp:ListItem Text="Österreich" Value="AT" />
                                                            <asp:ListItem Text="Schweiz" Value="CH" />
                                                            <asp:ListItem Text="Liechtenstein" Value="LI" />
                                                            <asp:ListItem Text="Luxemburg" Value="LU" />
                                                            <asp:ListItem Text="Niederlande" Value="NL" />
                                                            <asp:ListItem Text="Belgien" Value="BE" />
                                                        </asp:DropDownList>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="span3 offset1"><label><asp:Label ID="lbl_city2" runat="server" Text="Stadt" /></label></div>
                                                    <div class="span4"><asp:TextBox ID="txbx_city_map" class="typeahead" runat="server" EnableViewState="false" autocomplete="off" /></div>
                                                </div>
                                                <div class="row">
                                                    <div class="span3 offset1"></div>
                                                    <div class="span4">
                                                        <asp:HyperLink ID="img_findPostcode" runat="server" class="btn btn-success" Text="Stadt anzeigen" ToolTip="Stadt in die Kartenmitte holen" CausesValidation="False" />
                                                    </div>
                                                </div>
                                                <div class="row"><br /><br /></div>
                                            </div>

                                            <!-- ##### regional postcode-selection ###### -->
                                            <div id="regio_tab" class="tab-pane">
                                                 <div class="row">
                                                    <div id="Div2211" class="span10 offset1 alert alert-info">
                                                        <asp:Label ID="Label19" runat="server" Text="<strong>Suche eine bestimmte Adresse.</strong><br /><br />" />
                                                        <asp:Label ID="Label20" runat="server" Text="Stadt auswählen und Straße eingeben. Nach Knopfdruck erscheint die Straße in der Mitte.<br />Danach markiere den gewünschten Ort mit einem Klick auf die Karte."></asp:Label>
                                                    </div>
                                                </div>
                                                <div class="row"><br /></div>
                                                <div class="row">
                                                    <div class="span3 offset1"><label><asp:Label ID="lbl_city" runat="server" Text="Ort" /></label></div>
                                                    <div class="span4"><asp:DropDownList ID="sel_lctn" runat="server" EnableViewState="True" /></div>
                                                </div>
                                                <div class="row">
                                                    <div class="span3 offset1"><label><asp:Label ID="lbl_street" runat="server" Text="Straße" /></label></div>
                                                    <div class="span4"><asp:TextBox ID="txbx_street" runat="server" ToolTip="Bitte nur den Namen der Strasse eingeben. Hausnummer weglassen!"></asp:TextBox></div>
                                                </div>
                                                <div class="row">
                                                    <div class="span3 offset1"></div>
                                                    <div class="span4">
                                                        <asp:HyperLink ID="img_findLocation" runat="server" class="btn btn-success" Text="Straße anzeigen" ToolTip="Straße in die Kartenmitte holen" CausesValidation="False" />
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- ##### coordinates directly  ###### -->
                                            <div id="goggle_map" class="tab-pane">
                                                <div class="row">
                                                    <div id="Div3" class="span10 offset1 alert alert-info">
                                                        <asp:Label ID="Label14" runat="server" Text="Du kannst hier den Kartendienst von Google aufrufen falls du mit der eingebauten Suche nicht zurecht kommst.<br /><br />" />
                                                        <asp:Label ID="Label15" runat="server" Text="Wenn du die Koordinaten kennst trage sie in die Felder ein. Ansonsten werden hier die Positionsdaten vom Marker eingetragen, den du in der Karte mit einem einzelnen Klick gesetzt hast.<br/><br/>"></asp:Label>
                                                        <asp:Label ID="Label16" runat="server" Text="<strong>Das Dezimaltrennzeichen ist hier der Punkt (.) und nicht das Komma-Zeichen (,).</strong>"></asp:Label>
                                                    </div>
                                                </div>
                                                <div class="row"><br /></div>
                                                <div class="row">
                                                    <div class="span1"></div>
                                                    <div class="span10 img-polaroid"><asp:HyperLink ID="hyli_mapcoordinates" runat="server" Text="GoogleMaps nutzen" NavigateUrl="http://www.mapcoordinates.net/" ImageUrl="../style/pic/Google_maps_logo.png" Target="_blank" ToolTip="Breiten- und Längengrad per 'Cut and Paste' in die Textfelder" /></div>
                                                    <div class="span1"></div>
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
                                                    <div class="span3 offset1"></div>
                                                    <div class="span4">
                                                        <asp:HyperLink ID="img_centerMap" runat="server" class="btn btn-success" Text="Koordinaten in die Mitte" ToolTip="Kartenmitte anhand der eingegebenen Koordinaten einstellen" CausesValidation="False" />
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->

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
                            <h5><asp:Label ID="Label12" runat="server" class="spacedTop span3" Text="Stadt / PLZ" ToolTip="Name oder Postleitzahl der gewünschten Daten" /></h5>
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
        <div class="row" id="div_show_loctn" runat="server">
            <div class="span12 well">
                <div class="row">
                    <div id="Div2" class="span10 offset1 alert alert-info">
                        <asp:Label ID="Label22" runat="server" Text="<strong>Wo soll der Beitrag veröffentlicht werden?</strong><br /><br />" />
                        <asp:Label ID="Label30" runat="server" Text="Beiträge werden einem bestimmten Postleitzahlgebiet zugeordnet. Lege hier fest in welcher Stadt dein Beitrag erscheinen soll.<br />Lege den Ort fest BEVOR du eine Markierung auf der Karte machst."></asp:Label>
                    </div>
                </div>
                <div class="span3"></div>
                <div class="span6">
                    <!-- LOCATION ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                    <div class="row">
                        <div class="span8 offset1">
                            <h5><asp:Label ID="lbl_show_loctn_city" runat="server" class="spacedTop span3" Text="Ort" ToolTip="Momentanes Postleitzahlgebiet oder Stadt" /></h5>
                            <asp:TextBox ID="txbx_location" runat="server" class="span7 pull-right" EnableViewState="false" disabled="disabled" ToolTip="Das momentan eingestellte Postleitzahlgebiet." />
                        </div>
                    </div>
                    <div class="row">
                        <div class="span8 offset1">
                            <a id="button_opnloc_srch" class="span6 btn btn-large btn-warning pull-right" data-toggle="tooltip" title="Ändere den Ziel-Ort"><i class="icon-road icon-black"></i> Ort wechseln</a>
                        </div>
                    </div>
                    <div class="row"><br /><br /></div>

                    <!-- BUTTONS TO GO FORWARD ### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                    <div class="row">
                        <div class="span8 offset1">
                            <div class="span6"></div>
                            <a id="btn_showPreview" class="span6 btn btn-large btn-warning pull-right" data-toggle="tooltip" title="Zur Kontrolle eine Vorschau anzeigen"><i class="icon-check icon-black"></i> Vorschau</a>
                        </div>
                    </div>
                    <div class="row"><br /></div>
                </div>
                <div class="span3"></div>
            </div>
        </div>
        <div class="row"><br /><br /></div>
    <!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->


    </div>      <!-- END of the EDITPART    END of the EDITPART    END of the EDITPART    END of the EDITPART    END of the EDITPART    END of the EDITPART    -->











<!-- ########### INSPECTION: PREVIEW OF THE TEXT    INSPECTION: PREVIEW OF THE TEXT    INSPECTION: PREVIEW OF THE TEXT    INSPECTION: PREVIEW OF THE TEXT   ###########-->
<!-- ########### INSPECTION: PREVIEW OF THE TEXT    INSPECTION: PREVIEW OF THE TEXT    INSPECTION: PREVIEW OF THE TEXT    INSPECTION: PREVIEW OF THE TEXT   ###########-->
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
                <asp:Button ID="btn_Save" runat="server" class="btn btn-large btn-success pull-right" Text="Ver&ouml;ffentlichen" onclick="HandlBtnClick"/>
            </div>
        </div>
    </div>
<!-- ########### INSPECTION: PREVIEW OF THE TEXT    INSPECTION: PREVIEW OF THE TEXT    INSPECTION: PREVIEW OF THE TEXT    INSPECTION: PREVIEW OF THE TEXT   ###########-->
<!-- ########### INSPECTION: PREVIEW OF THE TEXT    INSPECTION: PREVIEW OF THE TEXT    INSPECTION: PREVIEW OF THE TEXT    INSPECTION: PREVIEW OF THE TEXT   ###########-->





    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ --><!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ --><!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ --><!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ --><!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
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


    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   modal dialog that shows the wait till data is loaded message                                                                      @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
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



<!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
<!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
<!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
<!-- @@                                                                                                                                     @@ -->
<!-- @@   hiddenstuff to be translated to have easy multilanguagesupport                                                                    @@ -->
<!-- @@                                                                                                                                     @@ -->
<!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
<!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
<!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
<div style="display:none;">
    <!-- the div-text will toggled by the type-select-buttons. used from javascript to choose the corresponding data-container-->
    <div id="toggle_div"></div>

    <asp:Label ID="lbl_countrycode" runat="server" Text=""></asp:Label>             <!-- the country-code of the user is used by javascript to make the geocoding by noatim   obsolete  13.09.2013-->
    <asp:TextBox ID="txbx_tagforitem" runat="server" />                             <!-- the hidden textbox stores the tag for a rubric -->
    <asp:TextBox ID="txbx_itemname" runat="server" />                               <!-- the hidden textbox stores the nice-name of choosen rubric -->
    <asp:TextBox ID="txbx_location_id" runat="server" />                            <!-- the hidden textboxes stores the location-id   of hometown -->
    <asp:TextBox ID="txbx_location_name" runat="server" />                          <!-- the hidden textboxes stores the location-name of hometown -->

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

    <!-- hidden text that is needed for the error-messages-->
    <asp:Label ID="lbl_header_needed" runat="server" Text="Eine Betreff-Zeile (Überschrift) ist zwingend erforderlich !"></asp:Label>
    <asp:Label ID="lbl_time_from_invalid_format" runat="server" Text="Deine Eingabe für den Start-Termin ist nicht gültig !"></asp:Label>
    <asp:Label ID="lbl_time_to_invalid_format" runat="server" Text="Deine Eingabe für den End-Termin ist nicht gültig !"></asp:Label>
    <asp:Label ID="lbl_missing_from_date" runat="server" Text="Du hast einen End- aber keinen Start-Termin eingegeben !"></asp:Label>
    <asp:Label ID="lbl_from_date_after_to" runat="server" Text="Datumsangaben haben vertauschte Start- und Endangabe !"></asp:Label>
    <asp:Label ID="lbl_latitude_error" runat="server" Text="Der eingegeben Breitengrad ist ungültig !"></asp:Label>
    <asp:Label ID="lbl_longitude_error" runat="server" Text="Der eingegeben Längengrad ist ungültig !"></asp:Label>
    <asp:Label ID="lbl_need_both_coords" runat="server" Text="Es werden beide Angaben für Längen- und Breitengrad benötigt !"></asp:Label>
    <asp:Label ID="msg_no_location_found" runat="server" Text="Du musst deinen Beitrag einem Postleitzahlgebiet zuordnen!<br /><br />Klicke dazu ganz unten auf 'Ort wechseln'"></asp:Label>
    <asp:Label ID="msg_no_location_selected" runat="server" Text="Du hast keinen Ort ausgewählt an dem dein Beitrag veröffentlicht werden soll. <br /><br />Bitte benutze den Button 'Ort wechseln' und wähle ein Ziel für deine Veröffentlichung aus. "></asp:Label>
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
        /*
        * click-handler for the show-preview button
        * 
        *  if button is clicked the webform opens a preview of the enterd data
        *  the user can go back and make corrections
        *  nejoba does not support edition of created items. here user has 
        *  the last chance to change his input
        *
        */
        $("#btn_showPreview").click(function () {
            // alert("click-Handler for #btn_showPreview called.");
            var tmpltTxt = $("#template").html()

            // tmpltTxt = tmpltTxt.replace("§§LOCATIONNAME§§", '<strong>Ort: </strong>' + $("#CoPlaBottom_sel_lctn option:selected").text().trim());

            tmpltTxt = tmpltTxt.replace("§§LOCATIONNAME§§", '<strong>Ort: </strong>' + $('#CoPlaBottom_txbx_location').val().trim());

            var rubric = $("#CoPlaBottom_txbx_itemname").val().trim();
            var dateFrom = $("#CoPlaBottom_txbx_timeFrom").val().trim();
            var dateTo = $("#CoPlaBottom_txbx_timeTo").val().trim();
            var header = $("#CoPlaBottom_txbHeader").val().trim();
            var docum = tinyMCE.activeEditor.getContent().trim();
            // length

            if (rubric.length > 0) { tmpltTxt = tmpltTxt.replace("§§RUBRICNAME§§", '<strong>Rubrik: </strong>' + rubric) }
            else { tmpltTxt = tmpltTxt.replace("§§RUBRICNAME§§", "") };
            if (dateFrom.length > 0) { tmpltTxt = tmpltTxt.replace("§§DATE_FROM§§", '<strong>Start-Termin: </strong>' + dateFrom) }
            else { tmpltTxt = tmpltTxt.replace("§§DATE_FROM§§", "") };
            if (dateTo.length > 0) { tmpltTxt = tmpltTxt.replace("§§DATE_TILL§§", '<strong>End-Termin: </strong>' + dateTo) }
            else { tmpltTxt = tmpltTxt.replace("§§DATE_TILL§§", "") };
            if (header.length > 0) { tmpltTxt = tmpltTxt.replace("§§HEADERTXT§§", '<strong>Kurznachricht: </strong><br/><h2>' + header + '</h2><br /><hr /><br />') }
            else { tmpltTxt = tmpltTxt.replace("§§HEADERTXT§§", "") };
            if (docum.length > 0) { tmpltTxt = tmpltTxt.replace("§§BODYTXT§§", '<strong>Dokument: </strong><br/>' + docum) }
            else { tmpltTxt = tmpltTxt.replace("§§BODYTXT§§", "") };

            $("#messagebox").hide();
            $("#canvas").html(tmpltTxt);
            $("#editpart").hide();
            $("#inspection").show();
        });


        /*
        *  handle autocomplete for 'txbx_city_map'
        *  this control is specific for the debate_editor. used to find an adress with noatim
        *
        */
        cityMapListFromServer = []                 // used as datasource for the bootstrap-typeahead 'txbx_city'
        $('#CoPlaBottom_txbx_city_map').typeahead({
            source: function (query, process) {
                var ajxurl = nejobaUrl(baseUrl + 'ajax/dataSource__city.aspx?')

                console.log('length cityMapListFromServer:' + cityMapListFromServer.length);

                if (cityMapListFromServer.length == 0) {
                    return $.get(ajxurl, { query: query }, function (data) {
                        cityMapListFromServer = JSON.parse(data).options;
                        return process(cityMapListFromServer);
                    });
                }
                else {
                    if (cityMapListFromServer[0].slice(0, 4).toLowerCase() == query.slice(0, 4).toLowerCase()) {
                        return cityMapListFromServer;
                    }
                    else {
                        return $.get(ajxurl, { query: query }, function (data) {
                            cityMapListFromServer = JSON.parse(data).options;
                            return process(cityMapListFromServer);
                        });
                    }
                }
            },
            minLength: 4,
            items: 7
        });


        /*
        * click-handler for the back_To_Edit button
        * 
        *  button is used to go back from preview to the edit-mode
        *  user can make a correction in his input
        */
        $("#btn_backToEdit").click(function () {
            $("#canvas").html('');
            $("#inspection").hide();
            $("#editpart").show();
        });


        
        /*
        * click-handler for chose a rubric
        * 
        *  button has no special function. just closes the carussel
        */
        $("#btn_rubric_choosen").click(function () {
            $("#collapseTwo").collapse('hide');
        });


        /*
        * init controls on the page
        *
        */
        // $("#CoPlaBottom_txtMain").wysihtml5();                                        // bootstrap free editor
        $("#CoPlaBottom_txbx_timeFrom").datepicker($.datepicker.regional["de"]);
        $("#CoPlaBottom_txbx_timeTo").datepicker($.datepicker.regional["de"]);
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


        // get the selected location via javascript
        $("#CoPlaBottom_sel_lctn").change(function () {
            $("#CoPlaBottom_txbx_location_id").val($('#CoPlaBottom_sel_lctn option:selected').val());
            $("#CoPlaBottom_txbx_location_name").val($('#CoPlaBottom_sel_lctn option:selected').text());
            // var valOfSel = $('#CoPlaBottom_sel_lctn option:selected').val();
            // var txtOfSel = $('#CoPlaBottom_sel_lctn option:selected').text();
            // alert("location-ID : " + valOfSel + ' ; placename : ' + txtOfSel);
        });

        /*
         * Viewstate is not working for disabeled controls. this hack shows the last selected reubric in the disabeled ctrl txbx_itemname_1
         *
         */
        $('#CoPlaBottom_txbx_itemname_1').val( $('#CoPlaBottom_txbx_itemname').val() );

        // the openlayer-map will be initiaized
        initMap();

        // prepare the matrix used to select a rubric
        mgr = new MtrxMngr();

    });



</script>
</asp:Content>

