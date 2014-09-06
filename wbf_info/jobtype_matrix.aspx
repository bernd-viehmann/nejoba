<%@ Page Title="nejoba: Nachbarschaftshilfe und Arbeitsmarkt" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="jobtype_matrix.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">

      <div class="row hero-unit">
        
          <asp:Image ID="Image1" runat="server" ImageUrl="~/style/pic/searchHelp.png" />
      </div>

      <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<div class="row">
    <div class="row span12">
    
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            
                <div class="span1 hero-unit" style="height:150px">
                    <h5>
                        <asp:LinkButton ID="lnk_home" runat="server" onclick="HndlrLinkClick" Text="Haus" />
                    </h5>
                    <asp:Label ID="Label4" runat="server" Text="Putzen <br/>Fensterreinigung <br/>Wäsche <br/>Kochen ..." ></asp:Label>
                </div>
                <div class="span1 hero-unit">
                    <h5>
                        <asp:LinkButton ID="lnk_garden" runat="server" onclick="HndlrLinkClick" Text="Garten" />
                    </h5>
                    <asp:Label ID="Label6" runat="server" Text="Gartenpflege <br/>Rasen <br/>Baumschnitt <br/>Fällungen ..." />
                </div>
                <div class="span1 hero-unit">
                    <h5>
                        <asp:LinkButton ID="lnk_craft" runat="server" onclick="HndlrLinkClick" Text="Handwerker" />
                    </h5>
                    <asp:Label ID="Label8" runat="server" Text="Renovieren <br/>Reperatur <br/>Bauen <br/>Technik ..." />
                </div>
                <div class="span1 hero-unit">
                    <h5>
                        <asp:LinkButton ID="lnk_human2human" runat="server" onclick="HndlrLinkClick" Text="Menschen" />
                    </h5>
                    <asp:Label ID="Label10" runat="server" Text="Betreuung <br/>Altenpflege <br/>Krankenpflege <br/>Geselligkeit ...." />
                </div>
                <div class="span1 hero-unit">
                    <h5>
                        <asp:LinkButton ID="LinkButton1" runat="server" onclick="HndlrLinkClick" Text="Menschen" />
                    </h5>
                    <asp:Label ID="Label1" runat="server" Text="Betreuung <br/>Altenpflege <br/>Krankenpflege <br/>Geselligkeit ...." />
                </div>
        </div>
            

            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            
            <div class="span2">
                <h3>
                    <asp:LinkButton ID="lnk_bringservice" runat="server" onclick="HndlrLinkClick" Text="Bringdienste" CssClass="table_headitem"/>
                </h3>
                <p>
                <asp:Label ID="Label12" runat="server" Text="<strong>Liefern und Holen:</strong> <br/><br/>Einkaufen <br/>Boteng&auml;nge <br/>Lieferungen <br/>Abholungen und so weiter" CssClass="table_normalitem"></asp:Label>
                </p>
            </div>
            <div class="span2">
                <h3>
                    <asp:LinkButton ID="lnk_personalhygiene" runat="server" onclick="HndlrLinkClick" Text="K&ouml;rperpflege" CssClass="table_headitem"/>
                </h3>
                <p>
                <asp:Label ID="Label14" runat="server" Text="<strong>Kosmetik und Gesundheit:</strong> <br/><br/>Manik&uuml;re <br/>Pedik&uuml;re <br/>Frisur <br/>Kosmetik und so weiter" CssClass="table_normalitem"></asp:Label>
                </p>
            </div>
            <div class="span2">
                <h3>
                    <asp:LinkButton ID="lnk_pets" runat="server" onclick="HndlrLinkClick" Text="Haustier" CssClass="table_headitem"/>
                </h3>
                <p>
                <asp:Label ID="Label16" runat="server" Text="<strong>Alles f&uuml;r die Haustiere:</strong> <br/><br/>Gassi <br/>Tierpflege <br/>Tierpension <br/>Hundeschule und so weiter" CssClass="table_normalitem"></asp:Label>
                </p>
            </div>
            <div class="span2">
                <h3>
                    <asp:LinkButton ID="lnk_children" runat="server" onclick="HndlrLinkClick" Text="Kinder" CssClass="table_headitem"/>
                </h3>
                <p>
                <asp:Label ID="Label18" runat="server" Text="<strong>Für die lieben Kleinen:</strong> <br/><br/>Babysitter <br/>Tagesmutter <br/>Hausaufgaben <br/>Nachhilfe und so weiter" CssClass="table_normalitem"></asp:Label>
                </p>
            </div>
            
            <br />

            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            
            <div class="span2">
                <h3>
                    <asp:LinkButton ID="lnk_computer" runat="server" onclick="HndlrLinkClick" Text="PC / Internet" CssClass="table_headitem"/>
                </h3>
                <p>
                <asp:Label ID="Label20" runat="server" Text="<strong>Computer und Kommunikation:</strong> <br/><br/>Hilfe <br/>Webdesign <br/>Netzwerk <br/>Programmierung und so weiter" CssClass="table_normalitem"></asp:Label>
                </p>
            </div>
            <div class="span2">
                <h3>
                    <asp:LinkButton ID="lnk_transport" runat="server" onclick="HndlrLinkClick" Text="Transport" CssClass="table_headitem"/>
                </h3>
                <p>
                <asp:Label ID="Label22" runat="server" Text="<strong>Lieferungen und Mobilit&auml;t:</strong> <br/><br/>Umz&uuml;ge <br/>Entsorgen <br/>Carsharing <br/>Mitfahren und so weiter" CssClass="table_normalitem"></asp:Label>
                </p>
            </div>
            <div class="span2">
                <h3>
                    <asp:LinkButton ID="lnk_homework" runat="server" onclick="HndlrLinkClick" Text="Heimarbeiten" CssClass="table_headitem"/>
                </h3>
                <p>
                <asp:Label ID="Label24" runat="server" Text="<strong>Arbeit von zu Hause:</strong> <br/><br/>Homeoffice <br/>Callcenter <br/>Produktion <br/>&Uuml;bersetzer und so weiter" CssClass="table_normalitem"></asp:Label>
                </p>
            </div>
            <div class="span2">
                <h3>
                    <asp:LinkButton ID="lnk_education" runat="server" onclick="HndlrLinkClick" Text="Bildung" CssClass="table_headitem"/>
                </h3>
                <p>
                <asp:Label ID="Label26" runat="server" Text="<strong>Fortbildung und Kultur:</strong> <br/><br/>Sprache <br/>Musik <br/>Literatur <br/>Foto und so weiter" CssClass="table_normalitem"></asp:Label>
                </p>
            </div>
            
            <br />

            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            
            <div class="span2">
                <h3>
                    <asp:LinkButton ID="lnk_office" runat="server" onclick="HndlrLinkClick" Text="B&uuml;ro" CssClass="table_headitem"/>
                </h3>
                <p>
                <asp:Label ID="Label28" runat="server" Text="<strong>Office-Dienstleistungen:</strong> <br/><br/>Schreiben <br/>Finanzen <br/>Buchhaltung <br/>Steuern und so weiter" CssClass="table_normalitem"></asp:Label>
                </p>
            </div>
            <div class="span2">
                <h3>
                    <asp:LinkButton ID="lnk_vehicles" runat="server" onclick="HndlrLinkClick" Text="KFZ/Krad" CssClass="table_headitem"/>
                </h3>
                <p>
                <asp:Label ID="Label30" runat="server" Text="<strong>Arbeiten am Fahrzeug:</strong> <br/><br/>Pflege <br/>Inspektion <br/>Reperatur <br/>Lackierung und so weiter" CssClass="table_normalitem"></asp:Label>
                </p>
            </div>
            <div class="span2">
                <h3>
                    <asp:LinkButton ID="lnk_leisure" runat="server" onclick="HndlrLinkClick" Text="Freizeit" CssClass="table_headitem"/>
                </h3>
                <p>
                <asp:Label ID="Label32" runat="server" Text="<strong>Hobbies und Interessen:</strong> <br/><br/>Sport <br/>Musik <br/>Kunst <br/>Basteln und so weiter" CssClass="table_normalitem"></asp:Label>
                </p>
            </div>
            <div class="span2">
                <h3>
                    <asp:LinkButton ID="lnk_notspecified" runat="server" onclick="HndlrLinkClick" Text="Sonstiges" CssClass="table_headitem"/>
                </h3>
                <p>
                <asp:Label ID="Label34" runat="server" Text="<strong>Soziale Betreuungen:</strong> <br/><br/>Alles andere <br/>Kontakte <br/>Anzeigen <br/>Gesuche und so weiter" CssClass="table_normalitem"></asp:Label>
                </p>
            </div>
            
    
</div>
<br /><br />
   
</asp:Content>

