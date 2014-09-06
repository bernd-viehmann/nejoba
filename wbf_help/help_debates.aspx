<%@ Page Title="Online-Hilfe" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="help_debates.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

<div class="container span10">

<h3>Das Nachbarforum</h3>
<br /><br />

<div class="well">
    <h5>Was ist das Nachbarforum?</h5>
    <br />
    <iframe width="480" height="360" src="//www.youtube.com/embed/42sYJAE6VbI" frameborder="0" allowfullscreen></iframe>
    <br /><br />
    Das Nachbarforum ist ein Sammelbecken für alle denkbaren Informationen einer Stadt. Eine Art regionales Twitter mit erweiterten Möglichkeiten. 
    <br /><br />
    Jedermann, der Informationen über seine Stadt veröffentlichen möchte, findet in nejoba die geeignete Plattform. Es ist möglich interessante Orte auf der Karte einzutragen, Termine oder Events zu veröffentlichen, regional über alle denkbaren Themen zu diskutieren oder auf Angebote hinzuweisen. Egal ob gewerblich oder privat. 
    <br /><br />
    <strong>
    nejoba erleichtert dir den Überblick über deine Stadt. 
    <br />
    Effizienter und einfacher als mit herkömmlichen Suchmaschinen oder sozialen Netzwerken.
    </strong>
    <br />
</div>

<div class="well">
    <h5>Wie funktioniert das Nachbarforum?</h5>
    <br />
    <iframe width="480" height="360" src="//www.youtube.com/embed/m5Kg7KOVaYU" frameborder="0" allowfullscreen></iframe>
    <br /><br />
    nejoba ermöglicht das Erstellen von Dokumenten, die einem Postleitzahlgebiet zugeordnet werden. So haben die Informationen immer einen regionalen Bezug. Außerdem haben die Dokumente im Nachbarforum folgende Eigenschaften:
    <br /><br />
    <strong>regionale Themen (Hashtags)</strong>
    <br />
    Über markierte Worte ( sogn. Hashtags ) können die Dokumente einem Themenbereich zugeordnet werden. Diese Themen gehören immer genau zu dem Gebiet zu dem auch das Dokument gehört.
    <br /><br />
    <strong>Rubriken</strong>
    <br />
    Wie der Kleinanzeigenteil einer Zeitung können im Nachbarforum Dokumente in vorgegeben Rubriken sortiert werden.
    <br /><br />
    <strong>Ortsmarkierung</strong>
    <br />
    Zu einem Dokument kann man einen Punkt auf der Karte markieren. So können Veranstalltungsorte oder sehenswerte Plätze übersichtlich dargestellt werden.
    <br /><br />
    <strong>Termine</strong>
    <br />
    Jedes Dokument kann einem Datum oder einem Bereich von mehreren Tagen zugeordnet werden. So können Veranstaltungen an einem bestimmten Tag leicht gefunden werden. Was am Wochenende abgeht erfährt man auf nejoba mit wenigen Klicks.
    <br />
</div>

