$(document).ready(function () {
    // Toggle the menu when the "closemenu" icon is clicked
    $("#closemenu").click(function () {
        $("#menu-link ul").toggleClass("active");
        $(this).toggleClass("active");
    });
});

// Get references to the topbar and header elements
const topbar = document.getElementById('topbar');
const header = document.querySelector('header');

// Get the height of the topbar
const topbarHeight = topbar.clientHeight;

// Function to update header position
function updateHeaderPosition() {
  if (window.scrollY > topbarHeight) {
    header.style.position = 'fixed';
    header.style.top = '0';
  } else {
    header.style.position = 'sticky';
  }
}

// Attach a scroll event listener to update header position
window.addEventListener('scroll', updateHeaderPosition);

// Initialize the header position
updateHeaderPosition();
