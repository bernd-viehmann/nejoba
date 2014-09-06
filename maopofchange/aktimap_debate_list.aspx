<%@ Page Title="Anmeldung" Language="IronPython" CodeFile="aktimap_debate_list.aspx.py" Inherits="Microsoft.Scripting.AspNet.UI.ScriptPage" EnableEventValidation="true"%>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">

<head id="Head1" runat="server">
    <meta charset="utf-8" />
    <title>...nejoba</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="" />
    <meta name="author" content="" />
    <!-- Le styles -->
    <link href="http://ajax.aspnetcdn.com/ajax/bootstrap/2.3.2/css/bootstrap.css" rel="stylesheet" type="text/css" />
    <link href="http://ajax.aspnetcdn.com/ajax/bootstrap/2.3.2/css/bootstrap-responsive.min.css" rel="stylesheet" type="text/css" />
    <link href="~/style/Default.css" rel="stylesheet" type="text/css" />
    <script type="text/javascript" src="../style/jquery-1.10.2.min.js"></script>
    <script type="text/javascript" src="../style/jqueryui/js/jquery-ui-1.8.23.custom.min.js"></script>
    <script type="text/javascript" src="../style/bootstrap/js/bootstrap.min.js"></script>
</head>

<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  -->

<body>
    <form id="form1" runat="server">

    <div class="row well">
        <div class="span12 offset1">
            <h5>
                <asp:Label ID="Label3" runat="server" Text="regionale Pinnwand " />
            </h5>
        </div>


        <div class="span3 offset1">
            <h5>
                <asp:Label ID="lbl_hashtags" runat="server" Text="Themen suchen:" />
            </h5>
            <asp:TextBox ID="txb_hashtags" runat="server" placeholder="Suche Themen in einer Stadt" ToolTip="Liste die Namen der regionalen Themen auf, die du suchst. Wenn du mehrere suchst trenne sie durch ein Komma."/>

            <h6><asp:Label ID="lbl_city" runat="server" Text="Orte:" /></h6>
            <asp:ListBox ID="sel_lctn" runat="server" ToolTip="Die hier aufgelisteten Orte werden für deine Suche auch berücksichtigt." Rows="5" Enabled="false" />
            <br />
        </div>


        <div class="span2 offset1">
            <h5>
                <asp:Label ID="Label2" runat="server" Text="Funktionen:" />
            </h5>
            <br /><br /><br />
            <asp:LinkButton ID="lnkbtn_addNewPin" runat="server" class="btn btn-small btn-danger span2" Text="hinzufügen" onclick="HandlBtnClick" ToolTip="Etwas an der Pinnwand veröffentlichen." UseSubmitBehavior="false" />
            <br /><br />
            <asp:HyperLink ID="hyli_getLink" runat="server" class="btn btn-small btn-info span2" Text="weiter geben" ToolTip="Pinnwand-Adresse zum weiterverwenden in sozialen Netzwerken." UseSubmitBehavior="false" />
            <br /><br />
            <asp:LinkButton ID="hyli_loadList" runat="server" class="btn btn-small btn-primary span2" Text="neu laden" onclick="HandlBtnClick" ToolTip="Die Liste mit Aushängen neu laden." UseSubmitBehavior="true" />
            <br /><br />
            <div id="twitter_button" runat="server" ></div>
            <div id="facebook_button" runat="server" ></div>

        </div>
    </div>


    <div class="span10 well row-fluid" id="external_link_div" runat="server" visible="false" >
        <div>
            <p>
                <asp:Label ID="lbl_linkLable" runat="server" Text="Folgenden Link kannst du in sozialen Netzen posten, in eine eMail kopieren oder als Lesezeichen nutzen.<br/>Einfach die Maus über den Link plazieren und die rechte Maustaste drücken. Dann 'Adresse kopieren' wählen" />
                <br /><br />
            </p>
            <asp:HyperLink ID="hyli_callPinnboardWithLink" runat="server" class="well">HyperLink</asp:HyperLink>
        </div>
        <div class="span1"></div>
    </div>




<div id="repeaterOutDiv" class="span12" runat="server" visible="true">

    <!-- ############################################################################################################################################ -->
    <!--   repeaer renders stuff from db to the outside world                                                                                         -->
    <!-- ############################################################################################################################################ -->
    <asp:Repeater ID="repDebateList" runat="server">
        <ItemTemplate>
            <div>
                <h5>
                    <asp:LinkButton ID="btn_openDebate" runat="server" ToolTip="Beitrag aufrufen" OnClick="HandlBtnClick"><%# Eval("subject")%></asp:LinkButton>
                </h5>
                <small>
                    <asp:Label ID='Label8' runat="server"  Text='Standort : ' />
                    <strong>
                        <asp:Label ID='Label9' runat="server"  Text='<%# Eval("locationname")%>' />
                    </strong>
                    <br />
                    <asp:Label ID='Label6' runat="server"  Text='Benutzer : ' />
                    <strong>
                        <asp:Label ID='lblBody' runat="server"  Text='<%# Eval("nickname")%>' />
                    </strong>
                    <strong>
                        <asp:Label ID='Label5' runat="server"  class="span12" Text='<%# Eval("body")%>' />
                        <br /><br />
                    </strong>
                </small>
            </div>
        </ItemTemplate>
    </asp:Repeater>
</div>

<div id="NoResultsFoundDiv" class="container" runat="server" visible="false">
    <br /><br />
    <div class="span2 offset2">
        <asp:Image ID="Image2" runat="server" ImageUrl="~/style/pic/Button-no-icon.png" />
    </div>
    <div class="span7 offset1">
        <br /><br />
        <asp:Image ID="Image3" runat="server" ImageUrl="~/style/pic/nejoba_logo_small.png" Text="...nejoba" />
        <br /><br />
        <label>
            <asp:Label ID="LabelAW6" runat="server" Text="Für dieses Postleitzahlgebiet gibt es noch keine Einträge." />
            <br />
            <asp:Label ID="LabelAW1" runat="server" Text="Melde dich an und werde der erste nejobaner in deinem Ort." />
            <br />
            <br />
            <asp:Label ID="Label1" runat="server" Text="Die nejoba Pilotstadt ist 41836 Hückelhoven." />
            <br />
            <asp:HyperLink ID="HyperLink2" runat="server" Text="Klicke hier um die Pinnwand dort als Beispiel anzusehen." NavigateUrl="parameter_result_list.aspx?loc=de|41836" ToolTip="Siehe dir ein Beispiel an" />
            <br />
            <br />
            <br />
            <asp:HyperLink ID="HyperLink1" runat="server" Text="Wenn du mehr über nejoba erfahren möchtest besuche unsere Hilfe." NavigateUrl="../wbf_help/help.aspx" ToolTip="Siehe dir ein Beispiel an" />
            <br />
        </label>
        <br /><br /><br />
    </div>
</div>



















<div style="visibility:hidden">
    <br />
    <asp:Label ID="Label4" runat="server" Text="Alle Beiträge oder die Schnittmenge   " />

    <asp:RadioButton runat="server" Checked="true" ID="radio_searchOr" GroupName="search_mode" ToolTip="Alle Beiträge in irgendeiner der Themengruppen" />
    <asp:RadioButton runat="server" Checked="false" ID="radio_searchAnd" GroupName="search_mode" ToolTip="Nur Beiträge in allen Themengruppen" />
</div>










    </form>
</body>
</html>

