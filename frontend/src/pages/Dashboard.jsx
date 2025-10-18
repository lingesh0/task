import React, { useState, useEffect } from 'react';
import SessionForm from '../components/SessionForm';
import SessionControls from '../components/SessionControls';
import { sessionsAPI } from '../api';

const Dashboard = () => {
  const [sessions, setSessions] = useState([]);
  const [activeSession, setActiveSession] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      setIsLoading(true);
      const data = await sessionsAPI.getSessionHistory();
      setSessions(data.sessions);
      
      // Find the most recent active or planned session
      const active = data.sessions.find(s => 
        s.status === 'active' || s.status === 'paused' || s.status === 'planned'
      );
      setActiveSession(active || null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch sessions');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSessionCreated = (newSession) => {
    setSessions(prev => [newSession, ...prev]);
    if (!activeSession) {
      setActiveSession(newSession);
    }
  };

  const handleSessionUpdated = (updatedSession) => {
    setSessions(prev => 
      prev.map(s => s.id === updatedSession.id ? updatedSession : s)
    );
    setActiveSession(updatedSession);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-md text-center max-w-md">
          <div className="text-red-600 mb-4">
            <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            <p className="text-lg font-semibold">Error Loading Dashboard</p>
            <p className="text-sm text-gray-600 mt-2">{error}</p>
          </div>
          <button
            onClick={fetchSessions}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Deep Work Session Tracker</h1>
          <p className="text-gray-600">Plan, track, and complete focused work sessions</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Session Management */}
          <div className="space-y-6">
            {/* Create New Session */}
            <SessionForm onSessionCreated={handleSessionCreated} />
            
            {/* Active Session Controls */}
            <SessionControls 
              session={activeSession} 
              onSessionUpdated={handleSessionUpdated}
            />
          </div>

          {/* Right Column - Recent Sessions */}
          <div className="bg-white rounded-lg shadow-md">
            <div className="p-6 border-b">
              <h2 className="text-2xl font-bold">Recent Sessions</h2>
            </div>
            <div className="divide-y divide-gray-200">
              {sessions.slice(0, 5).map((session) => (
                <div key={session.id} className="p-4 hover:bg-gray-50">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="font-semibold">{session.title}</h3>
                      <p className="text-sm text-gray-600 mt-1 line-clamp-2">{session.goal}</p>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      session.status === 'completed' ? 'bg-green-100 text-green-800' :
                      session.status === 'active' ? 'bg-blue-100 text-blue-800' :
                      session.status === 'paused' ? 'bg-yellow-100 text-yellow-800' :
                      session.status === 'interrupted' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {session.status}
                    </span>
                  </div>
                  <div className="mt-2 text-sm text-gray-500">
                    {session.scheduled_duration} min • {new Date(session.created_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
            {sessions.length === 0 && (
              <div className="p-6 text-center text-gray-500">
                No sessions yet. Create your first session to get started!
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
