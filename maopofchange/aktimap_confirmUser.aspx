<%@ Page Title="Anmeldung" Language="IronPython" CodeFile="aktimap_confirmUser.aspx.py" Inherits="Microsoft.Scripting.AspNet.UI.ScriptPage" EnableEventValidation="true"%>

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
        <div class="row span12">
            <legend>Aktiviere Dein Konto</legend>
        </div>

        <div class="row">
            <div class="span11 offset1">
                <label><asp:Label ID="lbl_explain" runat="server" Text="AktiMap.net hat dir eine Email geschickt. In dieser findest du den Aktivierungscode, den du hier ben&ouml;tigst. <br/>Gib dein selbst gew&auml;hltes Passwort ein. Darunter den Aktivierungscode aus der E-Mail. <br />Dann setze ein H&auml;ckchen f&uuml;r die AGB und klicke auf Aktivieren. Schon kann es losgehen. " ViewStateMode="Disabled" /></label>
            </div>
        </div>

        <div class="row"><div class="span4 offset1"><br /></div></div>

        <div class="row">
            <div class="span4 offset1">
                <label><asp:Label ID="lbl_email" runat="server" Text="Email" /></label>
                <asp:TextBox ID="txbx_email" runat="server" TextMode="SingleLine" Enabled="false" ></asp:TextBox>
            </div>
        </div>

        <div class="row">
            <div class="span4 offset1">
                <label><asp:Label ID="lbl_password" runat="server" Text="Passwort" /></label>
                <asp:TextBox ID="txbx_password" runat="server" TextMode="Password"></asp:TextBox>
            </div>
        </div>

        <div class="row">
            <div class="span4 offset1">
                <label><asp:Label ID="lbl_captcha" runat="server" Text="Zugangscode aus der Email" /></label>
                <asp:TextBox ID="txbx_captcha" runat="server" TextMode="SingleLine"></asp:TextBox>
            </div>
        </div>

        <div class="row"><div class="span4 offset1"><br /><br /><br /></div></div>

        <div class="row">
            <div class="span4 offset1">
                <asp:Button ID="btn_activate" runat="server" class="btn btn-large btn-primary" Text="Aktivieren" onclick="HndlrButtonClick"/>
            </div>
        </div>

        <div class="row" style="visibility:hidden">
            <div class="span8 offset1">
                <asp:HyperLink ID="HyperLink1" runat="server" Text="Bestätige die nejoba Geschäftsbedingungen." NavigateUrl="~/wbf_info/agb.aspx" Target="_blank" />
                <br />
                <asp:CheckBox ID="chbx_accepted" runat="server" Checked="true" />
            </div>
        </div>

        <div class="thehidden">
            <label><asp:Label ID="lbl_missing_password" runat="server" Text="<br /><br /><strong>Bitte gib dein Passwort ein, das du bei der Registrierung vergeben hast.</strong>" /></label>
            <label><asp:Label ID="lbl_missing_captcha" runat="server" Text="<br /><br /><strong>Bitte gib dein gew&auml;hltes Passwort und den Aktivierungscode ein, den du per Mail erhalten hast.</strong>" /></label>
            <label><asp:Label ID="lbl_agb_not_accepted" runat="server" Text="<br /><br /><strong>Bitte aktzeptiere die AGB von nejoba.</strong>" /></label>
            <label><asp:Label ID="lbl_no_data_found" runat="server" Text="<br /><br /><strong>Es wurden keine Daten gefunden Bitte melden dich beim nejoba-Team!.</strong>" /></label>

            <label><asp:Label ID="lbl_wrong_password" runat="server" Text="<br /><br /><strong>Das eingegebene Passwort ist nicht korrekt.</strong>" /></label>
            <label><asp:Label ID="lbl_wrong_captcha" runat="server" Text="<br /><br /><strong>Der Aktivieruns-Code ist nicht korrekt.</strong>" /></label>
    
        </div>











    </form>
</body>
</html>

