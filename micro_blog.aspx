<%@ Page Title="Microblog für deine Stadt" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="micro_blog.aspx.py" %>

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
                            Nachbarforum
                        </a>
                    </h4>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
                            



<h5>Was ist das Nachbarforum ?</h5>
<br />
Beim Nachbarforum handelt es sich um eine regionale Kommunikations- und Informationsbörse. Sie funktioniert wie ein Microblog. Allerdings mit dem Unterschied das nicht ein Mensch einen solchen persönlichen Blog betreibt sondern ein Postleitzahlgebiet.  Diesen Blog teilen sich alle Anwohner oder Besucher dieser Stadt (oder Stadtteils). 
<br /><br />
Auf diese Weise entsteht ein zentraler Sammelpunkt für Informationen und ein neuartiges regionales Kommunikationsmedium. Denn jeder Beitrag im Nachbarforum kann öffentlich diskutiert werden.
<br /><br />
Anschaulich könnte man nejoba mit einer Pinnwand vergleichen, wie sie häufig in Einkaufszentren stehen. 
<br /><br />
Dabei können Beitrag mit einem geographischen Punkt versehen werden um auf einer Karte visualisiert zu werden. Oder man kann einen Termin angeben um z.B. auf eine Veranstaltung hinzuweisen. Über regional gültige Hashtags lassen sich Themenbereiche gruppieren. 
<br /><br /><br />

<h5>Die Bedienung</h5>
<br />
Die grün hinterlegten Links leiten dich auf die Übersichten mit den Beiträgen weiter. Es gibt eine Liste in der alle Beiträge entsprechend der eingestellten Filterung dargestellt werden und eine Karte die die Beiträge darstellt die mit einer geographischen Koordinate markiert sind. Es werden Daten für die Region dargestellt die du auf der Startseite ausgewählt hast.
<br />
Wenn du eine Ansicht aufgerufen hast kannst du die Filterung über das dortige Luppensymbol ändern.
<br /><br />
Die blau hinterlegten Links rufen Seiten auf in denen du nach bestimmten Daten suchen kannst. 
<br /><br />
<strong>Rubriken</strong>
<br /><br />
Verwaltete Themengebiete. Hier können Anzeigen geschaltet werden, man findet Diskussionen zu bestimmten Themengebieten oder spezielle regionale Informationen.
<br /><br />
<strong>Hashtag</strong>
<br /><br />
Ein Hashtag ist ein mit einem ‘#’-Symbol markierten Suchbegriff. Auf diese Weise können Beiträge thematisch gruppiert werden. 
<br /><br />
<strong>Termin</strong>
<br /><br />
Filtere die Daten zu einem bestimmten Tag oder beispielsweise des Wochenendes heraus. So hilft nejoba bei der Freizeitgestaltung und wird zum regionalen Veranstaltungskalender.
<br /><br />

<h5>Dein Leben spielt sich vor deiner Haustüre ab. nejoba verbindet dich mit deinen Nachbarn <br /><br /></h5>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div class="row"><br /></div>



<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div class="row-fluid">
        <div class="span10 offset1">
            <div class="span3">

                <div id ="div4" class="row well label-success" style="color:White;">
                    <h5>
                        <asp:HyperLink ID="hyLnk_showList" runat="server" Text="Liste zeigen" NavigateUrl="projector_DebateList.aspx" style="cursor:pointer;text-decoration:underline;color:White;"/>
                    </h5>
                </div>

                <div id ="div5" class="row well label-success" style="color:White;">
                    <h5>
                        <asp:HyperLink ID="hyLnk_showMap" runat="server" Text="Karte zeigen" NavigateUrl="projector_DebateMap.aspx" style="cursor:pointer;text-decoration:underline;color:White;"/>
                    </h5>
                </div>

                <div id ="div_business" class="row well label-info" style="color:White;">
                    <h5>
                        <asp:HyperLink ID="hyLnk_sarchRubric" runat="server" NavigateUrl="Search_Rubric.aspx" Text="Rubrik suchen" style="cursor:pointer;text-decoration:underline;color:White;"/>
                    </h5>
                </div>

                <div id ="div2" class="row well label-info" style="color:White;">
                    <h5>
                        <asp:HyperLink ID="hyLnk_searchRubric" runat="server" Text="Hashtag suchen" NavigateUrl="Search_Hashtag.aspx" style="cursor:pointer;text-decoration:underline;color:White;"/>
                    </h5>
                </div>

                <div id ="div3" class="row well label-info" style="color:White;">
                    <h5>
                        <asp:HyperLink ID="hyLnk_searchDate" runat="server" Text="Termin suchen" NavigateUrl="Search_Appointment.aspx" style="cursor:pointer;text-decoration:underline;color:White;"/>
                    </h5>
                </div>


            </div>

            <div class="span7 offset1">
                <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/forum_wallpaper.png" />
            </div>
        </div>
    </div>

    <div class="row hidden">
        <asp:Label ID="timeIsNow" runat="server" ></asp:Label> 
    </div>

</asp:Content>

