// START OF PASSWORD FUNCTIONS
const togglePassword = document.querySelector("#togglePassword");
const togglePassword2 = document.querySelector("#togglePassword2");
const password = document.querySelector("#password");
const confirmpassword = document.querySelector("#confirmpassword");

togglePassword2.addEventListener("click", function () {
    // toggle the type attribute
    const type = confirmpassword.getAttribute("type") === "password" ? "text" : "password";
    confirmpassword.setAttribute("type", type);
    
    // toggle the icon
    this.classList.toggle("bi-eye");
});

togglePassword.addEventListener("click", function () {
    // toggle the type attribute
    const type = password.getAttribute("type") === "password" ? "text" : "password";
    password.setAttribute("type", type);
    
    // toggle the icon
    this.classList.toggle("bi-eye");
});



// prevent form submit
const form = document.querySelector("form");
form.addEventListener('submit', function (e) {
    e.preventDefault();
});


function validateregister(){
    var username = document.getElementById("username").value
    var password = document.getElementById("password").value
    var confpassword = document.getElementById("confirmpassword").value
    var email = document.getElementById("email").value
    var code = document.getElementById("code").value
    var number = document.getElementById("number").value
    var day = document.getElementById("day").value
    var month = document.getElementById("month").value
    var year = document.getElementById("year").value

    var errormessage = []
    
    if(username.length < 8){
        errormessage.push("Username must have more than 8 characters!")
    }
    if(password != confpassword){
        errormessage.push("Passwords do not match!")
    }
    if(password.length < 8){
        errormessage.push("Passwords must have more than 8 characters!")
    }
    if(!containsSpecialChars(password)){
        errormessage.push("Password must contain at least one special character! (!@#$%^&*)")
    }
    if(!containsNumber(password)){
        errormessage.push("Password must contain at least one number (0-9)")
    }
    if(!containsUppercase(password)){
        errormessage.push("Password must contain at least one Uppercase character (A-Z)")
    }
    if(!containsLowercase(password)){
        errormessage.push("Password must contain at least one Lowercase character (a-z)")
    }
    if(!email.includes("@")){
        errormessage.push("Email is Invalid")
    }
    if(!code.includes("+")){
        errormessage.push("Please include (+) in Country Code")
    }
    if(number.length < 7 || !containsOnlyNumbers(number)){
        errormessage.push("Invalid Contact Number")
    }
    if(day.length != 2 || month.length != 2 || year.length != 4 || !containsOnlyNumbers(day) || !containsOnlyNumbers(month) || !containsOnlyNumbers(year)){
        errormessage.push("Invalid Date of Birth (dd/mm/yyyy)")
    }
    if(!document.getElementById("registration").checkValidity()){
        errormessage.push("Please fill in required fields!")
    }
    if(errormessage.length > 0){
        var text = document.getElementById("errormessage")
        var str = `Please change accordingly :D<br>
        `
        console.log(errormessage != [])
        
        for(i=0;i<errormessage.length;i++){
            str += `${i+1}. ${errormessage[i]} <br>`
        }
        text.innerHTML = str
    }
    else{
        register(username,confpassword)
        console.log("registering")
        var text = document.getElementById("errormessage")
        var title = document.getElementById("staticBackdropLabel")
        text.innerHTML = "Do click on the Close button to get to Log In Page"
        title.innerHTML = "Successful Registration"
        document.getElementById("tologin").href= "login_patient.html"
        document.getElementById("registration").reset()
    }
}

function containsSpecialChars(str) {
    const specialChars = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
    return specialChars.test(str);
}

function containsNumber(str) {
    return /\d/.test(str);
}

function containsUppercase(str) {
    return /[A-Z]/.test(str);
}
function containsLowercase(str) {
    return /[a-z]/.test(str);
}
function containsOnlyNumbers(str) {
    return /^\d+$/.test(str);
}

const firebaseConfig = {
    apiKey: "AIzaSyD9ouBle0s4OAyamcvXrmjKRpHrSXc_unI",
    authDomain: "firebasics-281dd.firebaseapp.com",
    projectId: "fiitemsRefrebasics-281dd",
    storageBucket: "firebasics-281dd.appspot.com",
    messagingSenderId: "941290209708",
    appId: "1:941290209708:web:93f3bf62c88882e40afa09",
    measurementId: "G-YWMCHYLBS7",
    databaseURL: "https://firebasics-281dd-default-rtdb.asia-southeast1.firebasedatabase.app/"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

function register(user, pw){

    console.log('====Start Register====')
    firebase.database().ref('accounts/' + user).set({
    username: user,//adding the details into the database, format--> column name: variable
    password:pw
    })
    console.log('====End Register====')

}
async function login(user, pw){
    //return bool t/f 
    // await as config with firebase is slower than process
    login_success=false

    var acctsRef = firebase.database().ref().child("accounts")
    
       await acctsRef.once('value', function (snapshot) {
            snapshot.forEach(function (acct_snapshot) {
            // console.log(user, acct_snapshot.val().username)
                if(user == acct_snapshot.val().username && pw == acct_snapshot.val().password)
                    login_success = true
        
                })
            })
            // console.log(login_success)
            return login_success
}
