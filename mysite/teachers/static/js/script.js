// Get references to the trigger and target divs
const btnDiv = document.getElementById('addbtn');
const courseDiv = document.getElementById('coursediv');


// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseDiv.style.display = 'block';
});

const divs = document.querySelectorAll('.cards');

// Add a click event listener to each div
divs.forEach(function(div) {
    div.addEventListener('click', function() {
        // Your event handling code here
        courseId = div.getAttribute('data-class-id');
        window.location.href = `course/${courseId}/`;
    });
});