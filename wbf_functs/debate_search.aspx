<%@ Page Title="Suche Diskussionen" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="debate_search.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server" EnableViewState="true">
    <div class="container">

        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <!-- # #   Heading                                                                                                                                                                                                     # # # -->
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div ID="SetUpFiltering" runat="server" class="row hero-unit" visible="true">
            <div class="container-fluid">
                <div class="row-fluid">
                    <div class="span3 offset1">
                        <h3><asp:Label ID="Label8" runat="server" Text="Themen suchen" /></h3>
                        <br />
                        <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/quatschtuete.png" ToolTip="Liste von Themen" />

                    </div>
                    <div class="span6 offset1">

                        <h5><asp:Label ID="Label9" runat="server" Text="Suchbegriffe" /></h5>
                        <asp:TextBox ID="txb_hashtags" runat="server" placeholder="Suchbegriffe (sogn. Hashtags) " class="span10" />

                        <div id="kaese" runat="server" visible="true" >
                            <div id="PostCodeText" runat="server" visible="true">
                                <h5><asp:Label ID="lblPstCode" runat="server" Text="Postleitzahl" /></h5>
                                <asp:TextBox ID="txbx_postCode" runat="server" class="span10"/>
                            </div>
                            <div class="label label-warning" id="PostCodeSelect" runat="server" visible="false">
                                <h5><asp:Label ID="lblMultiSelCode" runat="server" Text="Postleitzahl" /></h5>
                                <asp:DropDownList ID="sel_mulitPostCode" runat="server" class="span10"/>
                            </div>
                        </div>
                        <h5><asp:Label ID="Label10" runat="server" Text="Ortsname" /></h5>
                        <asp:TextBox ID="txb_cityname" runat="server" class="span10" />

                        <h5><asp:Label ID="Label11" runat="server" Text="Land" /></h5>
                        <asp:DropDownList ID="sel_country" runat="server" class="span10" />

                        <br />
                        <asp:Label ID="Label12" runat="server" Text="W&auml;hle oben die Themen aus, die du suchst. Lasse das Feld leer, um alle Themen in einem Ort zu finden. <br/><br/>Gib darunter an, wo du suchst. Wenn es zu einem Ortsnamen mehrere Postleitzahlen gibt, musst du dich für eine entscheiden. Bei der Suche berücksichtigt nejoba auch die Nachbarorte.<br/><br/>Dann klicke den Button, um die Ergebnisse angezeigt zu bekommen." />
                        <br /><br />
                        <asp:Button ID="btn_search" runat="server" class="btn btn-large btn-primary" Text="Suchen" onclick="HndlrStartSearch"/>
                    </div>
                </div>
            </div>
        </div>
    </div> <!-- /container -->

    <div class="thehidden">
        <!-- hidden textfields used for statusmessages from the server (easier internationalization of the text -->
        <asp:Label ID="msg_pleaseSelPostCode" runat="server" Text="Bitte Postleitzahl bestimmen...." ></asp:Label>
        <asp:Label ID="msg_unknownPostCode" runat="server" Text="Aus Deiner Eingabe konnte keine Postleitzahl gewonnen werden. <br />Bitte &uuml;berpr&uuml;fe den Namen der Stadt und suche (z.B. bei Wikipedia) <br />nach der Postleitzahl des gesuchten Ortes." ></asp:Label>
    </div>
</asp:Content>

