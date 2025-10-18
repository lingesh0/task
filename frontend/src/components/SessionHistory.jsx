import React, { useState, useEffect } from 'react';
import { sessionsAPI } from '../api';

const SessionHistory = () => {
  const [history, setHistory] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setIsLoading(true);
      const data = await sessionsAPI.getSessionHistory();
      setHistory(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch session history');
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'planned': return 'bg-gray-100 text-gray-800';
      case 'active': return 'bg-green-100 text-green-800';
      case 'paused': return 'bg-yellow-100 text-yellow-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      case 'interrupted': return 'bg-red-100 text-red-800';
      case 'overdue': return 'bg-orange-100 text-orange-800';
      case 'abandoned': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDuration = (startTime, endTime) => {
    if (!startTime || !endTime) return 'N/A';
    const duration = Math.round((new Date(endTime) - new Date(startTime)) / 1000 / 60);
    return `${duration} min`;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  if (isLoading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-2 text-gray-600">Loading session history...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="text-red-600 text-center">
          <p>{error}</p>
          <button
            onClick={fetchHistory}
            className="mt-2 text-blue-600 hover:text-blue-800 underline"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  if (!history || history.sessions.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md text-center">
        <p className="text-gray-500">No sessions found. Create your first session to get started!</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Statistics */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Session Statistics</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">{history.total_sessions}</div>
            <div className="text-sm text-gray-600">Total Sessions</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">{history.completed_sessions}</div>
            <div className="text-sm text-gray-600">Completed</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-red-600">{history.interrupted_sessions}</div>
            <div className="text-sm text-gray-600">Interrupted</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">{Math.round(history.total_productive_time)}</div>
            <div className="text-sm text-gray-600">Minutes Focused</div>
          </div>
        </div>
        
        <div className="mt-4 grid grid-cols-2 md:grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-orange-600">{history.overdue_sessions}</div>
            <div className="text-sm text-gray-600">Overdue</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-gray-600">{history.abandoned_sessions}</div>
            <div className="text-sm text-gray-600">Abandoned</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-yellow-600">{history.total_interruptions}</div>
            <div className="text-sm text-gray-600">Total Interruptions</div>
          </div>
        </div>
      </div>

      {/* Session List */}
      <div className="bg-white rounded-lg shadow-md">
        <div className="p-6 border-b">
          <h2 className="text-2xl font-bold">Session History</h2>
        </div>
        <div className="divide-y divide-gray-200">
          {history.sessions.map((session) => (
            <div key={session.id} className="p-6 hover:bg-gray-50">
              <div className="flex justify-between items-start mb-2">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold">{session.title}</h3>
                  <p className="text-gray-600 text-sm mt-1">{session.goal}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(session.status)}`}>
                  {session.status.toUpperCase()}
                </span>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 text-sm text-gray-600">
                <div>
                  <span className="font-medium">Scheduled:</span> {session.scheduled_duration} min
                </div>
                <div>
                  <span className="font-medium">Duration:</span> {formatDuration(session.start_time, session.end_time)}
                </div>
                <div>
                  <span className="font-medium">Created:</span> {formatDate(session.created_at)}
                </div>
              </div>

              {session.start_time && (
                <div className="mt-2 text-sm text-gray-600">
                  <span className="font-medium">Started:</span> {formatDate(session.start_time)}
                  {session.end_time && (
                    <>
                      <span className="mx-2">•</span>
                      <span className="font-medium">Ended:</span> {formatDate(session.end_time)}
                    </>
                  )}
                </div>
              )}

              {session.interruptions && session.interruptions.length > 0 && (
                <div className="mt-3">
                  <div className="text-sm font-medium text-gray-700 mb-2">
                    Interruptions ({session.interruptions.length}):
                  </div>
                  <div className="space-y-1">
                    {session.interruptions.map((interruption, index) => (
                      <div key={index} className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                        <div>{interruption.reason}</div>
                        <div className="text-xs text-gray-500">
                          {formatDate(interruption.pause_time)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SessionHistory;
