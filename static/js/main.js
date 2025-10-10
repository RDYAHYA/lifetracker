document.addEventListener("DOMContentLoaded", () => {
//  monthly expenses chart
const chartCanvas = document.getElementById('expensesChart');
if (chartCanvas) {
    const labels = JSON.parse(chartCanvas.dataset.labels || '[]');
    const values = JSON.parse(chartCanvas.dataset.values || '[]');

    const data = {
        labels: labels.length ? labels : ["No Data"],
        datasets: [{
            label: "Monthly Expenses ($)",
            data: values.length ? values : [0],
            backgroundColor: 'rgba(128, 0, 128, 0.3)',
            borderColor: 'rgba(75, 0, 130, 1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 6, 
            pointBackgroundColor: 'rgba(75, 0, 130, 1)',
            pointBorderColor: '#fff',
            pointHoverRadius: 8,
            pointHoverBackgroundColor: 'rgba(255, 0, 255, 0.8)',
            pointHoverBorderColor: '#fff'
        }]
    };

    new Chart(chartCanvas.getContext('2d'), { type: 'line', data });
}
});