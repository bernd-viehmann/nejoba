<%@ Page Title="Starseite nejoba" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="loginfailure.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">


<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->

    <div class="row">
        <div class="accordion" id="Div1">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <h4>
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >Fehler beim LogIn</a>
                    </h4>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
                            

<br />
<h5>nejoba kann dein Konto nicht finden </h5>
<br />

<br /><br />
<strong>1. Konto anlegen</strong>
<br /><br />
<br /><br />

<strong>2. erneut anmelden</strong>
<br /><br />
<br /><br />
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row"><br /></div>

    <div class="row alert alert-error">
        <strong>
        <asp:Label ID="Label3" runat="server" Text="Die Anmeldung hat nicht geklappt. "></asp:Label>
        </strong>
        <br />
        <asp:Label ID="Label4" runat="server" Text="Bitte versuche es noch einmal. Wenn Du noch kein Konto hast lege dir eins an. "></asp:Label>
        <br />
    </div>

    <div class="row"><br /><br /></div>

<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div class="row well">
        <strong><asp:Label ID="Label2" runat="server" Text="Versuche dich noch einmal anzumelden"></asp:Label></strong>
        <br /><br />
        <asp:HyperLink ID="HyperLink1" runat="server" class="btn btn-large btn-success" NavigateUrl="~/wbf_account/user_home.aspx" >Erneut versuchen</asp:HyperLink>
    </div>

    <div class="row"><br /><br /></div>

    <div class="row well">
        <strong><asp:Label ID="Label1" runat="server" Text="Erstelle ein eigenes Konto"></asp:Label></strong>
        <br /><br />
        <asp:HyperLink ID="HyperLink2" runat="server" class="btn btn-large btn-inverse" NavigateUrl="~/wbf_activemap/create_map_user.aspx" >Konto anlegen</asp:HyperLink>
    </div>

    <div class="row hidden">
        <asp:Label ID="timeIsNow" runat="server" ></asp:Label> 
    </div>

</asp:Content>

