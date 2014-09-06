<%@ Page Title="Liste Debatten" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="debate_list.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server" EnableViewState="True">

<div class="container">
    <!-- # # #  HEADER for tuning search-results # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div ID="SetUpFiltering" runat="server" class="span10" visible="true">

        <!-- # # #  HEADER for tuning search-results # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="span10">
            <div class="span3 offset1">
                <h4><asp:Label ID="lbl_head" runat="server" Text="Themen in deiner Stadt" /></h4>
                <br />
                <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/quatschtuete.png" ToolTip="Liste von Themen" />
            </div>
            <div class="span6 offset1">
                <h5><asp:Label ID="lbl_hashtags" runat="server" Text="Suchbegriff" /></h5>
                <asp:Label ID="Label2" runat="server" Text="Gib ein oder mehrere Suchbegriff als Thema ein. Wenn du keine Suchworte eingibst, bekommst du alle Themen aus der Region angezeigt" /><br />
                <asp:TextBox ID="txb_hashtags" runat="server" class="span10" placeholder="Suche Themen in einer Stadt" ToolTip="Ein Thema ist sind Stichworte das mit einem Ort verbunden ist. Du kannst auch mehrere gleichzeitig suchen." />

                <h5><asp:Label ID="lbl_city" runat="server" Text="Ort" /></h5>
                <asp:Label ID="Label4" runat="server" Text="W&auml;hle einen Ort f&uuml;r deine Suche. Die Postleitzahlen in der Umgebung einbezogen." />
                <br />
                <asp:Label ID="Label1" runat="server" Text="Der Button 'Ort ändern' l&auml;sst dich in eine andere Gegend wechseln. " />

                <asp:DropDownList ID="sel_lctn" runat="server" class="span10" ToolTip="W&auml;hle den Ort aus an dem diskutiert wird." />
                <asp:Button ID="btn_changeLocation" runat="server" class="btn btn-large btn-inverse" Text="Ort ändern" OnClick="HandlBtnClick" UseSubmitBehavior="false" />
                                        
                <br /><br />
                <asp:Label ID="Label7" runat="server" Text="Der blaue Button holt die Liste aus der Datenbank. Du kannst jedes Element in der Liste anklicken." />
                <br />
                <asp:Button ID="btn_search" runat="server" class="btn btn-large btn-primary" Text="Liste neu laden" onclick="HandlBtnClick" UseSubmitBehavior="true" />
            </div>
        </div>

    </div>


    <!-- ############################################################################################################################################ -->
    <!--   repeaer renders stuff from db to the outside world                                                                                         -->
    <!-- ############################################################################################################################################ -->

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
</div>
</asp:Content>

