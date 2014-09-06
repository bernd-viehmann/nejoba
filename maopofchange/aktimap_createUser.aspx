<%@ Page Title="Anmeldung" Language="IronPython" CodeFile="aktimap_createUser.aspx.py" Inherits="Microsoft.Scripting.AspNet.UI.ScriptPage" EnableEventValidation="true"%>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">

<head id="Head1" runat="server">
    <meta charset="utf-8" />
    <title>...nejoba</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="" />
    <meta name="author" content="" />
    <!-- Le styles -->

    <link href="http://ajax.aspnetcdn.com/ajax/bootstrap/2.3.2/css/bootstrap.css" rel="stylesheet" type="text/css" />
    <link href="http://ajax.aspnetcdn.com/ajax/bootstrap/2.3.2/css/bootstrap-responsive.css" rel="stylesheet" type="text/css" />
    <link href="~/style/Default.css" rel="stylesheet" type="text/css" />

    
    <script type="text/javascript" src="../style/jquery-1.10.2.min.js"></script>
    <script type="text/javascript" src="../style/jqueryui/js/jquery-ui-1.8.23.custom.min.js"></script>
    <script type="text/javascript" src="http://ajax.aspnetcdn.com/ajax/bootstrap/2.3.2/bootstrap.min.js"></script>

</head>

