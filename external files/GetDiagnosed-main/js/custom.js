// Start of ChatBot
function openForm() {
    document.getElementById("chatbot-popup").style.display = "block";
    document.getElementById("chatbot").style.display = "none";
}
  
function closeForm() {
    document.getElementById("chatbot-popup").style.display = "none";
    document.getElementById("chatbot").style.display = "block";
}

(function() {
    var textsubmit = document.getElementById('textsubmit');
    textsubmit.addEventListener('keypress', function(event) {
        var enter = event.keyCode
        if (enter == 13 && !event.shiftKey) {
            event.preventDefault()
            document.getElementById('send').click()
        }
    });
}());


async function message() {
    // get the resposes from call_chatgpt, varibale save as an array
    var user_input = document.getElementById('textsubmit').value
    let str_responses_innerhtml = await call_chatgpt(user_input)

    // console.log(str_responses_innerhtml)
    display_all_response(str_responses_innerhtml, user_input)
    
}
function display_all_response(str_responses_innerhtml,user_input){
// display of responses from user input and chatgpt response

    //first entry into chatbot
    if (typeof str == 'undefined'){
        str = ``
        str += `<div class="bg bg-white border border-danger" style="border-radius:5px;font-size:12px" id="spacing"><span style="font-weight:bold">Guest:</span> <br>${user_input}</div>`
        str += 
        `
        <div class="bg bg-white border border-danger" style="border-radius:5px; font-size:12px" id="spacing">
            <span><span style="font-weight:bold">Botty:</span><br> ${str_responses_innerhtml}</span>
        </div>
        `
        console.log(str_responses_innerhtml)
        document.getElementById('chatlog').style.display = "block"
        document.getElementById('chatlog').innerHTML = str
        document.getElementById('textsubmit').value = ""; 
    }
    //following entries into chatbot
    else{
        str += `<div class="bg bg-white border border-danger" style="border-radius:5px;font-size:12px" id="spacing"><span style="font-weight:bold">Guest:</span> <br>${user_input}</div>`
        str += 
        `
        <div class="bg bg-white border border-danger" style="border-radius:5px; font-size:12px" id="spacing">
            <span><span style="font-weight:bold">Botty:</span><br> ${str_responses_innerhtml}</span>
        </div>
        `
        console.log(str_responses_innerhtml)
        document.getElementById('chatlog').style.display = "block"
        document.getElementById('chatlog').innerHTML = str
        document.getElementById('textsubmit').value = ""; 
    }
}

async function call_chatgpt(user_input){
    let api_endpoint_url = "https://api.openai.com/v1/chat/completions"
    const encodedString = "V1hwS2VtUkdTa2xhU0ZKVFVtc3dlbGt6Y0U5aFJsWkZWVlJXVDFKVWJIZFZWRXAzVFVkTmVGWnNWazVOUlhCNlYxY3hNRkl4VG5GUmJrcFdUVEJ3UTFsV1drdE9SbXhZVkZoa1UySllhRTlWTWpFelpWZEdWVlpzWXowPQ=="
    const halfDecoded = atob(atob(encodedString))
    
    try {
     console.log("Getting GPT chat...")
     const data = {
      model: 'gpt-3.5-turbo',
      messages: [
          {
              role: 'system',
              content: 'You are as pre doctor check that allow users to type in symptoms. You will show basic reccomendations for the symptoms. Keep only 3 short recomendations  and in a list'
          },
          {
              role: 'user',
              content: user_input
          }
      ]
    };

    const requestOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + atob(atob(halfDecoded))
        },
    };

    // Get chat GPT response
    const res = await axios.post(api_endpoint_url, data, requestOptions)
    var ai_responses_split = (res.data.choices[0].message.content).split('\n')
    var setstr = ''
    // console.log('---------------------before----------------')
    // console.log(message)
    for(let i = 0; i<ai_responses_split.length;i++){
        if(ai_responses_split[i]==''){        
        }
        else{
            let input_text = ai_responses_split[i]
            setstr+= input_text + `<br>`
        }
    }
  return  setstr
 } catch (error) {
  console.log(error.message)
 }
}

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



