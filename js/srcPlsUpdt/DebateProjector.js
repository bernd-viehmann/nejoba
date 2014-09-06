// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//   Debate-Projector Class
// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//
//   The Class is responsible for displaying the list of debates as text-table. it shows the items seperated on pages
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
// 
//
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
function DebateProjector(dispUrl) {
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

    this.iconswtch = { 
        "§EVT": nejobaUrl("./style/marker/waiting.png"),
        "§ANO": nejobaUrl("./style/marker/schreibwaren_web.png"),
        "§INI": nejobaUrl("./style/marker/family.png"),
        "§BUI": nejobaUrl("./style/marker/mine.png"),
        "§LOC": nejobaUrl("./style/marker/home-2.png")
    };

    this.stndrIcon = nejobaUrl("./style/marker/text.png");
    this.displayUrl = nejobaUrl(dispUrl);

    this.printTmplt = [ '        <div id="Div1">',
                        '            <div class="row span12 well">',
                        '                <div class="span11">',
                        '                    <h5>',
                        '                        <a href="§§URL_LINK_TARGET§§" target="_blank">§§URL_LINK_TEXT§§</a>',
                        '                    </h5>',
                        '                </div>',
                        '                <div class="span4">',
                        '                    <strong>Ersteller: </strong>§§NICKNAME§§<br />',
                        '                    <strong>erstellt am: </strong>§§CREATIONTIME§§<br />',
                        '                </div>',
                        '                <div class="span3">',
                        '                    <strong>vom: </strong>§§DATE_FROM§§<br />',
                        '                    <strong>bis: </strong>§§DATE_TILL§§<br />',
                        '                </div>',
                        '                <div class="span3">',
                        '                    <strong>Ort: </strong>§§LOCATIONNAME§§<br />',
                        '                </div>',
                        '            <br />',
                        '            </div>',
                        '        </div>'].join('\n');



    /*
     * function DebateProjector.defineItemIcon defines which marker-icon will be used for this item. 
     *
     * parameter : dataItem is the item to display
     *
     * 30.06.2013 bervie initial realese
     *
     */
    this.defineDebateIcon = function (dataItm) {
        // console.log('DebateProjector.defineDebateIcon was called');
        if (dataItm.tagZero == undefined) {
            return this.stndrIcon
        }

        if (dataItm.tagZero.length > 0) {
            var typ = dataItm.tagZero.split("_")[0];
            var icon = this.iconswtch[typ];
        }
        else {
            var icon = this.stndrIcon;
        }

        if (typeof icon === "undefined") icon = this.stndrIcon;
        return icon;
    }


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
    this.createItemDiv = function (val) {
        
        var rslt = this.printTmplt;

        // ´put the data inside the template
        rslt = rslt.replace("§§URL_LINK_TARGET§§", this.displayUrl + val._ID);
        rslt = rslt.replace("§§URL_LINK_TEXT§§", val.subject);
        rslt = rslt.replace("§§NICKNAME§§", val.nickname);
        rslt = rslt.replace("§§CREATIONTIME§§", val.creationTime);
        rslt = rslt.replace("§§DATE_FROM§§", val.from);
        rslt = rslt.replace("§§DATE_TILL§§", val.till);
        rslt = rslt.replace("§§LOCATIONNAME§§", val.locationname);

        return rslt;
    }


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
    this.display = function (itemArray) {

        // console.log('DebateProjector.display was called ');
        var divContent = '';

        $.each(itemArray, function (i, val) {
            // console.log('Number ' + String(i) + ' ; Subject : ' + val.subject);

            divContent += projector.createItemDiv(val);
        });
        $('#canvasforlist').html(divContent);


        return;
    }

};






