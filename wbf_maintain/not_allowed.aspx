<%@ Page Title="No rigths to visit" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="not_allowed.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">

      <!-- Main hero unit for a primary marketing message or call to action -->
      <div class="hero-unit">
        <h2><asp:Label ID="Label1" runat="server" Text="Fehlende Berechtigung" /></h2>
        <p><asp:Label ID="lbl_advertisement" runat="server" Text="<br/>Zum Betrachten der Seite fehlt Dir die Berechtigung. Bei Fragen kontaktiere bitte das nejoba-Team." /></p>
        <br />
        <br />
          <asp:HyperLink ID="HyperLink1" runat="server" Text="Zur&uuml;ck" NavigateUrl="~/job_market.aspx" />
        <br />
      </div>

      <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
      <div class="row">
      <br />
    </div> <!-- /container -->
</asp:Content>

