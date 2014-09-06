<%@ Page Title="Liste Debatten" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="topic_display_taggs.aspx.py" %>

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

            <div class="row-fluid">
                <div class="span4 well">
                    <h4><asp:Label ID="Label12" runat="server" Text="Hashtaggs am Ort" /></h4>
                    <br />
                    <asp:Image ID="Image2" runat="server" class="img-polaroid" ImageUrl="~/style/pic/quatschtuete.png" ToolTip="Hier siehst du welche Stichworte (Hashtaggs) schon an einem bestimmten Ort verwendet werden." />

                        <div class="span12">
                            <h5><asp:Label ID="Label4" runat="server" Text="Ort:" /></h5>
                            <asp:DropDownList ID="sel_lctn" runat="server" class="span10" ToolTip="W&auml;hle einen Ort in der Nähe aus." AutoPostBack="true" />
                            <br />
                            <asp:Button ID="btn_Location" runat="server" class="btn btn-large btn-inverse" Text="Ort &auml;ndern" OnClick="HandlBtnClick"/>
                            <br /><br />
                            <h5><asp:Label ID="lbl_startingChar" runat="server" Text="Anfangsbuchstaben wählen" /></h5>
                        </div>
                        <div class="span12 well">
                            <asp:LinkButton ID="hyLnk_char_a" runat="server" Text="A" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_b" runat="server" Text="B" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_c" runat="server" Text="C" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_d" runat="server" Text="D" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_e" runat="server" Text="E" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_f" runat="server" Text="F" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_g" runat="server" Text="G" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                                
                            <asp:LinkButton ID="hyLnk_char_h" runat="server" Text="H" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_i" runat="server" Text="I" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_j" runat="server" Text="J" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_k" runat="server" Text="K" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_l" runat="server" Text="L" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_m" runat="server" Text="M" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_n" runat="server" Text="N" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                                
                            <asp:LinkButton ID="hyLnk_char_o" runat="server" Text="O" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_p" runat="server" Text="P" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_q" runat="server" Text="Q" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_r" runat="server" Text="R" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_s" runat="server" Text="S" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_t" runat="server" Text="T" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_u" runat="server" Text="U" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                                
                            <asp:LinkButton ID="hyLnk_char_v" runat="server" Text="V" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_w" runat="server" Text="W" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_x" runat="server" Text="X" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_y" runat="server" Text="Y" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                            <asp:LinkButton ID="hyLnk_char_z" runat="server" Text="Z" Width="20px" OnClick="HandlBtnClick" CssClass="label" EnableViewState="False" />
                        </div>
                        <div class="span10">
                            <h5><asp:Label ID="Label1456" runat="server" Text="Hashtagg:" /></h5>
                            <asp:TextBox ID="txb_hashtags" runat="server" class="span8" ToolTip="Wenn du einen Buchstaben gewählt hast kannst du hier per Text suchen." />
                            <br />
                            <asp:Button ID="btn_Find" runat="server" class="btn btn-large  btn-primary" Text="Liste laden" OnClick="HandlBtnClick"/>
                        </div>
                    </div>

                    <div class="span2 well">
                        <asp:Panel ID="pnl_0" runat="server" />
                    </div>
                    <div class="span2 well">
                        <asp:Panel ID="pnl_1" runat="server" />
                    </div>
                    <div class="span2 well">
                        <asp:Panel ID="pnl_2" runat="server" />
                    </div>
                    <div class="span2 well">
                        <asp:Panel ID="pnl_3" runat="server" />
                    </div>
            </div>
        </div>
    </div>

    <div class="hidden">
        <asp:Label ID="BeginningCharacterTextDefinition" runat="server" Text="Anfangsbuchstabe: " />
        <asp:Label ID="SelStartChar" runat="server" Text="Anfangsbuchstaben wählen " />
        <asp:Label ID="errorMsg_no_hashtag" runat="server" Text="Du musst ein regionales Thema eingeben oder einen Buchstaben auswählen und ein thema in der Tabelle anklicken." />

    </div>

    <div id="rawdata" runat="server" style="visibility:hidden;">
    </div>

     <style>
        .ui-autocomplete {
            max-height: 100px;
            width:160px;
            overflow-y: auto;
            /* prevent horizontal scrollbar */
            overflow-x: hidden;
            background-color:White;
        }
        /* IE 6 doesn't support max-height
        * we use height instead, but this forces the menu to always be this tall
        */
        * html .ui-autocomplete {
            height: 100px;
            width:160px;
            background-color:White;
        }
    </style>

    <script type="text/javascript">
        $(function () {
        /*
            var availableTags = [
                "ActionScript",
                "AppleScript",
                "Asp",
                "BASIC",
                "C",
                "C++",
                "Clojure",
                "COBOL",
                "ColdFusion",
                "Erlang",
                "Fortran",
                "Groovy",
                "Haskell",
                "Java",
                "JavaScript",
                "Lisp",
                "Perl",
                "PHP",
                "Python",
                "Ruby",
                "Scala",
                "Scheme"
            ];
            */
            var availableTags = $("#CoPlaBottom_rawdata").text().split(',')

            $("#CoPlaBottom_txb_hashtags").autocomplete({
                source: availableTags
            });
            });
    </script>

</asp:Content>

