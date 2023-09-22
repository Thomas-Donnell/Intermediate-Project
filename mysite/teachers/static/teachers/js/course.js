const btnDiv = document.getElementById('addstudents');
const courseDiv = document.getElementById('coursediv');
const tagWrapper = document.getElementById('tagwrapper')

// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    tagWrapper.style.display = 'none';
    courseDiv.style.display = 'flex';
});
