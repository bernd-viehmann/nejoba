<%@ Page Title="Online-Hilfe" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="help_three.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

<div class="container">
    <!-- Main hero unit for a primary marketing message or call to action -->
    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <!-- # #   Heading                                                                                                                                                                                                     # # # -->
    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div ID="SetUpFiltering" runat="server" class="row hero-unit" visible="true">
        <div class="container-fluid">
            <div class="row-fluid">
                <div class="span3 offset1">
                    <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/hilfe.png" ToolTip="Beginne ein neues Thema" />
                    </div>
                <div class="span7 offset1">
                    <br />
                    <h4><asp:Label ID="Label1" runat="server" Text="nejoba Bedienungsanleitung" /></h4>
                    <br />
                </div>
            </div>
        </div>
        <br /><br />

        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="row">
            <h3>Regionale Themen</h3>
            <br />
            <h5>
            <asp:HyperLink ID="HyperLink1" runat="server" NavigateUrl="http://www.nejoba.net/njb_02/wbf_functs/show_for_stranger.aspx?item=5182ad5de444b6385c33dd74" Target="_blank" >Eine Pinnwand finden und das Forum verwenden</asp:HyperLink>
            <br />
            </h5>
            <small>
                <asp:Label ID="Label2" runat="server" Text="Die regionale Pinnwand für Deine Stadt aufrufen." />
            </small>
            <br /><br /><br />

            <h5>
            <asp:HyperLink ID="HyperLink2" runat="server" NavigateUrl="http://www.nejoba.net/njb_02/wbf_functs/show_for_stranger.aspx?item=5182b0f3e444b6385c33dd76" Target="_blank" >Ein Benutzerkonto erstellen</asp:HyperLink>
            <br />
            </h5>
            <small>
                <asp:Label ID="Label3" runat="server" Text="Melde Dich an um selbst etwas veröffentlichen zu können." />
            </small>
            <br /><br /><br />

            <h5>
            <asp:HyperLink ID="HyperLink3" runat="server" NavigateUrl="http://www.nejoba.net/njb_02/wbf_functs/show_for_stranger.aspx?item=5182b406e444b6385c33dd78" Target="_blank" >Einen Beitrag auf nejoba veröffentlichen</asp:HyperLink>
            <br />
            </h5>
            <small>
                <asp:Label ID="Label4" runat="server" Text="Einen Beitrag erstellen und seine Nachbarn informieren." />
            </small>
            <br /><br /><br />

            <h5>
            <asp:HyperLink ID="HyperLink4" runat="server" NavigateUrl="http://www.nejoba.net/njb_02/wbf_functs/show_for_stranger.aspx?item=5182b6fce444b6385c33dd7a" Target="_blank" >Regionale Themen durchstöbern</asp:HyperLink>
            <br />
            </h5>
            <small>
                <asp:Label ID="Label5" runat="server" Text="Herausfinden welche Themen in einer Stadt besprochen werden." />
            </small>
            <br /><br /><br /><br /><br /><br />

            <label>
            Unsere Plattform bietet ein öffentliches Diskussionsforum mit regionalem Bezug. Dafür nutzt nejoba sogenannten Hashtags. Unsere Nachrichten sind auf diese Weise thematisch und geographisch sortiert.
            Wenn du willst, kannst du über nejoba auf diese Weise mit deiner Nachbarschaft in Kontakt treten. Spreche deine Nachbarn an und teile ihnen mit, was dir am Herzen liegt. Verabredet dich, plane soziale Aktivitäten, organisiere deinen Verein oder finde Nachbarn mit ähnlichen Interessen. 
            </label>
            <br />

            <label>
            nejoba ermöglicht Bilder und Videos in eine Nachricht einzubinden. Du kannst Links auf andere Webseiten einbauen. Jeder Nutzer kann außerdem öffentlich auf dein Thema antworten oder einen Beitrag verfassen. Hierdurch ist ein öffentliches Diskussionsforum realisiert, das immer regional ausgerichtet ist.
            </label>
            <br />

            <label>
            Die Funktion könnte man als virtuelle Versammlung im Internet verstehen.  
            </label>
            <br />

            <label>
            Zum Beispiel: Unter dem Tag ‘#Schillerstraße’ würden die Bewohner der Schillerstraße Meldungen zu ihrer Straße finden. Das Tag '#hundehalter' vernetzt Hundebesitzer einer Stadt miteinander. Oder du benutzt den namen deines Vereins, um alle Mitglieder mit den neusten Infos zu versorgen.
            </label>
            <br />

            <label>
            Auf die gleiche Weise lassen sich beliebige Initiativen in einer Stadt organisieren und die Kommunikation unter den Teilnehmern vereinfachen. Dabei kann jedes veröffentlichte Thema von den Mitmenschen der jeweiligen Umgebung öffentlich debattiert werden.
            </label>
            <br />

            <br /><br />
            <label><strong>
            Erstellen eines neuen regionalen Themas
            </strong></label>
            <br />

            <ol>
                <li>Wähle in der oberen schwarzen Menuleiste Funktionen aus</li>
                <li>Unter dem Unterpunkt Themen diskutieren sind die Funktion zur regionalen Vernetzung aufrufbar</li>
                <li>Um ein neues regionales Thema zu erstellen musst du über ein Benutzerkonto verfügen und mit diesem in nejoba engeloggt sein.</li>
                <li>Klicke auf den Unterpunkt Funktionen->Neues Thema  </li>
                <li>Unter Ort wähle bitte einen Ort in deiner Nachbarschaft aus, auf den sich dein Anliegen bezieht</li>
                <li>Die Kurzmeldung wird später bei Suchanfragen in der Ergebnissliste angezeigt. Der Texteditor bietet dir die Möglichkeit Bilder, Filme und typographische Elemente einzufügen.</li>
            </ol>
            <br /><br />

            <label><strong>
            Was sind Hashtags und wie verwende ich sie?
            </strong></label>
            <br />

            <label>
            Neben dem Ort, den du in der Auswahlliste selektiert hast, sortiert nejoba die Themen nach sogenannten Hashtags. Das sind Stichworte, mit denen die verschiedenen Meldungen zu einem Ort thematisch grupppiert werden.
            </label>
            <br />

            <label>
            Setze einfach ein “#”-Zeichen an den Anfang eines Wortes. Egal, ob in der Überschrift oder im Text, nejoba wird dieses Wort zur thematischen Sortierung verwenden. Ein Tag muss immer ein Wort sein.
            </label>
            <br />

            <label>
            Es sind mehrere Hashtags in einem Text erlaubt. Während der Testphase auf unserem kleinen Server unterstützt nejoba maximal 5 Tags in einer Nachricht.
            </label>
            <br />

            <label>
            Das war es schon. Drücke zum Abschluss auf “Beitrag veröffentlichen” und schon ist ein neues Thema für deine Stadt veröffentlicht.        
            </label>

            <br /><br /><br />

            <label><strong>
            Themen abonnieren
            </strong></label>

            <label>
            Wenn du ein Thema oder eine Debatte verfolgen möchtest, wäre es mühsam, sie über einen Stichwortsuche immer neu zu suchen. Daher bietet nejoba die Möglichkeit, Themen zu abonnieren. Setze einfach das unscheinbare Häkchen in der Titelzeile einer Nachricht.
            </label>
            <br />

            <label>
            Von da an findest du diese Thema unter “Dein Konto->Themen->Abonnierte Themen” und nejoba schickt dir eine Mail mit Link auf die Debatte, sobald jemand dem Thema ein Beitrag hinzufügt......
            </label>
            <br />


        </div> 
    </div>
</div><!-- /container -->

</asp:Content>

