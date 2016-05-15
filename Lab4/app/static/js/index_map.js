var myMap;
var AO_centres;
var Clasters;

var AO_names = ["szao", "sao", "svao", "vao", "uvao", "uao", "uzao", "zao", "cao", "new-msk"];


function render_map(okrug){
    var all_buttons = document.querySelectorAll(".active");
    for (var i =0; i < all_buttons.length; i++){
        all_buttons[i].className = "btn btn-primary btn-lg";
    }

    var current_button = document.getElementById(okrug);
    current_button.className = "btn btn-primary btn-lg active"
    refill_map(okrug, myMap)
}


function refill_map(okrug, myMap){
    myMap.geoObjects.removeAll();
    if (okrug == "main"){
        myMap.setZoom(10, {duration: 300}).then(function() {
            myMap.panTo([55.753559, 37.609218], {flying: 1});
        });

        AO_names.forEach(function(name, i, arr){
            myMap.geoObjects.add(new ymaps.Placemark([AO_centres[name]["coord_width"], AO_centres[name]["coord_length"]],
                {
                    balloonContent: name,
                    hintContent: name
                },
                {
                    preset: 'islands#redDotIcon'
                }));

        })


    }
    else {
        myMap.panTo([AO_centres[okrug]["coord_width"], AO_centres[okrug]["coord_length"]], {flying: 1})
            .then(function () {
                myMap.setZoom(12, {duration: 300});
            });

        myMap.geoObjects.add(new ymaps.Placemark([AO_centres[okrug]["coord_width"], AO_centres[okrug]["coord_length"]],
                {
                    balloonContent: okrug,
                    hintContent: okrug
                },
                {
                    preset: 'islands#redDotIcon'
                }));

        Clasters[0][okrug].forEach(function(obj, i, arr){
                myMap.geoObjects.add(new ymaps.Placemark([obj["Cells"]["geoData"]["coordinates"][0][1], obj["Cells"]["geoData"]["coordinates"][0][0]],
                    {
                        balloonContentHeader: obj["Cells"]["ShortName"],
                        balloonContentBody: obj["Cells"]["ObjectAddress"][0]["AdmArea"]
                    },
                    {
                        preset: 'islands#blueCircleDotIcon'
                    }))
            })

    }

}

function pass_centres_data(json_data){
    AO_centres = json_data
}

function pass_clasters_data(json_data){
    Clasters = json_data
}

ymaps.ready(function () {
    myMap = new ymaps.Map('map', {
            center: [55.753559, 37.609218],
            zoom: 10,
            controls: ['zoomControl']
        });

    refill_map("main", myMap);

});
