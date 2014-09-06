<%@ Page Title="Benutzerkonto" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="create_map_user.aspx.aspx.py" validateRequest="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

<div class="container">
    <!-- Main hero unit for a primary marketing message or call to action -->

    <div class="row span10">
        <div class="accordion" id="Div5">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <h4>
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >
                            <asp:Label ID="lbl_headline" runat="server" Text="Konto erstellen"></asp:Label>
                            
                        </a>
                    </h4>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
                    <strong>Hier kannst du ein Konto erstellen oder (bei einem bestehenden Konto) das Passwort ändern.</strong>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <br />
    <div id="messagebox" class="row" runat="server" visible="false" >
        <div class="label label-warning span10">
            <div class="span1">
                <br />
                    <asp:Image ID="warnimage" runat="server" ImageAlign="Left" ImageUrl="~/style/pic/warning.png" />
                <br /><br />
            </div>
            <div class="span11">
                <br />
                    <asp:Label ID="lbl_messageBox" runat="server" ForeColor="#474747" Text="Kein Fehler zu finden"></asp:Label>
                <br /><br />
            </div>
        </div>
    </div>

    <div class="row"><br /></div>

    <div class="row">
    <!--
        <div class="span12 offset1" style="visibility:hidden">
            <asp:CheckBox ID="ckbx_map_confirmation" CssClass="pull-right" runat="server" OnCheckedChanged="HndlrButtonClick" AutoPostBack="True" ToolTip="Du kannst dich auf der Initiativ-Karte als Mensch darstellen, der selbst aktiv an einem gesellschaftlichen Wandeln arbeiten möchte. Gleichgesinnte in Deiner Umgebung können so mit dir in Kontakt treten. Wenn du das nicht wünscht setzte kein Häkchen. Deine Daten werden dann nicht veröffentlicht." />
            <br /><br />
            <label><asp:Label ID="Label28" runat="server" Text="Deine Kontaktdaten auf die Karte?" ToolTip="Du kannst dich auf der Initiativ-Karte als Mensch darstellen, der selbst aktiv an einem gesellschaftlichen Wandeln arbeiten möchte. Gleichgesinnte in Deiner Umgebung können so mit dir in Kontakt treten. Wenn du das nicht wünscht setzte kein Häkchen. Deine Daten werden dann nicht veröffentlicht."/></label>
            <br /><br />
        </div>
    -->

        <div class="span4 offset1">
            <br />
            <asp:Label ID="lbl_whatisthenejobaname" runat="server" CssClass="spacedTop" Text="Lege fest unter welchem Namen du auf nejoba erscheinst: " />
        </div>

        <div class="span4">
            <asp:Label ID="Label1" runat="server" Text="Wähle ein Synonym" />
            <br />
            <asp:TextBox ID="txbx_nickname" runat="server" ToolTip="Dein Name im System. Du kannst hier auch ein Synonym eintragen." ></asp:TextBox>
            <br />
            <div id="div_picture_url_input" runat="server">
                <label><asp:Label ID="Label6" runat="server" Text="Profilbild-URL (optional) " /></label>
                <asp:TextBox ID="txbx_picturl" runat="server" ToolTip="Optional kannst du eine Webadresse von deinem Profilbild eintragen. Das Bild sollte gleiche X- und Y- Größe aufweisen. Beispiel : 512*512 Pixel. Du könntest hier beispielsweise den Link zu Deinem facebook-Profilbild eintragen."></asp:TextBox>
            </div>
        </div>

    </div>

    <div class="row">
        <div class="span4 offset1">
            <label><asp:Label ID="Label15" runat="server" Text="Land" /></label>
            <asp:DropDownList ID="drpd_countrycode" runat="server"  ToolTip="Derzeit ist nejoba nur in deutscher Sprache verfügbar. Daran wird aber gearbeitet.">
                <asp:ListItem Text="Deutschland" Value="DE" Selected="True" />
                <asp:ListItem Text="Österreich" Value="AT" />
                <asp:ListItem Text="Schweiz" Value="CH" />
                <asp:ListItem Text="Liechtenstein" Value="LI" />
                <asp:ListItem Text="Luxemburg" Value="LU" />
                <asp:ListItem Text="Niederlande" Value="NL" />
                <asp:ListItem Text="Belgien" Value="BE" />
            </asp:DropDownList>
        </div>

        <div class="span4">
            <label><asp:Label ID="Labeluz1" runat="server" Text="Postleitzahl" /></label>
            <asp:TextBox ID="txbx_postcode" runat="server" ToolTip="Die Postleitzahl muss korrekt sein damit Dein Account funktioniert. Sie entscheidet welche Foren Du nutzen kannst." ></asp:TextBox>
        </div>
    </div>

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

    <div class="row"><br /></div>

        <div id="div_remark_input" class="span8 offset1" runat="server">
            <label><asp:Label ID="Label16" runat="server" Text="Mitteilung" /></label>
            <asp:TextBox ID="txbx_info" Width="79%" runat="server" ToolTip="Dieser Text wird auf der Karte angezeigt Es sind 200 Zeichen möglich." TextMode="MultiLine" Rows="7" ></asp:TextBox>
        </div>


        <div id="div_coord_inpt" runat="server">
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
    </div>

    <div id="Div1" class="row" runat="server" visible="false" >
        <div>
            <div class="label label-warning span7 offset1">
                <div>
                    <br />
                    <asp:Image ID="Image2" runat="server" ImageAlign="Left" ImageUrl="~/style/pic/warning.png" />
                    <p style="padding-left:77px;">
                        <asp:Label ID="Label25" runat="server" class="" ForeColor="#474747" Text="Kein Fehler zu finden"></asp:Label>
                        <br /><br />
                    </p>
                </div>
            </div>
        </div>
    </div>


    <div class="row" runat="server" visible="false">
        <div class="row">
            <div id="Div2" runat="server" class="span6 offset1 alert alert-info">
                <asp:Label ID="Label2" runat="server" Text="Die folgenden Angaben sind freiwillig. Sie erleichtern anderen Nutzern von nejoba mit Dir in Kontakt zu treten. "></asp:Label>
            </div>
        </div>

        <div class="row"><br /></div>
        
        <div class="row">
            <div class="span4 offset1">
                <label><asp:Label ID="Label9" runat="server" Text="Website" /></label>
                <asp:TextBox ID="txbx_website" runat="server" ToolTip="Freiwillige Angabe: Die Adresse Deiner Website"></asp:TextBox>
            </div>
            <div class="span4">
                <label><asp:Label ID="lbl_twitterlable" runat="server" Text="twitter-Konto" /></label>
                <asp:TextBox ID="txbx_twitter" runat="server" ToolTip="Freiwillige Angabe: Wie ist der Name von deinem  @Twitter-Account."></asp:TextBox>
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
                <label><asp:Label ID="Label13" runat="server" Text="Skype-Konto" /></label>
                <asp:TextBox ID="txbx_skype" runat="server" ToolTip="Freiwillige Angabe: Kann man Dich mit Skype erreichen?"></asp:TextBox>
            </div>
            <div class="span4">
                <label><asp:Label ID="Label7" runat="server" Text="Mobiltelefon" /></label>
                <asp:TextBox ID="txbx_mobile" runat="server" ToolTip="Freiwillige Angabe: Deine Handy-Nummer."></asp:TextBox>
            </div>
        </div>

        <div class="row">
            <div class="span4 offset1">
                <label><asp:Label ID="Label14" runat="server" Text="Telefon" /></label>
                <asp:TextBox ID="txbx_phone" runat="server" ToolTip="Freiwillige Angabe: Deine Rufnummer im Festnetz."></asp:TextBox>
            </div>
            <div class="span4">
                <label><asp:Label ID="Label8" runat="server" Text="Fax-Nummer" /></label>
                <asp:TextBox ID="txbx_fax" runat="server" ToolTip="Freiwillige Angabe: Die Fax-Durchwahl"></asp:TextBox>
            </div>
        </div>


        <div class="row"><div class="span4 offset1"><br /><br /></div></div>


        <div class="row">
            <div class="span4 offset1">
                <label><asp:Label ID="Laubel3" runat="server" Text="Vorname" /></label>
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
    

        <div class="row">
            <div class="span4 offset1">
                <label><asp:Label ID="Lubel6" runat="server" Text="Stadt" /></label>
                <asp:TextBox ID="txbx_locationname" runat="server" ToolTip="Freiwillige Angabe."></asp:TextBox>
            </div>
            <div class="span4">
            </div>
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








    <div id="messageacceptprivacy" class="row span10" runat="server">
        <div id="Div4" runat="server" class="span12 alert alert-info">
            <asp:Label ID="Label21" runat="server" Text="Erteile Dein Einverständniss zu unseren " />
            <asp:HyperLink ID="hylnk_rulesofbui" runat="server" Text="allgemeinen Geschäftsbedingungen " NavigateUrl="~/wbf_info/agb.aspx" Target="_blank"  />
            <asp:Label ID="Label20" runat="server" Text="und zu unseren " />
            <asp:HyperLink ID="hylnk_privacyprotection" runat="server" Text="Datenschutzbestimmungen" NavigateUrl="~/wbf_info/privacy_protection.aspx" Target="_blank"  />
            <asp:CheckBox ID="ckbx_accept_privacy_statement" CssClass="pull-right" runat="server" ToolTip="Das akzeptieren der Bedingungen ist zwingend erforderlich ehe Du Daten eintragen kannst."/>  
        </div>
    </div>

    <div class="row">
        <div id="divPwdChanged" runat="server" class="span10 alert alert-info" visible="false">
            <asp:Label ID="Label4" runat="server" Text="Das Passwort für das Benutzerpasswort wurde erfolgreich geändert." />
        </div>
    </div>


    <div class="row">
        <div id="Div3" runat="server" class="span9 offset1">
            <asp:Button ID="btn_Create" runat="server" class="btn btn-large btn-success pull-right" Text="Speichern" onclick="HndlrButtonClick" ToolTip="Daten im System speichern."/>
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
        <asp:Label ID="msg_inputGap" runat="server" Text="Ihre Eingaben sind nicht komplett. Bitte kompletieren." ></asp:Label>
        <asp:Label ID="msg_userAlreadyExists" runat="server" Text="Die angegebene Mailadresse ist bereits im System registriert" ></asp:Label>
        <asp:Label ID="msg_unknownPlace" runat="server" Text="Die eingegebene Postleitzahl konnte nicht zugeordnet werden. Sie ist aber erforderlich!<br /><br />Es könnte sein das nejoba deine Postleitzahl noch nicht kennt. <br />In dem Fall nimm die des nächsten Nachbarorts und kontaktiere uns.<br />Dazu findest du ganz unten den Link Kontakt. <br />Schreibe uns den Ortsnamen und die PLZ rein. <br />Wir kümmern uns dann as soon as possible." ></asp:Label>
        <asp:Label ID="msg_accept_privacy" runat="server" Text="Bitte die AGB und Datenschutzbedingungen akzeptieren! Mache ein Häkchen über dem Speichern-Knopf." ></asp:Label>
        <asp:Label ID="msg_stupid_coords" runat="server" Text="Die eingegebenen Koordinaten sind nicht korrekt formatiert. Nutze einen Punkt und kein Komma als Trennzeichen!" ></asp:Label>
    
    
        <asp:TextBox ID="hidden_passwordQuestion" runat="server" Text="Nenne bitte Deinen nejoba-Aktivierungscode aus der ersten Email vom System. "></asp:TextBox>
        <asp:TextBox ID="hidden_geo_answer" runat="server" ></asp:TextBox>
        <asp:TextBox ID="hidden_requestClassification" runat="server" ></asp:TextBox>
        <asp:Label ID="hidden_debug" runat="server" Text=""></asp:Label>

        <asp:Label ID="hidden_button_edit_text" runat="server" Text="Passwort &auml;ndern" ></asp:Label>
        <asp:Label ID="edit_headline_label" runat="server" Text="Passwort &auml;ndern" ></asp:Label>


        <label><asp:Label ID="lbl_type_of_item" runat="server" Text="Art des Eintrages" /></label>
        <asp:DropDownList ID="drpd_item_type" runat="server" ToolTip="Lege fest was Du in die Karte eintragen möchtest." >
            <asp:ListItem Text="Mensch" Value="human" Selected="True" />
            <asp:ListItem Text="Initiative" Value="action" />
        </asp:DropDownList>

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
</div> <!-- /container -->


<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->

<script type="text/javascript">
    $(document).ready(function () {
        $("#CoPlaBottom_txbx_info").wysihtml5();
    }); 
</script>

</asp:Content>

