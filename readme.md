# Cloud-Synced Eye Tracker

![Logo](backend/image.png)

## Project Overview

The Eye Tracker is a comprehensive solution designed to monitor users' eye-blink patterns to promote digital wellness in workplace environments. This application helps users track their blink frequency—an important indicator of eye strain during computer use—and provides analytics through a secure web dashboard.

The project consists of three main components:
1. **Cross-Platform Desktop App**: PyQt-based application for real-time blink tracking
2. **Cloud Backend & Database**: AWS-hosted backend for data storage and API
3. **Web Platform**: React-based dashboard for data visualization

---

## Architecture Diagram

```
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│                   │     │                   │     │                   │
│  Desktop App      │     │  Cloud Backend    │     │  Web Dashboard    │
│  (PyQt)           │◄─┬─►│  (AWS EB/RDS)     │◄────┤  (React/Vercel)   │
│                   │  │  │                   │     │                   │
└───────────────────┘  │  └───────────────────┘     └───────────────────┘
                       │
                       │  ┌───────────────────┐
                       └──┤  Offline Storage  │
                          │  (Local Cache)    │
                          └───────────────────┘
```

### Data Flow:
1. Desktop app captures eye blinks using computer vision (mediapipe)
2. Data is securely sent to AWS backend via authenticated API calls
3. Data is stored in PostgreSQL database (AWS RDS)
4. Web dashboard fetches data via secure API endpoints
5. During offline periods, data is locally cached and synced when connection is restored

---

## Components

### 1. Cross-Platform Desktop Application

#### Technologies
- **Framework**: PyQt5
- **Computer Vision**: Mediapipe
- **Packaging**: PyInstaller (Windows)

#### Features
- **Modern UI**: Minimalist black, white, and gray interface
- **Real-time Blink Tracking**: Integration with mediapipe for accurate eye tracking
- **User Authentication**: Secure login system with cloud verification
- **Performance Monitoring**: Real-time CPU usage, memory usage, and power consumption
- **GDPR Compliance**: Explicit consent collection and privacy controls
- **Offline Support**: Local caching when network connection is unavailable

#### Screenshots
![home](image.png)
![blink data](image-1.png)
![app login](image-2.png)
![blink count](image-3.png)
### 2. Cloud Backend & Database

#### Technologies
- **Hosting**: AWS Elastic Beanstalk
- **Database**: AWS RDS (PostgreSQL)
- **API Framework**: FastAPI
- **Authentication**: JWT-based token system

#### Database Schema
```
Table: users
- id (PK)
- username
- password_hash
- email
- gdpr_consent
- created_at

Table: blink_data
- id (PK)
- user_id (FK -> users.id)
- blink_count
- timestamp
- session_id
- device_info
```

#### API Endpoints
- `/api/auth/register` - User registration
- `/api/auth/login` - User authentication
- `/api/blinks` - POST blink data
- `/api/blinks/{user_id}` - GET user's blink data (protected)
- `/api/users/me` - GET current user profile

### 3. Web Platform

#### Technologies
- **Framework**: React
- **Hosting**: Vercel
- **Data Visualization**: Chart.js [TBD]
- **State Management**: React Context API
- **Styling**: CSS with responsive design

#### Features
- **Secure Authentication**: JWT-based login system
- **Data Visualization**: Charts showing blink patterns over time [TBD]
- **Responsive Design**: Works across desktop and mobile devices
- **Read-Only Access**: Ensures data integrity
- **Session Management**: Automatic token refresh and secure logout

---

## GDPR Compliance

The Eye Tracker application was designed with privacy and GDPR compliance as core principles:

### Implemented Measures
- **Explicit Consent**: Users must opt-in during registration with a clear consent checkbox[TBD]
- **Data Minimization**: Only necessary data for the service's functionality is collected
- **Right to Access**: Users can view all their data through the dashboard
- **Data Portability**: Export functionality for user data [TBD]
- **Secure Storage**: All personal data is encrypted in transit and at rest
- **Privacy Policy**: Clear documentation of data usage and rights [TBD]

