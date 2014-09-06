<%@ Page Title="Anfragen" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="user_jobs.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <!-- Main hero unit for a primary marketing message or call to action -->

    <div class="row">
        <div class="accordion" id="Div1">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >
                        <h4>Deine Ausschreibungen für Job-Börse</h4>
                    </a>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <h5>
                            <asp:Label ID="Label2" runat="server" Text="Es wird eine Liste angezeigt mit allen Jobangeboten die du in nejoba veröffentlicht hast."></asp:Label>
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



    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div class="row">
    <!-- ############################################################################################################################################ -->
    <!--   repeaer renders stuff from db to the outside world                                                                                         -->
    <!-- ############################################################################################################################################ -->
        <div class="span12">
            <div class="accordion span10 offset1" id="Div2">
                <asp:Repeater ID="repUserJobsList" runat="server">
                    <ItemTemplate>
                    <div class="accordion-group">
                        <div class="accordion-heading">
                            <div class="row">
                                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href='#<%# Eval("_ID")%>'>
                                <div class="span9 offset1">
                                    <h5>
                                        <asp:Label ID="Label4" runat="server" Text='<%# Eval("subject")%>' />
                                    </h5>
                                </div>
                                </a>
                                <div class="span2">
                                    <asp:LinkButton ID="btn_ViewTrialList"  runat="server" OnClick="HndlrReactionClick" ToolTip="Zur Liste mit den Angeboten " class="btn btn-small" ><i class="icon-list"></i></asp:LinkButton>
                                    <asp:LinkButton ID="btn_DeleteComplete" runat="server" OnClick="HndlrReactionClick" ToolTip="Die Anfrage l&ouml;schen"     class="btn btn-small" ><i class="icon-trash"></i></asp:LinkButton>
                                </div>
                                
                            </div>
                        </div>
                        <div id='<%# Eval("_ID")%>' class="accordion-body collapse">
                            <div class="accordion-inner">
                                    <small>
                                        <asp:Label ID='Label8' runat="server"  Text='Standort : ' />
                                        <strong>
                                            <asp:Label ID='Label9' runat="server"  Text='<%# Eval("locationname")%>' />
                                        </strong>
                                        <br />
                                        <asp:Label ID='Label6' runat="server"  Text='Erstellt : ' />
                                        <strong>
                                            <asp:Label ID='lblBody' runat="server"  Text='<%# Eval("creationTime")%>' />
                                        </strong>
                                        <strong>
                                            <asp:Label ID='Label5' runat="server"  class="span12" Text='<%# Eval("body")%>' />
                                            <br /><br />
                                        </strong>
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

