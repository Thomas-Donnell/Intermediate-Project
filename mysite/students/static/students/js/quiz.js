const submitBtn = document.getElementById('submitbtn');
const form = document.getElementById('form');
// Add a click event listener to the trigger div
submitBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    form.submit()
});