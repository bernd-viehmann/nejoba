<%@ Page Title="Abmeldung" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="logout.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">

      <!-- Main hero unit for a primary marketing message or call to action -->
      <div class="hero-unit">
        <h3><asp:Label ID="Label1" runat="server" Text="Abmeldung wurde durchgef&uuml;hrt" ></asp:Label></h3>
      </div>
      <asp:Label ID="Label2" runat="server" Text="Besuche nejoba bald wieder" />

    </div> <!-- /container -->
</asp:Content>

