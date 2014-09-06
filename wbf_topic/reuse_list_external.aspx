<%@ Page Title="Liste Debatten" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="reuse_list_external.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <html xmlns:fb="http://ogp.me/ns/fb#">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server" EnableViewState="True">

    <div class="container">
        <!-- # # #  HEADER for tuning search-results # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div ID="SetUpFiltering" runat="server" class="row span12" visible="true">

            <!-- # # #  HEADER for tuning search-results # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="container-fluid">
                <div class="span12 well row-fluid">
                    <h5><asp:Label ID="headline" runat="server" Text="Pinnwand extern nutzen" /></h5>

                    <div class="span2 offset0">
                        <h5><asp:Label ID="lbl_city" runat="server" Text="Orte:" /></h5>
                        <asp:ListBox ID="sel_lctn" runat="server" ToolTip="Die hier auggelisteten Orte werden für deine Sucha auch berücksichtigt." Rows="11" Enabled="false" />
                        <br />
                    </div>

                    <div class="span2 offset1">
                        <h5><asp:Label ID="Label2" runat="server" Text="Themen:" /></h5>
                        <asp:ListBox ID="ListBox1" runat="server" ToolTip="Die hier auggelisteten Orte werden für deine Sucha auch berücksichtigt." Rows="11" Enabled="false" />
                        <br />
                    </div>

                    <div class="span3 offset1" runat="server">
                        <br /><br />
                        <div class="fb-like" id="facebook_button" data-href="http://www.nejoba.net/njb_02/wbf_topic/parameter_result_list.aspx?loc=DE|41836" data-send="true" data-layout="box_count" data-width="450" data-show-faces="true"></div>
                        <br /><br />
                        <div class="fb-like" ID="twitter_button" >
                            <a href="https://twitter.com/share" class="twitter-share-button" data-url="##LINK##" data-text="eine testseite" data-via="info_nejoba" data-lang="de" data-size="large" data-hashtags="nejoba">Twittern</a>
                            <script>                            !function (d, s, id) { var js, fjs = d.getElementsByTagName(s)[0], p = /^http:/.test(d.location) ? 'http' : 'https'; if (!d.getElementById(id)) { js = d.createElement(s); js.id = id; js.src = p + '://platform.twitter.com/widgets.js'; fjs.parentNode.insertBefore(js, fjs); } } (document, 'script', 'twitter-wjs');</script>
                        </div>
                    </div>
                </div>


                <div class="span12 well row-fluid">
                    <h5><asp:Label ID="lbl_hashtags" runat="server" Text="Der Link zur Pinnwand" /></h5>
                    <p> <asp:Label ID="Label3" runat="server" Text="Pinnwände lassen sich per eMail weitergeben- Nachfolgend steht der Link zu Deine Pinnwand. Du kannst ihn in eine eMail kopieren oder in ein soziales Netzwerk einfügen. " /> </p>
                    <br />
                    <div class="alert alert-info span10 offset1">
                        <asp:HyperLink  ID="Label4" runat="server" Text="Die Linkadresse am Schluß" />
                    </div>
                    
                </div>
            </div>

        </div>
    </div>

</asp:Content>

