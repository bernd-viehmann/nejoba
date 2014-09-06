<%@ Page Title="" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="violation_editor.aspx.py" validateRequest="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
<script src="<%# ResolveUrl("~/style/tinymce/jscripts/tiny_mce/tiny_mce.js") %>" type="text/javascript"></script>
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container">
        <!-- Top Headline Box -->
        <div class="hero-unit">
        <h3>Melde etwas an das nejoba-Team</h3>
        
        <br />
        </div>


        <!-- ###  Header with abo-checkbox              ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## -->
        <div ID="SetUpFiltering" runat="server" class="hero-unit" visible="true">
            <!-- ###  Server DIV 2 display the thread       ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## -->
            <div id="divShowThread" runat="server" visible="true">
            
            </div>

            <!-- ###  tinyMCE Editor ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## -->
            <div id="divEditArea" runat="server">
                <p>
                    <h4><asp:Label ID="lbl_hint" runat="server" Text="Was m&ouml;chtest Du melden ?"></asp:Label></h4>
                    <asp:TextBox runat="server" ID="txtMain" TextMode="MultiLine" Rows="17" style="width:100%"></asp:TextBox>
                </p>
            </div>
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->

            <br />
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
            <div class="row">
                <div class="span6">
                    <br />
                    <asp:Button ID="btnPublish" runat="server" class="btn-large btn-primary" Text="Absenden" onclick="HndlrButtonClick"/>
                </div>    
            </div>    
            <!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        </div>
    </div> <!-- /container -->
    
    <div style="visibility:hidden;"></div>
    
    <script type="text/javascript">
        function ResolveUrl(url) {
            if (url.indexOf("~/") == 0) {
                url = baseUrl + url.substring(2);
            }
            return url;
        }

        tinyMCE.init({
            // General options
            mode: "textareas",
            theme: "advanced",
            plugins: "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",

            // Theme options
            theme_advanced_buttons1: "newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,formatselect,fontselect,fontsizeselect,|,cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo",
            theme_advanced_toolbar_location: "top",
            theme_advanced_toolbar_align: "left",
            theme_advanced_statusbar_location: "bottom",
            theme_advanced_resizing: true,

            // Skin options
            skin: "o2k7",
            skin_variant: "silver",

            // Example content CSS (should be your site CSS)
            content_css: ResolveUrl("http://ajax.aspnetcdn.com/ajax/bootstrap/2.3.2/css/bootstrap.min.css"),

            // Drop lists for link/image/media/template dialogs
            template_external_list_url: "js/template_list.js"
        });
    </script>
</asp:Content>