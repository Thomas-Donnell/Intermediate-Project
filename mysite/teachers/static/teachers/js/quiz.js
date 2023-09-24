const btnDiv = document.getElementById('grades-link');
const courseDiv = document.getElementById('coursediv');
const content = document.getElementById('content');
// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseDiv.style.display = 'flex';
    content.style.display = 'none';
});

const closeBtn = document.getElementById('close');

closeBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseDiv.style.display = 'none';
    content.style.display = 'block';
});

const deleteBtn = document.getElementById('delete-btn');
deleteBtn.addEventListener('click', function() {
    courseId = deleteBtn.getAttribute('data-class-courseId');
    id = deleteBtn.getAttribute('data-class-id');
    window.location.href = `/teachers/delete_quiz/${id}/${courseId}/`;
});