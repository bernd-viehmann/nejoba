<%@ Page Title="Online-Hilfe" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="about.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <style type="text/css">
        .style1
        {
            color: #FF0000;
        }
    </style>
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">

      <!-- Main hero unit for a primary marketing message or call to action -->
      <div class="hero-unit">
        <div class="row">
            <div class="span3">
                <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/about_nejoba.png" ToolTip="Über nejoba" />
            </div>
            <div class="span7">
                <h3>
                    <asp:Label ID="lbl_advertisement" runat="server" Text="ne<span class='style1'>jo</span>ba - das neue kostenfreie Nachbarschafts-Netzwerk für regionale private Jobangebote, Dienstleistungen & Kommunikation" />
                    <br /><br /><br />
                </h3>
            </div>
        </div>
      </div>

      <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
      <div class="well">
            <p class="lead"><strong>Was ist ne<span class="style1">jo</span>ba?</strong></p>
            <p class="lead">Wer putzt meine Fenster, wer mäht den Rasen, wer pflegt meine Mutter, wer liest mir etwas vor, wer gibt Nachhilfe, kauft ein, repariert mein Auto, passt auf den Hund auf, repariert mein Haus, putzt die Wohnung und hilft mir im Alter? Diese und andere Fragen beantwortet künftig ne<span class="style1">jo</span>ba.</p>
            <p class="lead">ne<span class="style1">jo</span>ba ist ein regionaler Marktplatz im vorerst deutschsprachigen Raum für private häusliche Arbeitsangebote. Und für alle die möchten, stellt ne<span class="style1">jo</span>ba in einem separaten Bereich eine intelligente Kommunikationsplattform zur Verfügung.</p>
            <p class="lead">Idee ist es, dass Nachbarn in vielerlei Hinsicht zueinander finden. Nachbarn, die einen Dienstleister suchen - sei es bei der Hilfe im Garten, im Haus, bei der Betreuung der Kinder oder bei der Installation des Computers - vergeben auf ne<span class="style1">jo</span>ba ein Arbeitsangebot. Nachbarn, die als Dienstleister Arbeit suchen, finden diese Arbeitsangebote und melden sich beim Anbieter. Ganz nebenbei sorgt ne<span class="style1">jo</span>ba für bessere Kontakte in der Gemeinde.</p>
            <br />
            <p class="lead"><strong>Was ist neu und anders an ne<span class="style1">jo</span>ba?</strong></p>
            <p class="lead">Neben der regionalen Jobsuche nach Postleitzahlen, kann ne<span class="style1">jo</span>ba auch als Sprachrohr der Gemeinde fungieren. Im separaten Bereich "Kommunikation" werden alle auf ne<span class="style1">jo</span>ba eingepflegten Themen einer Postleitzahl und einer damit verbundenen Geo-Koordinate zugewiesen. Damit ist regionale Kommunikation z.B.  im privaten Bereich, für Vereine oder zwischen Kommune und Menschen kinderleicht. Das einfache Auffinden von Themen wird durch das Setzen von Wortmarkierungen (Hashtags) unterstützt. Alle Menschen, Kommunen, Städte, Institutionen und Geschäfte können so mit ihrem geographischen Umfeld, und umgekehrt "Open Data" kommunizieren und es mit Daten und Neuigkeiten versorgen.</p>
            <p class="lead">ne<span class="style1">jo</span>ba ist kostenfrei - für alle, die Arbeit zu vergeben haben, sowie für alle privaten und gewerblichen Dienstleister ohne Mitarbeiter. Dienstleister haben zusätzlich die Möglichkeit, sich durch den Erwerb eines kostenpflichtigen Premium-Zugangs einen Zeitvorteil bei möglichen Aufträgen zu verschaffen. Sie können sich 48 Stunden früher mit den Auftraggebern in Verbindung setzen, wenn jemand z. B. Hilfe im Haus, im Garten oder bei anderen Tätigkeiten sucht.</p>
            <br />
            <p class="lead"><strong>ne<span class="style1">jo</span>ba & Spenden</strong></p>
            <p class="lead">ne<span class="style1">jo</span>ba wird mindestens 50 % (Startphase) eines eventuellen Gewinnes nach Steuern am Ende eines jeden Geschäftsjahres einer gemeinnützigen Organisation zukommen lassen und darüber berichten. Ab einer noch zu bestimmenden Höhe, können die eingetragenen Mitglieder der ne<span class="style1">jo</span>ba-Plattform auch Vorschläge über den Verwendungszweck der Spenden machen.</p>
            <br />
            <p class="lead"><strong>Dafür steht ne<span class="style1">jo</span>ba</strong></p>
            <p class="lead">ne<span class="style1">jo</span>ba schafft neue Jobs, die es vorher nicht gab, leistet einen Beitrag zum Lebensunterhalt, bringt Menschen zusammen, verhindert im günstigsten Fall verfrühte Haushaltsaufgabe, steht für Eigenaktivität und ermöglicht vielleicht einen positiveren Umgang mit der individuellen Lebenssituation.      </p>
      </div> 

      <div>
            <p class="lead">
            <strong>credits:</strong>
            
            
            <asp:HyperLink ID="HyperLink2" runat="server" ImageUrl="../style/pic/ironpython.png" NavigateUrl="http://ironpython.net/" ToolTip="IronPython" Target="_blank" />

            <asp:HyperLink ID="HyperLink6" runat="server" ImageUrl="http://www.openstreetmap.de/img/osm_logo.png" NavigateUrl="http://www.openstreetmap.de/" ToolTip="OpenStreetMap" Target="_blank" />
            <asp:HyperLink ID="HyperLink3" runat="server" ImageUrl="http://www.openlayers.org/images/OpenLayers.trac.png" NavigateUrl="http://openlayers.org/" ToolTip="OpenLayers: Free Maps for the Web" Target="_blank" />
            <asp:HyperLink ID="HyperLink1" runat="server" ImageUrl="../style/marker/credits_map_icons.gif" NavigateUrl="http://mapicons.nicolasmollet.com/" ToolTip="mapicons: nicolas mollet" Target="_blank" />
            </p>
      </div>
    </div><!-- /container -->
</asp:Content>

