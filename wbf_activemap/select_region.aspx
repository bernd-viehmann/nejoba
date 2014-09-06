<%@ Page Title="Starseite nejoba" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="select_region.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div class="row-fluid">
        <div class="span10 offset1">
        <br />
            <div class="span3">
                <h4>
                    <asp:Label ID="Labelds1" runat="server" Text="Finde Initiativen und aktive Menschen" class="muted"></asp:Label>
                </h4>
                <h5><asp:Label ID="Label11" runat="server" Text="Land" /></h5>
                <asp:DropDownList ID="sel_country" runat="server" />
                <h5><asp:Label ID="Label10" runat="server" Text="Ortsname" /></h5>
                <asp:TextBox ID="txb_cityname" runat="server" />
                <div id="kaese" runat="server" visible="true" >
                    <div id="PostCodeText" runat="server" visible="true">
                    <h5><asp:Label ID="lblPstCode" runat="server" Text="Postleitzahl" /></h5>
                    <asp:TextBox ID="txbx_postCode" runat="server" />
                    </div>
                    <div class="label label-warning" id="PostCodeSelect" runat="server" visible="false">
                    <h5><asp:Label ID="lblMultiSelCode" runat="server" Text="Postleitzahl" /></h5>
                    <asp:DropDownList ID="sel_mulitPostCode" runat="server" />
                    </div>
                </div>
                <br /><br />
                <asp:Button ID="btn_showPinBoard" runat="server" class="btn btn-large btn-primary" Text="Anzeigen" ToolTip="Zentriert die Karte nach deiner Eingabe" onclick="HndlrButtonClick" />
            </div>

            <div class="span6 offset1">
                <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/map_wallpaper.png" />
            </div>
    </div>
    <div class="row hidden">
        <asp:Label ID="timeIsNow" runat="server" ></asp:Label> 
    </div>
    <div class="thehidden">
        <!-- hidden textfields used for statusmessages from the server (easier internationalization of the text -->
        <asp:Label ID="msg_pleaseSelPostCode" runat="server" Text="Bitte Postleitzahl bestimmen...." ></asp:Label>
        <asp:Label ID="msg_unknownPostCode" runat="server" Text="Aus Deiner Eingabe konnte keine Postleitzahl gewonnen werden. <br />Bitte &uuml;berpr&uuml;fe den Namen der Stadt und suche (z.B. bei Wikipedia) <br />nach der Postleitzahl des gesuchten Ortes." ></asp:Label>
    </div>

</asp:Content>

