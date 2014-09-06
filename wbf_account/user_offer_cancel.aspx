<%@ Page Title="" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="user_offer_cancel.aspx.py" validateRequest="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>


<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>


<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <div class="container span10">
        <!-- Top Headline Box -->
        <div class="row span11">
            <h4>
                <asp:Label ID="Label1" runat="server" Text="Eintrag l&ouml;schen" />
            </h4>
        </div>
    
        <div id="divShowMain" class="row span11" runat="server" visible="true">
            <!-- display the main-object (must be loaded from thre database) in a div-container -->
            Dataoutputarea
        </div>

        <div id="buttonDiv" runat="server" class="row well">
            <div class="span11">
                <asp:Button ID="btnCancelOffer" runat="server" class="btn btn-large btn-danger" Text="Entfernen" onclick="HndlrButtonClick" ToolTip="Die Daten werden komplett und restlos aus der nejoba-Datenbank gel&ouml;scht" />
                <br /><br /><br />
                <asp:Label ID="Label2" runat="server" Text="Die Daten werden durch einen Klick auf den Button endgültig in der Datenbank gelöscht." />
            </div>
        </div>

        <div id="messageDiv" runat="server" class="row alert alert-success" visible="false">
            <div class="span11">
                <asp:Label ID="Label3" runat="server" Text="Vorgang erfolgreich abgeschlossen. Die Daten wurden gelöscht" />
            </div>
        </div>

    </div>



    <div style="visibility:hidden;">
    
    </div>
     <!-- /container -->
</asp:Content>

