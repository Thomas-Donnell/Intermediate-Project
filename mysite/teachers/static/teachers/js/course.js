const btnDiv = document.getElementById('addstudents');
const gradeDiv = document.getElementById('grades-link');
const courseGradesDiv = document.getElementById('coursediv-grades');
const courseDiv = document.getElementById('coursediv');
const tagWrapper = document.getElementById('tagwrapper')

// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    tagWrapper.style.display = 'none';
    courseDiv.style.display = 'flex';
});

gradeDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseGradesDiv.style.display = 'flex';
    content.style.display = 'none';
});

const closeBtn = document.getElementById('close');

closeBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseGradesDiv.style.display = 'none';
    content.style.display = 'block';
});

const divs = document.querySelectorAll('.grades');

// Add a click event listener to each div
divs.forEach(function(div) {
    div.addEventListener('click', function() {
        // Your event handling code here
        courseId = div.getAttribute('data-class-courseId');
        studentId = div.getAttribute('data-class-studentId');
        window.location.href = `/teachers/student_view/${courseId}/${studentId}/`;
    });
});