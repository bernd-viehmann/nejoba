<%@ Page Title="Zahlung" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="pay_payPalOrder.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">

    <!-- Main hero unit for a primary marketing message or call to action -->
        <div class="row hero-unit">
            <div class="span3">
                <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/premium.png" ToolTip="Der Premium-Zugang" />
                <br /><br /><br /><br />
            </div>
            <div class="span7">
                <p>
                <!-- PayPal Logo --><table border="0" cellpadding="10" cellspacing="0" align="center"><tr><td align="center"></td></tr> <tr><td align="center"><a href="https://www.paypal.com/de/" target="_blank"><img src="https://www.paypalobjects.com/webstatic/de_DE/i/de-pp-logo-200px.png" border="0" alt="Logo 'PayPal empfohlen'"></a></td></tr></table><!-- PayPal Logo -->
                <br /><br />
                <asp:Label ID="lbl_advertisement" runat="server" Text="Bezahlung mit PayPal." />
                </p>
            </div>
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div id="checkInputDiv" class="span12" runat="server">
                <div class="span9">

                    <asp:Label ID="Label4" runat="server" Text="Bitte bestätige die Richtigkeit deiner Eingaben mit dem grünen Button." />

                    <br /><br /><br /><br />

                    <div class="row">
                        <div class="span3">
                            <label><asp:Label ID="lbl_duration" runat="server" Text="Laufzeit in Tagen" /></label>
                            <asp:TextBox ID="txbx_duration" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
                        </div>
                        <div class="span3 offset1">
                        </div>
                    </div>
                    <div class="row">
                        <div class="span3">
                            <label><asp:Label ID="lbl_employees" runat="server" Text="Anzahl Mitarbeiter" /></label>
                            <asp:TextBox ID="txt_employees" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
                        </div>
                        <div class="span2 offset1">
                            <br />
                            <asp:Button ID="btn_changeOrder" runat="server" onclick="HndlrButtonClick" class="btn btn-block btn-warning" Text="Bestellung ändern" ToolTip="Bestellung eines Premium-Zugangs für Unternehmen" />
                        </div>
                    </div>
                    <div class="row">
                        <div class="span3">
                            <label><asp:Label ID="lbl_" runat="server" Text="Betrag" /></label>
                            <asp:TextBox ID="txbx_amountOfMoney" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
                        </div>
                        <div class="span2 offset1">
                            <br />
                            <asp:Button ID="btn_acceptData" runat="server" onclick="HndlrButtonClick" class="btn  btn-block btn-success" Text="Daten übernehmen" ToolTip="Bestellung eines Premium-Zugangs für Unternehmen" />
                        </div>
                    </div>
                    <br /><br />
                </div>


        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div id="PaymentDetails" class="span12" runat="server" visible="false">
            <div class="span8 offset1">
                <asp:Label ID="Label5" runat="server" Text="Vielen Dank das du nejoba unterst&uuml;zen m&ouml;chtest. Bitte best&auml;tige unsere AGB. Dann erscheint der Pay-Pal Button zur Bezahlung. Wenn du den Zahlvorgang auf PayPal erfolgreich abgeschlossen hast wird dein Premium-Zugang innerhalb weniger Minuten freigeschaltet. <br /><br />Es ist ein erneutes Einloggen erforderlich, um den Premium-Zugang zu aktivieren."></asp:Label>
                <br /><br />
            </div>
    
            <div class="span4 offset1">
                <label><asp:Label ID="lbl_logInName" runat="server" Text="Kontoinhaber" /></label>
                <asp:TextBox ID="txbx_accountowner" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
            </div>
            <div class="span4">
                <label><asp:Label ID="lbl_billNumber" runat="server" Text="Vorgang" /></label>
                <asp:TextBox ID="txbx_billGui" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
            </div>
            <div class="span4 offset1">
                <label><asp:Label ID="lbl_periodlength" runat="server" Text="Laufzeit in Tagen" /></label>
                <asp:TextBox ID="txbx_payedPeriodLength" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
            </div>
            <div class="span4">
                <label><asp:Label ID="lbl_money" runat="server" Text="Betrag" /></label>
                <asp:TextBox ID="txbx_amountOfMoney2" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
            </div>

            <div class="span4 offset1" ID="accept" runat="server">
                <asp:CheckBox ID="ckbx_accept" runat="server" AutoPostBack="true" OnCheckedChanged="HndlrButtonClick" ToolTip="Haken muss gesetzt worden sein.  " />
                <br />
                <asp:Label ID="Label1" runat="server" Text="Ich habe die "></asp:Label>
                <asp:HyperLink ID="HyperLink1" runat="server" Text=" AGB " NavigateUrl="~/wbf_info/agb.aspx"></asp:HyperLink>
                <asp:Label ID="Label2" runat="server" Text="und die "></asp:Label>
                <asp:HyperLink ID="HyperLink2" runat="server" Text=" Datenschutzerkl&auml;rung " NavigateUrl="~/wbf_info/privacy_protection.aspx"></asp:HyperLink>
                <asp:Label ID="Label3" runat="server" Text="gelesen und bin einverstanden. "></asp:Label>
            </div>
            <div class="span4 offset1" ID="order" runat="server" >
                <asp:ImageButton ID="btnPayNow" runat="server" ImageUrl="~/style/pic/de-btn-expresscheckout.gif" Enabled="false" PostBackUrl="https://www.sandbox.paypal.com/cgi-bin/webscr"  OnClientClick="window.document.forms[0].target='_blank';" />
            </div>
        </div>
    </div>



    </div> 
</div> <!-- /container -->

        <div ID="paypalform" runat="server" class="hidden">
        </div>
    </div>

</asp:Content>