### Future Enhancements (If Given More Time)
- **Right to be Forgotten**: Implementation of account deletion functionality
- **Enhanced Audit Logs**: More comprehensive tracking of data access
- **Automated Data Retention Policies**: Configurable data retention periods
- **Regional Data Storage Options**: EU-specific data centers for European users

---

## Security Measures

The application implements several security best practices:

### Implemented Security Features
- **Authentication**: JWT-based token system with expiration
- **Password Security**: Bcrypt hashing with appropriate work factors
- **API Protection**: All sensitive endpoints require authentication
- **HTTPS**: All communications encrypted in transit
- **Environment Variables**: Secrets and credentials stored securely
- **Input Validation**: All user inputs validated and sanitized
- **Database Security**: Parameterized queries to prevent SQL injection

### Future Security Enhancements (If Given More Time)
- **Two-Factor Authentication**: Additional security layer for user accounts
- **Rate Limiting**: Prevention of brute force attempts
- **IP Filtering**: Unusual access pattern detection
- **Enhanced Logging**: Security event monitoring
- **Regular Security Audits**: Automated vulnerability scanning

---

## Testing Strategy

The project includes comprehensive testing at multiple levels:

### Unit Tests
- Backend API endpoint testing with pytest
- React component testing with Jest

### Integration Tests
- End-to-end API flow testing
- UI interaction testing

### Sample Test Cases
```python
# Backend Test Example
def test_user_authentication():
    response = client.post("/api/auth/login", json={"username": "test", "password": "test"})
    assert response.status_code == 200
    assert "token" in response.json()

# Frontend Test Example
test('renders Blink Tracker heading', () => {
  render(<App />);
  expect(screen.getByText(/Blink Tracker/i)).toBeInTheDocument();
});
```

---

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

### Backend CI/CD
- **Trigger**: Push to `backend/**` or backend.yml
- **Steps**:
  1. Set up Python environment
  2. Install dependencies
  3. Run pytest test suite
  4. Package application
  5. Deploy to AWS Elastic Beanstalk

### Frontend CI/CD
- **Trigger**: Push to `blink-dashboard/**` or blink-dashboard.yml
- **Steps**:
  1. Set up Node.js environment
  2. Install dependencies
  3. Run Jest tests
  4. Deploy to Vercel

### Pipeline Structure
```
.github/
  workflows/
    backend.yml      # Backend deployment workflow
    blink-dashboard.yml  # Frontend deployment workflow
```

---

## Installation Instructions

### Windows Desktop Application
1. Download the latest `.exe` file from the releases page
2. Run the installer
3. Launch the WaW Eye Tracker from your Start Menu

### Development Setup
1. Clone the repository
   ```
   git clone https://github.com/vickypedia-12/eye-blink.git
   cd eye-blink
   ```

2. Set up backend
   ```
   cd backend
   python -m venv myenv
   myenv\Scripts\activate
   pip install -r requirements2.txt
   ```

3. Configure environment variables
   ```
   # Create .env file with:
   DATABASE_URL=postgresql://user:password@host:port/db
   SECRET_KEY=your_secret_key
   ```

4. Set up frontend
   ```
   cd ../blink-dashboard
   npm install
   ```

5. Run locally
   ```
   # Backend
   cd backend
   uvicorn app:app --reload

   # Frontend
   cd ../blink-dashboard
   npm start

   # Desktop App
   cd ..
   python main.py
   ```

---

## Known Limitations

1. **macOS Application**: The macOS version is not currently packaged, signed, or distributed. This remains a future task.

2. **Optional Features Not Implemented**:
   - Device notifications for low blink count
   - Microservice architecture
   - System tray/menu bar integration
   - C++ blink counter optimization
   - Comprehensive testing methodology for different OS versions

---

## Contact

For any questions or feedback, please contact the development team at [vikasmourya54321@gmail.com].

---

## License

This project is proprietary and confidential. All rights reserved.
