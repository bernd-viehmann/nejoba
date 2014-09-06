<%@ Page Title="Kontakt" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="maintain_users_initiatives.aspx.py" %>

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
                <div class="span2 offset1">
                    <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/240x216_search_globe.png" ToolTip="Kartendaten durchsuchen" />
                    </div>
                <div class="span8 offset1">
                    <h4><asp:Label ID="Label2" runat="server" Text="Eingetragenen Initiativen bearbeiten" /></h4>
                    <br />
                    <asp:Label ID="Label1" runat="server" Text="Du kannst hier die von Dir eingetragenen Initiativen aufrufen um sie zu bearbeiten oder sie löschen." />
                </div>
            </div>
        </div>
    </div>

    <div id="divDataArea" class="well" runat="server"></div>

</div>


<div style="visibility:hidden;">
</div>


</asp:Content>

