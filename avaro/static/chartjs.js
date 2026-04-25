// Variabel global untuk menyimpan instance chart
let myChartInstance = null;

function initDashboardChart() {
    const ctxElement = document.getElementById('myChart');

    // 1. Cek apakah elemen canvas ada. Jika tidak ada, hentikan fungsi.
    if (!ctxElement) return;

    // 2. PENTING: Jika chart sudah ada sebelumnya, hancurkan dulu
    // Ini mencegah error "Canvas is already in use" saat HTMX merefresh konten
    if (myChartInstance) {
        myChartInstance.destroy();
    }

    const ctx = ctxElement.getContext('2d');

    let gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(13, 110, 253, 0.5)');
    gradient.addColorStop(1, 'rgba(13, 110, 253, 0.0)');

    const labelsElement = document.getElementById('json-chart-labels');
    const dataAB2Element = document.getElementById('json-oms-ab2');
    const dataAB3Element = document.getElementById('json-oms-ab3');
    const dataAB4Element = document.getElementById('json-oms-ab4');

    // Default Data
    let chartLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
    let omsAB2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    let omsAB3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    let omsAB4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    // Parsing data dari Django template (jika ada)
    try {
        if (labelsElement && labelsElement.textContent !== "null") {
            const rawLabels = JSON.parse(labelsElement.textContent);
            
            // Ubah format Uppercase (JAN 2025) menjadi Title Case (Jan 2025)
            chartLabels = rawLabels.map(label => {
                // Pastikan label string, lalu lowercase semua, lalu uppercase huruf pertama tiap kata
                return String(label).toLowerCase().replace(/\b\w/g, char => char.toUpperCase());
            });
        }
        if (dataAB2Element && dataAB2Element.textContent !== "null") {
            omsAB2 = JSON.parse(dataAB2Element.textContent);
        }
        if (dataAB3Element && dataAB3Element.textContent !== "null") {
            omsAB3 = JSON.parse(dataAB3Element.textContent);
        }
        if (dataAB4Element && dataAB4Element.textContent !== "null") {
            omsAB4 = JSON.parse(dataAB4Element.textContent);
        }
    } catch (e) {
        console.error("Gagal parsing data chart dari Django:", e);
    }

    // 3. Render Chart Baru dan simpan ke variabel instance
    myChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartLabels, // Gunakan variabel dinamis
            datasets: [{
                label: '11-AB2',
                data: omsAB2, // Masih dummy sesuai kode asli Anda
                borderColor: '#FFC000',
                borderWidth: 2,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: '#FFC000',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                tension: 0.4
            },{
                label: '31-AB3',
                data: omsAB3,
                borderColor: '#0000FF',
                borderWidth: 2,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: '#0000FF',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                tension: 0.4
            },{
                label: '32-AB4',
                data: omsAB4,
                borderColor: '#33CCCC',
                borderWidth: 2,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: '#33CCCC',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, 
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(33, 37, 41, 0.9)',
                    padding: 10,
                    callbacks: {
                        label: function(context) {
                            let value = context.parsed.y;
                            let formattedValue = value.toLocaleString('id-ID', {
                                minimumFractionDigits: 0, 
                                maximumFractionDigits: 0
                            });
                            return context.dataset.label + ' : Rp ' + formattedValue;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#f0f0f0', borderDash: [5, 5] },
                    border: { display: false }
                },
                x: {
                    grid: { display: false },
                    border: { display: false }
                }
            },
            interaction: {
                mode: 'index',
                intersect: false,
            },
        }
    });
}

// Event Listener 1: Jalankan saat halaman pertama kali load (fallback)
document.addEventListener('DOMContentLoaded', initDashboardChart);

// Event Listener 2: Jalankan setiap kali HTMX selesai melakukan swap konten
document.body.addEventListener('htmx:afterSwap', function(event) {
    // Jalankan fungsi inisialisasi ulang
    initDashboardChart();
});