<%@ Page Title="Online-Hilfe" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="help_one.aspx.py" %>

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
                    <label><asp:Label ID="Label2" runat="server" Text="<strong>Grundsätzliches:</strong> Wenn du irgendwo nicht weiter kommst, weder vor noch zurück, klicke in der oberen Funktionsleiste auf 'Startseite' und mach es noch einmal, oder melde dich neu an. Nicht jeder Browser unterstützt die 'Zurück-Taste', d.h., du musst dich im Menü von nejoba zurecht finden. Beachte die Hinweise auf jeder Seite, das hilft. Du kannst diese Bedienungsanleitung auch als PDF-Datei runterladen, ausdrucken und Schritt für Schritt anwenden." /></label>
                </div>
            </div>
        </div>
        <br /><br />

        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="row">
            <br />
            <strong>Ich habe Arbeit zu vergeben (Auftrag einsetzen)</strong>
            <br /><br />
            <ol>
                <li>Gehe auf die nejoba-Startseite und klicke auf den ersten großen Button mit der Lupe und dem roten "HELP", dann öffnet sich die Seite mit der Arbeitsmatrix.</li>
                <li>In der Arbeitsmatrix suchst Du dir einen Bereich aus, in dem du Hilfe suchst. Hier klickst du eine der roten Überschriften an. Du kannst immer nur eine Arbeit vergeben, bei mehreren Arbeiten wiederholt sich dieser Ablauf jeweils.</li>
                <li>Nun musst du dich mit deinem Benutzernamen und deinem Passwort einloggen. Hast du dich vorher schon eingeloggt, gelangst du automatisch auf die Seite "Arbeit vergeben". Hast du noch keine Zugangsdaten, drücke den Button "Konto erstellen". Hier kannst du dich einfach und schnell als neuer Nutzer anmelden.</li>
                <li>Nun bist du fast am Ziel.  Auf der Seite "Arbeit vergeben" wählst du den von dir gewünschten Arbeitsbereich, in dem du Hilfe benötigst. Überprüfe die korrekte Postleitzahl. Erkläre in der Überschriftenzeile kurz, worum es geht. Solltest du mehr Platz für eine genaue Beschreibung benötigen, steht dir noch das untere größere Dialogfeld zur Verfügung. Wenn du alles aufgeschrieben hast, betätige den Button "Arbeit vergeben". Nun steht dein Arbeitsauftrag im System und kann von den Arbeitsuchenden in deiner Region bedient werden. In den ersten 48 Stunden kann der Arbeitsauftrag nur von Premium-Mitgliedern bedient werden. Weder deine persönlichen Daten noch deine E-Mailadresse sind sichtbar, lediglich der von dir gewählte (Phantasie) Name, unter dem du in nejoba auftreten möchtest.
                Sobald jemand deine Arbeit erledigen möchte, bekommst du eine E-Mail. Antwortest du auf diese Mail, kann der Interessent deine Mailadresse auch sehen. Sollte deine Mailadresse deinen Namen enthalten, obwohl du an dieser Stelle noch anonym bleiben möchtest, so wähle für die Nutzung von nejoba eine Phantasie-Mailadresse aus.
                Ihr könnt euch per E-Mail verständigen, bis ihr euch, im günstigsten Fall, einig geworden seid. Nun tauscht ihr eure weiteren Kontaktdaten aus, die zur Erledigung des Jobs erforderlich sind.</li>
                <li>Du hast die Möglichkeit, deine Arbeitsangebote einzusehen und falls erforderlich zu löschen. Wenn Du angemeldet bist, klicke in der oberen Menüleiste auf „Startseite“, dann klicke auf den Button „ GO“. Nun kannst Du Deine Arbeitsangebote einsehen.  Gehe  auf den Arbeitsauftrag, den du löschen möchtest und als letztes einen Klick auf das Symbol mit der Mülltonne. Bei regelmäßig wiederkehrenden Arbeiten, kannst du deinen Auftrag einfach stehen lassen.</li>
                <li>Sollten sich dennoch Probleme ergeben, auf jeder nejoba-Seite findest du am unteren Rand einen Hinweis mit "Kontakt". Öffne die Seite, teile uns dein Problem mit und klicke unten links den roten Button "Senden", wir melden uns dann bei dir.</li>
                <li>Für dich ist die Nutzung von nejoba mit keinerlei Kosten verbunden. Kosten entstehen lediglich bei Nutzung des Premium-Zugangs, welcher jedoch nur für Arbeitsuchende vorgesehen ist.</li>
                <li>nejoba wird mindestens 50 % (Startphase) eines eventuellen Gewinnes nach Steuern, am Ende eines jeden Geschäftsjahres einer gemeinnützigen Organisation zukommen lassen und darüber berichten. Ab einer noch zu bestimmenden Höhe, können die eingetragenen Mitglieder der nejoba-Plattform auch Vorschläge über den Verwendungszweck der Spenden machen.</li>
            </ol>
        </div> 
    </div>
</div><!-- /container -->

</asp:Content>

