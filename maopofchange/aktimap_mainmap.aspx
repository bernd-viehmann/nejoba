<%@ Page Title="AktiMap.NET" Language="IronPython" CodeFile="aktimap_mainmap.aspx.py" Inherits="Microsoft.Scripting.AspNet.UI.ScriptPage" EnableEventValidation="true"%>


<html>

<head id="Head1" runat="server">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>AktiMap</title>        

    <script src="<%# ResolveUrl("~/js/OpenLayers-nejoba.js") %>" type="text/javascript"></script>
    <script type="text/javascript" src="../style/jquery-1.10.2.min.js"></script>
    <script type="text/javascript" src="../style/jqueryui/js/jquery-ui-1.8.23.custom.min.js"></script>
    <script type="text/javascript" src="../style/bootstrap/js/bootstrap.min.js""></script>

    <link href="http://ajax.aspnetcdn.com/ajax/bootstrap/2.3.2/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
    <link href="~/style/Default.css" rel="stylesheet" type="text/css" />

    <style type="text/css">
        /* for bootstrap compatibility */
        img.olTileImage {
            max-width: none;
        }
        /* for bootstrap compatibility */

        html, body, #map {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
        }
        
        #kopping{
            position: absolute;
            top: 0px;
            left: 0px;
            width: 581px;
            height: 20px;
            z-index: 20000;
            background-color:transparent;
            padding: 0 0.5em 0.5em 0.5em;
        }
        

        #text {
            position: absolute;
            top: 47px;
            left: 47px;
            width: 581px;
            height: 150px;
            z-index: 20000;
            background-color:transparent;
            padding: 0 0.5em 0.5em 0.5em;
            background:url(img/000_logo_aktimap.png);
            background-repeat:no-repeat;
            zoom: 1;
            filter: alpha(opacity=47);
            opacity: 0.47;
        }        
        #text:hover{
            filter: alpha(opacity=100);
            opacity: 1.0;
        }

        #buutons
        {
            position:relative;
            left: 453px;
            width:132px;
            height:128px;
            background-color:transparent;
        }
        
    </style>

</head>

<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  -->

<body onload="init()">
    <form id="form1" runat="server">
        <div id="kopping">
            <asp:HyperLink ID="hyli_regionalinfopint" runat="server" Text="Forum" ToolTip="Gehe zu einem regionalen Forum" NavigateUrl="~/PinBoard.aspx" />
            <asp:HyperLink ID="hyli_impressum" runat="server" Text="Impressum"  ToolTip="Zum Impressum" NavigateUrl="../wbf_info/impressum.aspx" />
            <asp:HyperLink ID="hyli_adduserheader" runat="server" Text="Mitmachen" ToolTip="Erstelle ein Benutzerkonto und vernetze Dich regional" NavigateUrl="aktimap_createUser.aspx" />
            <asp:HyperLink ID="hyli_login" runat="server" Text="Anmelden" ToolTip="Anmeldung für schon registrierte Benutzer" NavigateUrl="../login.aspx" />
            
        </div>


        <div id="text">
            <div id="buutons">
                <asp:HyperLink ID="hyli_onlinehelp" runat="server" ToolTip="Rufe die Bedienungsanleitung auf" ImageUrl="img/001_online_help.png" NavigateUrl="../wbf_help/help.aspx"  Target="_blank"/>
                <asp:HyperLink ID="hyli_adduser" runat="server" ToolTip="Trage Dich in die Karte ein und vernetze Dich regional" ImageUrl="img/002_add_user.png" NavigateUrl="aktimap_createUser.aspx" />
                <asp:HyperLink ID="hyli_change_account" runat="server" ToolTip="Bearbeite Deine Kontoinformationen" ImageUrl="img/005_change_account_settings.png" NavigateUrl="aktimap_createUser.aspx" Visible="false"/>
                <asp:HyperLink ID="hyli_userlist" runat="server" ToolTip="Eine Liste organisiert nach Postleitzahlen kommt noch" ImageUrl="img/003_show_list.png"  NavigateUrl="aktimap_listing_mapdata.aspx" />
                <asp:HyperLink ID="hyli_showforum" runat="server" ToolTip="Besuche das regionale Forum nejoba" ImageUrl="img/004_go_to_forum.png" NavigateUrl="../PinBoard.aspx" Target="_blank" />
            </div>
            <h4>Netzwerk für aktive Menschen und regionale Initiativen </h4>
        </div>

        <div id="btn_create_account" class="hvr_btn">
        </div>



    </form>

    <div id="map"></div>
    <script src="fullscreen.js" type="text/javascript"></script>

</body>
</html>

