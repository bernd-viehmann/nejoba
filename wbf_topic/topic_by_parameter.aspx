<%@ Page Title="Liste Debatten" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="topic_by_parameter.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server" EnableViewState="True">

<div class="container">
    <!-- # # #  HEADER for tuning search-results # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div ID="SetUpFiltering" runat="server" class="row span12" visible="true">

        <!-- # # #  HEADER for tuning search-results # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="container-fluid">
            <div class="span12 row-fluid">

                <div class="span3 well">
                    <h4><asp:Label ID="lbl_head" runat="server" Text="regionale Themen" /></h4>
                    <br />
                    <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/quatschtuete.png" ToolTip="Liste von Themen" />

                    <h5><asp:Label ID="lbl_hashtags" runat="server" Text="Suchbegriff(e) :" /></h5>
                    <asp:TextBox ID="txb_hashtags" runat="server" class="span12" placeholder="Suche Themen in einer Stadt" ToolTip="Du kannst mehrere Themen-Stichworte (getrennt durch Kommas) suchen." />
                    <br />

                    <h5><asp:Label ID="lbl_rubric" runat="server" Text="Rubrik :" /></h5>
                    <asp:TextBox ID="txb_rubricName" runat="server" class="span12" Enabled="false" ToolTip="Wenn du eine Rubrik gewählt hast steht sie hier." />
                    <br />

                    <h5><asp:Label ID="lbl_city" runat="server" Text="Liste der Orte :" /></h5>
                    <asp:ListBox ID="sel_lctn" runat="server" ToolTip="Die hier aufgelisteten Orte werden für deine Suche mit berücksichtigt." Rows="9" Enabled="false" />

                    <br />
                    <asp:Button ID="btn_changeLocation" runat="server" class="btn btn-large btn-inverse" Text="Ort ändern" OnClick="HandlBtnClick" ToolTip="Wähle einen anderen Ort als Eingang für deine Suche" UseSubmitBehavior="false" Visible="false" />
                    <br />
                    <asp:Button ID="btn_getNejobaButton" runat="server" class="btn btn-large btn-inverse" Text="Liste einbinden" OnClick="HandlBtnClick" ToolTip="Verwende die nejoba-Daten auf deiner Website." UseSubmitBehavior="false" Visible="false" />
                    <br /><br />
                    <asp:Button ID="btn_loadList" runat="server" class="btn btn btn-large btn-primary span12" Text="Liste laden" onclick="HandlBtnClick" ToolTip="Liste aktualisieren" UseSubmitBehavior="true" />
                </div>





                <div class="span9">

                    <div id="repeaterOutDiv" class="span12 row" runat="server" visible="true">
                        <!-- ############################################################################################################################################ -->
                        <!--   repeaer renders stuff from db to the outside world                                                                                         -->
                        <!-- ############################################################################################################################################ -->
                        <asp:Repeater ID="repDebateList" runat="server">
                            <ItemTemplate>
                                <div>
                                    <h5>
                                        <asp:HyperLink ID="hyLnk_opnDbt" runat="server" Text='<%# Eval("subject")%>' NavigateUrl='<%# Eval("tagZero")%>' Target="_blank" />
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

    


                    <!-- ############################################################################################################################################ -->
                    <!--   this div is shown when no results were found
                    <!-- ############################################################################################################################################ -->
                    <div id="NoResultsFoundDiv" class="container" runat="server" visible="false">
                        <br /><br />
                        <div class="span2 offset2">
                            <asp:Image ID="Image3" runat="server" ImageUrl="~/style/pic/nejoba_logo_small.png" Text="...nejoba" />
                            <asp:Image ID="Image2" runat="server" ImageUrl="~/style/pic/Button-no-icon.png" />
                        </div>
                        <div class="span7 offset1">
                            <br /><br /><br /><br />
                            <label>
                                <asp:Label ID="LabelAW6" runat="server" Text="Für dieses Postleitzahlgebiet gibt es noch keine Einträge." />
                                <br />
                                <asp:Label ID="LabelAW1" runat="server" Text="Melde dich an und werde der erste nejobaner in deinem Ort." />
                                <br />
                                <br />
                                <asp:Label ID="Label12" runat="server" Text="Die nejoba Pilotstadt ist 41836 Hückelhoven." />
                                <br />
                                <asp:HyperLink ID="hyLnk_demo" runat="server" Text="Klicke hier um die Pinnwand dort als Beispiel anzusehen." NavigateUrl="parameter_result_list.aspx?loc=de|41836" ToolTip="Siehe dir ein Beispiel an" />
                                <br />
                                <br />
                                <br />
                                <asp:HyperLink ID="hyLnk_help" runat="server" Text="Wenn du mehr über nejoba erfahren möchtest besuche unsere Hilfe." NavigateUrl="../wbf_help/help.aspx" ToolTip="Siehe dir ein Beispiel an" />
                                <br />
                            </label>
                            <br /><br /><br />
                        </div>
                    </div>













                    <div id="nejobaButtonDiv" runat="server" visible="false">
                        <h5>
                            <asp:Label ID="Label1" runat="server" Text="Der nejoba-Button" />
                            <img class="pull-right" src="style/pic/nejoba_button.png" />
                        </h5>
                        <br /><br />
                        <p>
                            <asp:Label ID="Label2" runat="server" Text="Nutze die offene nejoba-Datenbank für deine eigenen Website. Baue einen Button ein, der die Themenliste auf nejoba öffnet. " />
                            <asp:Label ID="Label3" runat="server" Text="So kannst du deine Besuche mit den aktuellen Beiträgen zu regionalen Themen auf nejoba informieren." />
                            <br /><br />
                            <asp:Label ID="Label10" runat="server" Text="Im unteren Kasten wird die der HTML-Code angezeigt, den du auf deinen eigene Website übertragen kannst." />
                            <asp:Label ID="Label7" runat="server" Text="So können die Besucher deiner Webseite diese Daten einfach abrufen und kommentieren." />
                        </p>
                        <br />
                        <pre><asp:Label ID="lbl_buttonCode" runat="server" Text="__HTML__CODE__" /></pre>
                        <br />
                        <p>
                            <asp:Label ID="Label11" runat="server" Text="Mit dem blauen Button 'Liste laden' werden wieder die Suchergebnisse angezeigt." />
                        </p>
                    </div>

                </div>













            </div>
        </div>
    </div>
</div>
</asp:Content>

