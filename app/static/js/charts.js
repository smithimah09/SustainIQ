

document.addEventListener('DOMContentLoaded', function() {
    // Helper to safely get chart contexts
    function getChartContext(id) {
        const canvas = document.getElementById(id);
        return canvas ? canvas.getContext('2d') : null;
    }

    // Parse JSON data from the page
    function parseDataFromPage(variableName, fallback) {
        try {
            if (window[variableName] && typeof window[variableName] === 'object') {
                return window[variableName];
            }
            return fallback;
        } catch (e) {
            console.error('Error parsing ' + variableName + ':', e);
            return fallback;
        }
    }

    // Utility to safely access object properties
    function safeGet(obj, key, defaultValue = 0) {
        return obj && obj[key] !== undefined ? obj[key] : defaultValue;
    }

    // Create category chart
    const categoryCtx = getChartContext('categoryChart');
    if (categoryCtx) {
        const categories = [
            { name: 'Energy Conservation', key: 'energy', color: '#28a745' },
            { name: 'Waste Reduction', key: 'waste', color: '#17a2b8' },
            { name: 'Sustainable Transport', key: 'transport', color: '#007bff' },
            { name: 'Sustainable Food', key: 'food', color: '#fd7e14' },
            { name: 'Water Conservation', key: 'water', color: '#6f42c1' },
            { name: 'Other', key: 'other', color: '#6c757d' }
        ];

        const categoryCounts = parseDataFromPage('categoryCounts', {});

        new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: categories.map(c => c.name),
                datasets: [{
                    data: categories.map(c => safeGet(categoryCounts, c.key)),
                    backgroundColor: categories.map(c => c.color),
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Create progress chart
    const progressCtx = getChartContext('progressChart');
    if (progressCtx) {
        const dailyActions = parseDataFromPage('dailyActions', []);

        new Chart(progressCtx, {
            type: 'line',
            data: {
                labels: dailyActions.map(d => d.date),
                datasets: [{
                    label: 'Actions',
                    data: dailyActions.map(d => d.count),
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    borderWidth: 3,
                    tension: 0.3,
                    fill: true,
                    pointBackgroundColor: '#ffffff',
                    pointBorderColor: '#28a745',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            precision: 0
                        },
                        grid: {
                            display: true,
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.7)',
                        padding: 10,
                        cornerRadius: 6,
                        caretSize: 6,
                        displayColors: false,
                        callbacks: {
                            title: function(tooltipItems) {
                                return tooltipItems[0].label;
                            },
                            label: function(context) {
                                const value = context.raw;
                                return `${value} action${value !== 1 ? 's' : ''}`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Animate the stat cards
    const statsCards = document.querySelectorAll('.col-md-4 .card');
    if (statsCards.length) {
        statsCards.forEach(card => {
            const valueEl = card.querySelector('.card-text');
            if (valueEl) {
                const value = parseInt(valueEl.textContent, 10);
                if (!isNaN(value)) animateCounter(valueEl, 0, value, 1000);
            }
        });
    }

    // Counter animation helper
    function animateCounter(element, start, end, duration) {
        let startTime = null;
        const step = timestamp => {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            const currentValue = Math.floor(progress * (end - start) + start);
            element.textContent = currentValue;
            if (progress < 1) window.requestAnimationFrame(step);
        };
        window.requestAnimationFrame(step);
    }
});
