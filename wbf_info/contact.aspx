<%@ Page Title="Kontakt" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="contact.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

<div class="container">
    <!-- Main hero unit for a primary marketing message or call to action -->
    <div class="hero-unit">
        <div class="container-fluid">
            <div class="row-fluid">
                <div class="span3 offset1">
                    <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/contact_nejoba.png" ToolTip="Kontaktformular" />
                    </div>
                <div class="span7 offset1">
                    <div class="row offset1">
                        <h4><asp:Label ID="Label2" runat="server" Text="Kontaktiere das nejoba-Team" /></h4>
                        <br />
                    </div>
                    <div class="row offset1">
                        <adress>
                            <strong>nejoba UG (haftungsbeschränkt) & Co. KG</strong><br />
                            Waldstraße 9<br />
                            41470 Neuss<br />
                            Deutschland <br />
                            <br />
                            <asp:HyperLink ID="HyperLink1" runat="server" NavigateUrl="mailto:info.nejoba@gmail.com" Text="E-Mail:	  info.nejoba@gmail.com" Target="_blank" /><br />
                        </adress>
                        <br /><br />
                    </div>
                </div>
            </div>
        </div>
    </div>
    <br />

    
    
    <div id="divEditArea" class="well" runat="server">
        <div class="row">
            <div class="span10 offset1">
                <h4>
                    <asp:Label ID="Label1" runat="server" Text="Betrifft:"></asp:Label>
                </h4>
                <asp:TextBox ID="txbHeader" runat="server" Width="96%"></asp:TextBox>
            </div>
        </div>

        <div class="row">
            <div class="span10 offset1">
                <h4><asp:Label ID="lbl_hint" runat="server" Text="Deine Nachricht an uns:"></asp:Label></h4>
                <asp:TextBox runat="server" ID="txtMain" TextMode="MultiLine" Rows="17" style="width:96%"></asp:TextBox>
            </div>
        </div>


        <div class="row">
            <div class="span11">
            <br />
            <asp:Button ID="btnSendReport" runat="server" CssClass="btn btn-large btn-success pull-right" Text="Senden" onclick="HndlrButtonClick" />
            </div>
        </div>
    </div>


    <div id="mailSendSuccesfullyMessage" class="well" runat="server" visible="false">
        <p><asp:Label ID="Label3" runat="server" class="alert alert-success" Text="Danke. Deine Nachricht wurde gesendet." /></p>
    </div>


</div>







    <div style="visibility:hidden;">
    </div>

      <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    </div> <!-- /container -->

</asp:Content>

