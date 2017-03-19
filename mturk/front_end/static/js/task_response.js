/*
 * Requires:
 *     psiturk.js
 *     utils.js
 */

// Initalize psiturk object
var psiTurk = new PsiTurk(uniqueId, adServerLoc, mode);

var mycondition = condition;  // these two variables are passed by the psiturk server process
var mycounterbalance = counterbalance;  // they tell you which condition you have been assigned to
// they are not used in the stroop code but may be useful to you

// All pages to be loaded
var pages = [
    "instructions/instruct-1.html",
    "instructions/instruct-ready.html",
    "chat.html",
    "postquestionnaire.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
    "instructions/instruct-1.html",
    "instructions/instruct-ready.html"
];

var MAX_CONTEXT_COUNT = 5;
if (typeof KeyEvent == "undefined") {
    var KeyEvent = {
        DOM_VK_CANCEL: 3,
        DOM_VK_HELP: 6,
        DOM_VK_BACK_SPACE: 8,
        DOM_VK_TAB: 9,
        DOM_VK_CLEAR: 12,
        DOM_VK_RETURN: 13,
        DOM_VK_ENTER: 14,
        DOM_VK_SHIFT: 16,
        DOM_VK_CONTROL: 17,
        DOM_VK_ALT: 18,
        DOM_VK_PAUSE: 19,
        DOM_VK_CAPS_LOCK: 20,
        DOM_VK_ESCAPE: 27,
        DOM_VK_SPACE: 32,
        DOM_VK_PAGE_UP: 33,
        DOM_VK_PAGE_DOWN: 34,
        DOM_VK_END: 35,
        DOM_VK_HOME: 36,
        DOM_VK_LEFT: 37,
        DOM_VK_UP: 38,
        DOM_VK_RIGHT: 39,
        DOM_VK_DOWN: 40,
        DOM_VK_PRINTSCREEN: 44,
        DOM_VK_INSERT: 45,
        DOM_VK_DELETE: 46,
        DOM_VK_0: 48,
        DOM_VK_1: 49,
        DOM_VK_2: 50,
        DOM_VK_3: 51,
        DOM_VK_4: 52,
        DOM_VK_5: 53,
        DOM_VK_6: 54,
        DOM_VK_7: 55,
        DOM_VK_8: 56,
        DOM_VK_9: 57,
        DOM_VK_SEMICOLON: 59,
        DOM_VK_EQUALS: 61,
        DOM_VK_A: 65,
        DOM_VK_B: 66,
        DOM_VK_C: 67,
        DOM_VK_D: 68,
        DOM_VK_E: 69,
        DOM_VK_F: 70,
        DOM_VK_G: 71,
        DOM_VK_H: 72,
        DOM_VK_I: 73,
        DOM_VK_J: 74,
        DOM_VK_K: 75,
        DOM_VK_L: 76,
        DOM_VK_M: 77,
        DOM_VK_N: 78,
        DOM_VK_O: 79,
        DOM_VK_P: 80,
        DOM_VK_Q: 81,
        DOM_VK_R: 82,
        DOM_VK_S: 83,
        DOM_VK_T: 84,
        DOM_VK_U: 85,
        DOM_VK_V: 86,
        DOM_VK_W: 87,
        DOM_VK_X: 88,
        DOM_VK_Y: 89,
        DOM_VK_Z: 90,
        DOM_VK_CONTEXT_MENU: 93,
        DOM_VK_NUMPAD0: 96,
        DOM_VK_NUMPAD1: 97,
        DOM_VK_NUMPAD2: 98,
        DOM_VK_NUMPAD3: 99,
        DOM_VK_NUMPAD4: 100,
        DOM_VK_NUMPAD5: 101,
        DOM_VK_NUMPAD6: 102,
        DOM_VK_NUMPAD7: 103,
        DOM_VK_NUMPAD8: 104,
        DOM_VK_NUMPAD9: 105,
        DOM_VK_MULTIPLY: 106,
        DOM_VK_ADD: 107,
        DOM_VK_SEPARATOR: 108,
        DOM_VK_SUBTRACT: 109,
        DOM_VK_DECIMAL: 110,
        DOM_VK_DIVIDE: 111,
        DOM_VK_F1: 112,
        DOM_VK_F2: 113,
        DOM_VK_F3: 114,
        DOM_VK_F4: 115,
        DOM_VK_F5: 116,
        DOM_VK_F6: 117,
        DOM_VK_F7: 118,
        DOM_VK_F8: 119,
        DOM_VK_F9: 120,
        DOM_VK_F10: 121,
        DOM_VK_F11: 122,
        DOM_VK_F12: 123,
        DOM_VK_F13: 124,
        DOM_VK_F14: 125,
        DOM_VK_F15: 126,
        DOM_VK_F16: 127,
        DOM_VK_F17: 128,
        DOM_VK_F18: 129,
        DOM_VK_F19: 130,
        DOM_VK_F20: 131,
        DOM_VK_F21: 132,
        DOM_VK_F22: 133,
        DOM_VK_F23: 134,
        DOM_VK_F24: 135,
        DOM_VK_NUM_LOCK: 144,
        DOM_VK_SCROLL_LOCK: 145,
        DOM_VK_COMMA: 188,
        DOM_VK_PERIOD: 190,
        DOM_VK_SLASH: 191,
        DOM_VK_BACK_QUOTE: 192,
        DOM_VK_OPEN_BRACKET: 219,
        DOM_VK_BACK_SLASH: 220,
        DOM_VK_CLOSE_BRACKET: 221,
        DOM_VK_QUOTE: 222,
        DOM_VK_META: 224
    };
}

