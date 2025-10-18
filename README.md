# Deep Work Session Tracker

A comprehensive system for planning, tracking, and managing focused work sessions with interruption management and productivity analytics.

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd deepwork-session-tracker

# 2. Run automated setup (Windows)
setupdev.bat

# 3. Start the application
runapplication.bat

# 4. Open http://localhost:3000 in your browser
```

**That's it!** 🎉 The application will be running with both backend and frontend.

## 🎯 Overview

The Deep Work Session Tracker helps you maintain focus and track productivity by providing tools to:
- Plan work sessions with specific goals and durations
- Start, pause, resume, and complete sessions
- Track interruptions and their reasons
- Analyze productivity patterns and session history
- Generate comprehensive reports

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations

### Frontend
- **React 18** - Modern React with hooks
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Tailwind CSS** - Utility-first CSS framework

### Development Tools
- **pytest** - Testing framework
- **OpenAPI Generator** - Auto-generate Python SDK
- **Uvicorn** - ASGI server for FastAPI

## 📁 Project Structure

```
deepwork/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for API validation
│   ├── crud.py              # Database operations
│   ├── database.py          # Database configuration
│   ├── routers/
│   │   └── sessions.py      # Session API endpoints
│   └── tests/
│       └── test_sessions.py # Comprehensive test suite
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── api.js          # API client
│   │   └── App.jsx         # Main app component
│   └── package.json        # Frontend dependencies
├── alembic/                # Database migrations
├── deepwork_sdk/           # Auto-generated Python SDK
├── setupdev.bat           # Development setup script
├── runapplication.bat     # Application startup script
├── generate_sdk.py        # SDK generation script
└── requirements.txt       # Python dependencies
```

## 🚀 How to Run the Project

### Prerequisites
- **Python 3.8+** (Download from [python.org](https://python.org))
- **Node.js 16+** (Download from [nodejs.org](https://nodejs.org))
- **Git** (Download from [git-scm.com](https://git-scm.com))

### Method 1: Quick Start (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd deepwork-session-tracker
   ```

2. **Run the automated setup:**
   ```bash
   # Windows
   setupdev.bat
   
   # Linux/Mac
   chmod +x setupdev.sh
   ./setupdev.sh
   ```

3. **Start the application:**
   ```bash
   # Windows
   runapplication.bat
   
   # Linux/Mac
   chmod +x runapplication.sh
   ./runapplication.sh
   ```

4. **Access the application:**
   - 🌐 **Frontend**: http://localhost:3000
   - 🔧 **Backend API**: http://localhost:8000
   - 📚 **API Documentation**: http://localhost:8000/docs

### Method 2: Manual Setup

#### Step 1: Backend Setup

1. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv env
   env\Scripts\activate
   
   # Linux/Mac
   python3 -m venv env
   source env/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database:**
   ```bash
   alembic upgrade head
   ```

4. **Start the backend server:**
   ```bash
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### Step 2: Frontend Setup

1. **Open a new terminal and navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend development server:**
   ```bash
   npm start
   ```

### Method 3: Using Docker (Optional)

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

### 🎯 First Time Usage

1. **Open your browser** and go to http://localhost:3000
2. **Create your first session:**
   - Enter a title (max 50 characters)
   - Describe your goal (max 200 characters)
   - Set duration (1-240 minutes)
3. **Start working:**
   - Click "Start Session" to begin
   - Use "Pause" if interrupted (with reason)
   - Click "Resume" to continue
   - Click "Complete" when done

### 🔧 Troubleshooting

#### Backend Issues
- **Port 8000 in use**: Change port in `backend/main.py` or kill process using port 8000
- **Database errors**: Run `alembic upgrade head` to apply migrations
- **Import errors**: Ensure virtual environment is activated

#### Frontend Issues
- **Port 3000 in use**: React will automatically suggest an alternative port
- **API connection failed**: Ensure backend is running on port 8000
- **Build errors**: Delete `node_modules` and run `npm install` again

#### General Issues
- **Permission denied**: Use `chmod +x` on shell scripts (Linux/Mac)
- **Python not found**: Add Python to PATH or use `python3` instead of `python`
- **Node not found**: Install Node.js from [nodejs.org](https://nodejs.org)

### 📊 Verify Everything is Working

1. **Check backend health:**
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status":"healthy"}
   ```

2. **Check API documentation:**
   - Visit http://localhost:8000/docs
   - You should see the Swagger UI with all endpoints

3. **Test frontend:**
   - Visit http://localhost:3000
   - You should see the Deep Work Session Tracker interface

### 🚀 Production Deployment

For production deployment:

1. **Build frontend:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Set production database:**
   ```bash
   export DATABASE_URL="postgresql://user:pass@localhost/deepwork"
   ```

