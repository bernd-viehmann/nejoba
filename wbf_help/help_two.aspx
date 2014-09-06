<%@ Page Title="Online-Hilfe" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="help_two.aspx.py" %>

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
                    <label><asp:Label ID="Label2" runat="server" Text="Wenn du irgendwo nicht weiter kommst, weder vor noch zurück, drücke in der oberen Funktionsleiste auf Startseite und mach es noch einmal, oder melde dich neu an. Nicht jeder Browser unterstützt die Zurück-Taste, d.h., du musst dich innerhalb des nejoba-Menüs zurecht finden. Beachte die Hinweise auf jeder Seite, das hilft. Du kannst diese Bedienungsanleitung auch als PDF-Datei runterladen, ausdrucken und Schritt für Schritt anwenden." /></label>
                </div>
            </div>
        </div>
        <br /><br />

        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="row">
            <br />
            <strong>Ich suche Arbeit</strong>
            <br /><br />
            <ol>
                <li>Gehe auf die nejoba-Startseite und klicke auf den zweiten großen Button mit dem grünen Schriftzug  "JOB", dann öffnet sich die Seite mit der Arbeitsmatrix. (Hier kannst du dich auch über den 48-Stunden Vorsprung informieren).</li>
                <li>In der Arbeitsmatrix suchst du dir einen Bereich aus, der deinen Fähigkeiten entspricht. Hier klickst du eine der roten Überschriften an.</li>
                <li>Nun musst du dich mit deinem Benutzernamen und deinem Passwort anmelden. Hast du dich vorher schon eingeloggt, gelangst du automatisch auf die Seite "Arbeit suchen". Hast du noch keine Zugangsdaten, drücke den Button "Konto erstellen". Hier kannst du dich einfach und schnell als neuer Nutzer anmelden.
                Auf der Seite "Arbeit suchen"  wählst du deinen Arbeitsbereich aus. Möchtest du dir alle Jobangebote aus allen Bereichen in deiner Nähe anschauen, wähle unter Arbeitsbereich  "bitte wählen" aus. Nun gib unter "Postleitzahl" deine Postleitzahl ein. Das Programm zeigt dir automatisch alle Jobangebote im Umkreis von ca. 25 Kilometern an. (Gib nejoba ein wenig Zeit, bis sich in der Anfangsphase genügend Angebote angesammelt haben).
                Nun drücke den Button "Arbeit suchen".</li>
                <li>Jetzt erscheinen, soweit schon vorhanden, Arbeitsangebote in deiner Nähe. Klicke in ein für dich interessantes Angebot hinein. Es erscheint der Button "Kontakt aufnehmen", klicke ihn an. Im folgenden Dialogfeld kannst du unter "deine Nachricht an den Auftraggeber" mit dem Auftraggeber kommunizieren. Hier kannst du Fragen zu dem jeweiligen Jobangebot stellen oder direkt ein Angebot zur Erledigung der Arbeit übersenden. Sobald du dich auf ein Jobangebot über nejoba meldest, kann der Jobanbieter deine Mailadresse sehen und ihr könnt kommunizieren, bis ihr euch einig geworden seid. (Sollte deine Mailadresse deinen Namen enthalten, obwohl du an dieser Stelle noch anonym bleiben möchtest, so wähle für die Nutzung von nejoba eine Phantasie-Mailadresse aus.) Nun tauscht ihr die erforderlichen Kontaktdaten zur Erledigung des Jobs aus.</li>
                <li>Du kannst deine Angebote an Auftraggeber einsehen und falls erforderlich wieder löschen. Wenn Du angemeldet bist, klicke in der oberen Menüleiste auf „Startseite“, dann klicke auf den Button „ GO“. Nun kannst du deine Antworten auf Jobangebote einsehen, indem du auf das Zeichen für "Liste" klickst.
                Möchtest du deine Antwort auf den Arbeitsauftrag löschen, klicke auf das Symbol  mit der Mülltonne.</li>
                <li>Bist du privater Dienstleister oder Gewerbetreibender ohne Mitarbeiter, ist die Nutzung von nejoba grundsätzlich kostenfrei.
                Dienstleister haben zusätzlich die Möglichkeit, sich durch den Erwerb eines Premium-Accounts einen Zeitvorteil bei möglichen Aufträgen zu verschaffen. Premium-Mitglieder können sich 48 Stunden früher auf einen neu eingestellten Arbeitsauftrag mit dem  Auftraggebern in Verbindung setzen, wenn jemand z. B. Hilfe im Haus, im Garten oder bei anderen Tätigkeiten sucht.
                Hast du Mitarbeiter, oder möchtest du den 48-Stunden Vorsprung nutzen, ist ein Premium-Zugang erforderlich. Um die Modalitäten zu erfahren, klickst du in der oberen Menüleiste auf „Startseite“, dann klicke auf den Button „48H“ mit der Stoppuhr und du kannst dich ausführlich informieren. Das funktioniert natürlich nur, wenn du angemeldet bist.</li>
                <li>nejoba wird mindestens 50 % von einem eventuellen Gewinn nach Steuern, am Ende eines jeden Geschäftsjahres, einer gemeinnützigen Organisation zukommen lassen und darüber berichten. Ab einer noch zu bestimmenden Höhe, können die eingetragenen Mitglieder der nejoba-Plattform auch Vorschläge über den Verwendungszweck der Spenden machen.</li>
            </ol>
        </div> 
    </div>
</div><!-- /container -->

</asp:Content>