<div class="well">
    <h5>Bedienung</h5>
    <br />
    <p>
        <strong>1. Sich auf dem Nachbarforum informieren.</strong>
        <br /><br />
        <img src="pics/pict000.jpg" class="img-polaroid">
        <br /><br />
        Wenn man die Seite <asp:HyperLink ID="HyperLink2" runat="server" NavigateUrl="http://www.nejoba.net" Target="_blank">www.nejoba.net</asp:HyperLink> aufruft gelangt man zur Kartenansicht. Hier werden alle Daten die mit einem Ort verknüpft sind auf einer Karte dargestellt. Wenn man auf eine Markierung klickt öffnet sich ein Fenster mit der Betreffzeile des Eintrags. Diese kann wiederum angeklickt werden um den eigentlichen Beitrag zu öffnen.
        <br /><br />
        <hr />
        <img src="pics/pict01.jpg" class="img-polaroid">
        <br /><br />
        Nejoba zeigt zuerst immer die Daten an, die zuletzt angelegt wurden. Dabei wird aus Gründen der Übersichtlichkeit nur ein Teil angezeigt. Um durch das Angebot zu blättern findest du oben links auf der Karte Buttons.
        <br />
        Die Buttons, die mit Pfeilen gekennzeichnet sind, werden für das Blättern durch die Daten benutzt.  Der Pfeil-nach-links wechselt zur nächsten Ansicht mit den älteren Daten. Der Pfeil-nach-rechts blättert in die andere Richtung, also zu den neueren Beiträgen.
        <br /><br />
        <hr />

        <img src="pics/pict02.jpg" class="img-polaroid">
        <br /><br />
        Standartmäßig zeigt die Karte alles an was im System gespeichert ist.Um die Suche zu spezifizieren gibt es einen Button mit Lupensymbol. Er öffnet ein neues Fenster. 
        <br /><br /><br /><br />
        <h5>Suche benutzen</h5>
        <br /><br />

        <strong>1. Ort</strong>
        <br /><br />
        <img src="pics/pict03.jpg" class="img-polaroid">
        <br />
        Um zu den Daten für deine Stadt zu gelangen wähle hier dein Land aus und gib deine  Postleitzahl ein. Es ist auch möglich nur das Land zu wählen um Daten überregional angezeigt zu bekommen. Wenn ‘alle vorhandenen Länder’ gewählt wird spielt der Ort bei der Suche keine Rolle.
        <br /><br />

        <strong>2. Termin</strong>
        <br /><br />
        <img src="pics/pict04.jpg" class="img-polaroid"><br />
        Du kannst ein Startdatum und End-Datum angeben. nejoba zeigt dann die Daten innerhalb des von dir gewählten Bereichs. Wenn du nur das Startdatum angibst zeigt nejoba die passenden Events für diesen Tag an. 
        <br /><br />

        <strong>3. Thema</strong>
        <br /><br />
        <img src="pics/pict05.jpg" class="img-polaroid">
        <br />
        In nejoba können <asp:HyperLink ID="HyperLink1" runat="server" NavigateUrl="http://de.wikipedia.org/wiki/Hashtag" Target="_blank">Hashtags</asp:HyperLink> benutzt werden um Daten zu gruppieren. Wenn du diese Option in Verbindung mit der Postleitzahl suchst findet nejoba nur die regionalen Themenbeiträge. Weitere Informationen zu regionalen Themen findest Du auf dem nejoba-<asp:HyperLink ID="HyperLink3" runat="server" NavigateUrl="http://www.youtube.com/user/nejobavideo?feature=guide" Target="_blank">YouTube</asp:HyperLink> Kanal.
        <br /><br />

        <strong>4. Rubrik</strong>
        <br /><br />
        <img src="pics/pict06.jpg" class="img-polaroid">
        <br />
        Hier kannst du nach vorgefertigten Themengebieten suchen. Klicke auf den Button mit den Sprechblasen und es öffnet sich die Rubrikauswahl. Falls vorhanden werden bei jeder für die Suche gewählten Rubrik auch die Beiträge gefunden die zu den Unterrubriken gehören. Wenn du also einen Oberbegriff wählst zeigt nejoba auch alle Unterbegriffe an.
        <br /><br />
        Wenn Du fertig bist drücke den “Suchen-Button”. Alle Such-Parameter die du in dem Dialog eingestellt hast werden genutzt. Wenn nejoba nichts findet kannst du mit löschen alle Suchparameter wieder zurück setzen.
        <br /><br />
        <br /><br />
        <h5>Suche wiederverwenden </h5>
        <br /><br />
        <img src="pics/pict07.jpg" class="img-polaroid">
        <br />
        <img src="pics/pict08.jpg" class="img-polaroid">
        <br />
        Um die Einstellungen der Suche wieder zu verwenden kann man nejoba einen Link erstellen lassen. Diesen kann man als Lesezeichen verwenden oder in sozialen Netzwerken posten. Dafür gibt es den Lesezeichen-Button. Wenn er gedrückt wird öffnet sich ein Fenster mit dem Spezial-Link. Klicke mit der rechten Mauszeile auf den Link um ihn zu kopieren oder ein Lesezeichen hinzu zu fügen.
        <br /><br />

        <strong>Liste oder Karte verwenden</strong>
        <br /><br />
        <img src="pics/pict09.jpg" class="img-polaroid">
        <br />
        Neben dem Lesezeichen-Button befindet sich ein Button zum Wechseln in die jeweils andere Ansicht. Wenn du dich auf der Karte befindest öffnet der Button die Liste und umgekehrt. Dabei werden deine Einstellungen aus dem Suchfenster in die andere Ansicht übertragen.
        <br /><br />

        Die Listenansicht wird genau wie die Karte bedient. Im Unterschied werden hier aber auch Daten angezeigt, die nicht mit einem Ort verknüpft sind. Um einen Beitrag zu öffnen klicke einfach auf die Kurzmeldung.
    </p>
</div>


<div class="well">
    <strong>
        <asp:HyperLink ID="HyperLink4" runat="server" NavigateUrl="help_debates_edit_new_item.aspx">Wie erstellt man einen eigenen Beitrag ?</asp:HyperLink>
    </strong>
    <br />
</div>



</div>

<!-- /container -->

</asp:Content>

