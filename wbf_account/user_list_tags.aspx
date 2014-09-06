<%@ Page Title="" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="user_list_tags.aspx.py" validateRequest="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>


<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>


<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">
    
        <!-- Top Headline Box -->
        <div class="hero-unit">
        <h3>Deine Hashtag-Liste</h3>
        </div>

        <label><asp:Label ID="lblHintForUsage" runat="server" Text="Hier werden die Hashtags (#beispiel) angezeigt die du dir merken wolltest"></asp:Label></label> 
        <div id="divStatus" runat="server" visible="false">
                <h5><asp:Label ID="lblStatusMsg" runat="server" Text="...." /></h5>
        </div>
    
        <div>
            <!-- display the main-object (must be loaded from thre database) in a div-container -->
            <div id="divShowMain" class="well" runat="server" visible="true">
            Wird vorbereitet 
            </div>
            <br /><br />    
            <!--
            <div class="btn-toolbar">
                <div class="btn-group">
                    <asp:LinkButton ID="btnList" runat="server" OnClick="HndlrReactionClick" class="btn" ToolTip="Zur Liste"><i class="icon-tasks"></i></asp:LinkButton>
                    <asp:LinkButton ID="btnOffr" runat="server" OnClick="HndlrReactionClick" class="btn" ToolTip="Ein Angebot machen"><i class="icon-wrench"></i></asp:LinkButton>
                    <asp:LinkButton ID="btnRprt" runat="server" OnClick="HndlrReactionClick" class="btn" ToolTip="Die Anfrage melden"><i class="icon-warning-sign"></i></asp:LinkButton>
                </div>
            </div>
            -->
        </div>
    </div>

    <div style="visibility:hidden;">
    
    </div>
     <!-- /container -->
</asp:Content>

