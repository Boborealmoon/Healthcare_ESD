


function foo(event){
    document.getElementById("before").style.display = "none"
    document.getElementById("after").style.display = "flex"
}


var submit_btn = document.getElementById("submit-btn")

submit_btn.addEventListener('submit',foo)
