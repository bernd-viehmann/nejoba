<%@ Page Title="Initiative hinzufügen" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="create_map_initiative.aspx.py"  validateRequest="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

<div class="container">
    <!-- Main hero unit for a primary marketing message or call to action -->
    <div class="hero-unit">
        <div class="container-fluid">
            <div class="row-fluid">
                <div class="span3 offset1">
                    <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/240x216_add_user_group.png" ToolTip="Kontaktformular" />
                    </div>
                <div class="span7 offset1">
                    <h4><asp:Label ID="Label2" runat="server" Text="Bügerinitaven und gesellschaftlich Alternativen" /></h4>
                    <br />
                    <br />
                    <div>
                    <label>
                        <asp:Label ID="Label4" runat="server" Text="Trage eine Initiative in einer Region ein." />
                        <br />
                    </label>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <br />

    <div class="row">
        <div class="span4 offset1">
            <asp:Label ID="Label1" runat="server" Text="Der Name der Initiative" />
            <br />
            <asp:TextBox ID="txbx_nickname" runat="server" ToolTip="Die Bezeichnung für den Eintrag auf der Karte" ></asp:TextBox>
            <br />
            <label><asp:Label ID="lbl_type_of_item" runat="server" Text="Art des Eintrages" /></label>
            <asp:DropDownList ID="drpd_item_type" runat="server" ToolTip="Lege fest was Du in die Karte eintragen möchtest." >
                <asp:ListItem Text="Gemeinschaften und Kommunen" Value="communities" />
                <asp:ListItem Text="Politik und Justiz" Value="politics" />
                <asp:ListItem Text="regionales Geld / Wirtschaft" Value="monetary" />
                <asp:ListItem Text="Tauschen und Schenken" Value="giveandswap" />
                <asp:ListItem Text="nachhaltige Unternehmen" Value="sustainable_business" />
                <asp:ListItem Text="alternative Landwirtschaft / Urban Gardening" Value="agriculture" />
                <asp:ListItem Text="Umwelt- und Tierschutz" Value="environmental" />
                <asp:ListItem Text="sonstige Initiativen" Value="initiatives" />
                <asp:ListItem Text="Hilfsorganisationen" Value="charities" />
                <asp:ListItem Text="Vereine und Selbsthilfegruppen" Value="associations" />
            </asp:DropDownList>
        </div>
        <div class="span4">
            <label><asp:Label ID="lbl_whatisthenejobaname" runat="server" Text="<br/>Bezeichne die Markierung auf der Karte mit einem Namen.<br/><br/>Der <strong>Art des Eintrages</strong> bestimmt dabei die Farbe der Markierung." /></label>
        </div>
    </div>
    <br />

    <div class="row">
        <div class="span8 offset1">
            <label><asp:Label ID="Label16" runat="server" Text="Mitteilung" /></label>
            <asp:TextBox ID="txbx_info" class="span8" runat="server" ToolTip="Dieser Text wird auf der Karte angezeigt Es sind 200 Zeichen möglich." TextMode="MultiLine" Rows="8"></asp:TextBox>
        </div>
    </div>
    <br />



    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label15" runat="server" Text="Land" /></label>
            <asp:DropDownList ID="drpd_country" runat="server"  ToolTip="Derzeitig von nejoba unterstüzte Länder">
                <asp:ListItem Text="Belgien" Value="BE" />
                <asp:ListItem Text="Dänemark" Value="DK" />
                <asp:ListItem Text="Deutschland" Value="DE" Selected="True" />
                <asp:ListItem Text="Liechtenstein" Value="LI" />
                <asp:ListItem Text="Luxemburg" Value="LU" />
                <asp:ListItem Text="Niederlande" Value="NL" />
                <asp:ListItem Text="Österreich" Value="AT" />
                <asp:ListItem Text="Polen" Value="PL" />
                <asp:ListItem Text="Tschechien" Value="CZ" />
            </asp:DropDownList>
        </div>

        <div class="span4">
            <label><asp:Label ID="Labeluz1" runat="server" Text="Postleitzahl" /></label>
            <asp:TextBox ID="txbx_postcode" runat="server" ToolTip="Die Postleitzahl muss korrekt sein. Sie entscheidet welche Foren Du standartmäßig nutzen kannst und wo der Marker (zufällig) gesetzt wird." ></asp:TextBox>
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label3" runat="server" Text="E-mail" /></label>
            <asp:TextBox ID="txbx_email" runat="server" ToolTip="EineMailadresse um mit der Initiative in Kontakt zu treten."></asp:TextBox>
        </div>
        <div class="span4">
        </div>
    </div>

    <div class="row">
    </div>

    <div id="messagebox" class="row" runat="server" visible="false" >
        <div>
            <div class="label label-warning span7 offset1">
                <div>
                    <br />
                    <asp:Image ID="warnimage" runat="server" ImageAlign="Left" ImageUrl="~/style/pic/warning.png" />
                    <p style="padding-left:77px;">
                        <asp:Label ID="lbl_messageBox" runat="server" class="" ForeColor="#474747" Text="Kein Fehler zu finden"></asp:Label>
                        <br /><br />
                    </p>
                </div>
            </div>
        </div>
    </div>


    <div class="row">
        <div class="span4 offset1">
            <br /><br />
        </div>
        <div class="span4 offset1">
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label6" runat="server" Text="Profilbild-URL" /></label>
            <asp:TextBox ID="txbx_picturl" runat="server" ToolTip="Freiwillige Angabe: Webadresse für das Profilbild. Das Bild sollte gleiche X- und Y- Größe aufweisen. Beispiel : 512*512 Pixel. Du kannst hier beispielsweise den Link zum zugehörigen Profilbild in einem sozialen Netzwerk eintragen."></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label5" runat="server" Text="Hashtag" /></label>
            <asp:TextBox ID="txbx_hashtag" runat="server" ToolTip="nejoba basiert auf Hashtags. Hier kann ein solches Tag für die Initiative vergeben werden."></asp:TextBox>
        </div>
        <br />
        <div class="span4 offset1">
            <label><asp:Label ID="Label9" runat="server" Text="Website" /></label>
            <asp:TextBox ID="txbx_website" runat="server" ToolTip="Freiwillige Angabe: URL der Internetseite der Initiative"></asp:TextBox>
            <br /><br />
        </div>
        <div class="span4">
            <label><asp:Label ID="Label23" runat="server" Text="Soziales Netzwerk" /></label>
            <asp:TextBox ID="txbx_socialnetwork" runat="server" ToolTip="Freiwillige Angabe: Falls vorhanden nenne die URL der facebook-Gruppe, FB-FanPage oder Google+ Seite."></asp:TextBox>
        </div>
    </div>



    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="lbl_twitterlable" runat="server" Text="twitter-Konto" /></label>
            <asp:TextBox ID="txbx_twitter" runat="server" ToolTip="Freiwillige Angabe: @Twitter-Account des Ansprechpartners"></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label13" runat="server" Text="Skype-Konto" /></label>
            <asp:TextBox ID="txbx_skype" runat="server" ToolTip="Freiwillige Angabe: Skype-Konot des Ansprechpartners"></asp:TextBox>
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label7" runat="server" Text="Mobiltelefon" /></label>
            <asp:TextBox ID="txbx_mobile" runat="server" ToolTip="Freiwillige Angabe: Handy-Nummer des Ansprechpartners"></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label14" runat="server" Text="Telefon" /></label>
            <asp:TextBox ID="txbx_phone" runat="server" ToolTip="Freiwillige Angabe: Festnetz-Nummer des Ansprechpartners"></asp:TextBox>
        </div>
    </div>
    <br /><br /><br />

        <div id="div_coord_inpt" class="row" runat="server">
            <div class="span4 offset1">
                <label><asp:Label ID="Label30" runat="server" Text="Breitengrad" /></label>
                <asp:TextBox ID="txbx_lat" runat="server" ToolTip="Wenn das Feld leer bleibt wird die Markierung zufällig im Postleitzahlgebiet gesetzt. Wenn du die Koordinaten kennst targe diese ein. Beachte das ein PUNKT (.) anstatt einem Komma als dezimales Trennzeichen benutzt werden muss"></asp:TextBox>
            </div>
            <div class="span4">
                <label><asp:Label ID="Label29" runat="server" Text="Längengrad" /></label>
                <asp:TextBox ID="txbx_lon" runat="server" ToolTip="Wenn das Feld leer bleibt wird die Markierung zufällig im Postleitzahlgebiet gesetzt. Wenn du die Koordinaten kennst targe diese ein. Beachte das ein PUNKT (.) anstatt einem Komma als dezimales Trennzeichen benutzt werden muss"></asp:TextBox>
            </div>
            <div class="span8 offset1">
                <asp:HyperLink ID="hyli_mapcoordinates" runat="server" Text="Koordinaten ermitteln" NavigateUrl="http://www.mapcoordinates.net/" Target="_blank" />
            </div>
        </div>

    <br /><br />



    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Laubel3" runat="server" Text="Vorname" /></label>
            <asp:TextBox ID="txbx_forename" runat="server" ToolTip="Optional: Ansprechpartner"></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label10" runat="server" Text="Nachname" /></label>
            <asp:TextBox ID="txbx_familyname" runat="server" ToolTip="Optional: Ansprechpartner"></asp:TextBox>
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label11" runat="server" Text="Straße" /></label>
            <asp:TextBox ID="txbx_street" runat="server" ToolTip="Optional: Postanschrift"></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label12" runat="server" Text="Hausnummer" /></label>
            <asp:TextBox ID="txbx_housenumber" runat="server" ToolTip="Optional: Postanschrift"></asp:TextBox>
        </div>
    </div>
    <br />

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Lubel6" runat="server" Text="Stadt" /></label>
            <asp:TextBox ID="txbx_city" runat="server" ToolTip="Optional: Postanschrift"></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label8" runat="server" Text="Zusatz" /></label>
            <asp:TextBox ID="txbx_adress_add" runat="server" ToolTip="Optional: Postanschrift"></asp:TextBox>
        </div>
    </div>
    <br />

    <div class="row">
        <div class="span4 offset1">
        </div>
    </div>


    <div class="row">
        <div class="span4 offset1">
        </div>
        <div class="span4">
            <asp:Button ID="btn_Create" runat="server" class="btn btn-large btn-primary" Text="Speichern" onclick="HndlrButtonClick" ToolTip="Daten im System speichern."/>
        </div>
    </div>

</div>


    <div style="visibility:hidden;">
    <label><asp:Label ID="Label22" runat="server" Text="Sprache" /></label>
    <asp:DropDownList ID="drpd_language" runat="server" Enabled="false"  ToolTip="Derzeit ist AktiMap nur in deutscher Sprache verfügbar. Daran wird aber gearbeitet.">
        <asp:ListItem Text="deutsch" Value="de" Selected="True" />
        <asp:ListItem Text="niederl&auml;ndisch" Value="nl" />
        <asp:ListItem Text="franz&ouml;sisch" Value="fr" />
        <asp:ListItem Text="polnisch" Value="pl" />
        <asp:ListItem Text="tschechisch" Value="cz" />
        <asp:ListItem Text="d&auml;nisch" Value="dk" />
    </asp:DropDownList>


    </div>

      <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->

<script type="text/javascript">
    $(document).ready(function () {
        $("#CoPlaBottom_txbx_info").wysihtml5();
    }); 
</script>

</asp:Content>

