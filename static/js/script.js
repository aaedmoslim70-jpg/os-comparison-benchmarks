const API_BASE = '/api';
let statusCheckInterval = null;

// Load system info on page load
document.addEventListener('DOMContentLoaded', function() {
    loadSystemInfo();
});

function loadSystemInfo() {
    fetch(`${API_BASE}/system-info`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('os-name').textContent = data.os;
            document.getElementById('processor').textContent = data.processor || 'غير متوفر';
            document.getElementById('architecture').textContent = data.architecture;
            document.getElementById('python-version').textContent = data.python_version;
            document.getElementById('platform').textContent = data.platform;
            document.getElementById('timestamp').textContent = new Date(data.timestamp).toLocaleString('ar-SA');
        })
        .catch(error => console.error('خطأ:', error));
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
                currentTest.textContent = `جاري اختبار: ${status.current_test}`;

                if (status.progress >= 100 && !status.running) {
                    clearInterval(statusCheckInterval);
                    setTimeout(displayResults, 1000);
                }
            })
            .catch(error => console.error('خطأ:', error));
    }, 500);
}

function displayResults() {
    fetch(`${API_BASE}/benchmarks/results`)
        .then(response => response.json())
        .then(data => {
            // Display results
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
        .catch(error => console.error('خطأ:', error));
}

function displayMemoryResults(data) {
    const container = document.getElementById('memory-results');
    container.innerHTML = '';

    const metrics = [
        { label: 'سرعة تخصيص الذاكرة', key: 'memory_allocation_time', unit: 'ms', multiply: 1000 },
        { label: 'الوصول المتسلسل', key: 'memory_sequential_access', unit: 'ms', multiply: 1000 },
        { label: 'الوصول العشوائي', key: 'memory_random_access', unit: 'ms', multiply: 1000 },
        { label: 'أداء CPU', key: 'cpu_performance', unit: 'ops/sec', multiply: 1 },
        { label: 'متوسط الذاكرة', key: 'avg_memory', unit: 'MB', multiply: 1 },
        { label: 'ذروة الذاكرة', key: 'peak_memory', unit: 'MB', multiply: 1 }
    ];

    metrics.forEach(metric => {
        if (data[metric.key] !== undefined) {
            const value = (data[metric.key] * metric.multiply).toFixed(2);
            container.innerHTML += `
                <div class="metric-card">
                    <div class="label">${metric.label}</div>
                    <div class="value">${value}<span class="unit">${metric.unit}</span></div>
                </div>
            `;
        }
    });
}

function displayProcessResults(data) {
    const container = document.getElementById('process-results');
    container.innerHTML = '';

    const metrics = [
        { label: 'وقت إنشاء العمليات', key: 'process_creation_time', unit: 's', multiply: 1 },
        { label: 'تبديلات السياق', key: 'context_switches', unit: 'switches', multiply: 1 },
        { label: 'وقت إنشاء الخيوط', key: 'thread_creation_time', unit: 's', multiply: 1 }
    ];

    metrics.forEach(metric => {
        if (data[metric.key] !== undefined) {
            const value = typeof data[metric.key] === 'number' ? data[metric.key].toFixed(4) : data[metric.key];
            container.innerHTML += `
                <div class="metric-card">
                    <div class="label">${metric.label}</div>
                    <div class="value">${value}<span class="unit">${metric.unit}</span></div>
                </div>
            `;
        }
    });
}

function displayFilesystemResults(data) {
    const container = document.getElementById('filesystem-results');
    container.innerHTML = '';

    const metrics = [
        { label: 'وقت إنشاء الملفات', key: 'file_creation_time', unit: 's', multiply: 1 },
        { label: 'وقت قراءة الملفات', key: 'file_read_time', unit: 's', multiply: 1 },
        { label: 'إنتاجية الكتابة', key: 'file_write_throughput', unit: 'MB/s', multiply: 1 },
        { label: 'وقت إنشاء المجلدات', key: 'directory_creation_time', unit: 's', multiply: 1 }
    ];

    metrics.forEach(metric => {
        if (data[metric.key] !== undefined) {
            const value = typeof data[metric.key] === 'number' ? data[metric.key].toFixed(2) : data[metric.key];
            container.innerHTML += `
                <div class="metric-card">
                    <div class="label">${metric.label}</div>
                    <div class="value">${value}<span class="unit">${metric.unit}</span></div>
                </div>
            `;
        }
    });
}

function displaySecurityResults(data) {
    const container = document.getElementById('security-results');
    container.innerHTML = '';

    const metrics = [
        { label: 'MD5 Throughput', key: 'hash_md5_throughput', unit: 'MB/s', multiply: 1 },
        { label: 'SHA256 Throughput', key: 'hash_sha256_throughput', unit: 'MB/s', multiply: 1 },
        { label: 'SHA512 Throughput', key: 'hash_sha512_throughput', unit: 'MB/s', multiply: 1 },
        { label: 'عمليات التشفير', key: 'encryption_ops_per_sec', unit: 'ops/sec', multiply: 1 }
    ];

    metrics.forEach(metric => {
        if (data[metric.key] !== undefined) {
            const value = typeof data[metric.key] === 'number' ? data[metric.key].toFixed(2) : data[metric.key];
            container.innerHTML += `
                <div class="metric-card">
                    <div class="label">${metric.label}</div>
                    <div class="value">${value}<span class="unit">${metric.unit}</span></div>
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
