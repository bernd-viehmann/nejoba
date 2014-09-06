<%@ Page Title="Diskussionen" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="user_debates_started.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
<div class="container span10">

    <!-- Main hero unit for a primary marketing message or call to action -->
    <div class="row">
        <div class="accordion" id="Div1">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <h4>
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseRemark" >
                            Deine Beiträge im Nachbarforum
                        </a>
                    </h4>
                </div>
                <div id="collapseRemark" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <h5>
                            <asp:Label ID="Label21" runat="server" Text="Hier werden alle Beiträge aufgelistet die von dir erstellt wurden."></asp:Label>
                        </h5>
                        <br />
                        <a id="show_help"        class="btn" href="#guidance" role="button" title="Anleitung" data-placement="bottom" data-toggle="modal" data-original-title="Anleitung"><i class="icon-info-sign"></i></a>
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
                <asp:Image ID="Image1" runat="server" ImageUrl="~/style/pic/mainhead_pict_nejoba.jpg" ImageAlign="Middle" />
            </div>
            <div class="span1"></div>
        </div>
    </div>

    <div class="row"><br /><br /></div>

    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   modal dialog with a short guidance how to use this webform                                                                        @@ -->
    <!-- @@                                                                                                                                     @@ -->
    <!-- @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@   @@ -->
    <div id="guidance" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="linkreuseLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h4>Anleitung: Lesezeichen in nejoba</h4>
        </div>
        <div class="modal-body">
        <br />
        <iframe width="480" height="360" src="//www.youtube.com/embed/MhFjlYCjGlg" frameborder="0" allowfullscreen></iframe>
        <br /><br />
        <asp:HyperLink ID="HyperLink2" runat="server" NavigateUrl="./wbf_help/help_debates.aspx" Target="_blank">Zur Bedienungsanleitung</asp:HyperLink>
        <br /><br />
        <asp:HyperLink ID="HyperLink33" runat="server" NavigateUrl="http://www.youtube.com/user/nejobavideo" Target="_blank">Videos zum Thema nejoba auf YouTube</asp:HyperLink>
        <br /><br />
        <asp:HyperLink ID="HyperLink3" runat="server" NavigateUrl="https://www.facebook.com/nejoba" Target="_blank">Unser Benutzerforum auf facebook.</asp:HyperLink>
        </div>
        
        <div class="modal-footer">
            <button class="btn" data-dismiss="modal" aria-hidden="true">Fertig</button>
        </div>
    </div>


    <!-- ############################################################################################################################################ -->
    <!--   repeaer renders stuff from db to the outside world                                                                                         -->
    <!-- ############################################################################################################################################ -->
    <div id="repeaterOutDiv" class="span10" runat="server" visible="true">
        <asp:Repeater ID="repUsrOwnDbtsLst" runat="server">
            <ItemTemplate>
                <div>
                    <h5>
                        <asp:LinkButton ID="btn_DelDebate"  runat="server" OnClick="HndlrReactionClick" class="btn" ToolTip="Abo beenden"><i class="icon-trash"></i></asp:LinkButton>
                        <asp:LinkButton ID="btn_CallDebate" runat="server" ToolTip="Beitrag aufrufen" OnClick="HndlrReactionClick"><%# Eval("subject")%></asp:LinkButton>
                    </h5>
                    <small>
                        <asp:Label ID='Label8' runat="server"  Text='Standort : ' />
                        <strong>
                            <asp:Label ID='Label9' runat="server"  Text='<%# Eval("locationname")%>' />
                        </strong>
                        <br />
                        <asp:Label ID='Label6' runat="server"  Text='Benutzer : ' />
                        <strong>
                            <asp:Label ID='lblBody' runat="server"  Text='<%# Eval("nickname")%>' />
                        </strong>
                        <strong>
                            <asp:Label ID='Label5' runat="server"  class="span12" Text='<%# Eval("body")%>' />
                            <br /><br />
                        </strong>
                    </small>
                                    
                </div>
                                
            </ItemTemplate>
        </asp:Repeater>
    </div>

</div> <!-- /container -->
</asp:Content>

