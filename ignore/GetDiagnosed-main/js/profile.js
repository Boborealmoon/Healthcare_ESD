function profile(){

    var button_content1 = document.getElementById("edit_profile_btn")
    button_content1.innerHTML = 
    `
        <img src="https://cdn-icons-png.flaticon.com/512/4751/4751751.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-danger border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;"> Profile</button>
    `

    var button_content2 = document.getElementById("consults_btn")
    button_content2.innerHTML = 
    `
        <img src="https://cdn-icons-png.flaticon.com/512/5351/5351119.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-white border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;">Consults</button>
    `

    var button_content3 = document.getElementById("med_hist_btn")
    button_content3.innerHTML = 
    `   
        <img src="https://cdn-icons-png.flaticon.com/512/10299/10299454.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-white border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;">Medical History</button>
    `

    var button_content5 = document.getElementById("past_prescriptions_btn")
    button_content5.innerHTML = 
    `   
        <img src="https://cdn-icons-png.flaticon.com/512/6599/6599288.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-white border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;">Past Prescriptions</button>
    `


    var change_content = document.getElementById("change_content")
    change_content.innerHTML = 
    `
        <div class="row g-3 mx-3 mt-3" style="font-size: 18px; padding: 0; margin: auto;">
            <h1 style="margin-bottom: 10px;">Profile</h1>

            <div class="col-md-5">
                <p>Username</p>
                <p>Hyunbinhubby</p>
            </div>
            <div class="col-md-5">
                <p>Email</p>
                <p>taepyung@gmail.com</p>
            </div>
            <div class="col-md-2">
                
            </div>


            <div class="col-md-5">
                <p>Name</p>
                <p>Kim Tae Pyung</p>
            </div>
            <div class="col-md-5">
                <p>Gender</p>
                <p>Male</p>
            </div>
            <div class="col-md-2">
                
            </div>


            <div class="col-md-5">
                <p>Nationality</p>
                <p>South Korean</p>
            </div>
            <div class="col-md-5">
                <p>Date of Birth</p>
                <p>25 September 1982</p>
            </div>
            <div class="col-md-2">
                
            </div>


            <div class="col-md-5">
                <p>Country, City</p>
                <p>South Korea, Seoul</p>
            </div>
            <div class="col-md-5">
                <p>Phone Number</p>
                <p>+82 1-910-2755</p>
            </div>
            <div class="col-md-2">
                
            </div>

        
            <div class="col-md-6">
                <p>Address</p>
                <p>288-8, Sajeong-dong</p>
            </div>

        </div>
    `
}


function consults(){

    var button_content1 = document.getElementById("edit_profile_btn")
    button_content1.innerHTML = 
    `
        <img src="https://cdn-icons-png.flaticon.com/512/4751/4751751.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-white border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;"> Profile</button>
    `

    var button_content2 = document.getElementById("consults_btn")
    button_content2.innerHTML = 
    `
        <img src="https://cdn-icons-png.flaticon.com/512/5351/5351119.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-danger border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;">Consults</button>
    `

    var button_content3 = document.getElementById("med_hist_btn")
    button_content3.innerHTML = 
    `   
        <img src="https://cdn-icons-png.flaticon.com/512/10299/10299454.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-white border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;">Medical History</button>
    `

    var button_content5 = document.getElementById("past_prescriptions_btn")
    button_content5.innerHTML = 
    `   
        <img src="https://cdn-icons-png.flaticon.com/512/6599/6599288.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-white border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;">Past Prescriptions</button>
    `

    

    var change_content = document.getElementById("change_content")
    change_content.innerHTML =
    `
        <div class="row g-3 mx-3 mt-3">
            <h1 style="margin-bottom: 10px;" id="content_header">Consults</h1>
            <p> Edit the rest below </p>
        </div>
    `
}


function medical_history(){

    var button_content1 = document.getElementById("edit_profile_btn")
    button_content1.innerHTML = 
    `
        <img src="https://cdn-icons-png.flaticon.com/512/4751/4751751.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-white border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;"> Profile</button>
    `

    var button_content2 = document.getElementById("consults_btn")
    button_content2.innerHTML = 
    `
        <img src="https://cdn-icons-png.flaticon.com/512/5351/5351119.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-white border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;">Consults</button>
    `

    var button_content3 = document.getElementById("med_hist_btn")
    button_content3.innerHTML = 
    `   
        <img src="https://cdn-icons-png.flaticon.com/512/10299/10299454.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-danger border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;">Medical History</button>
    `


    var button_content5 = document.getElementById("past_prescriptions_btn")
    button_content5.innerHTML = 
    `   
        <img src="https://cdn-icons-png.flaticon.com/512/6599/6599288.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-white border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;">Past Prescriptions</button>
    `


    var change_content = document.getElementById("change_content")
    change_content.innerHTML =
    `
        <div class="row g-3 mx-3 mt-3">
            <h1 style="margin-bottom: 10px;" id="content_header">Medical History</h1>
            <p> Edit the rest below </p>
        </div>
    `
}


function past_prescriptions(){

    var button_content1 = document.getElementById("edit_profile_btn")
    button_content1.innerHTML = 
    `
        <img src="https://cdn-icons-png.flaticon.com/512/4751/4751751.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-white border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;"> Profile</button>
    `

    var button_content2 = document.getElementById("consults_btn")
    button_content2.innerHTML = 
    `
        <img src="https://cdn-icons-png.flaticon.com/512/5351/5351119.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-white border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;">Consults</button>
    `

    var button_content3 = document.getElementById("med_hist_btn")
    button_content3.innerHTML = 
    `   
        <img src="https://cdn-icons-png.flaticon.com/512/10299/10299454.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-white border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;">Medical History</button>
    `

    var button_content5 = document.getElementById("past_prescriptions_btn")
    button_content5.innerHTML = 
    `   
        <img src="https://cdn-icons-png.flaticon.com/512/6599/6599288.png" alt="personal_icon" class="img-fluid align-middle" style="height: 40px; width: 40px; margin-right: 10px;">
        <button type="button" class="btn btn-danger border border-0 btn-block m-0 p-2" style="width:auto; font-size:18px; text-align: left;">Past Prescriptions</button>
    `

    var change_content = document.getElementById("change_content")
    change_content.innerHTML =
    `
        <div class="row g-3 mx-3 mt-3">
            <h1 style="margin-bottom: 10px;" id="content_header">Past Prescriptions</h1>
            <p> Edit the rest below </p>
        </div>
    `
}



