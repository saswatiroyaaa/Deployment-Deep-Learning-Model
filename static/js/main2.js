let uniformButtons = () => {
    let buttons = [...document.getElementsByClassName("model-choose")];
    let max_width = Math.max(...buttons.map((button) => {return button.style.width}));
    for(button in buttons) {
        button.style.width = max_width;
    }
}


let addMenu = (data) => {
    let dropdown_menu = document.getElementsByClassName("dropdown-menu")[0];
    console.log(dropdown_menu);
    document.getElementById("dropdownMenu2").innerHTML = "-- Select model --";
    dropdown_menu.innerHTML = "";
    for(model in data) {
        let temp = document.createElement("button");
        temp.setAttribute("class", "dropdown-item");
        temp.setAttribute("type", "button");
        temp.appendChild(document.createTextNode(model));
        dropdown_menu.appendChild(temp);
    }
}

let addCard = (model, data) => {
    let card = document.getElementsByClassName('card')[0];
    console.log(card.classList);
    card.classList.remove("bg-info", "bg-danger");
    let modelName = document.getElementById('model-name');
    let probabillity = document.getElementById('probabillity');
    let verdict = document.getElementById('verdict');
    modelName.innerHTML = "<strong>Model Name: </strong>" + model;
    probabillity.innerHTML = "<strong>Probabillity: </strong>" + data[model];
    if(Number(data[model]) > 0.5) {
        verdict.innerHTML = "<strong>Verdict: </strong> Infection is Lyme!";
        card.classList.add("text-white", "bg-danger", "mb-3");
    } else {
        verdict.innerHTML = "<strong>Verdict: </strong> Infection is not Lyme. Don't worry!";
        card.classList.add("text-white", "bg-info", "mb-3");
    }
}
$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    //uniformButtons();
    $('.model-choosing').hide()
    $('.dropdown').hide();

    // Upload Preview
    function readURL(input) {
        // $('.dropdown-menu').hide();
        // document.getElementById("dropdownMenu2").innerHTML = "-- Select a model --";
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        
        $('.image-section').show();
        $('#btn-predict').show();
        // $('#result').text('');
        $('.dropdown').hide();
        $('#result').hide();
        $('.model-choosing').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                console.log(typeof data)
                console.log(JSON.stringify(data, null, 2));
                // Get and display the result
                $('.loader').hide();
                $('.model-choosing').fadeIn(400);
                //uniformButtons();

                // New code
                $('.model-choose').click( function() {
                    let choosen_model = $(this).attr("id"); 
                    console.log(choosen_model)
                    console.log(data[choosen_model])
                    addMenu(data[choosen_model]);
                    $('.dropdown').fadeIn(600);
                    $(".dropdown-item").click(function () {
                        $('#result').hide();
                        let model = this.innerHTML;
                        document.getElementById("dropdownMenu2").innerHTML = model;
                        console.log(model);
                        addCard(model, data[choosen_model]);
                        $('#result').fadeIn(600);
                });
                });
                //$('#result').text(' Result:  ' + data["vgg"]);
                console.log('Success!');
            },
        });
    });

});
