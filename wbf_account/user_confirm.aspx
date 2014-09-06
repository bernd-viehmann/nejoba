<%@ Page Title="" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="user_confirm.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">

</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>



<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">

        <!-- header to show the selction for area and typ of jobs -->
        <div class="row span12">
            <legend>Aktiviere Dein Konto</legend>
        </div>

        <div class="row">
            <div class="span10 offset1">
                <label><asp:Label ID="lbl_explain" runat="server" Text="nejoba hat dir eine Email geschickt. In dieser findest du den Aktivierungscode, den du hier ben&ouml;tigst. <br/>Gib dein selbst gew&auml;hltes Passwort ein. Darunter den Aktivierungscode aus der E-Mail. <br />Danach nur noch aktivieren und loslegen. " ViewStateMode="Disabled" /></label>
            </div>
            <div class="span1">
                <a id="A1" class="btn pull-rigth" href="#guidance" role="button" title="Anleitung" data-placement="bottom" data-toggle="modal" data-toggle="tooltip" data-original-title="Wie erstelle ich mir ein nejoba-Konto?"><i class="icon-info-sign" data-toggle="tooltip" title="Anleitung"></i></a>
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

        <div class="row"><div class="span4 offset1"><br /></div></div>

        <div class="row">
            <div class="span4 offset1">
                <asp:Button ID="btn_activate" runat="server" class="btn btn-large btn-primary" Text="Aktivieren" onclick="HndlrButtonClick"/>
            </div>
        </div>

        <div class="row" style="visibility:hidden;">
            <div class="span8 offset1">
                <asp:HyperLink ID="HyperLink1" runat="server" Text="Bestätige die nejoba Geschäftsbedingungen." NavigateUrl="~/wbf_info/agb.aspx" Target="_blank" />
                <br />
                <asp:CheckBox ID="chbx_accepted" runat="server" Checked="True" />
            </div>
        </div>



        <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
        <!-- @@                                                                                                                                     @@ -->
        <!-- @@   modal dialog with a short guidance how to use this webform                                                                        @@ -->
        <!-- @@                                                                                                                                     @@ -->
        <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
        <div id="guidance" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="linkreuseLabel" aria-hidden="true">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                <h4>Anleitung: Wie erstelle ich ein eigenes Benutzerkonto?</h4>
            </div>
            <div class="modal-body">
            <br /><br />
            <asp:HyperLink ID="HyperLink2" runat="server" NavigateUrl="../wbf_help/help_debates.aspx" Target="_blank">Zur Bedienungsanleitung</asp:HyperLink>
            <br /><br />
            <asp:HyperLink ID="HyperLink_YouTube" runat="server" NavigateUrl="http://www.youtube.com/user/nejobavideo" Target="_blank">Videos zum Thema nejoba auf YouTube</asp:HyperLink>
            <br /><br />
            <asp:HyperLink ID="HyperLink_facebook" runat="server" NavigateUrl="https://www.facebook.com/nejoba" Target="_blank">Unser Benutzerforum auf facebook.</asp:HyperLink>
            </div>
        
            <div class="modal-footer">
                <button class="btn" data-dismiss="modal" aria-hidden="true">Fertig</button>
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

    </div> <!-- /container -->

</asp:Content>

