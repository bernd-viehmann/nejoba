<%@ Page Title="Online-Hilfe" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="intro.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">

      <!-- Main hero unit for a primary marketing message or call to action -->
      <div class="hero-unit">
        <h1>...nejoba  </h1>
        <h3>Deine Nachbarschaft 2.0</h3>
      </div>

      <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
      <div class="row">
          <h4>Die Aufgabe</h4>
          <p>...nejoba ist eine Webplattform zur regionalen Vernetzung. Ziel ist die Erstellung von Kontakten zwischen Nachbarn oder Bewohnern einer Stadt.
          Dabei beinhaltet ...nejoba derzeit zwei Funktionen:</p>

          <br />

          <h4>Jobbörse für Job-Börse</h4>
          <p>...nejoba bietet jedem die Möglichkeit eine Ausschreibung zu veröffentlichen um eine Dienstleistung nachzufragen. Dabei ist es egal ob nach einem Handwerker gesucht wird, eine Gefälligkeit von einem Nachbarn oder eine Leistung im Tausch mit einer Gegenleistung.
          Wer putzt meine Fenster? Wer mäht meinen Rasen?  Wer pflegt meine Mutter? Wer gibt Nachhilfe? Wer repariert mein Internet? Wer fährt mich zum Arzt? Wer macht mir den Garten ?
          Auf solche Fragen soll ...nejoba eine Antwort geben. Man veröffentlicht hier seinen Bedarf oder seinen Wunsch anonym und unverbindlich. Die Anfrage  erscheint auf ...nejoba verbunden mit der Postleitzahl des jeweiligen Einsatzortes. Leute aus der Umgebung können so regional suchen und Ihre Hilfe anbieten.</p>

          <br />

          <h4>Regional diskutieren</h4>
          <p>Auf der Plattform können öffentliche Diskussionen geführt werden, die mit einem bestimmten Ort verknüpft sind. Diese Debaten können von allen ...nejoba-Benutzer gelesen und mit eigenen Beiträgen erweitert werden. Eine Debatte kann von einem Nutzer abonniert werden. Auf diese Weise bekommt er einen Mitteilung wenn die Debatte erweitert wird.
          ...nejoba verbindet Themen mit Postleitzahlen. Dies ist die Grundlage für nejoba-Debatten. Dadurch unterstützt die Anwendung die Organisation von regionalen Initiativen, bietet eine regionale Informationplattform zu beliebigen Themen und ermöglicht die einfache Verteilung von Informationen in Vereinen,Initiativen oder regionallen Gruppen.</p>
          <br />

          <h4>Bedienungsanleitung</h4>
          <ul>
            <li>
                <p>Die Grundvoraussetzung um ...nejoba nutzen zu können ist ein eigenes Benutzerkonto</p>
                <asp:HyperLink ID="hyLnk_creatAccount" Text="Neu anmelden" runat="server" NavigateUrl="~/wbf_help/createaccount.aspx" />
                <br /><br />
            </li>
            <li>
                <p>Nachbarschaftshilfe und Jobb&ouml;rse: Wie man Arbeit anbietet und arbeit sucht </p>
                <asp:HyperLink ID="hyLnk_askForhelp" Text="Arbeit vergeben" runat="server" NavigateUrl="~/wbf_help/askhelp.aspx" />
                <br />
                <asp:HyperLink ID="hyLnk_searchForJob" Text="Arbeit suchen" runat="server" NavigateUrl="~/wbf_help/searchjobs.aspx" />
                <br /><br />
            </li>
            <li>
                <p>Debatten und Diskussionen auf ...nejoba</p>
                <asp:HyperLink ID="hyLnk_Discussion" Text="Diskutieren auf ...nejoba" runat="server" NavigateUrl="~/wbf_help/discussion.aspx" />
                <br /><br />
            </li>
          
          </ul>
      </div> <!-- /container -->
    </div>
</asp:Content>