<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  -->
<body>
    <form id="form1" runat="server">

    <!-- header to show the selction for area and typ of jobs -->
    <div class="row well">
        <div class="span4 offset1">
        <h4>
            <asp:Label ID="lbl_headline" runat="server" Text="Benutzerkonto erstellen" />
        </h4>
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <asp:Label ID="Label1" runat="server" Text="Wähle ein Synonym" />
            <br />
            <asp:TextBox ID="txbx_nickname" runat="server" ToolTip="Die Bezeichnung für Deinen Eintrag auf der Karte" ></asp:TextBox>
            <br />
            <label><asp:Label ID="lbl_type_of_item" runat="server" Text="Art des Eintrages" /></label>
            <asp:DropDownList ID="drpd_item_type" runat="server" ToolTip="Lege fest was Du in die Karte eintragen möchtest." >
                <asp:ListItem Text="Mensch" Value="human" Selected="True" />
                <asp:ListItem Text="Initiative" Value="action" />
            </asp:DropDownList>

        </div>
        <div class="span4">
            <label><asp:Label ID="lbl_whatisthenejobaname" runat="server" Text="Bezeichne die Markierung auf der Karte mit einem Namen und einem Info-Text. <br />Wenn Du noch kein Konto auf AktiMap hast musst Du Dich zunächst als Mensch vorstellen. Danach kannst Du auch Aktivitäten oder Aktionen eintragen." /></label>
        </div>
    </div>
    <br />

    <div class="row">
        <div class="span8 offset1">
            <label><asp:Label ID="Label16" runat="server" Text="Mitteilung" /></label>
            <asp:TextBox ID="txbx_info" Width="79%" runat="server" ToolTip="Dieser Text wird auf der Karte angezeigt Es sind 200 Zeichen möglich." TextMode="MultiLine"></asp:TextBox>
        </div>
    </div>
    <br />



    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label15" runat="server" Text="Land" /></label>
            <asp:DropDownList ID="drpd_country" runat="server"  ToolTip="Derzeit ist AktiMap nur in deutscher Sprache verfügbar. Daran wird aber gearbeitet.">
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
    </div>

    <div class="row">
        <div class="span8 offset1">
            <label><asp:Label ID="Label2" runat="server" Text="Postleitzahl" /></label>
            <asp:TextBox ID="txbx_postcode" runat="server" ToolTip="Die Postleitzahl muss korrekt sein damit Dein Account funktioniert. Sie entscheidet welche Foren Du als Standart nutzen wirst." ></asp:TextBox>
        </div>
    </div>
    <br />


    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label3" runat="server" Text="E-mail" /></label>
            <asp:TextBox ID="txbx_email" runat="server" ToolTip="Die Mailadresse wird für den LogIn benötigt. Deshalb kann sie immer nur einmal im System verwendet werden."></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label19" runat="server" Text="E-Mail Best&auml;tigung" /></label>
            <asp:TextBox ID="txbx_emailconfirm" runat="server" ToolTip="Die Mailadresse wird für den LogIn benötigt. Deshalb kann sie immer nur einmal im System verwendet werden."></asp:TextBox>
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label17" runat="server" Text="Passwort" /></label>
            <asp:TextBox ID="txbx_pwd1" runat="server" TextMode="Password"></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label18" runat="server" Text="Passwortbestätigung" /></label>
            <asp:TextBox ID="txbx_pwd2" runat="server" TextMode="Password"></asp:TextBox>
        </div>
    </div>

    <br />

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
    <br /><br />


    <div class="row">
        <div class="span4 offset1">
            <asp:CheckBox ID="ckbx_accept_privacy_statement" CssClass="pull-right" runat="server" ToolTip="Das akzeptieren der DS-Bedingungen ist zwingend erforderlich ehe Du Daten eintragen kannst."/>
            <asp:Label ID="Label21" runat="server" Text="Erteile Dein Einverständniss zu den " />
            <br />
            <asp:HyperLink ID="hylnk_privacyprotection" runat="server" Text="Datenschutzbestimmungen" NavigateUrl="~/wbf_info/privacy_protection.aspx" Target="_blank"  />
        </div>
        <div class="span4">
            <asp:Button ID="btn_Create" runat="server" class="btn btn-large btn-primary" Text="Speichern" onclick="HndlrButtonClick" ToolTip="Daten im System speichern."/>
        </div>
    </div>
    <br /><br /><br /><br />

    
    <hr />

    <div class="row">
        <div class="span4 offset1">
            <br /><br />
        </div>
        <div class="span4 offset1">
        </div>
    </div>

    <div class="row">
        <div class="span10 offset1">
            <label><asp:Label ID="Label20" runat="server" Text="Die folgenden Angaben sind freiwillig. Wenn Du etwas einträgst wird es öffentlich dargestellt." /></label>
            <br />
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label9" runat="server" Text="Website" /></label>
            <asp:TextBox ID="txbx_website" runat="server" ToolTip="Freiwillige Angabe: Die Adresse Deiner Website"></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label6" runat="server" Text="Profilbild-URL" /></label>
            <asp:TextBox ID="txbx_picturl" runat="server" ToolTip="Freiwillige Angabe: Webadresse für das Profilbild. Das Bild sollte gleiche X- und Y- Größe aufweisen. Beispiel : 512*512 Pixel. Du kannst hier beispielsweise den Link zu Deinem facebook-Profilbild eintragen."></asp:TextBox>
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label23" runat="server" Text="facebook Profil-URL" /></label>
            <asp:TextBox ID="txbx_facebook" runat="server" ToolTip="Freiwillige Angabe: Veröffentliche hier Dein facebook-Profil"></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label24" runat="server" Text="google+ Profil-URL" /></label>
            <asp:TextBox ID="txbx_google_plus" runat="server" ToolTip="Freiwillige Angabe: Veröffentliche hier Dein google+ Profil"></asp:TextBox>
        </div>
    </div>


    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="lbl_twitterlable" runat="server" Text="twitter-Konto" /></label>
            <asp:TextBox ID="txbx_twitter" runat="server" ToolTip="Freiwillige Angabe: Wie ist der Name von deinem  @Twitter-Account."></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label13" runat="server" Text="Skype-Konto" /></label>
            <asp:TextBox ID="txbx_skype" runat="server" ToolTip="Freiwillige Angabe: Kann man Dich mit Skype erreichen"></asp:TextBox>
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label7" runat="server" Text="Mobiltelefon" /></label>
            <asp:TextBox ID="txbx_mobile" runat="server" ToolTip="Freiwillige Angabe: Deine Handy-Nummer."></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label14" runat="server" Text="Telefon" /></label>
            <asp:TextBox ID="txbx_phone" runat="server" ToolTip="Freiwillige Angabe: Deine Rufnummer im Festnetz."></asp:TextBox>
        </div>
    </div>

    <div class="row"><div class="span4 offset1"><br /><br /></div></div>






    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label4" runat="server" Text="Vorname" /></label>
            <asp:TextBox ID="txbx_forename" runat="server" ToolTip="Freiwillige Angabe."></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label10" runat="server" Text="Nachname" /></label>
            <asp:TextBox ID="txbx_familyname" runat="server" ToolTip="Freiwillige Angabe."></asp:TextBox>
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label11" runat="server" Text="Straße" /></label>
            <asp:TextBox ID="txbx_street" runat="server" ToolTip="Freiwillige Angabe."></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label12" runat="server" Text="Hausnummer" /></label>
            <asp:TextBox ID="txbx_housenumber" runat="server" ToolTip="Freiwillige Angabe."></asp:TextBox>
        </div>
    </div>
    <br />

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label5" runat="server" Text="Stadt" /></label>
            <asp:TextBox ID="txbx_city" runat="server" ToolTip="Freiwillige Angabe.Den Namen der Stadt"></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label8" runat="server" Text="Zusatz" /></label>
            <asp:TextBox ID="txbx_adress_add" runat="server" ToolTip="Freiwillige Angabe."></asp:TextBox>
        </div>
    </div>
    <br />

    <div class="row">
    </div>

    <div class="row"><div class="span4 offset1"><br />
    </div>
