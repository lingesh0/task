import React, { useState, useEffect } from 'react';
import { sessionsAPI } from '../api';

const SessionControls = ({ session, onSessionUpdated }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [pauseReason, setPauseReason] = useState('');
  const [showPauseForm, setShowPauseForm] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);

  // Timer effect for active sessions
  useEffect(() => {
    let interval = null;
    if (session?.status === 'active' && session?.start_time) {
      interval = setInterval(() => {
        const now = new Date();
        const start = new Date(session.start_time);
        setElapsedTime(Math.floor((now - start) / 1000));
      }, 1000);
    } else {
      setElapsedTime(0);
    }
    return () => clearInterval(interval);
  }, [session]);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleAction = async (action) => {
    setIsLoading(true);
    setError('');

    try {
      let updatedSession;
      switch (action) {
        case 'start':
          updatedSession = await sessionsAPI.startSession(session.id);
          break;
        case 'pause':
          if (!pauseReason.trim()) {
            setError('Please provide a reason for pausing');
            setIsLoading(false);
            return;
          }
          updatedSession = await sessionsAPI.pauseSession(session.id, pauseReason);
          setPauseReason('');
          setShowPauseForm(false);
          break;
        case 'resume':
          updatedSession = await sessionsAPI.resumeSession(session.id);
          break;
        case 'complete':
          updatedSession = await sessionsAPI.completeSession(session.id);
          break;
        default:
          throw new Error('Invalid action');
      }
      onSessionUpdated(updatedSession);
    } catch (err) {
      setError(err.response?.data?.detail || `Failed to ${action} session`);
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

  if (!session) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md text-center">
        <p className="text-gray-500">No active session</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h2 className="text-2xl font-bold">{session.title}</h2>
          <p className="text-gray-600 mt-1">{session.goal}</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(session.status)}`}>
          {session.status.toUpperCase()}
        </span>
      </div>

      <div className="mb-6">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>Scheduled: {session.scheduled_duration} minutes</span>
          {session.status === 'active' && (
            <span>Elapsed: {formatTime(elapsedTime)}</span>
          )}
        </div>
        
        {session.status === 'active' && (
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-1000"
              style={{ 
                width: `${Math.min(100, (elapsedTime / 60 / session.scheduled_duration) * 100)}%` 
              }}
            ></div>
          </div>
        )}
      </div>

      {error && (
        <div className="text-red-600 text-sm bg-red-50 p-3 rounded-md mb-4">
          {error}
        </div>
      )}

      <div className="space-y-3">
        {session.status === 'planned' && (
          <button
            onClick={() => handleAction('start')}
            disabled={isLoading}
            className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
          >
            {isLoading ? 'Starting...' : 'Start Session'}
          </button>
        )}

        {session.status === 'active' && (
          <>
            <button
              onClick={() => setShowPauseForm(true)}
              disabled={isLoading}
              className="w-full bg-yellow-600 text-white py-2 px-4 rounded-md hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 disabled:opacity-50"
            >
              Pause Session
            </button>
            <button
              onClick={() => handleAction('complete')}
              disabled={isLoading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              Complete Session
            </button>
          </>
        )}

        {session.status === 'paused' && (
          <>
            <button
              onClick={() => handleAction('resume')}
              disabled={isLoading}
              className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
            >
              Resume Session
            </button>
            <button
              onClick={() => handleAction('complete')}
              disabled={isLoading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              Complete Session
            </button>
          </>
        )}

        {showPauseForm && (
          <div className="border-t pt-4">
            <div className="mb-3">
              <label htmlFor="pauseReason" className="block text-sm font-medium text-gray-700 mb-1">
                Reason for pausing:
              </label>
              <input
                type="text"
                id="pauseReason"
                value={pauseReason}
                onChange={(e) => setPauseReason(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                placeholder="e.g., Phone call, urgent email"
              />
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => handleAction('pause')}
                disabled={isLoading || !pauseReason.trim()}
                className="flex-1 bg-yellow-600 text-white py-2 px-4 rounded-md hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 disabled:opacity-50"
              >
                {isLoading ? 'Pausing...' : 'Confirm Pause'}
              </button>
              <button
                onClick={() => {
                  setShowPauseForm(false);
                  setPauseReason('');
                }}
                className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>

      {session.interruptions && session.interruptions.length > 0 && (
        <div className="mt-6 border-t pt-4">
          <h3 className="text-lg font-semibold mb-2">Interruptions ({session.interruptions.length})</h3>
          <div className="space-y-2">
            {session.interruptions.map((interruption, index) => (
              <div key={index} className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                <div className="font-medium">{interruption.reason}</div>
                <div className="text-xs">
                  {new Date(interruption.pause_time).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SessionControls;
