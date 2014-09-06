<%@ Page Title="" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="user_create.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>



<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">

    <!-- header to show the selction for area and typ of jobs -->
      <div class="hero-unit">
        <h3>
            <asp:Label ID="lbl_headline" runat="server" Text="Benutzerkonto erstellen" />
        </h3>
      </div>

    <div class="row">
        <div class="span4 offset1">
            <asp:Label ID="Label1" runat="server" Text="Wie willst du in nejoba hei&szlig;en?" />
            <asp:TextBox ID="txbx_nickname" runat="server" ToolTip="Dein Synonym auf nejoba" ></asp:TextBox>
        </div>
        <div class="span6">
            <label><asp:Label ID="lbl_whatisthenejobaname" runat="server" Text="Der nejoba-Name legt fest, unter welchem Namen du in nejoba erscheinst. Du kannst ein Synonym w&auml;hlen um inkognito zu bleiben oder zum Beispiel die Webadresse deiner Firmen-HomePage angeben." /></label>
        </div>
    </div>
    <br /><br />

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label4" runat="server" Text="Vorname" /></label>
            <asp:TextBox ID="txbx_forename" runat="server" ></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label10" runat="server" Text="Nachname" /></label>
            <asp:TextBox ID="txbx_familyname" runat="server" ></asp:TextBox>
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label2" runat="server" Text="Postleitzahl" /></label>
            <asp:TextBox ID="txbx_postcode" runat="server" ToolTip="Die Postleitzahl muss korrekt sein damit Dein Account funktioniert!" ></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label5" runat="server" Text="Stadt" /></label>
            <asp:TextBox ID="txbx_city" runat="server" ></asp:TextBox>
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label11" runat="server" Text="Straße" /></label>
            <asp:TextBox ID="txbx_street" runat="server" ></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label12" runat="server" Text="Hausnummer" /></label>
            <asp:TextBox ID="txbx_housenumber" runat="server" ></asp:TextBox>
        </div>
    </div>
    <br />
    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label3" runat="server" Text="E-mail" /></label>
            <asp:TextBox ID="txbx_email" runat="server" ></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label19" runat="server" Text="E-Mail Best&auml;tigung" /></label>
            <asp:TextBox ID="txbx_emailconfirm" runat="server" ></asp:TextBox>
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

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label15" runat="server" Text="Land" /></label>
            <asp:DropDownList ID="drpd_country" runat="server">
                <asp:ListItem Text="Deutschland" Value="DE" Selected="True" />
                <asp:ListItem Text="&Ouml;sterreich" Value="AT" />
                <asp:ListItem Text="Schweiz" Value="CH" />
                <asp:ListItem Text="Luxemburg" Value="LU" />
                <asp:ListItem Text="Belgien" Value="BE" />
                <asp:ListItem Text="Niederlande" Value="NL" />
            </asp:DropDownList>

        </div>
        <div class="span4">
            <label><asp:Label ID="Label16" runat="server" Text="Sprache" /></label>
            <asp:DropDownList ID="drpd_language" runat="server" Enabled="false">
                <asp:ListItem Text="deutsch" Value="de" Selected="True" />
                <asp:ListItem Text="niederl&auml;ndisch" Value="nl" />
                <asp:ListItem Text="franz&ouml;sisch" Value="fr" />
                <asp:ListItem Text="polnisch" Value="pl" />
                <asp:ListItem Text="tschechisch" Value="cz" />
                <asp:ListItem Text="d&auml;nisch" Value="dk" />
            </asp:DropDownList>
        </div>
    </div>
    <br />
    <div id="alertbox" runat="server" class="alert alert-info">
        <asp:Label ID="Label1238" runat="server" Text="<strong>Hinweis: </strong>nejoba sendet dir eine Mail mit einem Zugangscode. Diesen benötigst du auf der nächsten Seite."></asp:Label>
    </div>


    <div class="row">
        <div class="span4 offset1">
        </div>
        <div class="span4 offset1">
            <br /><br />
            <asp:Button ID="btn_Create" runat="server" class="btn btn-large btn-primary" Text="Konto anlegen" onclick="HndlrButtonClick" />
            <br />
        </div>
    </div>

    <hr />

    <div class="row">
        <div class="span10 offset1">
            <label><asp:Label ID="Label20" runat="server" Text="Die folgenden Angaben sind freiwillig. Von nejoba werden deine Daten gesch&uuml;tzt. Informiere dich &uuml;ber unseren Datenschutz" /></label>
            <br />
        </div>
    </div>

    <div class="row"><div class="span4 offset1"><br /></div></div>


    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label6" runat="server" Text="Telefon" /></label>
            <asp:TextBox ID="txbx_phone" runat="server" ></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label14" runat="server" Text="Faxnummer" /></label>
            <asp:TextBox ID="txbx_fax" runat="server" ></asp:TextBox>
        </div>
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label7" runat="server" Text="Mobiltelefon" /></label>
            <asp:TextBox ID="txbx_mobile" runat="server" ></asp:TextBox>
        </div>
        <div class="span4">
            <label><asp:Label ID="Label9" runat="server" Text="Website" /></label>
            <asp:TextBox ID="txbx_website" runat="server" ></asp:TextBox>
        </div>
    </div>

    <div class="row">
    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label13" runat="server" Text="Skype" /></label>
            <asp:TextBox ID="txbx_skype" runat="server" ToolTip="Skype ist eine Software um im Internet zu telefonieren."></asp:TextBox>
        </div>
        <div class="span4">
        </div>
    </div>

    <div class="row"><div class="span4 offset1"><br /></div></div>

    </div> <!-- /container -->



