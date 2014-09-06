<%@ Page Title="Geo Import" Language="IronPython" Inherits="Microsoft.Scripting.AspNet.UI.ScriptPage" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="data_geoimport.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">

      <!-- Main hero unit for a primary marketing message or call to action -->
      <div class="hero-unit">
        <h2>Geodaten importieren</h2>
            <p>
                <asp:Label ID="lbl_advertisement" runat="server" Text="<br/><strong>Geodaten</strong> in die Stammdaten kopieren." ></asp:Label>
                <br />
                <asp:HyperLink ID="HyperLink1" runat="server" NavigateUrl="http://download.geonames.org/export/zip/">Quelle der Daten ist www.geonames.org </asp:HyperLink>
            </p>
        <br /><br />
        <asp:FileUpload ID="fileUploadCtrl" runat="server" />
        <br /><br /><br /><br />
        <label><asp:Label ID="lblImportHint" runat="server" Text="Datei importieren" /></label>
        <asp:Button ID="btnImport" runat="server" CssClass="btn btn-success" Text="Import" onclick="HndlrButtonClick" />

      </div>
        

      <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
      <div class="row">
      <br />
    </div> <!-- /container -->
</asp:Content>

