//Script that changes E-Mail Stuff for each method
const EMAIL_TITLE = "Email Content:";
const REVIEW_TITLE = "Review Content:";
const EMAIL_PREVIEW = "Type your email here!";
const REVIEW_PREVIEW = "Type your review here!";

// End of Constants

var email_enter = document.getElementById("email-enter");
var email_text = document.getElementById("email-text");
var rating = document.getElementById("rating");
var form_check = document.getElementById("anonymous-form");
var sub_button = document.getElementById("SubmitEmailButton");
var textarea = document.getElementById("email-textarea");

var breaks = document.getElementsByClassName("breakPage");

function updateForm() { //function that updates the form (css values :))
    val = document.getElementById("FormControlSelect1").value;
    if (val == "-- Choose Contact Method --"){
        email_enter.style.display = "none";
        email_text.style.display = "none";
        document.getElementById("inputSubject").setAttribute("value", "");
        document.getElementById("inputEmail").setAttribute("value", "");
        document.getElementById("inputName").setAttribute("value", "");
        document.getElementById("email-textarea").innerHTML = "";
        rating.style.display = "none";
        document.getElementById("check1").disabled = true;
        sub_button.disabled = true;
        document.getElementById("emailHelpSubtext").innerHTML = "Choose the contact method that fits your use case."

        references = document.getElementsByClassName("breakPage");
        for (var i = 0; i < 3; i++){
            if (i == 1){
                references[i].style.display = "block";
            } else {
                references[i].style.display = "none";
            }
        }
    }
    else if (val == "webfeedback"){
        email_enter.style.display = "none";
        email_text.style.display = "block";
        rating.style.display = "block";
        document.getElementById("check1").disabled = true;
        sub_button.disabled = false;
        document.getElementById("emailHelpSubtext").innerHTML = "Choose the contact method that fits your use case."

        email_text.children[0].innerHTML = REVIEW_TITLE;
        email_text.children[1].setAttribute("placeholder", REVIEW_PREVIEW);

        references = document.getElementsByClassName("breakPage");
        for (var i = 0; i < 3; i++){
            if (i == 0 || i == 1){
                references[i].style.display = "block";
            } else {
                references[i].style.display = "block";
            }
        }
    }
    else if (val == "stucofeedback"){
        email_enter.style.display = "block";
        email_text.style.display = "block";
        rating.style.display = "block";
        document.getElementById("check1").disabled = false;
        sub_button.disabled = false;
        document.getElementById("emailHelpSubtext").innerHTML = "Choose the contact method that fits your use case."

        email_text.children[0].innerHTML = REVIEW_TITLE;
        email_text.children[1].setAttribute("placeholder", REVIEW_PREVIEW);

        references = document.getElementsByClassName("breakPage");
        for (var i = 0; i < 3; i++){
            if (i == 0 || i == 1){
                references[i].style.display = "block";
            } else {
                references[i].style.display = "block";
            }
        }
    }
    else if (val == "srhighstuco"){
        email_enter.style.display = "block";
        email_text.style.display = "block";
        rating.style.display = "none";
        document.getElementById("check1").disabled = false;
        sub_button.disabled = false;
        document.getElementById("emailHelpSubtext").innerHTML = "This method will send your email to the advisor and secretary for Sr High Student Council"

        email_text.children[0].innerHTML = EMAIL_TITLE;
        email_text.children[1].setAttribute("placeholder", EMAIL_PREVIEW);

        references = document.getElementsByClassName("breakPage");
        for (var i = 0; i < 3; i++){
            if (i == 0 || i == 1){
                references[i].style.display = "block";
            } else {
                references[i].style.display = "none";
            }
        }
    }
    else if (val == "jrhighstuco"){
        email_enter.style.display = "block";
        email_text.style.display = "block";
        rating.style.display = "none";
        document.getElementById("check1").disabled = false;
        sub_button.disabled = false;
        document.getElementById("emailHelpSubtext").innerHTML = "This method will send your email to the advisor for Jr High Student Council"

        email_text.children[0].innerHTML = EMAIL_TITLE;
        email_text.children[1].setAttribute("placeholder", EMAIL_PREVIEW);

        references = document.getElementsByClassName("breakPage");
        for (var i = 0; i < 3; i++){
            if (i == 0 || i == 1){
                references[i].style.display = "block";
            } else {
                references[i].style.display = "none";
            }
        }
    }
    else if (val == "bugreports"){
        email_enter.style.display = "none";
        email_text.style.display = "block";
        rating.style.display = "none";
        document.getElementById("check1").disabled = true;
        sub_button.disabled = false;
        document.getElementById("emailHelpSubtext").innerHTML = "This method will store your bug report to be fixed!"

        email_text.children[0].innerHTML = "Bug Fix:";
        email_text.children[1].setAttribute("placeholder", "Type a description and recreation attempt of the bug here...");

        references = document.getElementsByClassName("breakPage");
        for (var i = 0; i < 3; i++){
            if (i == 0 || i == 1){
                references[i].style.display = "block";
            } else {
                references[i].style.display = "none";
            }
        }
    }
}

function validateForm() {
    function errorIt(msg){
        close[0].parentElement.style.transition = "0.1s linear";
        close[0].parentElement.style.backgroundColor = "#f44336";
        close[0].parentElement.style.opacity = "0.8";
        close[0].parentElement.style.display = "block";
        document.getElementById("AlertMessage").innerHTML = msg;
    }

    var close = document.getElementsByClassName("closebtn");
    var validRegex = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

    let email = document.forms["FeedbackForm"]["email"].value;
    let subject = document.forms["FeedbackForm"]["subject"].value;
    let nickname = document.forms["FeedbackForm"]["nickname"].value;
    let emailContent = document.forms["FeedbackForm"]["emailContent"].value;
    let rating = document.forms["FeedbackForm"]["rating"].value;
    let contactMethod = document.forms["FeedbackForm"]["contactMethod"].value;

    if (contactMethod == "-- Choose Contact Method --"){
        errorIt("Please choose a contact method!");
        return false;
    } if (validRegex.test(email) == false) {
        if (contactMethod == "jrhighstuco" || contactMethod == "srhighstuco" || contactMethod == "stucofeedback") {
            errorIt("Email address is not valid!");
            return false;
        }
    } if (email.length <= 0){
        if (contactMethod == "jrhighstuco" || contactMethod == "srhighstuco" || contactMethod == "stucofeedback") {
            errorIt("Email address is required!!!");
            return false;
        }
    } if (emailContent.length <= 20) {
        errorIt("Content within Email/Feedback should be longer than 20 characters!!!")
        return false
    } if (emailContent.length >= 3000) {
        errorIt("Content within Email/Feedback cannot exceed 2000 characters!!!")
        return false
    }
  }

updateForm(); //inits website (not fast :()