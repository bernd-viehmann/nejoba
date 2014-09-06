<%@ Page Title="Initiativen bearbeiten" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="selectlist_initiatives.aspx.py" %>

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
                    <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/240x216_search_globe.png" ToolTip="Kartendaten durchsuchen" />
                    </div>
                <div class="span7 offset1">
                    <h4><asp:Label ID="Label2" runat="server" Text="Bearbeite von dir eingetragene Initiativen" /></h4>
                    <br />
                </div>
            </div>
        </div>
    </div>

    <div id="divDataArea" runat="server">
    
        <!-- ############################################################################################################################################ -->
        <!--   repeaer renders stuff from db to the outside world                                                                                         -->
        <!-- ############################################################################################################################################ -->
        <asp:Repeater ID="repInitiativesList" runat="server">
            <ItemTemplate>
                <div class="well">
                    <div class="btn-group span2">
                        <asp:LinkButton ID="btn_EditInitiative"   runat="server" OnClick="HandlBtnClick" ToolTip="Initiative: Daten bearbeiten"   class="btn btn-small" ><i class="icon-pencil"></i></asp:LinkButton>
                        <asp:LinkButton ID="btn_DeleteInitiative" runat="server" OnClick="HandlBtnClick" ToolTip="Initiative: Daten l&ouml;schen" class="btn btn-small" ><i class="icon-trash"></i></asp:LinkButton>
                    </div>
                    <div class="span10">
                        <h5>
                            <asp:Label ID='Label1' runat="server"  Text='<%# Eval("nickname")%>' />
                        </h5>
                        <br />
                    </div>
                    <asp:Label ID='Label3' runat="server"  Text='<%# Eval("marker_line")%>' />
                </div>
                <div class="row-fluid span12">
                    <hr /><br />
                </div>
            </ItemTemplate>
        </asp:Repeater>
    
    </div>

</div>


<div style="visibility:hidden;">
</div>


</asp:Content>

