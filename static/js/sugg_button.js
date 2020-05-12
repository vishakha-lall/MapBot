function toggle_sugg(ele_id) {
    var ele = document.getElementById(ele_id);
    if (ele.style.display === "none") {
        ele.style.display = "block";
    } else {
        ele.style.display = "none";
    }
}

function get_data(form_elements) {
    var form_data = [];
    for (i = 0, len = form_elements.length; i < len; i++) {
        form_data.push(form_elements.item(i).value);
    }
    return form_data;
}

function add_user_data(innerText) {
    var rownode = document.createElement('div');
    rownode.setAttribute('class', 'row justify-content-md-center');
    var usernode = document.createElement("div");
    usernode.setAttribute('class', 'col shadow-sm p-3 mb-1 text-left text-break');
    usernode.innerText = innerText;
    rownode.appendChild(usernode);
    return rownode;
}

function add_bot_data(botText, rownode) {
    var botnode = document.createElement("div");
    botnode.setAttribute('class', 'col shadow-sm p-3 mb-1 text-right text-break');
    botnode.innerText = botText;
    rownode.appendChild(botnode);
    document.getElementById("chats").appendChild(rownode);
}

function create_innerText(form_id, form_data) {
    var innerText = "";
    switch (form_id) {
        case "form_directions":
            origin = form_data[0];
            destination = form_data[1];
            innerText = "Origin: " + origin + "\nDestination: " + destination;
            break;
        case "form_geocoding":
            geocoding_text = form_data[0];
            innerText = "Location: " + geocoding_text;
            break;
        case "form_timezone":
            tz_location_text = form_data[0];
            tz_option = form_data[1];
            innerText = "Location: " + tz_location_text + "\nOption: " + tz_option;
            break;
        case "form_elevation":
            elev_location_text_1 = form_data[0];
            elev_location_text_2 = form_data[1];
            innerText = "Height of: " + elev_location_text_1 + "\nCompared to: " + elev_location_text_2;
            break;
        case "form_map":
            map_location_text = form_data[0];
            zoom = form_data[1];
            size = form_data[2];
            innerText = "Location: " + map_location_text + "\nZoom: " + zoom + "\nSize: " + size;
            break;
        default:
            innerText = "ERROR";
    }
    return innerText;
}

$(function() {
    $("[id^=form]:not(#form_usrInput)").on('submit', function(event) {
        var that = this;
        var form_id = this.id;
        var form_data = get_data(this.elements);
        var innerText = create_innerText(form_id, form_data);
        var rownode = add_user_data(innerText);
        $.ajax({
                data: {
                    id: form_id,
                    eles: form_data,
                },
                type: 'POST',
                url: '/suggestions',
                beforeSend: function() {
                    $("#loading-spinner").show();
                },
                success: function(data) {
                    $("#loading-spinner").hide();
                    that.reset();
                }
            })
            .done(function(data) {
                add_bot_data(data.botText, rownode);
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
