const API_BASE = '/api';
let statusCheckInterval = null;

// تحميل معلومات النظام عند فتح الصفحة
document.addEventListener('DOMContentLoaded', function() {
    loadSystemInfo();
});

function loadSystemInfo() {
    fetch(`${API_BASE}/system-info`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('os-name').textContent = data.os || 'غير متوفر';
            document.getElementById('processor').textContent = data.processor || 'غير متوفر';
            document.getElementById('architecture').textContent = data.architecture || 'غير متوفر';
            document.getElementById('python-version').textContent = data.python_version || 'غير متوفر';
            document.getElementById('platform').textContent = data.platform || 'غير متوفر';
            document.getElementById('timestamp').textContent = new Date(data.timestamp).toLocaleString('ar-SA');
        })
        .catch(error => {
            console.error('خطأ:', error);
            document.getElementById('os-name').textContent = 'خطأ في الحصول على البيانات';
        });
}

function startBenchmarks() {
    const startBtn = document.getElementById('start-btn');
    startBtn.disabled = true;
    startBtn.innerHTML = '<span class="icon loading">⏳</span> جاري الاختبار...';

    fetch(`${API_BASE}/benchmarks/start`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('progress-section').style.display = 'block';
        startProgressMonitoring();
    })
    .catch(error => {
        console.error('خطأ:', error);
        startBtn.disabled = false;
        startBtn.innerHTML = '<span class="icon">▶️</span> بدء الاختبارات';
        alert('حدث خطأ: ' + error);
    });
}

function startProgressMonitoring() {
    if (statusCheckInterval) clearInterval(statusCheckInterval);
    
    statusCheckInterval = setInterval(function() {
        fetch(`${API_BASE}/benchmarks/status`)
            .then(response => response.json())
            .then(status => {
                const progressFill = document.getElementById('progress-fill');
                const progressPercent = document.getElementById('progress-percent');
                const currentTest = document.getElementById('current-test');

                progressFill.style.width = status.progress + '%';
                progressFill.textContent = status.progress + '%';
                progressPercent.textContent = status.progress + '%';
                currentTest.textContent = `▶️ جاري: ${status.current_test}`;

                if (status.progress >= 100 && !status.running) {
                    clearInterval(statusCheckInterval);
                    setTimeout(displayResults, 500);
                }
            })
            .catch(error => console.error('خطأ في المراقبة:', error));
    }, 500);
}

function displayResults() {
    fetch(`${API_BASE}/benchmarks/results`)
        .then(response => response.json())
        .then(data => {
            displayMemoryResults(data.benchmarks.memory);
            displayProcessResults(data.benchmarks.processes);
            displayFilesystemResults(data.benchmarks.filesystem);
            displaySecurityResults(data.benchmarks.security);

            document.getElementById('results-section').style.display = 'block';
            document.getElementById('export-btn').disabled = false;

            const startBtn = document.getElementById('start-btn');
            startBtn.disabled = false;
            startBtn.innerHTML = '<span class="icon">▶️</span> بدء الاختبارات';
        })
        .catch(error => {
            console.error('خطأ:', error);
            alert('لم يتم الحصول على النتائج');
        });
}

function displayMemoryResults(data) {
    const container = document.getElementById('memory-results');
    container.innerHTML = '';

    const metrics = [
        { label: '⚡ أداء CPU (ops/sec)', key: 'cpu_performance', format: (v) => v.toFixed(0) },
        { label: '💾 متوسط الذاكرة (MB)', key: 'avg_memory', format: (v) => v.toFixed(2) },
        { label: '📊 ذروة الذاكرة (MB)', key: 'peak_memory', format: (v) => v.toFixed(2) },
        { label: '⏱️ وقت تخصيص الذاكرة (ms)', key: 'memory_allocation_time', format: (v) => (v * 1000).toFixed(2) }
    ];

    metrics.forEach(metric => {
        if (data[metric.key] !== undefined && data[metric.key] !== null) {
            const value = metric.format(data[metric.key]);
            container.innerHTML += `
                <div class="metric-card">
                    <div class="label">${metric.label}</div>
                    <div class="value">${value}</div>
                </div>
            `;
        }
    });
}

function displayProcessResults(data) {
    const container = document.getElementById('process-results');
    container.innerHTML = '';

    const metrics = [
        { label: '⚙️ وقت إنشاء العمليات (s)', key: 'process_creation_time', format: (v) => v.toFixed(4) },
        { label: '🧵 وقت إنشاء الخيوط (s)', key: 'thread_creation_time', format: (v) => v.toFixed(4) }
    ];

    metrics.forEach(metric => {
        if (data[metric.key] !== undefined && data[metric.key] !== null) {
            const value = metric.format(data[metric.key]);
            container.innerHTML += `
                <div class="metric-card">
                    <div class="label">${metric.label}</div>
                    <div class="value">${value}</div>
                </div>
            `;
        }
    });
}

function displayFilesystemResults(data) {
    const container = document.getElementById('filesystem-results');
    container.innerHTML = '';

    const metrics = [
        { label: '📁 وقت إنشاء الملفات (s)', key: 'file_creation_time', format: (v) => v.toFixed(4) },
        { label: '✍️ سرعة الكتابة (MB/s)', key: 'file_write_throughput', format: (v) => v.toFixed(2) }
    ];

    metrics.forEach(metric => {
        if (data[metric.key] !== undefined && data[metric.key] !== null) {
            const value = metric.format(data[metric.key]);
            container.innerHTML += `
                <div class="metric-card">
                    <div class="label">${metric.label}</div>
                    <div class="value">${value}</div>
                </div>
            `;
        }
    });
}

function displaySecurityResults(data) {
    const container = document.getElementById('security-results');
    container.innerHTML = '';

    const metrics = [
        { label: '🔐 MD5 (MB/s)', key: 'hash_md5_throughput', format: (v) => v.toFixed(2) },
        { label: '🔐 SHA256 (MB/s)', key: 'hash_sha256_throughput', format: (v) => v.toFixed(2) },
        { label: '🔑 عمليات التشفير (ops/sec)', key: 'encryption_ops_per_sec', format: (v) => v.toFixed(0) }
    ];

    metrics.forEach(metric => {
        if (data[metric.key] !== undefined && data[metric.key] !== null) {
            const value = metric.format(data[metric.key]);
            container.innerHTML += `
                <div class="metric-card">
                    <div class="label">${metric.label}</div>
                    <div class="value">${value}</div>
                </div>
            `;
        }
    });
}

function exportResults() {
    fetch(`${API_BASE}/benchmarks/results`)
        .then(response => response.json())
        .then(data => {
            const element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(data, null, 2)));
            element.setAttribute('download', `benchmark_results_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`);
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
        })
        .catch(error => console.error('خطأ:', error));
}