<div class="thehidden">
    <!-- hidden textfields used for statusmessages from the server (easier internationalization of the text -->
    <asp:Label ID="msg_pwdToShort" runat="server" Text="Achtung: Das gew&auml;hlte Passwort muss mindestens 5 Zeichen lang sein" ></asp:Label>
    <asp:Label ID="msg_pwdNotMatch" runat="server" Text="Achtung: Die eingegebenen Passworte stimmen nicht &uuml;berein." ></asp:Label>

    <asp:Label ID="msg_emailNotMatch" runat="server" Text="Achtung: Die eingegebenen Mail-Adressen stimmen nicht &uuml;berein." ></asp:Label>
    <asp:Label ID="msg_emailWrongFormat" runat="server" Text="Achtung: Die eingegebenen Mail-Adresse hat das falsche Format" ></asp:Label>

    <asp:Label ID="msg_mailSubject" runat="server" Text="nejoba User Registrierung. " ></asp:Label>
    <asp:Label ID="msg_mailBody" runat="server" Text="Bitte best&auml;tigen Sie Ihre Registrierung bei nejoba. Geben Sie bitte folgenden Registrierungscode ein" ></asp:Label>
    <asp:Label ID="msg_inputGap" runat="server" Text="Ihre Eingaben sind nicht komplett. Bitte kompletieren." ></asp:Label>
    <asp:Label ID="msg_userAlreadyExists" runat="server" Text="Die angegebene Mailadresse ist bereits im System registriert" ></asp:Label>
    <asp:Label ID="msg_unknownPlace" runat="server" Text="Die eingegebene Postleitzahl konnte nicht zugeordnet werden. Sie ist erforderlich!" ></asp:Label>
    
    <asp:TextBox ID="hidden_passwordQuestion" runat="server" Text="Nenne bitte Deinen nejoba-Aktivierungscode aus der ersten Email vom System. "></asp:TextBox>
    <asp:TextBox ID="hidden_geo_answer" runat="server" ></asp:TextBox>
    <asp:TextBox ID="hidden_requestClassification" runat="server" ></asp:TextBox>
    <asp:Label ID="hidden_debug" runat="server" Text=""></asp:Label>

    <asp:Label ID="hidden_button_edit_text" runat="server" Text="Nutzerdaten &auml;ndern" ></asp:Label>
    <asp:Label ID="edit_headline_label" runat="server" Text="Kontodaten bearbeiten" ></asp:Label>
</div>

</asp:Content>

