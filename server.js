const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const os = require('os');
const fs = require('fs');
const path = require('path');
const http = require('http');
const WebSocket = require('ws');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// Configuration
const RESULTS_DIR = path.join(__dirname, 'results');
const LOGS_DIR = path.join(__dirname, 'logs');

// Create directories if they don't exist
if (!fs.existsSync(RESULTS_DIR)) fs.mkdirSync(RESULTS_DIR);
if (!fs.existsSync(LOGS_DIR)) fs.mkdirSync(LOGS_DIR);

// Global benchmark state
let benchmarkState = {
  running: false,
  progress: 0,
  currentTest: '',
  results: null,
  startTime: null,
  error: null
};

let clients = [];

// WebSocket connections
wss.on('connection', (ws) => {
  clients.push(ws);
  
  ws.on('close', () => {
    clients = clients.filter(client => client !== ws);
  });
});

function broadcastStatus() {
  clients.forEach(ws => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(benchmarkState));
    }
  });
}

// Benchmark Functions
function benchmarkCPU() {
  const iterations = 100000;
  const start = Date.now();
  let result = 0;
  
  for (let i = 0; i < iterations; i++) {
    result += Math.pow(i, 2);
  }
  
  const elapsed = (Date.now() - start) / 1000;
  return {
    cpu_performance: iterations / elapsed,
    cpu_time: elapsed
  };
}

function benchmarkMemory() {
  const results = {};
  const sizes = [1024 * 1024 * 5]; // 5 MB
  
  sizes.forEach(size => {
    const start = Date.now();
    const arr = new Array(size).fill(0).map((_, i) => Math.random());
    const elapsed = (Date.now() - start) / 1000;
    results[`memory_allocation_${size / (1024 * 1024)}mb`] = elapsed;
  });
  
  return results;
}

function benchmarkFileOperations() {
  const results = {};
  
  try {
    // Test file creation time
    const testDir = path.join(RESULTS_DIR, `test_${Date.now()}`);
    if (!fs.existsSync(testDir)) fs.mkdirSync(testDir);
    
    const start = Date.now();
    for (let i = 0; i < 50; i++) {
      fs.writeFileSync(path.join(testDir, `file_${i}.txt`), `Test file ${i}`);
    }
    const elapsed = (Date.now() - start) / 1000;
    results.file_creation_time = elapsed;
    
    // Cleanup
    fs.rmSync(testDir, { recursive: true });
  } catch (e) {
    console.error('File benchmark error:', e);
  }
  
  return results;
}

function benchmarkNetwork() {
  // Simulate network latency
  return {
    network_latency: Math.random() * 100,
    network_throughput: Math.random() * 1000
  };
}

function benchmarkSecurity() {
  const crypto = require('crypto');
  const data = Buffer.alloc(1024 * 1024 * 5); // 5 MB
  
  const results = {};
  
  const algorithms = ['md5', 'sha256'];
  algorithms.forEach(algo => {
    const start = Date.now();
    const hash = crypto.createHash(algo);
    hash.update(data);
    hash.digest();
    const elapsed = (Date.now() - start) / 1000;
    results[`${algo}_throughput`] = (5 / elapsed).toFixed(2); // MB/s
  });
  
  return results;
}

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/api/system-info', (req, res) => {
  try {
    const systemInfo = {
      os: os.platform(),
      arch: os.arch(),
      cpus: os.cpus().length,
      totalMemory: (os.totalmem() / 1024 / 1024 / 1024).toFixed(2) + ' GB',
      freeMemory: (os.freemem() / 1024 / 1024 / 1024).toFixed(2) + ' GB',
      hostname: os.hostname(),
      uptime: os.uptime(),
      timestamp: new Date().toISOString()
    };
    res.json(systemInfo);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/benchmarks/status', (req, res) => {
  res.json(benchmarkState);
});

app.post('/api/benchmarks/start', (req, res) => {
  if (benchmarkState.running) {
    return res.status(400).json({ error: 'Benchmarks already running' });
  }
  
  // Start benchmarks asynchronously
  runBenchmarks();
  res.json({ message: 'Benchmarks started' });
});

app.get('/api/benchmarks/results', (req, res) => {
  if (!benchmarkState.results) {
    return res.status(404).json({ error: 'No results available' });
  }
  res.json(benchmarkState.results);
});

app.get('/api/benchmarks/history', (req, res) => {
  try {
    const files = fs.readdirSync(RESULTS_DIR).filter(f => f.endsWith('.json'));
    const history = files.map(file => {
      const filePath = path.join(RESULTS_DIR, file);
      const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      return {
        timestamp: file,
        results: data
      };
    });
    res.json(history);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/benchmarks/export', (req, res) => {
  if (!benchmarkState.results) {
    return res.status(404).json({ error: 'No results available' });
  }
  
  const filename = `benchmark_${Date.now()}.json`;
  const filepath = path.join(RESULTS_DIR, filename);
  
  try {
    fs.writeFileSync(filepath, JSON.stringify(benchmarkState.results, null, 2));
    res.json({ message: 'Results exported', filename });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/benchmarks/download/:filename', (req, res) => {
  const filepath = path.join(RESULTS_DIR, req.params.filename);
  
  if (!fs.existsSync(filepath)) {
    return res.status(404).json({ error: 'File not found' });
  }
  
  res.download(filepath);
});

// Benchmark execution
async function runBenchmarks() {
  benchmarkState.running = true;
  benchmarkState.progress = 0;
  benchmarkState.results = null;
  benchmarkState.startTime = Date.now();
  benchmarkState.error = null;
  
  const results = {
    systemInfo: {
      os: os.platform(),
      arch: os.arch(),
      cpus: os.cpus().length,
      timestamp: new Date().toISOString()
    },
    benchmarks: {}
  };
  
  try {
    // CPU Benchmark
    benchmarkState.currentTest = '🧠 CPU Benchmarks';
    benchmarkState.progress = 10;
    broadcastStatus();
    await sleep(500);
    results.benchmarks.cpu = benchmarkCPU();
    
    // Memory Benchmark
    benchmarkState.currentTest = '💾 Memory Benchmarks';
    benchmarkState.progress = 30;
    broadcastStatus();
    await sleep(500);
    results.benchmarks.memory = benchmarkMemory();
    
    // File Operations
    benchmarkState.currentTest = '📁 File System Benchmarks';
    benchmarkState.progress = 50;
    broadcastStatus();
    await sleep(500);
    results.benchmarks.files = benchmarkFileOperations();
    
    // Network
    benchmarkState.currentTest = '🌐 Network Benchmarks';
    benchmarkState.progress = 70;
    broadcastStatus();
    await sleep(500);
    results.benchmarks.network = benchmarkNetwork();
    
    // Security
    benchmarkState.currentTest = '🔒 Security Benchmarks';
    benchmarkState.progress = 90;
    broadcastStatus();
    await sleep(500);
    results.benchmarks.security = benchmarkSecurity();
    
    // Save results
    const filename = `results_${Date.now()}.json`;
    fs.writeFileSync(
      path.join(RESULTS_DIR, filename),
      JSON.stringify(results, null, 2)
    );
    
    benchmarkState.results = results;
    benchmarkState.progress = 100;
    benchmarkState.currentTest = '✅ مكتمل';
    
  } catch (error) {
    benchmarkState.error = error.message;
    console.error('Benchmark error:', error);
  } finally {
    benchmarkState.running = false;
    broadcastStatus();
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Error handling
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: err.message });
});

app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

// Server startup
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});

module.exports = app;
