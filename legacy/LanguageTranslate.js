var CurrentCultureKey 
window.addEventListener('DOMContentLoaded', (event) => {
    //jsonDB Defined in JsonDb.js
    CurrentCultureKey = jsonDB.DefaultCultureKey
});

//Set Culture By Input
function SetCulture(param){
    console.log("Setting Culture :" ,param.value)
    Translate(param.value)
}


function GetCultureKey(Value){
    if(Value == "" || Value === "" || Value == null){//TODO:better nul or white space value check
        return null
    }

    switch (Value) {//TODO: add to lower and trim
        case "English":
            return "eng-en"
        case "עברית":
            return "he-il"
        case "Русский":
            return "rus-ru"
        default:
            return null
    }
}                                                                                                      

function SetPriceMenuDirection(cultureKey){
    let floatToPrice = "left"                                                                                                                                                                                                                                                                                                                                                                                                               
    let floatToName = "right"                         
    let direction = "rtl"

    if(cultureKey == "eng-en" || cultureKey == "rus-ru"){
        floatToPrice = "right"
        floatToName = "left"
        direction = "ltr"
    }

    // change direction to price
    document.querySelectorAll(".price").forEach(element => {
        element.style.float = floatToPrice
    })

    //change direction to item in list
    document.querySelectorAll(".name").forEach(element => {
        element.style.float = floatToName
        element.style.direction = direction
    })

    //change direction to additional terms
    document.querySelectorAll(".AdditionalTerm").forEach(element => {
        element.style.float = floatToName
        element.style.direction = direction
    })
}

//Get All Translate Elements
function Translate(culture){
    let elementsToTranslate = document.querySelectorAll(".CanTranslated")
    var CultureKey = GetCultureKey(culture)

    //dont translate if key null or same translation
    if(CultureKey == null || CurrentCultureKey == CultureKey){
        return
    }

    //fore-each DOM  element that have class CanTranslated
    console.log(elementsToTranslate)
    elementsToTranslate.forEach(ToTranslateObj => {  
        jsonDB.LanguageTranslateData.forEach(LanguageTranslationElement => {
            //find Dom element text in current culture value of JsonDB Array object - TODO: Find Fumction for faster find
            if(LanguageTranslationElement[CurrentCultureKey] == ToTranslateObj.innerHTML){
                //TODO:better nul or white space value check

                //console.log("ToTranslate:",LanguageTranslationElement[CultureKey]);  
                if(LanguageTranslationElement[CultureKey] != null && LanguageTranslationElement[CultureKey] != undefined && LanguageTranslationElement[CultureKey] != " " && LanguageTranslationElement[CultureKey] != ""){
                    //Translate
                    ToTranslateObj.innerHTML = LanguageTranslationElement[CultureKey]
                }
            }                
        });
    });
    // Set Current Culture
    CurrentCultureKey = CultureKey
    // set direction
    SetPriceMenuDirection(CurrentCultureKey)
}
