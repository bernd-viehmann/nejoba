<%@ Page Title="" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="job_trial_list.aspx.py" validateRequest="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>


<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>


<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    
    <div class="row">
        <div class="accordion" id="accordionic_main_root">
            <div class="accordion-group">

                <div class="accordion-heading">
                    <h4>
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >Antworten auf eine Anfrage</a>
                    </h4>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <h5>
                            <asp:Label ID="Label2" runat="server" Text="Antworten auf deine Ausschreibungen"></asp:Label>
                        </h5>
                        <br />
                        <asp:Label ID="Label10" runat="server" Text="Liste mit den Antworten auf deine Jobausschreibungen" />
                        <br />
                    </div>
                </div>


            </div>
        </div>
    </div>

    <div class="row">
        <div class="span12">
            <div class="span1"></div>
            <div class=" span10" style="background-color:White;">
                <asp:Image ID="Image2" runat="server" ImageUrl="~/style/pic/jobmarket_head.jpg" ImageAlign="Middle" />
            </div>
            <div class="span1"></div>
        </div>
    </div>

    <div class="row"><br /></div>

    <!-- # # canvas for the job-details from item.JOB_ROOT   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div id="divShowMain" class="well" runat="server" visible="true"></div>
    
    <div class="row"><br /></div>

    <!-- ############################################################################################################################################ -->
    <!--   repeaer renders stuff from db to the outside world                                                                                         -->
    <!-- ############################################################################################################################################ -->
    <div class="row">
            <div class="accordion span10 offset1" id="Div1">
                <asp:Repeater ID="repJobTrials" runat="server">
                    <ItemTemplate>
                    <div class="accordion-group">
                        <div class="accordion-heading">
                            <div class="row">
                                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href='#<%# Eval("_ID")%>'>
                                    <div class="span9 offset1">
                                        <h5><asp:Label ID="Label4" runat="server" Text='<%# Eval("nickname")%>' /></h5>
                                    </div>
                                </a>
                                <div class="btn-group span2">
                                    <asp:LinkButton ID="btn_OpenTrial"   runat="server" OnClick="HndlrReactionClick" ToolTip="Zur Verhandlung" class="btn btn-small" ><i class="icon-list"></i></asp:LinkButton>
                                    <asp:LinkButton ID="btn_CancleOffer" runat="server" OnClick="HndlrReactionClick" ToolTip="Die Verhandlung l&ouml;schen    " class="btn btn-small" ><i class="icon-trash"></i></asp:LinkButton>
                                </div>
                                <br />
                            </div>
                        </div>
                        <div id='<%# Eval("_ID")%>' class="accordion-body collapse">
                            <div class="accordion-inner">
                                <strong> 
                                    Postleitzahl : 
                                    <asp:Label ID='lblBody' runat="server"  Text='<%# Eval("postcode")%>' /> 
                                </strong>
                            </div>
                        </div>
                    </div>
                    <br />
                    </ItemTemplate>
                    <SeparatorTemplate></SeparatorTemplate>
                </asp:Repeater>
            </div>
        </div>

    <div style="visibility:hidden;">
        <asp:Label ID="msg_no_offers_available" runat="server" Text="<br />Es sind leider noch keine Angebote zu deiner Ausschreibung vorhanden <br />" />
    </div>

</asp:Content>

