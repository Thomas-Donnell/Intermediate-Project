const btnDiv = document.getElementById('addstudents');
const courseDiv = document.getElementById('coursediv');

// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseDiv.style.display = 'flex';
});
