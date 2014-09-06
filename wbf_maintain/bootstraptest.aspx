<%@ Page Title="" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="bootstraptest.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>






<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">

      <!-- Main hero unit for a primary marketing message or call to action -->
      <div class="hero-unit">
        <h1>...nejoba</h1>
        <p><asp:Label ID="lbl_advertisement" runat="server" Text="<strong>nejoba</strong> ist das Jobnetzwerk für Deine Nachbarschaft." ></asp:Label></p>
        <br />
        <p><a class="btn btn-primary btn-large">Beitreten !    &raquo;</a></p>
      </div>

      <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
      <div class="row">
        <div class="span2">
          <h3>
            <asp:Label ID="Label1" runat="server" Text="Haus" CssClass="table_headitem"></asp:Label>
          </h3>
          <p>
            <asp:Label ID="Label2" runat="server" Text="<strong>T&auml;tigkeiten im Haushalt:</strong> <br/><br/>Putzen <br/>Fensterreinigung <br/>Wäsche <br/>Kochen und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
        <div class="span2">
          <h3>
            <asp:Label ID="Label3" runat="server" Text="Garten" CssClass="table_headitem"></asp:Label>
          </h3>
          <p>
            <asp:Label ID="Label4" runat="server" Text="<strong>Wald- und Gartenarbeiten:</strong> <br/><br/>Gartenpflege <br/>Rasen <br/>Baumschnitt <br/>Fällungen und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
        <div class="span2">
          <h3>
            <asp:Label ID="Label5" runat="server" Text="Handwerker" CssClass="table_headitem"></asp:Label>
          </h3>
          <p>
            <asp:Label ID="Label6" runat="server" Text="<strong>Bauen und reparieren:</strong> <br/><br/>Renovieren <br/>Reperatur <br/>Bauen <br/>Technik und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
        <div class="span2">
          <h3>
            <asp:Label ID="Label7" runat="server" Text="Menschen" CssClass="table_headitem"></asp:Label>
          </h3>
          <p>
            <asp:Label ID="Label8" runat="server" Text="<strong>Soziale Betreuungen:</strong> <br/><br/>Betreuung <br/>Altenpflege <br/>Krankenpflege <br/>Geselligkeit und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
      </div>


      <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
      <div class="row">
        <div class="span3">
          <h2>
            <asp:Label ID="Label9" runat="server" Text="Bringdienst" CssClass="table_headitem"></asp:Label>
          </h2>
          <p>
            <asp:Label ID="Label10" runat="server" Text="<strong>Liefern und Holen:</strong> <br/><br/>Einkaufen <br/>Boteng&auml;nge <br/>Lieferungen <br/>Abholungen und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
        <div class="span3">
          <h2>
            <asp:Label ID="Label11" runat="server" Text="K&ouml;rperpflege" CssClass="table_headitem"></asp:Label>
          </h2>
          <p>
            <asp:Label ID="Label12" runat="server" Text="<strong>Kosmetik und Gesundheit:</strong> <br/><br/>Manik&uuml;re <br/>Pedik&uuml;re <br/>Frisur <br/>Kosmetik und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
        <div class="span3">
          <h2>
            <asp:Label ID="Label13" runat="server" Text="Haustier" CssClass="table_headitem"></asp:Label>
          </h2>
          <p>
            <asp:Label ID="Label14" runat="server" Text="<strong>Alles f&uuml;r die Haustiere:</strong> <br/><br/>Gassi <br/>Tierpflege <br/>Tierpension <br/>Hundeschule und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
        <div class="span3">
          <h2>
            <asp:Label ID="Label15" runat="server" Text="Kinder" CssClass="table_headitem"></asp:Label>
          </h2>
          <p>
            <asp:Label ID="Label16" runat="server" Text="<strong>Für die lieben Kleinen:</strong> <br/><br/>Babysitter <br/>Tagesmutter <br/>Hausaufgaben <br/>Nachhilfe und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
      </div>


      <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
      <div class="row">
        <div class="span3">
          <h2>
            <asp:Label ID="Label17" runat="server" Text="PC / Internet" CssClass="table_headitem"></asp:Label>
          </h2>
          <p>
            <asp:Label ID="Label18" runat="server" Text="<strong>Computer und Kommunikation:</strong> <br/><br/>Hilfe <br/>Webdesign <br/>Netzwerk <br/>Programmierung und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
        <div class="span3">
          <h2>
            <asp:Label ID="Label19" runat="server" Text="Transport" CssClass="table_headitem"></asp:Label>
          </h2>
          <p>
            <asp:Label ID="Label20" runat="server" Text="<strong>Lieferungen und Mobilit&auml;t:</strong> <br/><br/>Umz&uuml;ge <br/>Entsorgen <br/>Carsharing <br/>Mitfahren und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
        <div class="span3">
          <h2>
            <asp:Label ID="Label21" runat="server" Text="Heimarbeit" CssClass="table_headitem"></asp:Label>
          </h2>
          <p>
            <asp:Label ID="Label22" runat="server" Text="<strong>Arbeit von zu Hause:</strong> <br/><br/>Homeoffice <br/>Callcenter <br/>Produktion <br/>&Uuml;bersetzer und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
        <div class="span3">
          <h2>
            <asp:Label ID="Label23" runat="server" Text="Bildung" CssClass="table_headitem"></asp:Label>
          </h2>
          <p>
            <asp:Label ID="Label24" runat="server" Text="<strong>Fortbildung und Kultur:</strong> <br/><br/>Sprache <br/>Musik <br/>Literatur <br/>Foto und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
      </div>


      <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
      <div class="row">
        <div class="span3">
          <h2>
            <asp:Label ID="Label25" runat="server" Text="B&uuml;ro" CssClass="table_headitem"></asp:Label>
          </h2>
          <p>
            <asp:Label ID="Label26" runat="server" Text="<strong>Office-Dienstleistungen:</strong> <br/><br/>Schreiben <br/>Finanzen <br/>Buchhaltung <br/>Steuern und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
        <div class="span3">
          <h2>
            <asp:Label ID="Label27" runat="server" Text="KFZ/Krad" CssClass="table_headitem"></asp:Label>
          </h2>
          <p>
            <asp:Label ID="Label28" runat="server" Text="<strong>Arbeiten am Fahrzeug:</strong> <br/><br/>Pflege <br/>Inspektion <br/>Reperatur <br/>Lackierung und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
        <div class="span3">
          <h2>
            <asp:Label ID="Label29" runat="server" Text="Freizeit" CssClass="table_headitem"></asp:Label>
          </h2>
          <p>
            <asp:Label ID="Label30" runat="server" Text="<strong>Hobbies und Interessen:</strong> <br/><br/>Sport <br/>Musik <br/>Kunst <br/>Basteln und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
        <div class="span3">
          <h2>
            <asp:Label ID="Label31" runat="server" Text="Sonstiges" CssClass="table_headitem"></asp:Label>
          </h2>
          <p>
            <asp:Label ID="Label32" runat="server" Text="<strong>Soziale Betreuungen:</strong> <br/><br/>Alles andere <br/>Kontakte <br/>Anzeigen <br/>Gesuche und so weiter" CssClass="table_normalitem"></asp:Label>
          </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
        </div>
      </div>
      <hr />


    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="http://code.jquery.com/jquery-latest.js" type="text/javascript"></script>    
    <script src="bootstrap/js/bootstrap.min.js" type="text/javascript"></script>
</asp:Content>

