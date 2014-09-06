// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//   List Extractor Class
// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//
//   The Class is the client-entrance for the data. it handles the communication to the server-data-source
//   and stores the received itmes in a global array.
//
//   this class is the data-container for the client. it also handles the pagging of datat to display.
//   additionally there is a server-side sclicing. when the 
//
//
// IMPORTANT: The server sends his data-array backwards. so the Pages-array starts at the end of data.
//
//
// member-attributes :
// ________________________________________________________________________________________________________________________________________________________________________________
//         AjxParam = {};                                                            object to store the attributes for the AJAX-Parameter
//         AjxParam.UrlCache = '../wbf_activemap/dataSource__cache.aspx'             source-url for items from the cache
//         AjxParam.UrlMongo = '../wbf_activemap/dataSource__mongo.aspx'             source-url for items from the database
//
//         UrlParam = {};
//         UrlParam.ResultLength = typeof rsltLngth !== 'undefined' ? rsltLngth : 1000;        maximum amount of items that will be in the result-set of the AJAX Call
//         UrlParam.ItemType = typeof itemType !== 'undefined' ? itemType : 'list';  define what kind of items should be loaded. 
//                                                                                   map : we load map-marker-items. must have location-coordinates
//                                                                                   date : we load date-items. must have a valid 'from'-date
//                                                                                   list : load every item for displaying a list. this kind of item is not pre-filtered
//         UrlParam.Loc = undefined;                                                 location : '0|' for undefined; 'AT|' for country austria; 'DE|41836' for Hueckelhoven in germany
//         UrlParam.Tag = undefined;                                                 hashtags. if we have a rubric-definition it is the first item in aray
//         UrlParam.StartDate = undefined;                                           the search-date starting
//         UrlParam.EndDate = undefined;                                             the search-date ending
//         UrlParam.SrchMode = undefined;                                            search-mode can be 'AND' or 'OR'
//
//         IntParam
//         IntParam.PageLength = typeof pgLen !== 'undefined' ? pgLen : 100;        number of items that are send from the list-extractor to the client in one go
//         IntParam.PageActive = undefined;                                         ID of last loaded page ( page is the segment that is send to the projector-class )
//         UrlParam.SliceActive = 0;                                                remind on what slide on the server we are currently reading?
//         IntParam.CrsCmd = '';                                                    the CursorCommand controlls the load of the next item
//
//         Items  the list with all data that we have received until now. this is a list of data-items that came from server via AJAX
//
//
// member-functions :
// ________________________________________________________________________________________________________________________________________________________________________________
//
//         serverSliceLoad()                        the function loads a part of the active slice on the server and copies this data into the member-array Items
//         getUrlParams()                           check if params were changed (reset class if so) and copy the user-input into the meber-attributes
//         prepareUrl()                             build the appropiet URL for AJAX request
//         clientPageSend()                         the functions is called to dispaly a new portion of data on the webform. it calls the receive-methode of the projector class
//         turnThePage(bool ForwardDirection)       change the page (stored in the local item-cache) to display
//         loadInitial()                            start data-load : reset class and take care of the new url-parameters 
//

/*
 *  ListExtractor
 *
 *  this class gets the data from the itam-app-cache with java-calls. it stores the 
 *  items in an array and is responsible for the paging of the received itmes.
 *  
 * constructor-parameter
 *  
 * itemType     = define typ of constructor (map/list/date)  the datasource-webform creates the JSON-items depending on thatz value (map-items need no date; list items need all
 * rsltLngth    = the number of items that will be returned by the AJAX data-source in a single call. these results will be stored in a 
 * pgLen        = the items that should be displayed once on the projector-page. this is internal and not send to server
 *
 * 18.07.2013  - bervie -   initial realese
 *
 */
