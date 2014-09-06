<%@ Page Title="Deine nejoba-Aktivitäten" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="user_choose_list.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <div class="row">
        <div class="accordion" id="Div1">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <h4>
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >
                            Aktivitäten
                        </a>
                    </h4>
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
<br />
<br />
<h5>
Dein Leben spielt sich vor deiner Haustüre ab. nejoba verbindet dich mit deinen Nachbarn <br /><br />
</h5>
                    </div>
                </div>
            </div>
        </div>
    </div>

    
    <div class="row">
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="span2 offset1">
            <asp:HyperLink ID="HyperLink3" runat="server" class="btn img-polaroid" ImageUrl="~/style/pic/quatschtuete.png" ToolTip="Themen von dir begonnen." NavigateUrl="~/wbf_account/user_debates_started.aspx" />
            <h4>
                <asp:Label ID="Label3" runat="server" Text="Deine Beiträge" class="muted"></asp:Label>
            </h4>
        </div>
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="span2 offset1">
            <asp:HyperLink ID="HyperLink1" runat="server" class="btn img-polaroid" ImageUrl="~/style/pic/searchHelp.png" ToolTip="Ruft die Liste mit deinen eigenen Arbeitsaufträgen auf." NavigateUrl="~/wbf_account/user_jobs.aspx" />
            <h4>
                <asp:Label ID="Labelds1" runat="server" Text="Ausschreibungen" class="muted"></asp:Label>
            </h4>
        </div>
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="span2 offset1">
            <asp:HyperLink ID="HyperLink2" runat="server" class="btn img-polaroid" ImageUrl="~/style/pic/searchJob.png" ToolTip="Die Liste mit den Aufträgen auf die du geantwortet hast" NavigateUrl="~/wbf_account/user_offers.aspx" />
            <h4>
                <asp:Label ID="Label6" runat="server" Text="Nachfragen" class="muted"></asp:Label>
            </h4>
        </div>
    </div>
    <hr />
</asp:Content>

