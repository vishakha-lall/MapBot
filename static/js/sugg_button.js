function toggleSugg(eleId) {
    var ele = document.getElementById(eleId);
    if (ele.style.display === "none") {
        $("[id^=form]:not(#form_usrInput)").parent().each(function() {
            this.style.display = "none";
        });
        ele.style.display = "block";
    } else {
        ele.style.display = "none";
    }
}

function getData(formElements) {
    var formData = [];
    for (let i = 0, len = formElements.length; i < len; i++) {
        formData.push(formElements.item(i).value);
    }
    return formData;
}

function addUserData(innerText) {
    var rownode = document.createElement("div");
    rownode.setAttribute("class", "row justify-content-md-center");
    var usernode = document.createElement("div");
    usernode.setAttribute("class", "col shadow-sm p-3 mb-1 text-left text-break");
    usernode.innerText = innerText;
    rownode.appendChild(usernode);
    return rownode;
}

function addBotData(botText, rownode) {
    var botnode = document.createElement("div");
    botnode.setAttribute("class", "col shadow-sm p-3 mb-1 text-right text-break");
    botnode.innerText = botText;
    rownode.appendChild(botnode);
    document.getElementById("chats").appendChild(rownode);
}

function create_innerText(formId, formData) {
    var innerText = "";
    switch (formId) {
        case "form_directions":
            let origin = formData[0];
            let destination = formData[1];
            innerText = "Origin: " + origin + "\nDestination: " + destination;
            break;
        case "form_geocoding":
            let geocoding_text = formData[0];
            innerText = "Location: " + geocoding_text;
            break;
        case "form_timezone":
            let tz_location_text = formData[0];
            let tz_option = formData[1];
            innerText = "Location: " + tz_location_text + "\nOption: " + tz_option;
            break;
        case "form_elevation":
            let elev_location_text_1 = formData[0];
            let elev_location_text_2 = formData[1];
            innerText = "Height of: " + elev_location_text_1 + "\nCompared to: " + elev_location_text_2;
            break;
        case "form_map":
            let map_location_text = formData[0];
            let zoom = formData[1];
            let size = formData[2];
            innerText = "Location: " + map_location_text + "\nZoom: " + zoom + "\nSize: " + size;
            break;
        default:
            innerText = "ERROR";
    }
    return innerText;
}

$(function() {
    $("[id^=form]:not(#form_usrInput)").on("submit", function(event) {
        var that = this;
        var formId = this.id;
        var formData = getData(this.elements);
        var innerText = create_innerText(formId, formData);
        var rownode = addUserData(innerText);
        $.ajax({
                data: {
                    id: formId,
                    eles: formData,
                },
                type: "POST",
                url: "/suggestions",
                beforeSend: function() {
                    $("#loading-spinner").show();
                },
                success: function(data) {
                    $("#loading-spinner").hide();
                    that.reset();
                    toggleSugg($(that).parent().attr("id"));
                }
            })
            .done(function(data) {
                addBotData(data.botText, rownode);
            });
        document
            .getElementById("form_usrInput")
            .scrollIntoView({
                block: "end",
                behavior: "smooth",
                inline: "nearest"
            });
        event.preventDefault();
    });
});
