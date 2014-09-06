<%@ Page Title="" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="job_trial_editor.aspx.py" validateRequest="false"%>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">

</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">
    <div class="container span10">
        <!-- ###  Header with abo-checkbox              ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## -->
        <div class="row"> 
            <h3><asp:Label ID="Label7" runat="server" Text="Kontakt zu einem Arbeitsauftrag" /></h3>
            <h4><asp:Label ID="lbl_headline" runat="server" Text=" " /></h4>
            <hr />
        </div>
            
        <!-- ###  Server DIV 2 display the thread       ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## -->
        <div id="divShowThread" runat="server" visible="true">
        </div>

        <!-- # # if user is same tham creator he can not interact with this offer # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div id="ownOfferDiv" runat="server" class="row alert alert-info" visible="false">
            <div class="span11">
                <strong><asp:Label ID="Label4" runat="server" Text="Du beantwortest deinen eigenen Arbeitsauftrag." /></strong>
            </div>
        </div>

        <!-- # #    editor for deabtes     # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->

        <div ID="YES_WE_CAN" runat="server" class="well" visible="true">
            <div class="row">
            <!-- < div id="divEditArea" run-at="server" > -->
                <div class="span10 offset1">
                    <br />
                    <h4><asp:Label ID="lbl_hint" runat="server" Text="Deine Nachricht:"></asp:Label></h4>
                    <asp:TextBox runat="server" ID="txtMain" TextMode="MultiLine" Rows="17" style="width:100%"></asp:TextBox>
                </div>
                <div class="span1"></div>
            </div>
            <div class="row">
                <div class="span3 offset9">
                    <br />
                    <asp:Button ID="btn_Publish" runat="server" class="btn btn-large btn-primary" Text="Nachricht senden" onclick="HndlrButtonClick"/>
                    <br /><br />
                </div>
            </div>
        </div>

        <!-- # # after send was clickes a successfull-message is displayed # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div ID="SuccessDiv" runat="server" class="row alert alert-success" visible="false">
            <!-- < div id="divEditArea" run-at="server" > -->
            <h5><asp:Label ID="Label1" runat="server" Text="Deine Nachricht wurde vom System entgegengenommen."></asp:Label></h5>
        </div>


    </div> <!-- /container -->
    
    <div style="visibility:hidden;">
        <asp:Label ID="msg_mailSubject" runat="server" Text="nejoba Verhandlungen : Es ist Angebot bearbeitet worden"></asp:Label>

        <!-- hidden textboxes for storing the location -->
        <asp:TextBox ID="txbx_location_id" runat="server" />        <!-- the hidden textboxes stores the location-id   of hometown -->
        <asp:TextBox ID="txbx_location_name" runat="server" />      <!-- the hidden textboxes stores the location-name of hometown -->


    </div>
    
    <script type="text/javascript">
        function ResolveUrl(url) {
            if (url.indexOf("~/") == 0) {
                url = baseUrl + url.substring(2);
            }
            return url;
        }

//        tinyMCE.init({
//            // General options
//            mode: "textareas",
//            theme: "advanced",
//            plugins: "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",

//            // Theme options
//            theme_advanced_buttons1: "newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,formatselect,fontselect,fontsizeselect,|,cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo",
//            theme_advanced_toolbar_location: "top",
//            theme_advanced_toolbar_align: "left",
//            theme_advanced_statusbar_location: "bottom",
//            theme_advanced_resizing: true,

//            // Skin options
//            skin: "o2k7",
//            skin_variant: "silver",

//            // Example content CSS (should be your site CSS)
//            content_css: ResolveUrl("http://ajax.aspnetcdn.com/ajax/bootstrap/2.3.2/css/bootstrap.min.css"),

//            // Drop lists for link/image/media/template dialogs
//            template_external_list_url: "js/template_list.js"
//        });


        $(document).ready(function () {
            $("#CoPlaBottom_txtMain").wysihtml5();
            initMap();
        }); 


    </script>




<!--
        <div ID="OFFER_PREMIUM_ACCOUNT" runat="server" class="row hero-unit" visible="true">
            <h5><asp:Label ID="lblOfferPremium" runat="server" Text="Diskussionen werden nach bestimmter Zeit &ouml;ffentlich. Um alle Funktionen von nejoba sofort nutzen zu können benötigst Du einen Premium-Account ."></asp:Label></h5>
            <br />
            <asp:Button ID="btn_GetPremiumAccount" runat="server" class="btn-large btn-primary" Text="Premium Mitglied werden" ToolTip="Werde Premium-Mitglied"  onclick="HndlrButtonClick" />

        </div>

        <div ID="INVITE_VISITOR" runat="server" class="row hero-unit" visible="true">
            <h5><asp:Label ID="lbl_inviteVisitor" runat="server" Text="Um an der Diskussion teilnehmen zu k&ouml;nnen musst Du ein eigenes Nutzerkonto auf nejoba haben."></asp:Label></h5>
            <br />
            <asp:Button ID="btn_BecomeMember" runat="server" class="btn-large btn-primary" Text="Eigenes Konto anlegen" ToolTip="Erstelle einen eigenen Account  " onclick="HndlrButtonClick" />
        </div>

        <div ID="YOUR_OWN_OFFER" runat="server" class="row hero-unit" visible="true">
            <h5><asp:Label ID="lbl_ownOffer" runat="server" Text="Der Auftrag wurde von Dir eingestellt."></asp:Label></h5>
            <br />
        </div>
-->


</asp:Content>












