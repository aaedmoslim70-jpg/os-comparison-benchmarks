# OS Comparison Benchmarks - Node.js Backend

## Heroku Deployment Guide

### Prerequisites
- Heroku CLI installed
- Git repository
- Node.js 18.x

### Steps

1. **Create Heroku App**
```bash
heroku create your-app-name
```

2. **Deploy**
```bash
git push heroku main
```

3. **View Logs**
```bash
heroku logs --tail
```

4. **Open App**
```bash
heroku open
```

## Local Development

```bash
npm install
npm start
```

Visit http://localhost:3000

## Features

- ⚡ Real-time benchmarking
- 📊 Dynamic dashboard
- 💾 Results storage
- 📈 Performance history
- 🔒 Security tests

## API Endpoints

```
GET  /api/system-info          - System information
GET  /api/benchmarks/status    - Current status
POST /api/benchmarks/start     - Start benchmarks
GET  /api/benchmarks/results   - Get results
GET  /api/benchmarks/history   - Get history
POST /api/benchmarks/export    - Export results
```
