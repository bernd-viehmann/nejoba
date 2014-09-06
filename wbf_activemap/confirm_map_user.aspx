<%@ Page Title="Benutzerkonto anlegen 2" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="confirm_map_user.aspx.aspx.py" %>

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
                    <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/contact_nejoba.png" ToolTip="Kontaktformular" />
                    </div>
                <div class="span7 offset1">
                    <h4><asp:Label ID="Label2" runat="server" Text="Neu angelegtes Benutzerkonto bestätigen" /></h4>
                    <div>
                        <label>
                            <asp:Label ID="Label4" runat="server" Text="Das Konto wird erst frei geschaltet nachdem der Zugangscode eingegeben wurde. Gib dein selbst gew&auml;hltes Passwort ein." />     
                            <br /><br />
                            <asp:Label ID="lbl_explain" runat="server" Text="Das System hat dir eine Email geschickt. In dieser findest du den <strong>Zugangscode</strong>, den du hier ben&ouml;tigst. <br/> <br />Dann klicke auf Aktivieren. Schon kann es losgehen. " ViewStateMode="Disabled" />
                        </label>
                        <a id="A1" class="btn pull-rigth" href="#guidance" role="button" title="Anleitung" data-placement="bottom" data-toggle="modal" data-toggle="tooltip" data-original-title="Wie erstelle ich mir ein nejoba-Konto?"><i class="icon-info-sign" data-toggle="tooltip" title="Anleitung"></i></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div id="divEditArea" class="well" runat="server">
        <div class="row">
            <div class="span11 offset1">
            </div>
        </div>

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
            <iframe width="480" height="360" src="//www.youtube.com/embed/ofsPJ3ta5qw" frameborder="0" allowfullscreen></iframe>
            <br /><br />
            <asp:HyperLink ID="HyperLink2" runat="server" NavigateUrl="../wbf_help/help_account.aspx" Target="_blank">Zur Bedienungsanleitung</asp:HyperLink>
            <br /><br />
            <asp:HyperLink ID="HyperLink_YouTube" runat="server" NavigateUrl="http://www.youtube.com/user/nejobavideo" Target="_blank">Videos zum Thema nejoba auf YouTube</asp:HyperLink>
            <br /><br />
            <asp:HyperLink ID="HyperLink_facebook" runat="server" NavigateUrl="https://www.facebook.com/nejoba" Target="_blank">Unser Benutzerforum auf facebook.</asp:HyperLink>
            </div>
        
            <div class="modal-footer">
                <button class="btn" data-dismiss="modal" aria-hidden="true">Fertig</button>
            </div>
        </div>


        <div class="row" style="visibility:hidden;">
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

    </div>


    <div id="mailSendSuccesfullyMessage" class="well" runat="server" visible="false">
        <p><asp:Label ID="Label3" runat="server" class="alert alert-success" Text="Danke. Deine Nachricht wurde gesendet." /></p>
    </div>


</div>







    <div style="visibility:hidden;">
    </div>

      <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    </div> <!-- /container -->

</asp:Content>

