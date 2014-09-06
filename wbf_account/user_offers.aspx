<%@ Page Title="Angebote" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="user_offers.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <div class="row">
        <div class="accordion" id="Div1">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <h4><a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >Deine Nachfragen auf Ausschreibungen in der Job-Börse</a></h4>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <h5>
                            <asp:Label ID="Label2" runat="server" Text="Die Liste zeigt die Jobangebote für die du dich beworben hast."></asp:Label>
                        </h5>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="span12">
            <div class="span1"></div>
            <div class=" span10" style="background-color:White;">
                <asp:Image ID="Image1" runat="server" ImageUrl="~/style/pic/jobmarket_head.jpg" ImageAlign="Middle" />
            </div>
            <div class="span1"></div>
        </div>
    </div>

    <div class="row"><br /><br /></div>

    <!-- ############################################################################################################################################ -->
    <!--   repeaer renders stuff from db to the outside world                                                                                         -->
    <!-- ############################################################################################################################################ -->
    <div class="row">
        <div class="span10 offset1">
            <div class="accordion" id="Div2">
                <asp:Repeater ID="repUserOfferList" runat="server">
                    <ItemTemplate>
                    <div class="accordion-group">
                        <div class="accordion-heading">
                            <div class="row">
                                <div class="span9 offset1">
                                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href='#<%# Eval("_ID")%>'>
                                        <h5><asp:Label ID="Label4" runat="server" Text='<%# Eval("subject")%>' /></h5>
                                    </a>
                                </div>

                                <div class="span2">
                                    <br />
                                    <asp:LinkButton ID="btn_OpenTrial"   runat="server" OnClick="HndlrReactionClick" ToolTip="Verhandlung mit dem Auftraggeber aufrufen" class="btn btn-small" ><i class="icon-thumbs-up"></i></asp:LinkButton>
                                    <asp:LinkButton ID="btn_CancleOffer" runat="server" OnClick="HndlrReactionClick" ToolTip="Nimm Dein Angebot zurück.                " class="btn btn-small" ><i class="icon-trash"></i></asp:LinkButton>
                                    <asp:LinkButton ID="btn_ReportOffer" runat="server" OnClick="HndlrReactionClick" ToolTip="Verstoss melden. Der Mecker-Button :-)   " class="btn btn-small" ><i class="icon-warning-sign"></i></asp:LinkButton>
                                </div>
                            </div>
                        </div>
                        <div id='<%# Eval("_ID")%>' class="accordion-body collapse">
                            <div class="accordion-inner">
                                <small>
                                    <div class="span12">
                                        <label><asp:Label ID='Label5' runat="server"  Text='<%# Eval("body")%>' /></label>    
                                    </div>
                                </small>
                                <br />
                            </div>
                        </div>
                    </div>
                    <br />
                    </ItemTemplate>
                    <SeparatorTemplate></SeparatorTemplate>
                </asp:Repeater>
            </div>
            </div>
        </div>

</asp:Content>

