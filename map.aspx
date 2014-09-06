<%@ Page Title="Karte aktiver Menschen und Initiativen" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="map.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <style type="text/css">
        /* for bootstrap compatibility */
        img.olTileImage {
            max-width: none;
        }
        /* for bootstrap compatibility */

        body {
            margin: 0;
            padding-top: 0px;
            padding-bottom: 10px;
        }
        
        #map 
        {
            position:relative;
            width: 99%;
            height: 735px;
            top:21px;
            left:33px;
            padding: 0.5em 0.5em 0.5em 0.5em;
        }
        
        #butn {
            position: absolute;
            top: 177px;
            left: 21px;
            width: 64px;
            z-index: 20;
            background-color:transparent;
            zoom: 1;
            filter: alpha(opacity=47);
            opacity: 0.47;
        }        
        #butn:hover{
            filter: alpha(opacity=100);
            opacity: 1.0;
        }
        
    </style>

    <script src="<%# ResolveUrl("~/js/OpenLayers-nejoba.js") %>" type="text/javascript"></script>
    <script src="<%# ResolveUrl("~/js/fullscreen.js") %>" type="text/javascript"></script>


</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <div id="map" class="row span12">
    </div>

    <div id="butn">
        <img src="" />
        <br/><br/>
        <asp:HyperLink ID="hyli_showforum" runat="server" ToolTip="Besuche nejobas regionales Forum und vernetze dich mit deinen Nachbarn" ImageUrl="./wbf_activemap/img/32icn__document_checkbox.png" NavigateUrl="~/PinBoard.aspx" />
        <br/>
        <asp:HyperLink ID="hyli_adduser" runat="server" ToolTip="Trage Dich in die Karte ein und vernetze Dich regional" ImageUrl="./wbf_activemap/img/32icn__user-add-icon.png" NavigateUrl="~/wbf_activemap/create_map_user.aspx?insert=map" />
        <br/>
        <asp:HyperLink ID="hyli_addinititive" runat="server" ToolTip="Trage eine Initiative in die Karte ein (in Arbeit)" ImageUrl="./wbf_activemap/img/32icn__users-icon.png" NavigateUrl="~/wbf_activemap/create_map_initiative.aspx" />
        <br/>
        <asp:HyperLink ID="hyli_userlist" runat="server" ToolTip="Eine Liste organisiert nach Postleitzahlen (in Arbeit)" ImageUrl="./wbf_activemap/img/32icn__user-search-icon.png"  NavigateUrl="~/wbf_activemap/list_map_data.aspx" />
        <br/>
        <asp:HyperLink ID="hyli_zoom_to_postcode" runat="server" ToolTip="Ein Postleitzahlengebiet auf der Karte anzeigen" ImageUrl="./wbf_activemap/img/32icn__globe_search.png"  NavigateUrl="~/wbf_activemap/select_region.aspx" />
        <br/><br/>
        <asp:HyperLink ID="hyli_onlinehelp" runat="server" ImageUrl="./wbf_activemap/img/32icn__question-faq-icon.png" NavigateUrl="#myModal" ToolTip="Was stellt die Karte dar?" role="button" data-toggle="modal"/>
        <br/>
    </div>


    <!-- Modal HELP dialog starts here  -->
    <div id="myModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h5><asp:Label ID="Label7" runat="server" Text="Was zeigt die Karte ?" /></h5>
                    
        </div>
        <div class="modal-body">
            <p>
                <asp:Label ID="Label10" runat="server" Text="Die Karte verzeichnet regionale Initiativen und Menschen mit Wunsch zur Vernetzung." />
            </p>
        </div>
        <div class="modal-footer">
            <button class="btn" data-dismiss="modal" aria-hidden="true">Zurück</button>
        </div>
    </div>
    <!-- Modal HELP dialog ends here  -->



    <script type="text/javascript">
        $(document).ready(function () {
            init();
        });
    </script>
</asp:Content>

