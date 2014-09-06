<%@ Page Title="Zahlung" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="pay_banktransfer.aspx.py" %>

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
                <h3>Bank-&Uuml;berweisung</h3>
                <p>
                    <asp:Label ID="lbl_advertisement" runat="server" Text="Bezahlung per Bank-Überweisung." />
                </p>
            </div>

           <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
      
            <div id="checkInputDiv" class="span12" runat="server">
                <div class="span9 offset1">

                    <asp:Label ID="Label5" runat="server" Text="Bitte &uuml;bertrage die Angaben, die dir unten angezeigt werden, in die &Uuml;berweisung und best&auml;tige die AGB. Danach erscheint ein Button. Klicke diesen an, damit nejoba die Zahlungsdaten speichert. <br />In der Regel ben&ouml;tigen wir 3 Werktage nach Zahlungseingang, um den Premium-Zugang freizuschalten." />
                    <br /><br />

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
            </div>

            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->

            <div id="PaymentDetails" class="span12" runat="server" visible="false">
                <div class="row">
                    <div class="span4 offset1">
                        <label><asp:Label ID="Label17" runat="server" Text="Kreditinstitut" /></label>
                        <asp:TextBox ID="txbx_bankname" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
                    </div>
                    <div class="span4">
                        <label><asp:Label ID="Label18" runat="server" Text="Kontoinhaber" /></label>
                        <asp:TextBox ID="txbx_accountowner" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
                    </div>
                </div>

                <div class="row">
                    <div class="span4 offset1">
                        <label><asp:Label ID="Label9" runat="server" Text="Bankleitzahl" /></label>
                        <asp:TextBox ID="txbx_bankcode" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
                    </div>
                    <div class="span4">
                        <label><asp:Label ID="Label10" runat="server" Text="Kontonummer" /></label>
                        <asp:TextBox ID="txbx_accountnumber" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
                    </div>
                </div>
                <br /><br />

                <div class="row">
                    <div class="span4 offset1">
                        <label><asp:Label ID="Label3" runat="server" Text="Verwendungszweck 1" /></label>
                        <asp:TextBox ID="txbx_designated_one" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
                    </div>
                    <div class="span4">
                        <label><asp:Label ID="Label4" runat="server" Text="Verwendungszweck 2" /></label>
                        <asp:TextBox ID="txbx_designated_two" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
                    </div>
                </div>

                <div class="row">
                    <div class="span4 offset1">
                    </div>
                    <div class="span4">
                        <label><asp:Label ID="Label2" runat="server" Text="Betrag" /></label>
                        <asp:TextBox ID="txbx_amount" runat="server" TextMode="SingleLine" Enabled="false"></asp:TextBox>
                    </div>
                </div>

                <br /><br />

                <div class="row" >
                    <div class="span4 offset1" ID="accept" runat="server">
                        <asp:CheckBox ID="ckbx_accept" runat="server" AutoPostBack="true" OnCheckedChanged="HndlrButtonClick" ToolTip="Haken muss gesetzt worden sein.  " />
                        <br />
                        <asp:Label ID="Label6" runat="server" Text="Ich aktzeptiere die "></asp:Label>
                        <asp:HyperLink ID="HyperLink1" runat="server" Text=" AGB " NavigateUrl="~/wbf_info/agb.aspx"></asp:HyperLink>
                        
                    </div>
                    <div class="span4 offset1" ID="order" runat="server">
                        <asp:Button ID="btnStartBankPay" runat="server" Text="Bestellen" onclick="HndlrButtonClick" class="btn btn-large btn-primary" />
                    </div>
                </div>
            </div>
    
        </div> 

    </div><!-- /container -->

<!-- ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##   -->
<div class="hidden">
    <asp:Label ID="msg_noEmployessGiven" runat="server" Text="Keine Mitarbeiter angegeben. "></asp:Label>
    <asp:Label ID="msg_useIntegerVals" runat="server" Text="Bitte für die Mitarbeiteranzahl nur ganze, positive Zahlen verwenden. "></asp:Label>
</div> 

</asp:Content>