function ListExtractor(c,a,b){
    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  
    //
    // Member-Attributes
    //
    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  

    // parameter for the server-communication
    this.AjxParam={};
    this.AjxParam.Tmplt=nejobaUrl("./ajax/dataSource__cache.aspx");
    this.AjxParam.AjaxUrl="";
    
    // URL-parameter will be send to the data-source-webform
    this.UrlParam={};
    this.UrlParam.SliceActive=0;
    this.UrlParam.CrsCmd="";
    
    this.UrlParam.ResultLength="undefined"!==typeof a?a:1500;
    this.UrlParam.ItemType="undefined"!==typeof c?c:"list";
    
    this.UrlParam.Loc=void 0;
    this.UrlParam.City=void 0;
    this.UrlParam.Tag=void 0;
    this.UrlParam.StartDate=void 0;
    this.UrlParam.EndDate=void 0;
    this.UrlParam.SrchMode=void 0;
    
    // internal parameter and setings for the list-extractor
    this.IntParam={};
    this.IntParam.PageActive= 0;
    this.IntParam.PageLength="undefined"!==typeof b?b:150;
    
    // the data-container
    this.Items=[];					// the list with all data that we have received until now. this is a list of data-items that came from server via AJAX
    
    // bind the buttons to the handlers
    $('#foreward_in_list').click(function () {
        if ($('#foreward_in_list').hasClass('disabled') != true) {
            lstExtr.turnThePage('forward');
            $('#back_in_list').removeClass('disabled');
        }
    });
    
    $('#back_in_list').click(function () {
        if ($('#back_in_list').hasClass('disabled') != true ) {
            lstExtr.turnThePage('backward');
            $('#foreward_in_list').removeClass('disabled');
        }
    });





    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  
    //
    // control-functions the start an action. these functions are called from the projector class 
    //
    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  

    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
     * loadInitial()
     *
     * the function is the main-event handler. it is called when the user press the search-button and from constructor.
     * resetz all data loaded yet and begins with a new server-load-process
     *
     * 18.07.2013  - bervie -   initial realese
     *
     */
    this.loadInitial=function(){
        //console.log("ListExtractor.loadInitial called");
        
        // reset the internal params
        this.Items=[];
        this.IntParam.PageActive= 0;
        this.UrlParam.SliceActive=0;
        this.UrlParam.CrsCmd="";
        
        this.getUrlParams();
        this.turnThePage()
    }


    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * clearSearchDialog()
    *
    * this is the click-event-handler for deleting the search-parameter-dialog
    *
    * 22.07.2013  - bervie -   initial realese
    *
    */
    this.clearSearchDialog=function(){
        //console.log("ListExtractor.clearSearchDialog called ");
        
        $("#CoPlaBottom_txbx_timeFrom").datepicker("setDate",null);
        $("#CoPlaBottom_txbx_timeTo").datepicker("setDate",null);
        $("#CoPlaBottom_txbx_hashtag").val("");
        $("#CoPlaBottom_sel_country option[value!='0']").attr("selected",!1);
        $("#CoPlaBottom_sel_country option[value='0']").attr("selected", !0);
        $("#CoPlaBottom_txbx_city").val("");
        $("#CoPlaBottom_txbx_postCode").val("");
        $("#CoPlaBottom_txbx_city").attr("disabled",!0);
        $("#CoPlaBottom_txbx_postCode").attr("disabled",!0);

        $("input[id*='CoPlaBottom_txbx_tagforitem']").val('');          // remove selected internal tag identifier
        $("input[id*='CoPlaBottom_txbx_itemname']").val('');            // remove selected tagnames for UI
        
        return false;
    };


    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  
    //
    // STUFF for the the asynchronus data load
    //
    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  

    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * getUrlParams()
    *
    * check if params were changed (reset class if so) and copy the user-input into the meber-attributes
    * the URL string construction will be done in 'prepareUrl'-function
    *
    * returns false if nothing has been changed since last call. then the ListExtractor can go on with the existing data
    *
    */
    this.getUrlParams = function () {
        //console.log("ListExtractor.getUrlParams called");

        // 1. at first users settings will be copied into local object
        //
        this.UrlParam.Loc = $("#CoPlaBottom_sel_country").val() + "," + $.trim($("#CoPlaBottom_txbx_postCode").val());
        this.UrlParam.City = $.trim($("#CoPlaBottom_txbx_city").val());
        this.UrlParam.SrchMd = "OR"; var a = $("#CoPlaBottom_txbx_timeFrom").datepicker("getDate");

        if (null != a) {
            var b = String(a.getDate()), c = String(a.getMonth() + 1), a = String(a.getFullYear());
            this.UrlParam.StartDate = a + "-" + c + "-" + b
        }
        else
            this.UrlParam.StartDate = "";

        a = $("#CoPlaBottom_txbx_timeTo").datepicker("getDate");
        null != a ? (b = String(a.getDate()), c = String(a.getMonth() + 1), a = String(a.getFullYear()), this.UrlParam.EndDate = a + "-" + c + "-" + b) : this.UrlParam.EndDate = "";
        b = $("#CoPlaBottom_txbx_tagforitem").val();
        c = $("#CoPlaBottom_txbx_hashtag").val();
        c = c.toLowerCase();
        c = c.replace(/#/g, "");
        // alert('Rubric received : ' + b + '<br />URL-Params 4 Tags : ' + c);
        this.UrlParam.Tags = b + "," + c
    };

    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * prepareUrl()
    *
    * create the URL for the AJAX request
    * 
    *
    */
    this.prepareUrl=function(){
        //console.log("ListExtractor.prepareUrl called");
        var a="?",b;
        
        for(b in this.UrlParam){
            var c=this.UrlParam[b];
            null!=c&&(a+=b+"="+String(c)+"&")
        }
        
        this.AjxParam.AjaxUrl=this.AjxParam.Tmplt+$.trim(a.slice(0,-1));                    // remove last '&'
        return a
    };

    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * serverSliceLoad()
    *
    * the function loads a part of the active slice on the server and copies this data into the member-array Items
    * here the ajax-magic is happening
    *
    * HINT : the instance of the ListExtractor MUST be named lstExtr
    *        the asyncron function that receives the data calls the ItemContainer like this:
    *        lstExtr.Items.push(newDataItem);
    *
    * 18.07.2013 - bervie - initial realese
    * 10.08.2013 - bervie - added warning if nothing was loaded
    * 15.09.2013 - bervie - added repositioning if a place was received
    *
    */
    this.serverSliceLoad = function () {
        //console.log("ListExtractor.serverSliceLoad called");
        $("#loadNwait").modal("show");

        this.prepareUrl(); 	// build a string with the AJAX-call-URL
        $.getJSON(this.AjxParam.AjaxUrl, function (a) {
            var b = -1;
            $.each(a.items, function (a, c) {
                lstExtr.Items.push(c);
                b = a
            });
            // store the config-parameters in the local vars
            lstExtr.UrlParam.SliceActive = a.config.SliceActive;
            lstExtr.UrlParam.CrsCmd = a.config.CrsCmd;

            //console.log(" -- -- -- --  serverSliceLoad -- -- -- -- -- -- -- -- -- -- -- ---- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- start" );
            //console.log("Amount of items loaded from server : " + (b + 1));
            //console.log("configuration received from server : ACTIVE-SLICE " + lstExtr.UrlParam.SliceActive);
            //console.log("configuration received from server : CRSR_OFFSET " + lstExtr.UrlParam.CrsCmd);
            //console.log("configuration received from server : len of array " + lstExtr.Items.length);
            // console.log("configuration received from server : first item " + lstExtr.Items[0]);
            //console.log(" -- -- -- --  serverSliceLoad -- -- -- -- -- -- -- -- -- -- -- ---- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- end");

            // if we have an empty answer show 'no date' message else show the data
            // if we have an empty answer show 'no date' message else show the data
            if (lstExtr.Items[0]['_objectDetailID'] != undefined) {
                lstExtr.clientPageSend();
                $('#loadNwait').modal('hide');

                // todo: receive the map-configuration lat,lon,zoom {}["mapcnf"] 
            }
            else {
                $('#noDataFound').modal('show');
                $('#loadNwait').modal('hide');

                //$('#foreward_in_list').addClass('disabled');
                $('#back_in_list').addClass('disabled');
            }

            // *****************************************************************************************************************
            // if we have received a list of places center the map to the first place and zoom in 
            // 15.09.2013  bervie
            // *****************************************************************************************************************
            if (a.places != undefined) {
                if (projector.map != undefined) {
                    var cityLon = a.places[0]['longitude'];
                    var cityLat = a.places[0]['latitude'];
                    var proj4326 = new OpenLayers.Projection("EPSG:4326");
                    var projmerc = new OpenLayers.Projection("EPSG:900913");
                    var lonlat = new OpenLayers.LonLat(cityLon, cityLat).transform(proj4326, projmerc);
                    projector.map.setCenter(lonlat);
                    projector.map.zoomTo(12);
                }
            }
        })
    };
    
    
    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * turnThePage()
    *
    * handler for the arrow-button which change the currently displayed data
    *
    * 18.07.2013  - bervie -   initial realese
    *
    */
    this.turnThePage = function (direction) {
        //console.log('ListExtractor.turnThePage called with DIRECTION : ' + String(direction));

        // the forward-button was pressed -> get the next items
        if (direction == 'forward') {
            // forward means to the left : page-index will be - 1
            // console.log('ListExtractor.turnThePage  TURN THE PAGE FORWARD    ->');
            this.IntParam.PageActive = this.IntParam.PageActive - 1;    // ! ! ! ! ! ! ! ! ! we get data from newer items to older. so forwar in UI means bachward in the list
        };

        // the backward-button was pressed -> go back in the JSON-client-list and display already displayed stuff
        if (direction == 'backward') {
            // console.log('ListExtractor.turnThePage  TURN THE PAGE BACKWARD   <-');
            if (this.IntParam.PageActive > 0) { $('#foreward_in_list').removeClass('disabled'); }       // disable the forward-button if we have reached the start-point
            this.IntParam.PageActive = this.IntParam.PageActive + 1;                                    // ! ! ! ! ! ! ! ! ! we get data from newer items to older. so backward in UI means forward in the list
        };

        // enable/disable buttons by the currentz active page 
        if (this.IntParam.PageActive == 0) {
            $('#foreward_in_list').addClass('disabled');
            $('#back_in_list').removeClass('disabled');
        }
        else {
            $('#foreward_in_list').removeClass('disabled');
            $('#back_in_list').removeClass('disabled');
        }

        // get the page-bounds to display only a part of the data we have.
        this.setPageBounds();
        var lastItemIndx = this.Items.length - 1;

        // if we reached the end of local Items-List start a new load from the server
        if (lastItemIndx < this.ItmLstLftIdx) {           
            if (this.UrlParam.CrsCmd == 'end_of_data') {
                // the left page index is bigger than the end of the item-array .
                // go back to last valid page
                // alert('Keine weiteren Daten vorhanden !');
                // ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
                $('#endOfDataReached').modal('show');

                //console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');
                //console.log('-NO MORE DATA - - WILL NOT BE DISPLAYED - - -  ');
                //console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');
                //console.log('ListExtractor.turnThePage - - - - - - - - - -  ');
                //console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');
                //console.log('  current page       : ' + String(this.IntParam.PageActive));
                //console.log('  this.ItmLstLftIdx  : ' + String(this.ItmLstLftIdx));
                //console.log('  this.ItmLstRgtIdx  : ' + String(this.ItmLstRgtIdx));
                //console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');
                //console.log('  ACTIVE-SLICE       : ' + this.UrlParam.SliceActive);
                //console.log('  CRSR_OFFSET        : ' + this.UrlParam.CrsCmd);
                //console.log('  length Items[]     : ' + String(this.Items.length));
                //console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');
                //console.log('-NO MORE DATA - - WILL NOT BE DISPLAYED - - -  ');
                //console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');

                this.IntParam.PageActive = this.IntParam.PageActive - 1;
                this.setPageBounds();

                return;
            }
            else {
                this.serverSliceLoad();
                return;
            }
        }

        // send the available data to the projector
        this.clientPageSend();

        //console.log('ListExtractor.turnThePage - - - - - - - - - -  ');
        //console.log('                          current page       : ' + String(this.IntParam.PageActive));
        //console.log('                          this.ItmLstLftIdx  : ' + String(this.ItmLstLftIdx));
        //console.log('                          this.ItmLstRgtIdx  : ' + String(this.ItmLstRgtIdx));
        //console.log('                          ACTIVE-SLICE       : ' + this.UrlParam.SliceActive);
        //console.log('                          CRSR_OFFSET        : ' + this.UrlParam.CrsCmd);
        //console.log('                          length Items[]     : ' + String(this.Items.length));
        //console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');
    }


    
    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * setPageBounds()
    *
    * this functions calculates the left and rigth border-indexes of a page by giving the page-index
    *
    */
    this.setPageBounds=function(){
        //console.log("ListExtractor.setPageBounds called");
        this.ItmLstLftIdx=this.IntParam.PageActive*this.IntParam.PageLength; this.ItmLstRgtIdx=this.ItmLstLftIdx+this.IntParam.PageLength
    };


    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
     * clientPageSend()
     *
     * this functions creates the package of items that should be displayed and send it to the display()-function of the projector. it dependece on the projector what will be done with the 
     * data. if we have a map the projector will creater markers, if we have a item-list the projector will create a text-list
     *
     * HINT : be sure to give the projector-instance allways the rigth name. this function will just call projector.display( [ItemList] )
     *
     */
    this.clientPageSend=function(){
        //console.log("ListExtractor.clientPageSend called");
        dsplyLst=this.Items.slice(this.ItmLstLftIdx,this.ItmLstRgtIdx);
        projector.display(dsplyLst)
    };

    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * showBookmark()
    *
    * the function prepares the bookmark-link
    *
    * ToDo ToDo   HINT for copying text to the clipboard : http://stackoverflow.com/questions/400212/how-to-copy-to-the-clipboard-in-javascript 
    * ToDo ToDo   
    * ToDo ToDo   URL-generator http://www.sharelinkgenerator.com/
    * ToDo ToDo   
    *
    */
    this.showBookmark = function () {
        // create a link to the current view : asShown
        this.getUrlParams();
        var urlParams = this.prepareUrl()

        var urlBase = document.baseURI
        var urlStart = document.baseURI.indexOf('?SliceActive');
        if (urlStart != -1) { urlBase = document.baseURI.substr(0, urlStart); }

        var absltURI = urlBase + urlParams;

        // alert('var absltURI =  ' + absltURI);

        var gsprUrl = 'http://sharetodiaspora.github.io/?title=' + document.title + "&url=" + encodeURIComponent(absltURI);
        var goglplsUrl = 'https://plus.google.com/share?url=' + encodeURIComponent(absltURI) + '';
        var twtrUrl = 'https://twitter.com/home?status=' + document.title + ' ' + encodeURIComponent(absltURI);
        var fcBkUrl = 'http://www.facebook.com/sharer.php?u=' + encodeURIComponent(absltURI);
        var bkmrkUrl = encodeURI(absltURI);

        //        var tmpTxt = '';
        //        tmpTxt += 'baseUrl      : ' + document.baseURI + '\n\n';
        //        tmpTxt += 'urlParams    : ' + urlParams + '\n';
        //        tmpTxt += 'rsltURI      : ' + absltURI + '\n';
        //        tmpTxt += 'fcBkUrl      : ' + fcBkUrl + '\n';
        //        tmpTxt += 'gsprUrl      : ' + gsprUrl + '\n';
        //        alert(tmpTxt);

        $("#extLinkDisplay").prop("href", encodeURI(absltURI)).prop("target", "_blank").text("Der Lesezeichen-Link");
        var userId = $("#CoPlaBottom_lbl_userId").text();
        "" != userId && (rltvPath = absltURI + "usrId=" + userId, $("#usrSpecfcItemLnk").prop("href", encodeURI(rltvPath)).prop("target", "_blank").text("nejoba Beitr\u00e4ge"));

        $("#post_on_diaspora").prop("href", gsprUrl).prop("target", "_blank");     // prepare diaspora
        $("#post_on_googleplus").prop("href", goglplsUrl).prop("target", "_blank");     // prepare diaspora
        $("#post_on_twitter").prop("href", twtrUrl).prop("target", "_blank");     // prepare diaspora
        $("#post_on_facebook").prop("href", fcBkUrl).prop("target", "_blank");     // prepare facebook

        $("#post_on_clipboard").prop("href", bkmrkUrl).prop("target", "_blank");     // prepare diaspora

        // alert('this.showBookmark called in the end  !');
    };














    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * showBookmark()
    *
    * the function prepares the bookmark-link
    *
    */
//    this.showBookmark = function () {
//        // create a link to the current view : asShown
//        var a = window.location.pathname;
//        this.getUrlParams();
//        var urlParams = this.prepareUrl()

//        //var b = a + this.prepareUrl();
//        var bkmrk = encodeURI('http://www.nejoba.net' + a + urlParams);

//        alert(bkmrk);

//        $("#extLinkDisplay").prop("href", bkmrk).prop("target", "_blank").text("Der Lesezeichen-Link");
//        var b = $("#CoPlaBottom_lbl_userId").text();
//        "" != b && (a = a + "?usrId=" + b, $("#usrSpecfcItemLnk").prop("href", a).prop("target", "_blank").text("nejoba Beitr\u00e4ge"));

//        // prepare facebook
//        var fbLnk = 'http://www.facebook.com/sharer.php?u=';
//        var fullEnc = encodeURI(fbLnk + bkmrk);
//        $("#post_on_facebook").prop("href", fullEnc).prop("target", "_blank");

//        var geapoLnk = "http://sharetodiaspora.github.io/?title=" + encodeURIComponent(document.title);
//        geapoLnk += "&url=" + bkmrk;
//        $("#post_on_diaspora").prop("href", geapoLnk).prop("target", "_blank");
//    };

    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    this.loadInitial();      // kickstarter : get server-data initialy from the ajax-source
};






// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//   Debate-Projector Class
// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//
//   The Class is responsible for displaying the list of debates as text-table. it shows the items seperated on pages
//
// member-attributes :
// ________________________________________________________________________________________________________________________________________________________________________________
//
// member-functions :
// ________________________________________________________________________________________________________________________________________________________________________________
//
//
//
/*
 *  DebateProjector
 *
 *  this class is responsible for displaying the items in the DB as table.view. it allows paging
 *
 * parameter : displayurl is the url that will be used to show the details of an item
 *
 * 28.06.2013 bervie initial realese
 *
 */
function DebateProjector(c){
    //
    // debate-list initialization 
    //

    // icons used for the markers
    //    this.iconswtch = { "§EVT": "./style/marker/waiting.png",
    //        "§ANO": "./style/marker/schreibwaren_web.png",
    //        "§INI": "./style/marker/family.png",
    //        "§BUI": "./style/marker/mine.png",
    //        "§LOC": "./style/marker/home-2.png"
    //    };

    //    this.stndrIcon = "./style/marker/text.png";
    //    this.displayUrl = dispUrl;
    this.iconswtch={
        "\u00a7EVT":nejobaUrl("./style/marker/waiting.png"),
        "\u00a7ANO":nejobaUrl("./style/marker/schreibwaren_web.png"),
        "\u00a7INI":nejobaUrl("./style/marker/family.png"),
        "\u00a7BUI":nejobaUrl("./style/marker/mine.png"),
        "\u00a7LOC":nejobaUrl("./style/marker/home-2.png")
    };

    this.stndrIcon = nejobaUrl("./style/marker/information.png");
    this.displayUrl=nejobaUrl(c);
    
     //this.printTmplt=' <div id="Div1">\n <div class="row span12 well">\n <div class="span11">\n <h5>\n <a href="\u00a7\u00a7URL_LINK_TARGET\u00a7\u00a7" target="_blank">\u00a7\u00a7URL_LINK_TEXT\u00a7\u00a7</a>\n </h5>\n </div>\n <div class="span4">\n <strong>Ersteller: </strong>\u00a7\u00a7NICKNAME\u00a7\u00a7<br />\n <strong>erstellt am: </strong>\u00a7\u00a7CREATIONTIME\u00a7\u00a7<br />\n </div>\n <div class="span3">\n <strong>vom: </strong>\u00a7\u00a7DATE_FROM\u00a7\u00a7<br />\n <strong>bis: </strong>\u00a7\u00a7DATE_TILL\u00a7\u00a7<br />\n </div>\n <div class="span3">\n <strong>Ort: </strong>\u00a7\u00a7LOCATIONNAME\u00a7\u00a7<br />\n </div>\n <br />\n </div>\n </div>';
//    this.printTmplt = ['        <div id="Div1">',
//                    '            <div class="row span12 well">',
//                    '                <div class="span11">',
//                    '                    <h5>',
//                    '                        <a href="§§URL_LINK_TARGET§§" target="_blank">§§URL_LINK_TEXT§§</a>',
//                    '                    </h5>',
//                    '                </div>',
//                    '                <div class="span4">',
//                    '                    <strong>Ersteller: </strong>§§NICKNAME§§<br />',
//                    '                    <strong>erstellt am: </strong>§§CREATIONTIME§§<br />',
//                    '                </div>',
//                    '                <div class="span3">',
//                    '                    <strong>vom: </strong>§§DATE_FROM§§<br />',
//                    '                    <strong>bis: </strong>§§DATE_TILL§§<br />',
//                    '                </div>',
//                    '                <div class="span3">',
//                    '                    <strong>Ort: </strong>§§LOCATIONNAME§§<br />',
//                    '                </div>',
//                    '            <br />',
//                    '            </div>',
//                    '        </div>'].join('\n');

    this.printTmplt = [ '        <div id="template">',
                        '            <div class="row">',
                        '                <div class="span12">',
                        '                    <h5>',
                        '                        <a href="§§URL_LINK_TARGET§§" target="_blank">§§URL_LINK_TEXT§§</a>',
                        '                    </h5>',
                        '                </div>',
                        '            </div>',
                        '            <div class="row">',
                        '                <div class="span12">',
                        '                    <div class="span4">',
                        '                        <strong>Ersteller: </strong>§§NICKNAME§§<br />',
                        '                        <!--<strong>erstellt am: </strong>§§CREATIONTIME§§<br />-->',
                        '                    </div>',
                        '                    <div class="span4">',
                        '                        <!--<strong>vom: </strong>§§DATE_FROM§§<br />-->',
                        '                        <!--<strong>bis: </strong>§§DATE_TILL§§<br />-->',
                        '                    </div>',
                        '                    <div class="span4">',
                        '                        <strong>Ort: </strong>§§LOCATIONNAME§§<br />',
                        '                    </div>',
                        '                </div> ',
                        '            </div>',
                        '        </div>',
                        '        <br/>'].join('\n');

    /*
     * function DebateProjector.defineItemIcon defines which marker-icon will be used for this item. 
     *
     * parameter : dataItem is the item to display
     *
     * 30.06.2013 bervie initial realese
     *
     */
    this.defineDebateIcon= function(a){
        // console.log('DebateProjector.defineDebateIcon was called');
        if(void 0==a.tagZero)return this.stndrIcon;
        
        0<a.tagZero.length?(a=a.tagZero.split("_")[0],a=this.iconswtch[a]):a=this.stndrIcon;
        
        "undefined"===typeof a&&(a=this.stndrIcon);
        return a
        };

    /*
     * display : this function is called from the ListExtractor. It creates the DIVs with the item-infos and writes it to the destination-DIV
     *
     * parameter :  ItemArray 
     *              the array contains all items that should be displayed. the items are chosen from the ListExtractor
     *              this projector-class has no logic for item-selection. it is only a dispaly-idiot
     *
     * 05.06.2013 bervie initial realese
     *
     */
    this.createItemDiv=function(a){
        var b=this.printTmplt,
        b=b.replace("\u00a7\u00a7URL_LINK_TARGET\u00a7\u00a7",this.displayUrl+a._ID),
        b=b.replace("\u00a7\u00a7URL_LINK_TEXT\u00a7\u00a7",a.subject),
        b=b.replace("\u00a7\u00a7NICKNAME\u00a7\u00a7",a.nickname),
        b=b.replace("\u00a7\u00a7CREATIONTIME\u00a7\u00a7",a.creationTime), 
        b=b.replace("\u00a7\u00a7DATE_FROM\u00a7\u00a7",a.from),
        b=b.replace("\u00a7\u00a7DATE_TILL\u00a7\u00a7",a.till);
        
        return b=b.replace("\u00a7\u00a7LOCATIONNAME\u00a7\u00a7",a.locationname)
        };
        
        
    /*
     * display : this function is called from the ListExtractor. It creates the DIVs with the item-infos and writes it to the destination-DIV
     *
     * parameter :  ItemArray 
     *              the array contains all items that should be displayed. the items are chosen from the ListExtractor
     *              this projector-class has no logic for item-selection. it is only a dispaly-idiot
     *
     * 05.06.2013 bervie initial realese
     *
     */
     this.display=function(a){
        var b="";
        $.each(a,function(a,c){b+=projector.createItemDiv(c)});
        $("#canvasforlist").html(b)
        }
    };


    
    
    
// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//   Map-Projector Class
// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//
//   The Class is responsible for displaying the stuff we have in the ListExtractor on the map. using openlayers with open-street-map
//
// member-attributes :
// ________________________________________________________________________________________________________________________________________________________________________________
//
//   
//   
//   
//
// member-functions :
// ________________________________________________________________________________________________________________________________________________________________________________
//
// addMarker
//
//
//
//

// global definitions # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
// # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
AutoSizeAnchoredMinSize=OpenLayers.Class(OpenLayers.Popup.Anchored,{autoSize:!0,minSize:new OpenLayers.Size(400,200)}); 
AutoSizeFramedCloudMinSize=OpenLayers.Class(OpenLayers.Popup.FramedCloud,{autoSize:!0,minSize:new OpenLayers.Size(400,30)}); 




/*
 *  MapProjector
 *
 *  this class gets data from the ListExtrctor-Class and displays it 
 *  on the map with open-layers stuff. 
 *
 * parameter : displayurl is the url that will be used to show the details of an item
 *
 * 28.06.2013 bervie initial realese
 *
 */
function MapProjector(c){
    this.urls=[ "http://a.tile.openstreetmap.org/${z}/${x}/${y}.png",
                "http://b.tile.openstreetmap.org/${z}/${x}/${y}.png",
                "http://c.tile.openstreetmap.org/${z}/${x}/${y}.png"];
                
    this.iconswtch={
        "\u00a7EVT":nejobaUrl("./style/marker/waiting.png"),
        "\u00a7ANO":nejobaUrl("./style/marker/schreibwaren_web.png"),
        "\u00a7INI":nejobaUrl("./style/marker/family.png"),
        "\u00a7BUI":nejobaUrl("./style/marker/mine.png"),
        "\u00a7LOC":nejobaUrl("./style/marker/home-2.png")};
        
    this.stndrIcon=nejobaUrl("./style/marker/information.png"); 
    this.displayUrl=nejobaUrl(c);
    
    this.map=new OpenLayers.Map("map");
    
    this.wms=new OpenLayers.Layer.XYZ("OSM",this.urls,{transitionEffect:"resize",buffer:4,sphericalMercator:!0});
    
    this.markers=new OpenLayers.Layer.Markers("pinsOnMap");
    this.map.addLayers([this.wms,this.markers]);
    this.map.updateSize();
    c=(new OpenLayers.LonLat(5.27,45.82)).transform(new OpenLayers.Projection("EPSG:4326"),new OpenLayers.Projection("EPSG:900913"));
    this.map.setCenter(c);
    this.map.zoomTo(5);

    /**
    * Function: addMarker
    * Add a new marker to the markers layer given the following lonlat, popupClass, and popup contents HTML. Also allow specifying 
    * whether or not to give the popup a close box.
    * 
    * Parameters:
    * ll -              OpenLayers.LonLat       Where to place the marker
    * iconURL           String                  the URL to the marker-icon
    * popupClass -      OpenLayers.Class        Which class of popup to bring up when the marker is clicked.
    * popupContentHTML  String                  What to put in the popup
    * closeBox -        Boolean                 Should popup have a close box?
    * overflow -        Boolean                 Let the popup overflow scrollbars?
    *
    */
    this.addMarker=function(a,b,c,f,g,d){
        var e= new OpenLayers.Size(32,37),h=new OpenLayers.Pixel(-(e.w/2),-e.h);
        b=new OpenLayers.Icon(b,e,h);
        a=new OpenLayers.Feature(this.markers,a);
        a.closeBox=g;a.popupClass=c;
        a.data.popupContentHTML=f;
        a.data.overflow=d?"auto":"hidden";
        a.data.icon=b;
        c=a.createMarker();
        
        c.events.register("mousedown",a,function(a){
            for(var b=0;b<projector.map.popups.length;b++)projector.map.popups[b].hide();
            null==this.popup?(this.popup=this.createPopup(this.closeBox),projector.map.addPopup(this.popup),this.popup.show()):this.popup.toggle(); 
            currentPopup=this.popup;
            OpenLayers.Event.stop(a)
        });
        this.markers.addMarker(c)
    };

    
    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  
    /*
    * function MapProjector.createHtmlPU creates the link that is shown in the PopUp
    *
    * parameter : dataItem is the item to display
    *
    * HINT: the function uses this.displayUrl to get the URL that will be used as detail-displayer
    *       this attribute is set in the constructor and set by the server. the url depends on if 
    *       user is logged in or not. 
    *       url is set in a hidden server-control
    *
    * 30.06.2013 bervie initial realese
    *
    */
    this.createHtmlPU=function(a){
        return'<h5><a href="'+(this.displayUrl+String(a._ID))+'" target="_blank">'+String(a.subject)+"</a></h5>"
    };


    
    /*
     * function MapProjector.defineMrkrIcon defines which marker-icon will be used for this item. 
     *
     * parameter : dataItem is the item to display
     *
     * 30.06.2013 bervie initial realese
     *
     */
    this.defineMrkrIcon=function(a){
        if(void 0==a.tagZero)
            return this.stndrIcon;
        0<a.tagZero.length?(a=a.tagZero.split("_")[0],a=this.iconswtch[a]):a=this.stndrIcon;
        "undefined"===typeof a&&(a=this.stndrIcon);
        
        return a;
    };




    /*
     * display : this function is called from the ListExtractor. It creates and display the markers on the map
     *
     * parameter :  ItemArray 
     *              the array contains all items that should be displayed. the items are chosen from the ListExtractor
     *              this projector-class has no logic for item-selection. it is only a dispaly-idiot
     *
     * 28.06.2013 bervie initial realese
     *
     */
    this.display=function(a){
        for(var b=0;b<projector.map.popups.length;b++)projector.map.popups[b].hide(); 
        this.markers.clearMarkers();
        
        $.each(a,function(a,b){
            ll=(new OpenLayers.LonLat(b.lon,b.lat)).transform(new OpenLayers.Projection("EPSG:4326"),new OpenLayers.Projection("EPSG:900913"));
            popupClass=AutoSizeFramedCloudMinSize;
            popupContentHTML=projector.createHtmlPU(b);
            iconURL=projector.defineMrkrIcon(b);
            projector.addMarker(ll,iconURL,popupClass,popupContentHTML,!0,!0)})
    }
}


// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
// MatrixManager is the class managing the rtubric-selection-matrixes
// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
// --------------------------------------------------------------------------------------------------------------------------------------
// --  object to define the data-item in an array
// -- 
// -- 17-06-2013  bervie  initial realese
// --------------------------------------------------------------------------------------------------------------------------------------
function DataItem(c,a,b){
    this.ValStr=c||null;
    this.TagCode=a||null;
    this.PosArray=Array(b)||[null,null,null,null,null]
} 


// ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

/*
 *  MatrixManager : MtrxMngr
 *
 *  the matrix-manager class is used for managing the multi-list-box selection which 
 *  defines the type of an data-item for the nejoba pinn-board.
 *
 *  it is designed for a general usage and can be used for different 
 *  it reads the source for the matrix ( a string with tab-idents ) from a server-
 *  managed div and builds an array with positioning-information
 *
 *  
 *  
 */
function MtrxMngr(){
    try{
        // --------------------------------------------------------------------------------------------------------------------------------------
        // --  create the source-data-array from the source-text in the div
        // --  insert the first row into the list-boxes
        // -- 
        // -- 17-06-2013  bervie  initial realese
        // --------------------------------------------------------------------------------------------------------------------------------------
        this.initItemArray=function(){
            //console.log("Matrix-Manager-initItemArray");
            try{
                this.Elems=[];
                for(var a=this.matrixSource.split("\n"),b=[null,null,null,null,null],c=0,f=0;c<a.length;){
                    var g=a[c].replace(/^\s+|\s+$/g,""),d=a[c].split("\t").length-1;0<c&&(f=a[c-1].split("\t").length-1);
                    if(null==b[d])b[d]=0;
                    else if(d==f)b[d]+=1;
                    else if(d>f)b[d]+=1;
                    else if(d<f)for(b[d]+=1,idx=d+1;
                    idx<b.length;idx++)b[idx]=null;
                    var e=this.tagPrefix;
                    for(idx=0;idx<b.length;idx++)null!=b[idx]&&(e+="_"+ b[idx].toString());
                    for(var h=[],k=0,l=b.length;k<l;k++)h[k]=b[k];
                    var m=new DataItem(g,e,h);
                    this.Elems[this.Elems.length]=m;c++}for(c=0;c<this.Elems.length;c++);
            }
            catch(n){
                txt="There was an error in the MtrxMngr.initItemArray\n\n",
                txt+="Error description: "+n.message+"\n------------------------------------------------------------------------------------------------------------------------------------------------------------\n",
                console.log(txt)
            }
        },
        
        // --------------------------------------------------------------------------------------------------------------------------------------
        // --  the function fills the first listbox with the items we have for it : position-array = ( i,null,null,null,null )
        // -- 
        // -- 17-06-2013  bervie  initial realese
        // --------------------------------------------------------------------------------------------------------------------------------------
        this.fillUpInitial=function(){
            //console.log("Matrix-Manager-fillUpInitial"); 
            try{
                $('select[id*="lsbx_"]').html("");
            
                for(var a=0;a<this.Elems.length;a++)
                if(0==this.Elems[a].PosArray.toString().split(",")[1].length){
                    var b="<option value="+this.Elems[a].TagCode+">"+this.Elems[a].ValStr+"</option>";
                    //console.log("add option to select : "+b);
                    
                    $("#lsbx_0").append(b)}
            }
            catch(c){
                txt="There was an error in the MtrxMngr.fillUpInitial\n\n",
                txt+="Error description: "+c.message+"\n------------------------------------------------------------------------------------------------------------------------------------------------------------\n", 
                console.log(txt)}
        },


        // --------------------------------------------------------------------------------------------------------------------------------------
        // --  handleSelection is called every time a select-option was clicked
        // -- 
        // -- 18-06-2013  bervie  initial realese
        // --------------------------------------------------------------------------------------------------------------------------------------
        this.handleSelection=function(a){
            //console.log("Matrix-Manager-handleSelection");
            try{var b=a.target.value,c=a.target.text;
            $("#CoPlaBottom_txbx_tagforitem").val(b);
            $("#CoPlaBottom_txbx_itemname").val(c);
            var f=a.currentTarget.id.split("_"),g=parseInt(f[1])+1,d=f[0]+"_"+g;
            //console.log("handleSelection : SelectNext = "+d);
            
            if(5>g)for($('select[id*="lsbx_"]:gt('+(g-1)+")").html(""),a=0;
            a<this.Elems.length;a++){var e=this.Elems[a].TagCode;
            
            if(0==e.indexOf(b)){var h=e.split("_").length,k=b.split("_").length; 
            if(h==k+1){var l="<option value="+this.Elems[a].TagCode+">"+this.Elems[a].ValStr+"</option>";
            //console.log("found item for next select : "+this.Elems[a].ValStr+" - "+e+" - nxt box "+d+" - "+l);
            
            $("#"+d).append(l)}}}}catch(m){txt="There was an error in the MtrxMngr.fillUpInitial\n\n",txt+="Error description: "+m.message+"\n------------------------------------------------------------------------------------------------------------------------------------------------------------\n",console.log(txt)}
        }
    }
    catch (c) {
        txt = "There was an error in the MtrxMngr\n";
        txt += "Error description: " + c.message + "\n------------------------------------------------------------------------------------------------------------------------------------------------------------\n";
        console.log(txt);
    }
}

//
// if drop-down (select) country was changed we have to enable or diable the txtboxes
// no country selected means city and plz is disabled
//
//
function countrySelectChanged() {
    var c = document.getElementById("CoPlaBottom_sel_country");
    if ('0' != c.options[c.selectedIndex].value) {
        // alert('c.options[c.selectedIndex].value : ' + c.options[c.selectedIndex].value);
        $("#CoPlaBottom_txbx_postCode").removeAttr('disabled');
        $("#CoPlaBottom_txbx_city").removeAttr('disabled');
    }
    else {
        $("#CoPlaBottom_txbx_postCode").attr('disabled', 'disabled');
        $("#CoPlaBottom_txbx_city").attr('disabled', 'disabled');
    }
    $("#CoPlaBottom_txbx_postCode").val('');
    $("#CoPlaBottom_txbx_city").val('');

} 

// ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

// ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


$(document).ready(function(){
    // --------------------------------------------------------------------------------------------------------------------------------------
    // -- 
    // -- object of type matrix-manager will handle the stuff
    // -- 
    // --------------------------------------------------------------------------------------------------------------------------------------
    var c=new MtrxMngr;
    
    // --------------------------------------------------------------------------------------------------------------------------------------
    // -- 
    // -- add the click-event-handlers for the image-buttons
    // -- 
    // --------------------------------------------------------------------------------------------------------------------------------------
    $("img[id*='img_select']").click(function(a){
        //console.log("Matrix-Manager- ButtonClicked");
        $("#CoPlaBottom_txbx_tagforitem").val("");
        $("#CoPlaBottom_txbx_itemname").val("");
        a=String(this.id);
        $("#CoPlaBottom_toggle_div").text(this.typeButtonPressed);
        
        switch(a){
            case "CoPlaBottom_img_selectEvent":
                c.tagPrefix="EVT";
                c.matrixSource=$("#CoPlaBottom_date_event_div").text();
                break;
            
            case "CoPlaBottom_img_selectAnnonceType":
                c.tagPrefix="ANO";
                c.matrixSource=$("#CoPlaBottom_annonce_div").text(); 
                break;
                
            case "CoPlaBottom_img_selectInitiatives":
                c.tagPrefix="INI";
                c.matrixSource=$("#CoPlaBottom_initiative_div").text();
                break;
            case "CoPlaBottom_img_selectBusiness":
                c.tagPrefix="BUI";
                c.matrixSource=$("#CoPlaBottom_business_div").text();
                break;
            case "CoPlaBottom_img_selectLocation":
                c.tagPrefix="LOC";
                c.matrixSource=$("#CoPlaBottom_location_div").text();
                break;
            default:
                c.tagPrefix="";
                //console.log("unknown button pressed for itm-type definition!")
        }
        
        // --------------------------------------------------------------------------------------------------------------------------------------
        // -- 
        // -- add the click-event-handler for the selects 
        // -- 
        // --------------------------------------------------------------------------------------------------------------------------------------
        $("select[id*='lsbx_']").click(function(a){	c.handleSelection(a)}); 
        //console.log("Matrix-Manager- choosen source typ : "+c.tagPrefix);
        
        c.initItemArray();
        c.fillUpInitial()})
    }
);




