</div>

    <div class="thehidden">
        <!-- hidden textfields used for statusmessages from the server (easier internationalization of the text -->
        <asp:Label ID="msg_pwdToShort" runat="server" Text="Achtung: Das gew&auml;hlte Passwort muss mindestens 5 Zeichen lang sein" ></asp:Label>
        <asp:Label ID="msg_pwdNotMatch" runat="server" Text="Achtung: Die eingegebenen Passworte stimmen nicht &uuml;berein." ></asp:Label>

        <asp:Label ID="msg_emailNotMatch" runat="server" Text="Achtung: Die eingegebenen Mail-Adressen stimmen nicht &uuml;berein." ></asp:Label>
        <asp:Label ID="msg_emailWrongFormat" runat="server" Text="Achtung: Die eingegebenen Mail-Adresse hat das falsche Format" ></asp:Label>

        <asp:Label ID="msg_mailSubject" runat="server" Text="nejoba User Registrierung. " ></asp:Label>
        <asp:Label ID="msg_mailBody" runat="server" Text="Bitte best&auml;tigen Sie Ihre Registrierung bei nejoba. Geben Sie bitte folgenden Registrierungscode ein" ></asp:Label>
        <asp:Label ID="msg_inputGap" runat="server" Text="Die Felder oben müssen komplett ausgefüllt sein." ></asp:Label>
        <asp:Label ID="msg_userAlreadyExists" runat="server" Text="Die angegebene Mailadresse ist bereits im System registriert" ></asp:Label>
        <asp:Label ID="msg_unknownPlace" runat="server" Text="Die eingegebene Postleitzahl konnte nicht zugeordnet werden. Sie ist erforderlich!" ></asp:Label>

        <asp:Label ID="msg_accept_privacy" runat="server" Text="Bitte bestätige das Du mit den Datenschutzbestimmungen einverstanden bist. <br />Neben dem Speichern-Button musst Du bitte abhaken." ></asp:Label>
    
        <asp:TextBox ID="hidden_passwordQuestion" runat="server" Text="Nenne bitte Deinen nejoba-Aktivierungscode aus der ersten Email vom System. "></asp:TextBox>
        <asp:TextBox ID="hidden_geo_answer" runat="server" ></asp:TextBox>
        <asp:TextBox ID="hidden_requestClassification" runat="server" ></asp:TextBox>
        <asp:Label ID="hidden_debug" runat="server" Text=""></asp:Label>

        <asp:Label ID="hidden_button_edit_text" runat="server" Text="Nutzerdaten &auml;ndern" ></asp:Label>
        <asp:Label ID="edit_headline_label" runat="server" Text="Kontodaten bearbeiten" ></asp:Label>
    </div>

    </form>
</body>
</html>

