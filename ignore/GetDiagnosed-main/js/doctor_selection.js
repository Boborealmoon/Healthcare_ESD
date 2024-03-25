

//Start of firebase configure
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

//get specialisation variable
const urlParams = new URLSearchParams(window.location.search);
const pass_variable = urlParams.get('specialisation');
console.log(pass_variable)

//get all data - may not need in final
function readData() {
    console.log('start of read data')
    var itemsRef = firebase.database().ref().child("doctors");
    var tableBody = document.querySelector('#table tbody');
    console.log(document.querySelector('#table tbody'))
    tableBody.innerHTML=`<tr>
                <th>Name</th>
                <th>Clinic Name</th>
                <th>Country</th>
                <th>Specialty</th>
                <th>Availabilty</th>
            </tr>`;

    itemsRef.once('value', function (snapshot) {
    snapshot.forEach(function (item_snapshot) {
    //Create html elements, TRs, TD,s etc.
    var row = document.createElement("tr");
    var col1 = document.createElement("td");
    var col2 = document.createElement("td");
    var col3 = document.createElement("td");
    var col4 = document.createElement("td");
    var col5 = document.createElement("td");
    var button = document.createElement("button")
    //check for avialiabity t/f
    is_avial=item_snapshot.val().available
    let settext=''
    if(is_avial.toUpperCase() ==='T'){
        settext=`<span style="background-color: yellowgreen;"><a href="success.html">Available</a></span>`
    }
    else{
        settext=` <span style="background-color: red;">Not Available</span>`
    }

    //Add data to the new elements.
    col1.innerText = item_snapshot.val().name;
    col2.innerText = item_snapshot.val().clinic;
    col3.innerText = item_snapshot.val().country;
    col4.innerText = item_snapshot.val().specialty;
    col5.innerHTML = settext

    //Append the cells into the row and the row into the table body.
    row.appendChild(col1);
    row.appendChild(col2);
    row.appendChild(col3);
    row.appendChild(col4);
    row.appendChild(col5);


    tableBody.appendChild(row);
});
});

}
async function filter_specialty(){
    var itemsRef = firebase.database().ref().child("doctors");
    var tableBody = document.querySelector('#table tbody');

    // var search_special = document.getElementById('special').value

    tableBody.innerHTML=`<tr>
                    <th>Name</th>
                    <th>Clinic Name</th>
                    <th>Country</th>
                    <th>Specialty</th>
                    <th>Availability</th>
                </tr>`;


        itemsRef.once('value', function (snapshot) {
        snapshot.forEach(function (item_snapshot) {
        for(spec of item_snapshot.val().specialty){
            // console.log(item_snapshot.val().specialty, spec, search_special)
            if(spec == pass_variable){
                // console.log(item_snapshot.val().name)
                //Create html elements, TRs, TD,s etc.
                var row = document.createElement("tr");
                var col1 = document.createElement("td");
                var col2 = document.createElement("td");
                var col3 = document.createElement("td");
                var col4 = document.createElement("td");
                var col5 = document.createElement("td");

                //check for avialiabity t/f
                is_avial=item_snapshot.val().available
                let settext=''
                if(is_avial.toUpperCase() ==='T'){
                    settext=`
                    <input class="btn btn-primary btn-sm" type="submit" value="Available" data-bs-toggle="modal" data-bs-target="#warningModal" id="">
                    `
                }
                else{
                    settext=`<input class="btn btn-danger btn-sm" type="submit" value="Unavailable" " >
                    `
                }
                
                //Add data to the new elements.
                col1.innerText = item_snapshot.val().name;
                col2.innerText = item_snapshot.val().clinic;
                col3.innerText = item_snapshot.val().country;
                col4.innerText = item_snapshot.val().specialty;
                col5.innerHTML = settext

                //Append the cells into the row and the row into the table body.
                row.appendChild(col1);
                row.appendChild(col2);
                row.appendChild(col3);
                row.appendChild(col4);
                row.appendChild(col5);


                tableBody.appendChild(row);
            }

        }


    });
}
);

}