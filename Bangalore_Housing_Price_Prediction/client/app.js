function onPageLoad(){
    console.log("Document Loaded");
    var url = "http://127.0.0.1:5000/get_locations";
    $.get(url,function(data,status){
        console.log("got request for get_location_names request");
        if(data){
            var locations = data.locations;
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty();
            for(var i in locations){
                var opt = new Option(locations[i]);
                $('#uiLocations').append(opt);
            }
        }
    });
}


function getBathValue(){
    var uiBathRooms = document.getElementsByName("uibath");
    for(var i in uiBathRooms){
        if(uiBathRooms[i].checked){
            return parseInt(i)+1;
        }
    }
    return -1;
}

function getBHKValue(){
    var uiBHKRooms = document.getElementsByName("uiBHK");
    for(var i in uiBHKRooms){
        if(uiBHKRooms[i].checked){
            return parseInt(i)+1;
        }
    }
    return -1;
}

function getBalconyValue(){
    var uiBalconyRooms = document.getElementsByName("uibalcony");
    for(var i in uiBalconyRooms){
        if(uiBalconyRooms[i].checked){
            return parseInt(i)+1;
        }
    }
    return -1;  // Invalid Value
}

function onClickedEstimatedPrice(){
    console.log("Predicting Price...");
    var sqft = document.getElementById("uiSqft");
    var location = document.getElementById("uiLocations");
    var bhk = getBHKValue();
    var balcony = getBalconyValue();
    var bath = getBathValue();
    var estimatedPrice = document.getElementById("uiEstimatePrice");

    var url = "http://localhost:5000/predict_home_price";
    $.post(url,{
        total_sqft: parseFloat(sqft.value),
        location: location.value,
        bhk: bhk,
        balcony: balcony,
        bath: bath
    },function(data,status){
        console.log("Estimated Price: ",data.estimated_price);
        estimatedPrice.innerHTML = "<h2>" + data.estimated_price.toString() + "Lakhs </h2>";
        console.log("Status: " + status);
    });
}

window.onload = onPageLoad();