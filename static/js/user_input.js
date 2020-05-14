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

$(function() {
    $("#form_usrInput").on("submit", function(event) {
        var that = this;
        var usrText = $("#usrInput").val();
        var rownode = addUserData(usrText);
        $.ajax({
                data: {
                    usrInput: usrText,
                },
                type: "POST",
                url: "/process",
                beforeSend: function() {
                    $("#loading-spinner").show();
                },
                success: function(data) {
                    $("#loading-spinner").hide();
                    that.reset();
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
