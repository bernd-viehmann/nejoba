<%@ Page Title="Online-Hilfe" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="help.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

<div class="container span11">

    <h3>nejoba: deine Nachbarschaft 2.0  </h3>
    <br />
    <h5>
    nejoba ist eine Internetplattform die den Kontakt unter Nachbarn fördern soll. Mit Hilfe von nejoba können sich Menschen einer Stadt gegenseitig informieren, sie können miteinander in Kontakt kommen und einander helfen.
    <br /><br />
    </h5>

    <p>
    Die Idee ist ein schwarzes Brett für eine Stadt. Stell Dir vor in deinem Heimatort stünde vor dem Rathaus eine Pinnwand, an der jeder Bewohner einen Zettel aushängen könnte. 
    nejoba steht aber nicht am Rathhaus sondern im Internet. Es ist eine Website die zu jeder Postleitzahl eine Info-Datenbank bietet, auf der Anwohner etwas veröffentlichen und alle sich informieren können.
    Dabei sind nicht nur Texte möglich. Man kann vielmehr auch Photos und Filme zeigen. Außerdem  lassen sich Verweise auf externe Websites einbauen.
    Dabei sind die Informationen gut organisiert. Jedem Beitrag kann man einen Ort zuweisen, der auf einer Karte dargestellt wird. Es lassen sich Termine festlegen und über regional gültige Hashtags werden die Daten gruppiert.  
    Zudem bietet nejoba ein Forum an um Job-Börse zu organisieren. So entsteht ein neuer regionaler Arbeitsmarkt, der auch für den Tausch von Dienstleistungen geeignet ist.
    </p>
    <br />
    
    <asp:HyperLink ID="HyperLink_YouTube" runat="server" NavigateUrl="http://www.youtube.com/user/nejobavideo" Target="_blank">Videos zum Thema nejoba auf YouTube</asp:HyperLink>
    <br />
    <asp:HyperLink ID="HyperLink_facebook" runat="server" NavigateUrl="https://www.facebook.com/nejoba" Target="_blank">Unser Benutzerforum auf facebook.</asp:HyperLink>
    <br />
    <br /><br />

    <strong>
        nejoba bietet zwei Funktionen:
    </strong>
    <br /><br />

    <div class="well">
        <asp:Image ID="Image8" runat="server" class="img-polaroid" ImageUrl="~/style/pic/quatschtuete.png" ToolTip="Regional kommunizieren, informieren und vernetzen" />
        <br />
        <strong>1. Das Nachbarforum</strong>
        <br /><br />
        Das Nachbarforum kann man sich als öffentliches schwarzes Brett für Deine Stadt vorstellen. Jeder kann dort Infos zu seinem Ort lesen als auch etwas veröffentlichen. So entsteht eine einfache öffentliche Infobörse für die Bewohner oder Besucher einer Stadt.
        Dabei kann nicht nur reiner Text geteilt werden. nejoba bietet auch die Möglichkeit Bilder und Videos einzubinden, Orte auf einer Karte zu markieren und Termine festzulegen.
        <br /><br />
        So verrät dir nejoba was wann und wo abgeht in deiner Gegend.
        <br /><br />
        <a href="help_debates.aspx">Erfahre mehr zum Nachbarforum</a>
        <br /><br />
    </div>
    <br />

    <div class="well">
        <asp:Image ID="Image9" runat="server" class="img-polaroid" ImageUrl="~/style/pic/searchHelp.png" ToolTip="Privater Arbeitsmarkt" />
        <br />
        <strong>2. Die Job-Börse</strong>
        <br /><br />
        Die Job-Börse ist eine private Jobbörse. Sie funktioniert nach dem Prinzip von Auftrags-Ausschreibungen. Wenn jemand etwas erledigt haben möchte veröffentlicht er eine Anfrage auf nejoba. Diese kann nun von anderen Leuten aus der Gegend eingesehen werden. Wenn jemand helfen kann antwortet er dem Nachbarn. 
        <br /><br />
        <a href="help_jobmarket.aspx">Erfahre mehr zur Job-Börse</a>
        
        <br /><br />
    </div>
    <br />

    <div class="well">
        <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="https://www.youtube.com/yt/brand/media/image/yt-brand-standard-logo-95x40.png" ToolTip="Anleitungen auf YouTube" />
        <strong>Videoanleitungen</strong>
        
        <div class="span12"><br /></div>

        <div>
            <div class="span4">
            <iframe width="320" height="240" src="//www.youtube.com/embed/m5Kg7KOVaYU" frameborder="0" allowfullscreen></iframe>
            </div>
            <div class="span4 offset1">
            <iframe width="320" height="240" src="//www.youtube.com/embed/ofsPJ3ta5qw" frameborder="0" allowfullscreen></iframe>
            </div>
            <br /><br />
        </div>
        <div class="span12"><br /></div>
        <div>
            <div class="span4">
            <iframe width="320" height="240" src="//www.youtube.com/embed/Kkg3GQm7Hdc" frameborder="0" allowfullscreen></iframe>
            </div>
            <div class="span4 offset1">
            <iframe width="320" height="240" src="//www.youtube.com/embed/otCK2HGi4t0" frameborder="0" allowfullscreen></iframe>
            </div>
            <br /><br />
        </div>
        <div class="span12"><br /></div>
        <div>
            <div class="span4">
            <iframe width="320" height="240" src="//www.youtube.com/embed/MhFjlYCjGlg" frameborder="0" allowfullscreen></iframe>
            </div>
            <div class="span4 offset1">
            <iframe width="320" height="240" src="//www.youtube.com/embed/42sYJAE6VbI" frameborder="0" allowfullscreen></iframe>
            </div>
            <br /><br />
        </div>
    </div>
    <br /><br />


</div>

<!-- /container -->

</asp:Content>

