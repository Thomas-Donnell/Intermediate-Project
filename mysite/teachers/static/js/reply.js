const backDiv = document.getElementById('backbtn');

// Add a click event listener to the trigger div
backDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    window.history.back();
});


const btnDiv = document.getElementById('reply-btn');
const courseDiv = document.getElementById('coursediv');
const postWrapper = document.getElementById('post-wrapper');
// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseDiv.style.display = 'flex';
    postWrapper.style.display = 'none';
});