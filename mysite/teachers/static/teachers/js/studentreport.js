const content = document.getElementById('content')
var studentId = content.getAttribute('data-class-studentId');
var labels = [];  // Course names
var dataValues = [];  // Percentiles

function createPieChart(labels, data) {
    var ctx = document.getElementById('myBarChart').getContext('2d');

    var myBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Percentile',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(255, 255, 99, 0.7)',
                    'rgba(99, 255, 132, 0.7)',
                    'rgba(99, 132, 255, 0.7)',
                    'rgba(255, 99, 255, 0.7)',
                ],
            }],
        },
    });
    return myBarChart;
}

fetch('/teachers/student_report/' + studentId + '/', {
    headers: {
        'X-Requested-With': 'XMLHttpRequest'
    }
})
.then(response => response.json())
.then(data => {
    data.forEach(grade => {
        labels.push(grade.course_name);
        dataValues.push(grade.percentile);
    });
    createPieChart(labels, dataValues);
})
.catch(error => console.error('Error fetching data:', error));

// Event listener for window resize
window.addEventListener('resize', function () {
    // Redraw all charts when the window is resized
    createPieChart(labels, dataValues);
});