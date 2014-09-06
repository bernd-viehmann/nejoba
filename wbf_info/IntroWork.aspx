<%@ Page Title="nejoba: Nachbarschaftshilfe und Arbeitsmarkt" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="IntroWork.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
<div class="container">

    <div id="offerJobDiv" class="row hero-unit" runat="server">
            <div class="span3">
                <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/searchHelp.png" ToolTip="Hier findest du etwas zu tun " />
            </div>
            <div class="span5">
                <h3>
                    <asp:Label ID="Label2" runat="server" Text="Arbeit vergeben" />
                </h3>
                <label>
                    <asp:Label ID="Label1" runat="server" Text="W&auml;hle einen Oberbegriff aus, unter dem du deinen Auftrag einsortieren m&ouml;chtest. Klicke dazu auf den roten Arbeitsbereich" />
                    <br /><br />
                    <strong>
                        <asp:Label ID="Label7" runat="server" Text="Auftr&auml;ge werden auf nejoba kostenfrei ver&ouml;ffentlicht" />
                    </strong>
                    
                </label>
            </div>
    </div>


    <div id="searchJobDiv" class="row hero-unit" runat="server">
            <div class="span3">
                <asp:Image ID="Image2" runat="server" class="img-polaroid" ImageUrl="~/style/pic/searchJob.png" ToolTip="Hier findest du etwas zu tun " />
            </div>
            <div class="span5">
                <h3>
                    <asp:Label ID="Label3" runat="server" Text="Arbeit suchen" />
                </h3>
                <label>
                    <asp:Label ID="Label5" runat="server" Text="Klicke hier auf einen roten Arbeitsbereich, um eine Vorauswahl zu treffen.<br/>Es erscheint dann eine Liste mit den passenden Arbeiten, die zu vergeben sind." />
                    <br /><br />
                    <asp:Label ID="Label9" runat="server" Text="Für private und gewerbliche Nutzer ohne Mitarbeiter ist nejoba kostenfrei." />
                    <br />
                    <asp:HyperLink ID="HyperLink1" runat="server" Text="Sicher dir einen Vorteil mit dem 48h-Vorsprung."  NavigateUrl="~/wbf_account/pay_start.aspx" />
                </label>
            </div>
    </div>


    <div class="row span12">

            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_home" runat="server" onclick="HndlrLinkClick" Text="Haus" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label4" runat="server" Text="<br/>Putzen <br/>Fensterreinigung <br/>Wäsche <br/>Kochen usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_garden" runat="server" onclick="HndlrLinkClick" Text="Garten" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label6" runat="server" Text="<br/>Gartenpflege <br/>Rasen <br/>Baumschnitt <br/>Fällungen usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_craft" runat="server" onclick="HndlrLinkClick" Text="Handwerker" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label8" runat="server" Text="<br/>Renovieren <br/>Reparatur <br/>Bauen <br/>Technik usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_human2human" runat="server" onclick="HndlrLinkClick" Text="Menschen" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label10" runat="server" Text="<br/>Betreuung <br/>Altenpflege <br/>Krankenpflege <br/>Geselligkeit usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_bringservice" runat="server" onclick="HndlrLinkClick" Text="Bringdienste" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label12" runat="server" Text="<br/>Einkaufen <br/>Boteng&auml;nge <br/>Lieferungen <br/>Abholungen usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_personalhygiene" runat="server" onclick="HndlrLinkClick" Text="K&ouml;rperpflege" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label14" runat="server" Text="<br/>Manik&uuml;re <br/>Pedik&uuml;re <br/>Frisur <br/>Kosmetik usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_pets" runat="server" onclick="HndlrLinkClick" Text="Haustier" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label16" runat="server" Text="<br/>Gassi <br/>Tierpflege <br/>Tierpension <br/>Hundeschule usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_children" runat="server" onclick="HndlrLinkClick" Text="Kinder" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label18" runat="server" Text="<br/>Babysitter <br/>Tagesmutter <br/>Hausaufgaben <br/>Nachhilfe usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_computer" runat="server" onclick="HndlrLinkClick" Text="PC / Internet" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label20" runat="server" Text="<br/>Hilfe <br/>Webdesign <br/>Netzwerk <br/>Programmierung usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_transport" runat="server" onclick="HndlrLinkClick" Text="Transport" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label22" runat="server" Text="<br/>Umz&uuml;ge <br/>Entsorgen <br/>Carsharing <br/>Mitfahren usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_homework" runat="server" onclick="HndlrLinkClick" Text="Heimarbeiten" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label24" runat="server" Text="<br/>Homeoffice <br/>Callcenter <br/>Produktion <br/>&Uuml;bersetzer usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_education" runat="server" onclick="HndlrLinkClick" Text="Bildung" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label26" runat="server" Text="<br/>Sprache <br/>Musik <br/>Literatur <br/>Foto usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_office" runat="server" onclick="HndlrLinkClick" Text="B&uuml;ro" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label28" runat="server" Text="<br/>Schreiben <br/>Finanzen <br/>Buchhaltung <br/>Steuern usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_vehicles" runat="server" onclick="HndlrLinkClick" Text="KFZ/Krad" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label30" runat="server" Text="<br/>Pflege <br/>Inspektion <br/>Reparatur <br/>Lackierung usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_leisure" runat="server" onclick="HndlrLinkClick" Text="Freizeit" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label32" runat="server" Text="<br/>Sport <br/>Musik <br/>Kunst <br/>Basteln usw...." CssClass="table_normalitem"></asp:Label>
            </div>
            <div class="span2">
                <strong>
                    <br />
                    <asp:LinkButton ID="hyLnk_notspecified" runat="server" onclick="HndlrLinkClick" Text="Sonstiges" CssClass="table_headitem"/>
                </strong>
                <asp:Label ID="Label34" runat="server" Text="<br/>Alles andere <br/>Kontakte <br/>Anzeigen <br/>Gesuche usw...." CssClass="table_normalitem"></asp:Label>
            </div>

        </div>

    </div>
    </div>

</div>
   
</asp:Content>

