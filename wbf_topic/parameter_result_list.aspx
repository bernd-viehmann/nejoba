<%@ Page Title="Liste Debatten" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="parameter_result_list.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <html xmlns:fb="http://ogp.me/ns/fb#">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server" EnableViewState="True">

    <div class="container">
        <!-- # # #  HEADER for tuning search-results # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div ID="SetUpFiltering" runat="server" class="row-fluid" visible="true">
            <!-- # # #  HEADER for tuning search-results # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="row-fluid well">
                <div class="span7 offset1">
                    <h4><asp:Label ID="Label2" runat="server" Text="Das regionale Forum" /></h4>
                    <br />
                </div>
                <div class="span7 offset1">
                    <div class="span12">
                        <h5><asp:Label ID="lbl_hashtags" runat="server" Text="Themen suchen:" /></h5>
                        <asp:TextBox ID="txb_hashtags" runat="server" CssClass="span12" placeholder="Suche Themen in einer Stadt" ToolTip="Liste die Namen der regionalen Themen auf, die du suchst. Wenn du mehrere suchst trenne sie durch ein Komma."/>
                    </div>
                    <h5><asp:Label ID="lbl_city" runat="server" Text="Orte:" /></h5>
                    <asp:ListBox ID="sel_lctn" runat="server" CssClass="span12" ToolTip="Die hier auggelisteten Orte werden für deine Sucha auch berücksichtigt." Rows="7" Enabled="false" />
                    <br />
                    <div id="twitter_button" runat="server" ></div>
                    <div id="facebook_button" runat="server" ></div>
                </div>


                <div class="span2 offset1">
                    <br />
                    <asp:ImageButton ID="btn_loadList" runat="server" onclick="HandlBtnClick" ImageUrl="../style/pic/64_reload_list.png" Text="Suchen" ToolTip="Suche starten" />
                    <br /><br />
                    <asp:ImageButton ID="btn_showLink" runat="server" onclick="HandlBtnClick" ImageUrl="../style/pic/64_facebook_button.png" NavigateUrl="#" ToolTip="Zeigt den Link zu diesem Forum zur Wiederverwendung in sozialen Netzen oder zum Verlinken auf anderen Websites" />
                    <br />
                    <asp:HyperLink ID="hyli_create_article" runat="server" ImageUrl="../style/pic/64_create_edit_item.png" NavigateUrl="../wbf_functs/debate_editor.aspx" ToolTip="Veröffentliche selbst einen Beitrag im Forum" />
                    <asp:HyperLink ID="hyli_online_help" runat="server" ImageUrl="../style/pic/64_online_help.png" NavigateUrl="#myModal" ToolTip="Was ist das regionale Forum?" role="button" data-toggle="modal"/>
                </div>

                <div style="visibility:hidden">
                    <br />
                    <asp:Label ID="Label4" runat="server" Text="Alle Beiträge oder die Schnittmenge   " />
                    <asp:RadioButton runat="server" Checked="true" ID="radio_searchOr" GroupName="search_mode" ToolTip="Alle Beiträge in irgendeiner der Themengruppen" />
                    <asp:RadioButton runat="server" Checked="false" ID="radio_searchAnd" GroupName="search_mode" ToolTip="Nur Beiträge in allen Themengruppen" />
                    <br />
                    <div>
                        <asp:Button ID="btn_loadList_hidden" runat="server" class="btn btn-large btn-primary span6 pull-right" Text="Suchen" onclick="HandlBtnClick" ToolTip="Liste laden" UseSubmitBehavior="true" />
                    </div>
                </div>
            </div>

            <div class="row-fluid well" id="external_link_div" runat="server" visible="false" >
                <div>
                    <h5><asp:Label ID="Label3" runat="server" Text="Forum veröffentlichen" /></h5>
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
                        <br /><br />
                        <asp:Label ID="Label1" runat="server" Text="Die nejoba Pilotstadt ist 41836 Hückelhoven." />
                        <br />
                        <asp:HyperLink ID="HyperLink2" runat="server" Text="Klicke hier um die Pinnwand dort als Beispiel anzusehen." NavigateUrl="parameter_result_list.aspx?loc=de|41836" ToolTip="Siehe dir ein Beispiel an" />
                        <br /><br /><br />
                        <asp:HyperLink ID="HyperLink1" runat="server" Text="Wenn du mehr über nejoba erfahren möchtest besuche unsere Hilfe." NavigateUrl="../wbf_help/help.aspx" ToolTip="Siehe dir ein Beispiel an" />
                        <br />
                    </label>
                    <br /><br /><br />
                </div>
            </div>

            <!-- Modal HELP dialog starts here  -->
            <div id="myModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                    <h5><asp:Label ID="Label7" runat="server" Text="Wozu dient das regionale Forum ?" /></h5>
                    
                </div>
                <div class="modal-body">
                    <p>
                        <asp:Label ID="Label10" runat="server" Text="Das regionale Forum dient dazu Nachbarn miteinander zu vernetzen. Es ist eine öffentliche Pinnwand, an der alle Anwohner etwas anschlagen können. Auf diese Weise entsteht eine regionaler Informationspunkt im Internet.<br /><br />So kann man sich informieren oder mit seinen Nachbarn kommunizieren. Dabei sorgen Hashtags dafür, dass der Überblick behalten bleibt. Über diese mit einem ‘#’ markierten Stichwörter ordnet man einen Beitrag einem regionalen Thema zu.<br /><br />So würde ‘#occuppy’ Leute mit Interesse an dieser Initiative miteinander vernetzen. Oder ‘#regiogeld’ wird zu einem lokalen Thema über regionale Wirtschaftsysteme. Es sind aber auch völlig andere Themen denkbar. Mit “#Fahrgemeinschaft” wird nejoba zur regionalen Mitfahrzentrale. Über den Straßennamen können Anwohner einer Straße miteinander in Kontakt bleiben." />
                    </p>
                </div>
                <div class="modal-footer">
                    <button class="btn" data-dismiss="modal" aria-hidden="true">Zurück</button>
                </div>
            </div>
            <!-- Modal HELP dialog ends here  -->

        </div>
    </div>

</asp:Content>

