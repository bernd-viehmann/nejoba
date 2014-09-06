<%@ Page Title="Anmeldung" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="login.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

        <!-- header to show the selction for area and typ of jobs -->
        <div class="row">
            <div class="accordion" id="Div5">
                <div class="accordion-group">
                    <div class="accordion-heading">
                        <h4>
                            <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >
                                Anmeldung
                            </a>
                        </h4>
                    </div>
                    <div id="collapseHeader" class="accordion-body collapse in">
                        <div class="accordion-inner">
                        <br />
                        <strong>Eine Anmeldung mit deinem Benutzerkonto ist erforderlich zum Veröffentlichen</strong>
                        <br /><br />
                        Um Daten einzugeben ist aber eine Registrierung erforderlich.
                        Falls du noch kein eigenes nejoba-Konto hast kannst du mit dem Button 'Konto erstellen' eines erstellen. 
                        <br /><br />nejoba verzichtet auf die Erhebung persönlicher Daten. Die Registrierung ist daher schnell erledigt.
                        <br /><br /><br />
                        Wenn du schon ein Konto hast, gib deine Zugangsdaten an und klicke auf  'Anmelden'.
                        <br />
                        Als Benutzername verwendet nejoba deine Mail-Adresse und <strong>nicht</strong> dein Synonym. 
                        <br /><br />
                        <h5>
                        Dein Leben spielt sich vor deiner Haustüre ab. nejoba verbindet dich mit deinen Nachbarn <br /><br />
                        </h5>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="row"><br /></div>

        <div class="row">
            <div class="span2">
                <h4>
                    <asp:Label ID="lbl_email" runat="server" Text="Email" />
                </h4>
            </div>
            <div class="span2">
                <asp:TextBox ID="txbx_email" runat="server" TextMode="SingleLine" class="spacedTop" ></asp:TextBox>
            </div>
        </div>
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="row">
            <div class="span2">
                <h4>
                    <asp:Label ID="lbl_password" runat="server" Text="Passwort" />
                </h4>
            </div>
            <div class="span9">
                    
                <asp:TextBox ID="txbx_password" runat="server" TextMode="Password" class="spacedTop" ></asp:TextBox>
            </div>
        </div>
        <div class="row"><br /></div>
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="row">
            <div class="span2"></div>
            <div class="span2">
                <asp:Button ID="btn_login" runat="server" class="span12 btn btn-large btn-primary" Text="Anmelden" onclick="HndlrButtonClick"/>
            </div>
        </div>
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="row"><br /></div>
        <div class="row">
            <div class="span2"></div>
            <div class="span2">
                <asp:Button ID="btn_create" runat="server" class="span12 btn btn-large btn-inverse" Text="Konto erstellen" onclick="HndlrButtonClick" ToolTip="Erstelle ein eigense Benutzerkonto"/>
            </div>
            <br />
        </div>
        <div class="row">
            <a id="A1" class="btn pull-rigth" href="#guidance" role="button" title="Anleitung" data-placement="bottom" data-toggle="modal" data-toggle="tooltip" data-original-title="Wie erstelle ich mir ein nejoba-Konto?"><i class="icon-info-sign" data-toggle="tooltip" title="Anleitung"></i></a>
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
        <label><asp:Label ID="lbl_missing_captcha" runat="server" Text="<br /><br /><strong>Bitte gib den Aktivierungscode ein, den du per Mail erhalten hast.</strong>" /></label>
        <label><asp:Label ID="lbl_agb_not_accepted" runat="server" Text="<br /><br /><strong>Bitte aktzeptiere die AGB von nejoba.</strong>" /></label>
        <label><asp:Label ID="lbl_no_data_found" runat="server" Text="<br /><br /><strong>Es wurden keine Daten gefunden Bitte melde dich beim Systemadministrator!</strong>" /></label>

        <label><asp:Label ID="lbl_wrong_password" runat="server" Text="<br /><br /><strong>Das eingegebene Passwort ist nicht korrekt.</strong>" /></label>
        <label><asp:Label ID="lbl_wrong_captcha" runat="server" Text="<br /><br /><strong>Der Aktivierungs-Code ist nicht korrekt.</strong>" /></label>
    
    </div>



</asp:Content>