3. **Run with production server:**
   ```bash
   gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## 📊 Features

### Session Management
- **Create Sessions**: Plan work with title, goal, and duration
- **Start Sessions**: Begin focused work periods
- **Pause/Resume**: Handle interruptions with reason tracking
- **Complete Sessions**: Finish work and get status analysis

### Smart Status Detection
The system automatically determines session status based on behavior:
- **Completed**: Normal completion within expected timeframe
- **Interrupted**: More than 3 pauses during session
- **Overdue**: Duration exceeds 110% of scheduled time
- **Abandoned**: Paused but never resumed

### Analytics & Reporting
- Session history with detailed statistics
- Productivity metrics and trends
- Interruption analysis
- Focus score calculations

## 🔧 API Documentation

### Core Endpoints

#### Sessions
- `POST /api/v1/sessions/` - Create new session
- `GET /api/v1/sessions/{id}` - Get specific session
- `PATCH /api/v1/sessions/{id}/start` - Start session
- `PATCH /api/v1/sessions/{id}/pause` - Pause session (requires reason)
- `PATCH /api/v1/sessions/{id}/resume` - Resume session
- `PATCH /api/v1/sessions/{id}/complete` - Complete session
- `GET /api/v1/sessions/history` - Get session history with statistics

### Example API Usage

```python
import requests

# Create a session
session_data = {
    "title": "Write documentation",
    "goal": "Complete API documentation",
    "scheduled_duration": 45.0
}
response = requests.post("http://localhost:8000/api/v1/sessions/", json=session_data)
session = response.json()

# Start the session
requests.patch(f"http://localhost:8000/api/v1/sessions/{session['id']}/start")

# Pause with reason
requests.patch(f"http://localhost:8000/api/v1/sessions/{session['id']}/pause", 
               json={"reason": "Phone call"})

# Resume
requests.patch(f"http://localhost:8000/api/v1/sessions/{session['id']}/resume")

# Complete
requests.patch(f"http://localhost:8000/api/v1/sessions/{session['id']}/complete")
```

## 🐍 Python SDK

The project includes an auto-generated Python SDK for easy integration:

### Generate SDK
```bash
python generate_sdk.py
```

### Use SDK
```python
from deepwork_sdk.api.sessions_api import SessionsApi
from deepwork_sdk import ApiClient

# Initialize client
client = ApiClient(host="http://localhost:8000")
api = SessionsApi(client)

# Create and manage sessions
session = api.create_session({
    "title": "Deep work session",
    "goal": "Complete important task",
    "scheduled_duration": 60.0
})

api.start_session(session.id)
api.pause_session(session.id, {"reason": "Break"})
api.resume_session(session.id)
api.complete_session(session.id)
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest backend/tests/

# Run with coverage
pytest backend/tests/ --cov=backend

# Run specific test file
pytest backend/tests/test_sessions.py -v
```

### Test Coverage
- Session state transitions
- Interruption logic validation
- Overdue/abandoned detection
- API endpoint functionality
- Error handling scenarios

## 📈 Business Logic

### Session States
1. **Planned** → **Active** (start)
2. **Active** → **Paused** (pause with reason)
3. **Paused** → **Active** (resume)
4. **Active/Paused** → **Completed/Interrupted/Overdue/Abandoned** (complete)

### Status Determination
- **Interrupted**: >3 pauses during session
- **Overdue**: Actual duration > 110% of scheduled duration
- **Abandoned**: Paused but never resumed before completion
- **Completed**: Normal completion within expected parameters

## 🎨 Frontend Features

### Dashboard
- Create new sessions
- Control active sessions (start/pause/resume/complete)
- Real-time timer for active sessions
- Recent sessions overview

### History Page
- Complete session history
- Productivity statistics
- Interruption analysis
- Session details and status

### UI/UX
- Modern, responsive design
- Real-time updates
- Error handling and validation
- Intuitive session controls

## 🔄 Database Schema

### Sessions Table
- `id` - Primary key
- `title` - Session title
- `goal` - Session objective
- `scheduled_duration` - Planned duration (minutes)
- `start_time` - When session started
- `end_time` - When session ended
- `status` - Current session status
- `created_at` - Creation timestamp

### Interruptions Table
- `id` - Primary key
- `session_id` - Foreign key to sessions
- `reason` - Reason for interruption
- `pause_time` - When interruption occurred

## 🚀 Deployment

### Production Setup
1. Set up production database (PostgreSQL recommended)
2. Configure environment variables
3. Run migrations: `alembic upgrade head`
4. Build frontend: `cd frontend && npm run build`
5. Serve with production ASGI server (Gunicorn + Uvicorn)

### Environment Variables
- `DATABASE_URL` - Database connection string
- `API_HOST` - Backend host (default: 0.0.0.0)
- `API_PORT` - Backend port (default: 8000)
- `FRONTEND_URL` - Frontend URL for CORS

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Future Enhancements

- **Real-time Collaboration**: Multi-user session tracking
- **Focus Score Algorithm**: Advanced productivity metrics
- **CSV Export**: Data export capabilities
- **Weekly Reports**: Automated productivity summaries
- **Mobile App**: React Native mobile application
- **Integration APIs**: Connect with calendar and task management tools
- **Advanced Analytics**: Machine learning insights
- **Team Dashboards**: Manager-level productivity views

## 🐛 Troubleshooting

### Common Issues

1. **Backend won't start**: Check if port 8000 is available
2. **Frontend won't connect**: Verify backend is running and CORS is configured
3. **Database errors**: Run `alembic upgrade head` to apply migrations
4. **SDK generation fails**: Ensure backend is running before generating SDK

### Support

For issues and questions:
- Check the API documentation at `/docs`
- Review test cases for usage examples
- Check logs for detailed error messages

---

**Built with ❤️ for productivity and focus**
