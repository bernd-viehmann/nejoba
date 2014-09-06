<%@ Page Title="Links" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="Links.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>






<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">

        <!-- Main hero unit for a primary marketing message or call to action -->
        <div class="hero-unit">
            <h2>Entwicklung Startform</h2>
            <p><asp:Label ID="lbl_advertisement" runat="server" Text="<br/><strong>nejoba</strong> ist das Jobnetzwerk in Deiner Nachbarschaft." ></asp:Label></p>
            <br />
        </div>

        <div class="row span12">
            <div class="span5">
                <br />
                <asp:Label ID="Label2" runat="server" Text="Start" style="font-size:large; font-weight:bold"></asp:Label>
                <br /><br />
                <a href="../job_market.aspx">Default.aspx - Home-Seite der Anwendung</a>
                <br /><br /><br />
                <asp:Label ID="Label6" runat="server" Text="Funktionen" style="font-size:large; font-weight:bold"></asp:Label>
                <br /><br />
                <a href="../wbf_functs/jobs_editor.aspx">jobs_editor.aspx - Ein Angebot einstellen</a>
                <br />
                <a href="../wbf_functs/jobs_search.aspx">jobs_search.aspx - Angebote suchen</a>
                <br />
                <a href="../wbf_functs/jobs_list.aspx">jobs_list.aspx - Liste mit Angeboten</a>
                <br />
                <br />
                <a href="../wbf_functs/debate_editor.aspx">debate_editor.aspx - &Ouml;ffentliche Diskussion starten</a>
                <br />
                <a href="../wbf_functs/debate_search.aspx">debate_search.aspx - Diskussionen suchen</a>
                <br />
                <a href="../wbf_functs/debate_list.aspx">debate_list.aspx - Diskussionsthemen Liste</a>
                <br />
                <br />
                <a href="../wbf_functs/debate_article_editor.aspx">debate_article_editor.aspx - Einer Diskussion einen Beitrag hinzufügen</a>
                <br />
                <a href="../wbf_functs/job_trial_editor.aspx">job_trial_editor.aspx - Verhandlungen zu einem Arbeitsangebot</a>
                <br />
                <a href="../wbf_functs/violation_editor.aspx">violation_editor.aspx - Einen verstoß an das nejoba-Team melden</a>
                <br />
                <a href="../wbf_functs/show_details.aspx">show_details.aspx - show the single-data of the main-root element</a>
                <br />
                <br />
                <br />
                <br />
            </div>



            <div class="span5">
                <br />
                <asp:Label ID="Label1" runat="server" Text="Dein Konto" style="font-size:large; font-weight:bold"></asp:Label>
                <br /><br />
                <a href="../wbf_account/user_home.aspx">user_home.aspx - Startseite mit den Nejoba-Funktionen</a>
                <br />
                <a href="../wbf_account/user_jobs.aspx">user_jobs.aspx - Anfragen des Users nach Hilfe / Eigene Jobangebote</a>
                <br />
                <a href="../wbf_account/user_offers.aspx">user_offers.aspx - Angebote des Users</a>
                <br />
                <a href="../wbf_account/user_debates.aspx">user_debates.aspx - Liste der Diskussionen des Users</a>
                <br />
                <a href="../wbf_account/user_create.aspx">user_create.aspx - User-Konto anlegen oder bearbeiten</a>
                <br />
                <a href="../wbf_account/pay_start.aspx">pay_start.aspx - Bezahlvorgang starten</a>
                
                <br /><br />
                <asp:Label ID="Label3" runat="server" Text="Ohne Menue-Eintr&auml;ge"></asp:Label>
                <br />
                
                <br />
                <a href="../wbf_account/pay_banktransfer.aspx">pay_banktransfer.aspx - Daten für &Uuml;berweisungstr&auml;ger ausgeben</a>
                <br />
                <a href="../wbf_account/pay_paypal.aspx">pay_paypal.aspx - Zahlung mit PayPal einleiten</a>
                <br />
                <a href="../wbf_account/pay_receive.aspx">pay_receive.aspx - Empfang der R&uuml;ckmeldungen von PayPal</a>
                <br />
                <a href="../wbf_account/user_confirm.aspx">user_confirm.aspx - Bestätigen eines initial angelegten user-Accounts</a>
                <br />
                <br />
            </div>
        </div>


        <div class="row span12">
            <div class="span5">
                <br />
                <asp:Label ID="Label4" runat="server" Text="Hilfe, Info und Internes" style="font-size:large; font-weight:bold"></asp:Label>
                <br /><br />
                <a href="../wbf_help/help.aspx">help.aspx - Online-Hilfe</a>
                <br />
                <a href="../wbf_info/agb.aspx">agb.aspx - AllgGeschBdng</a>
                <br />
                <a href="../wbf_info/impressum.aspx">impressum.aspx - vorgeschriebense Impressum</a>
                <br />
                <a href="../wbf_info/contact.aspx">contact.aspx - Kontaktformular</a>
                <br />
                <br />
                <br />
                <a href="data_geoimport.aspx">data_geoimport.aspx</a>
                <br />
                <a href="Links.aspx">Links.aspx</a>
                <br />
                <a href="not_allowed.aspx">not_allowed.aspx</a>
                <br />
                
                <br />
                
                <br />
                
                <br />
                
                <br />
                
            </div>


        </div>

    </div> <!-- /container -->
</asp:Content>

