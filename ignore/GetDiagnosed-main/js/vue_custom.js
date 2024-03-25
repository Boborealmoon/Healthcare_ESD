var app = Vue.createApp({

    data(){
        return{
            specialty_list:[
                
                "Obstetrics and Gynecology",
                "Cardiology",
                "Love therapy",
                "Heart Mending",
                "Surgery",
                "Gastroenterology",
                "Psychiatry",
                "Neurology",
                "Forensic Medicine",
                "Internal Medicine",
                "Plastic Surgery",
                "Orthopedics",
                "Pediatrics",
                "Emergency Medicine",
                "Family Medicine"
            ],

        selected_specialisation:'test',
        }
        
    }


})
app.mount("#patient_form")