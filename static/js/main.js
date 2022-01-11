$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
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
        $('#result').text('');
        $('#result').hide();
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
                // Get and display the result
                $('.loader').hide();
                // Creating the table
                var table = document.createElement("table");
                table.classList.add("table");
                var thead = document.createElement("thead");
                thead.classList.add("thead-dark")
                var firstRow = document.createElement("tr");
                var nameHeader = document.createElement("th");
                nameHeader.appendChild(document.createTextNode("Model Name"));
                var outputHeader = document.createElement("th");
                outputHeader.appendChild(document.createTextNode("P(Lyme Positive)"));
                var resultHeader = document.createElement("th");
                resultHeader.appendChild(document.createTextNode("Verdict"));

                firstRow.appendChild(nameHeader);
                firstRow.appendChild(outputHeader);
                firstRow.appendChild(resultHeader);
                thead.appendChild(firstRow);
                table.appendChild(thead);

                var tbody = document.createElement("tbody");
                for(model in data){
                    console.log(model)
                    console.log(data[model])
                    var currRow = document.createElement("tr");
                    var currModelName = document.createElement("td");
                    currModelName.appendChild(document.createTextNode(model));
                    var currModelOuput = document.createElement("td");
                    currModelOuput.appendChild(document.createTextNode(data[model]));
                    res = "";
                    var currModelVerdict = document.createElement("td");
                    if (Number(data[model]) > 0.5) {
                        res = "Positive";
                        currModelVerdict.classList.add("positive");
                    } else {
                        res = "Negative";
                        currModelVerdict.classList.add("negative");
                    }
                    currModelVerdict.appendChild(document.createTextNode(res));
                    currRow.appendChild(currModelName);
                    currRow.appendChild(currModelOuput);
                    currRow.appendChild(currModelVerdict);
                    tbody.appendChild(currRow);
                }
                table.appendChild(tbody);
                // document.body.appendChild(table);
                $("#result").append(table);
                $('#result').fadeIn(600);
                //$('#result').text(' Result:  ' + data["vgg"]);
                console.log('Success!');
            },
        });
    });

});
