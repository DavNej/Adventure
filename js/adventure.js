var Adventures = {};
//currentAdventure is used for the adventure we're currently on (id). This should be determined at the beginning of the program
Adventures.currentAdventure = 0; //todo keep track from db
//currentStep is used for the step we're currently on (id). This should be determined at every crossroad, depending on what the user chose
Adventures.currentStep = 1; //todo keep track from db
Adventures.currentUser = 0; //todo keep track from db

//TODO: remove for production
Adventures.debugMode = true;
Adventures.DEFAULT_IMG = "./images/choice.jpg";


//Handle Ajax Error, animation error and speech support
Adventures.bindErrorHandlers = function() {
    //Handle ajax error, if the server is not found or experienced an error
    $(document).ajaxError(function(event, jqxhr, settings, thrownError) {
        Adventures.handleServerError(thrownError);
    });

    //Making sure that we don't receive an animation that does not exist
    $("#situation-image").error(function() {
        Adventures.debugPrint("Failed to load img: " + $("#situation-image").attr("src"));
        Adventures.setImage(Adventures.DEFAULT_IMG);
    });
};


//The core function of the app, sends the user's choice and then parses the results to the server and handling the response
Adventures.chooseOption = function() {
    Adventures.currentStep++;
    $.ajax("/story", {
        type: "POST",
        data: {
            "user": Adventures.currentUser,
            "adventure": Adventures.currentAdventure,
            "stage": Adventures.currentStep,
            "choice": $(this).val(),
        },
        dataType: "json",
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            if (data.end) {
                console.log('runs')
                $('.game-options').hide();
                $('#life.score-tracking').hide();
                $('#coins.score-tracking').hide();
                Adventures.setImage(data.image);
                $(".situation-text").text(data.title).show();
                $('<h2/>').text(data.msg).append($('.options-list'));
            } else {
                Adventures.write(data);
            }
        }
    });
};

Adventures.write = function(data) {
    console.log('write funct')
        //update life and coins
    $('#life.score-tracking .count').text(data['life']);
    $('#coins.score-tracking .count').text(data['coins']);
    //write question
    $(".situation-text").text(data["text"]).show();
    //Writing new choices and image to screen
    for (var i = 0; i < data['options'].length; i++) {
        var opt = $("#option_" + (i + 1));
        opt.text(data['options'][i]['option_text']);
        opt.prop("value", data['options'][i]['choice']);
    }
    Adventures.setImage(data["image"]);
};


Adventures.start = function() {
    $(document).ready(function() {
        $(".game-option").click(Adventures.chooseOption);
        $("#nameField").keyup(Adventures.checkName);
        $(".adventure-button").click(Adventures.initAdventure);

        // show home screen hide game
        $(".adventure").hide();
        $(".welcome-screen").show();
    });
};

//Setting the relevant image according to the server response
Adventures.setImage = function(img_name) {
    $("#situation-image").attr("src", "./images/" + img_name);
};

Adventures.checkName = function() {
    if ($(this).val() !== undefined && $(this).val() !== null && $(this).val() !== "") {
        $(".adventure-button").prop("disabled", false);
    } else {
        $(".adventure-button").prop("disabled", true);
    }
};


Adventures.initAdventure = function() {

    $.ajax("/start", {
        type: "POST",
        data: {
            "user": $("#nameField").val(),
            "adventure_id": $(this).val(),
        },
        dataType: "json",
        contentType: "application/json",
        success: function(data) {
            console.log(data);

            Adventures.currentUser = data.user;
            Adventures.currentAdventure = data.adventure;
            Adventures.currentStep = data.stage;

            Adventures.write(data);

            // hide home screen show game
            $(".adventure").show();
            $(".welcome-screen").hide();
        }
    });
};

Adventures.handleServerError = function(errorThrown) {
    Adventures.debugPrint("Server Error: " + errorThrown);
    var actualError = "";
    if (Adventures.debugMode) {
        actualError = " ( " + errorThrown + " ) ";
    }
    Adventures.write("Sorry, there seems to be an error on the server. Let's talk later. " + actualError);

};

Adventures.debugPrint = function(msg) {
    if (Adventures.debugMode) {
        console.log("Adventures DEBUG: " + msg)
    }
};

Adventures.start();