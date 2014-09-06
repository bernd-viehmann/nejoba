<%@ Page Title="" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="show_details.aspx.py" validateRequest="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>


<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>


<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">
    
        <!--
        <div class="well" style="visibility:hidden" >
            <h3><asp:Label ID="lbl_header" runat="server" Text="Anfrage-Details "></asp:Label></h3>
        </div>
        -->
        <div class="row span10" >
            <div id="divStatus" runat="server" visible="false">
                    <h3><asp:Label ID="lblStatusMsg" runat="server" Text="...." /></h3>
            </div>
        </div>
    
        <div class="row span10 well" >
            <div id="divShowMain" runat="server" visible="true" >
                <!-- display the main-object (must be loaded from thre database) in a div-container -->
                Dataoutputarea
            </div>
        </div>

        <div class="row span10 well" >
            <h3>
                <asp:Label ID="Label1" runat="server" Text="Deine Eingaben sind nun in nejoba gespeichert" />
            </h3>
            
            <br /><br />
            <asp:LinkButton ID="btn_CancleInput" runat="server" OnClick="HndlrReactionClick" ToolTip="Den Eintrag l&ouml;schen" class="btn btn-small" ><i class="icon-trash"></i></asp:LinkButton>
            <asp:Label ID="Label2" runat="server" Text="Beitrag wieder löschen" />
            
        </div>
    </div>

    <div style="visibility:hidden;">
    
    </div>
     <!-- /container -->
</asp:Content>