/********************
* HTML manipulation
*
* All HTML files in the templates directory are requested
* from the server when the PsiTurk object is created above. We
* need code to get those pages from the PsiTurk object and
* insert them into the document.
*
********************/

/********************
* STROOP TEST       *
********************/
var StroopExperiment = function() {

    var wordon, // time word is presented
        listening = false;
    var current_context_id = 0;
    var context_count = 0;

    var user_id = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
        return v.toString(16);
    });

    var finish = function() {
        $("#trial").unbind("keydown", response_handler); // Unbind keys
        currentview = new Questionnaire();
    };

    var show_word = function(text, color) {
        d3.select("#stim")
            .append("div")
            .attr("id","word")
            .style("color",color)
            .style("text-align","center")
            .style("font-size","150px")
            .style("font-weight","400")
            .style("margin","20px")
            .text(text);
    };

    var next = function(new_context) {
        document.getElementById("conversation").innerHTML += new_context + "</br>";
        document.getElementById("user-response").value = "";
        listening = true;
    };

    var get_next_context = function(response) {
        var data = { "conversation_id" : user_id, "response" : null };
        if (context_count < MAX_CONTEXT_COUNT) {
            data.context = "";
        }

        if (response) { // Then submit this response together with the get context request.
            console.log("Submitting response " + response);
            data.response = {
                "id" : current_context_id,
                "data" : response
            };
        }


        var new_context_data = null;
        xhr = new XMLHttpRequest();
        var url = "http://localhost:22222";
        xhr.open("POST", url, false); // Synchronous request. TODO: handle failed requests.
        xhr.setRequestHeader("Content-type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var json = JSON.parse(xhr.responseText);
                console.log(json);
                if (json.hasOwnProperty('context')) {
                    current_context_id = json.context.id;
                    new_context_data = json.context.data;
                    console.log("BBBBBBBBBBBB");
                }
            }
        }
        xhr.send(JSON.stringify(data));

        context_count++;
        console.log(new_context_data);
        return new_context_data;
    };

    var fetch_context = function(response) {
        var new_context = get_next_context(response);
        if (new_context) {
            next(new_context);
        } else {
            finish();
        }
    }

    var response_handler = function(e) {
        if (!listening) return;

        var keyCode = e.keyCode,
            response;

        switch (keyCode) {
            case KeyEvent.DOM_VK_RETURN:
                e.preventDefault(); // So that the new line does not get to insert a new line.
                response =  document.getElementById("user-response").value;
                document.getElementById("conversation").innerHTML += response + "</br>";
                break;
            default:
                response = "";
                break;
        }

        if (response.length>0) {
            listening = false;
            // var hit = response == stim[1];
            // var rt = new Date().getTime() - wordon;

            // psiTurk.recordTrialData({'phase':"TEST",
            //                          'word':stim[0],
            //                          'color':stim[1],
            //                          'relation':stim[2],
            //                          'response':response,
            //                          'hit':hit,
            //                          'rt':rt}
            //                        );
            fetch_context(response);
        }
    };

    // Load the stage.html snippet into the body of the page
    // psiTurk.showPage('stage.html');
    psiTurk.showPage('chat.html');

    // Register the response handler that is defined above to handle any
    // key down events.
    $("#trial").focus().keydown(response_handler);

    // Start the test
    fetch_context(null);
};


/****************
* Questionnaire *
****************/

var Questionnaire = function() {

    var error_message = "<h1>Oops!</h1><p>Something went wrong submitting your HIT. This might happen if you lose your internet connection. Press the button to resubmit.</p><button id='resubmit'>Resubmit</button>";

    record_responses = function() {

        psiTurk.recordTrialData({'phase':'postquestionnaire', 'status':'submit'});

        $('textarea').each( function(i, val) {
            psiTurk.recordUnstructuredData(this.id, this.value);
        });
        $('select').each( function(i, val) {
            psiTurk.recordUnstructuredData(this.id, this.value);
        });

    };

    prompt_resubmit = function() {
        document.body.innerHTML = error_message;
        $("#resubmit").click(resubmit);
    };

    resubmit = function() {
        document.body.innerHTML = "<h1>Trying to resubmit...</h1>";
        reprompt = setTimeout(prompt_resubmit, 10000);

        psiTurk.saveData({
            success: function() {
                clearInterval(reprompt);
                psiTurk.computeBonus('compute_bonus', function(){finish()});
            },
            error: prompt_resubmit
        });
    };

    // Load the questionnaire snippet
    psiTurk.showPage('postquestionnaire.html');
    psiTurk.recordTrialData({'phase':'postquestionnaire', 'status':'begin'});

    $("#next").click(function () {
        record_responses();
        psiTurk.saveData({
            success: function(){
                psiTurk.computeBonus('compute_bonus', function() {
                    psiTurk.completeHIT(); // when finished saving compute bonus, the quit
                });
            },
            error: prompt_resubmit});
    });


};

// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
$(window).load( function(){
    psiTurk.doInstructions(
        instructionPages, // a list of pages you want to display in sequence
        function() { currentview = new StroopExperiment(); } // what you want to do when you are done with instructions
    );
});
