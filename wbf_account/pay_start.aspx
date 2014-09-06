<%@ Page Title="Bezahlung" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="pay_start.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">

    <div id="divStartFrame" class="row hero-unit" runat="server">
            <div class="span3">
                <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/premium.png" ToolTip="Der Premium-Zugang" />
            </div>
            <div class="span7">
                <h3>
                    <asp:Label ID="Label8" runat="server" Text="Premium-Zugang" />
                </h3>

                <asp:Label ID="Label13" class="alert alert-info" runat="server" Text="<strong>Hinweis: </strong>Das Nachbarforum ist und bleibt uneingeschränkt kostenlos nutzbar." />
                <br /><br /><br />
                <asp:Label ID="Label14" class="alert alert-info" runat="server" Text="<strong>Hinweis: </strong>Den regionalen Arbeitsmarkt ist noch im Aufbau." />
                <br /><br /><br />
                <asp:Label ID="Label15" class="alert alert-info" runat="server" Text="Daher ist er derzeit auch noch uneingeschränkt kostenlos nutzbar." />
                <br /><br /><br /><br />
                <asp:Label ID="Label4" runat="server" Text="Als Premium-Mitglied kannst du neu eingestellte Arbeitsauftäge sofort einsehen. Die anderen Nutzer sehen die Aufträge erst 48-Stunden später." />
                <asp:Label ID="Label5" runat="server" Text="Für private Dienstleister sowie Gewerbetreibende ohne Mitarbeiter, die die Vorteile der Premium-Mitgliedschaft (48 Stunden-Vorsprung) nutzen möchten." />
				<br /><br />

                <strong>
                <table style="width: 100%;">
                    <tr>
                        <td>
                            &nbsp;
                        </td>
                        <td align="right">
                            1 Monat
                            &nbsp;
                        </td>
                        <td align="right">
                            9,95 € inkl. MwSt.
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td>
                            &nbsp;
                        </td>
                        <td align="right">
                            12 Monate
                            &nbsp;
                        </td>
                        <td align="right">
                            99,95 € inkl. MwSt.
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td align="right" colspan="2">
                            <br />
                            <asp:Label ID="Label2" runat="server" Text="Premium-Zugang für Privatleute oder Gewerbetreibende ohne Mitarbeiter:"></asp:Label>
                            &nbsp;
                        </td>
                        <td align="right">
                            <br />
                            <asp:Button ID="btn_smallTrade" runat="server" onclick="HndlrButtonClick" class="pull-right btn btn-primary" Text="Bestellen" ToolTip="Zum Bestellvorgang" Enabled="false" />
                            &nbsp;
                        </td>
                    </tr>
                </table>
                </strong>
                <hr />
                <asp:Label ID="Label3" runat="server" Text="Gewerbetreibende mit einem Mitarbeiter oder mehr sind verpflichtet für die Dauer der Nutzung von nejoba eine Premium-Mitgliedschaft unter Angabe der Mitarbeiteranzahl abzuschließen."></asp:Label>
                <br />

                <br />
                <strong>
                <table style="width: 100%;">
                    <tr>
                        <td align="right">
                            Gewerbetreibende mit einem Mitarbeiter 
                            &nbsp;
                        </td>
                        <td align="right">
                            1 Monat
                            &nbsp;
                        </td>
                        <td align="right">
                            14,95 € inkl. MwSt.
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td align="right">
                            Kosten für jeden weiteren Mitarbeiter 
                            &nbsp;
                        </td>
                        <td align="right">
                            1 Monat
                            &nbsp;
                        </td>
                        <td align="right">
                            4,95 € inkl. MwSt.
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td>
                            &nbsp;
                        </td>
                        <td align="right">
                            &nbsp;
                        </td>
                        <td align="right">
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td align="right">
                            Gewerbetreibende mit einem Mitarbeiter 
                            &nbsp;
                        </td>
                        <td align="right">
                            12 Monate
                            &nbsp;
                        </td>
                        <td align="right">
                            149,95 € inkl. MwSt.
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td align="right">
                            Kosten für jeden weiteren Mitarbeiter	 
                            &nbsp;
                        </td>
                        <td align="right">
                            12 Monate
                            &nbsp;
                        </td>
                        <td align="right">
                            49,95 € inkl. MwSt.
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td align="right" colspan="2">
                            <br />
                            <asp:Label ID="Label1" runat="server" Text="Premium-Zugang für Gewerbetreibende mit einem Mitarbeiter oder mehr:"></asp:Label>
                        </td>
                        <td align="right">
                            <br />
                            <asp:Button ID="btn_bigCompany" runat="server" onclick="HndlrButtonClick" class="pull-right btn btn-primary" Text="Bestellen" ToolTip="Zum Bestellvorgang" Enabled="false" />
                            &nbsp;
                        </td>
                    </tr>
                </table>
                </strong>
                <hr />
                <strong>
                    <asp:Label ID="Label10" runat="server" Text="nejoba wird mindestens 10% vom Gewinn für gemeinnützige Zwecke spenden. Jeweils am Ende eines Geschäftsjahres wird eine gemeinnützigen Organisation so unterstützt." />
                </strong>
            </div>
    </div>



    <!-- divInitSmallBusiness ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##   -->
    <div id="divInitSmallBusiness" class="row hero-unit" runat="server">
            <div class="span3">
                <asp:Image ID="Image2" runat="server" class="img-polaroid" ImageUrl="~/style/pic/premium.png" ToolTip="Der Premium-Zugang" />
            </div>
            <div class="span7">
                <h3>
                    <asp:Label ID="Label6" runat="server" Text="Private Dienstleister oder<br />Gewerbetreibende ohne Mitarbeiter" />
                </h3>
                <asp:Label ID="Label7" runat="server" Text="Du kannst mit PayPal oder per Banküberwesung bezahlen. Bei der Zahlungsart Überweisung wird das Premium-Konto erst nach Registrierung deiner Zahlung durch unsere Buchhaltung freigeschaltet. Dies kann einige Werktage in Anspruch nehmen." />
				<br /><br /><br /><hr />

                <table style="width: 100%;">
                    <tr>
                        <td align="right">
                            <strong>
                            1 Monat
                            </strong>
                            &nbsp;
                        </td>
                        <td align="right">
                            <strong>
                            9,95 € inkl. MwSt.
                            </strong>
                            &nbsp;
                        </td>
                        <td align="right">
                            <asp:Button ID="btn_payPal_small_month" runat="server" onclick="HndlrButtonClick" class="pull-right btn btn-warning" Text="PayPal" ToolTip="Bestellung eines Premium-Zugangs für Kleinunternehmen und private Anwender" />
                            &nbsp;
                        </td>
                        <td align="right">
                            <asp:Button ID="btn_bank_small_month" runat="server" onclick="HndlrButtonClick" class="pull-right btn btn-danger" Text="Überweisen" ToolTip="Bestellung eines Premium-Zugangs für Kleinunternehmen und private Anwender" />
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td colspan="5">
                            <br />
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td align="right">
                            <strong>
                            1 Jahr
                            </strong>
                            &nbsp;
                        </td>
                        <td align="right">
                            <strong>
                            99,95 € inkl. MwSt.
                            </strong>
                            &nbsp;
                        </td>
                        <td align="right">
                            <asp:Button ID="btn_payPal_small_year" runat="server" onclick="HndlrButtonClick" class="pull-right btn btn-warning" Text="PayPal" ToolTip="Bestellung eines Premium-Zugangs für Kleinunternehmen und private Anwender" />
                            &nbsp;
                        </td>
                        <td align="right">
                            <asp:Button ID="btn_bank_small_year" runat="server" onclick="HndlrButtonClick" class="pull-right btn btn-danger" Text="Überweisen" ToolTip="Zum Bestellvorgang" />
                            &nbsp;
                        </td>
                    </tr>
                </table>
                <hr />
            </div>
    </div>



    <!-- divInitBigCompany ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##   -->
    <div id="divInitBigCompany" class="row hero-unit" runat="server">
            <div class="span3">
                <asp:Image ID="Image3" runat="server" class="img-polaroid" ImageUrl="~/style/pic/premium.png" ToolTip="Gewerbetreibende mit Mitarbeiter(n)" />
            </div>
            <div class="span7">
                <h3>
                    <asp:Label ID="Label9" runat="server" Text="Premium-Zugang für Gewerbetreibende mit einem oder mehreren Mitarbeitern." />
                </h3>
                <asp:Label ID="Label11" runat="server" Text="Du kannst mit PayPal oder per Banküberweisung bezahlen. Bei der Zahlungsart Überweisung wird das Premium-Konto erst nach Registrierung deiner Zahlung durch unsere Buchhaltung freigeschaltet. Dies kann einige Werktage in Anspruch nehmen." />
				
                <br /><hr />

                <asp:Label ID="Label12" runat="server" Text="Gib die Anzahl der Mitarbeiter in deinem Unternehmen ein. Dir wird nach dem Klick zunächst die zu zahlende Summe angezeigt, bevor du die Bestellung abschicken kannst." />
				
                <br /><hr />

                <label><asp:Label ID="lbl_numOfEmployees" runat="server" Text="Anzahl Mitarbeiter" /></label>
                <br />
                <asp:TextBox ID="txbx_employees" runat="server" TextMode="SingleLine" Text="0" />
                
                <br /><hr />

                <table style="width: 100%;">
                    <tr>
                        <td align="right">
                            Gewerbetreibende mit einem Mitarbeiter 
                            &nbsp;
                        </td>
                        <td align="right">
                            1 Monat
                            &nbsp;
                        </td>
                        <td align="right">
                            14,95 € inkl. MwSt.
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td align="right">
                            Kosten für jeden weiteren Mitarbeiter 
                            &nbsp;
                        </td>
                        <td align="right">
                            1 Monat
                            &nbsp;
                        </td>
                        <td align="right">
                            4,95 € inkl. MwSt.
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td>
                            &nbsp;
                        </td>
                        <td align="right">
                            &nbsp;
                        </td>
                        <td align="right">
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td align="right">
                            Gewerbetreibende mit einem Mitarbeiter 
                            &nbsp;
                        </td>
                        <td align="right">
                            12 Monate
                            &nbsp;
                        </td>
                        <td align="right">
                            149,95 € inkl. MwSt.
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td align="right">
                            Kosten für jeden weiteren Mitarbeiter	 
                            &nbsp;
                        </td>
                        <td align="right">
                            12 Monate
                            &nbsp;
                        </td>
                        <td align="right">
                            49,95 € inkl. MwSt.
                            &nbsp;
                        </td>
                    </tr>
                </table>
                <hr />
                <table style="width: 100%;">
                    <tr>
                        <td align="right">
                            <strong>1 Monat</strong>
                            &nbsp;
                        </td>
                        <td align="right">
                            <asp:Button ID="btn_payPal_big_month" runat="server" onclick="HndlrButtonClick" class="pull-right btn btn-warning" Text="PayPal" ToolTip="Bestellung eines Premium-Zugangs für Kleinunternehmen und private Anwender" />
                            &nbsp;
                        </td>
                        <td align="right">
                            <asp:Button ID="btn_bank_big_month" runat="server" onclick="HndlrButtonClick" class="pull-right btn btn-danger" Text="Überweisen" ToolTip="Bestellung eines Premium-Zugangs für Kleinunternehmen und private Anwender" />
                            &nbsp;
                        </td>

                    </tr>
                    <tr>
                        <td align="right" colspan="3">
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td align="right">
                            <strong>1 Jahr</strong>
                            &nbsp;
                        </td>
                        <td align="right">
                            <asp:Button ID="btn_payPal_big_year" runat="server" onclick="HndlrButtonClick" class="pull-right btn btn-warning" Text="PayPal" ToolTip="Bestellung eines Premium-Zugangs für Kleinunternehmen und private Anwender" />
                            &nbsp;
                        </td>
                        <td align="right">
                            <asp:Button ID="btn_bank_big_year" runat="server" onclick="HndlrButtonClick" class="pull-right btn btn-danger" Text="Überweisen" ToolTip="Bestellung eines Premium-Zugangs für Kleinunternehmen und private Anwender" />
                            &nbsp;
                        </td>

                    </tr>
                </table>
                <hr />
            </div>
    </div>


    <!-- ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##   -->
    <!-- ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##   -->
    <!-- ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##   -->
    <!-- ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##   -->
    <!-- ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##   -->
    <!-- ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##   -->
    <div class="hero-unit hidden">
        <asp:Label ID="msg_notNumericInput" runat="server" Text="Bitte kontrolliere deine Eingabe der Mitarbeiteranzahl. Es sind nur Zahlen mööglich. "></asp:Label>
        <asp:Label ID="msg_useIntegerVals" runat="server" Text="Bitte für die Mitarbeiteranzahl nur ganze, positive Zahlen verwenden. "></asp:Label>
    </div> 
    <!-- /container -->
</asp:Content>

