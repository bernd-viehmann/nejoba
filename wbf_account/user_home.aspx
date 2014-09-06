<%@ Page Title="nejoba Benutzerfunktionen" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="user_home.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">



    <div class="row">
        <div class="accordion" id="Div1">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <h4>
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >
                            Funktionen
                        </a>
                    </h4>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
<strong>Du findest hier Links zu den wichtigsten Funktionen auf nejoba</strong>
<br />
                    </div>
                </div>
            </div>
        </div>
    </div>





    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div class="row">
        <div class="span2 offset1">
            <asp:ImageButton ID="btn_helpwanted" class="btn img-polaroid" runat="server" Text="Arbeit suchen und Nachbarn helfen" onclick="HndlrButtonClick" ImageUrl="~/style/pic/searchHelp.png" ToolTip="Ver&ouml;ffentliche eine Arbeitsangebot und hole dir Hilfe bei deinen Nachbarn"  />
            <h4>
                <asp:Label ID="Labelds1" runat="server" Text="Arbeit vergeben" class="muted"></asp:Label>
            </h4>
        </div>
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="span2 offset1">
            <asp:ImageButton ID="btn_work" class="btn img-polaroid" runat="server" Text="Arbeit suchen und Nachbarn helfen" onclick="HndlrButtonClick" ImageUrl="~/style/pic/searchJob.png" ToolTip="Hilf deinen Nachbarn und finde Arbeit"  />
            <h4>
                <asp:Label ID="Label6" runat="server" Text="Arbeit suchen" class="muted"></asp:Label>
            </h4>
        </div>
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="span2 offset1">
            <asp:ImageButton ID="btn_debate" class="btn img-polaroid" runat="server" Text="Lokale Debaten" onclick="HndlrButtonClick" ImageUrl="~/style/pic/quatschtuete.png" ToolTip="Debatiere öffentlich mit deinen Nachbarn  "  />
            <h4>
                <asp:Label ID="Label3" runat="server" Text="Nachbarforum" class="muted"></asp:Label>
            </h4>
        </div>
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    </div>
    <hr />
    <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div class="row">
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="span2 offset1">
            <asp:ImageButton ID="btn_help" class="btn img-polaroid" runat="server" Text="nejoba bedienen" onclick="HndlrButtonClick" ImageUrl="~/style/pic/hilfe.png" ToolTip="Wie wird nejoba bedient"  />
            <h4>
                <asp:Label ID="Label4" runat="server" Text="Bedienung" class="muted"></asp:Label>
            </h4>
        </div>
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="span2 offset1">
            <asp:ImageButton ID="btn_ownlists" class="btn img-polaroid" runat="server" Text="Deine Anfragen und Angebote" onclick="HndlrButtonClick" ImageUrl="~/style/pic/beitreten.png" ToolTip="Deine Anfragen und Angebote"  />
            <h4>
                <asp:Label ID="Label9" runat="server" Text="Aktivitäten" class="muted"></asp:Label>
            </h4>
        </div>
        <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="span2 offset1">
            <!--
            <asp:ImageButton ID="btn_premium" class="btn img-polaroid" runat="server" Text="Der Premium-Account" onclick="HndlrButtonClick" ImageUrl="~/style/pic/premium.png" ToolTip="Der bezahlte Sonderservice"  />
            <h4>
                <asp:Label ID="Label1" runat="server" Text="48-Stunden Vorsprung" class="muted"></asp:Label>
            </h4>
            <label>
                <asp:Label ID="Label2" runat="server" Text="Als Premium-Mitglied kannst du 48 Stunden früher reagieren"></asp:Label>
            </label>
            -->
        </div>
    </div>    
</asp:Content>

