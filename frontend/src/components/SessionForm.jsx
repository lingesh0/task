import React, { useState } from 'react';
import { sessionsAPI } from '../api';

const SessionForm = ({ onSessionCreated }) => {
  const [formData, setFormData] = useState({
    title: '',
    goal: '',
    scheduled_duration: 25
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Add validation for title and goal length
    if (name === 'title' && value.length > 50) {
      setError('Title must be 50 characters or less');
      return;
    }
    if (name === 'goal' && value.length > 200) {
      setError('Goal must be 200 characters or less');
      return;
    }
    
    setFormData(prev => ({
      ...prev,
      [name]: name === 'scheduled_duration' ? parseFloat(value) : value
    }));
    
    // Clear error when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // Additional validation before submission
    if (formData.title.trim().length === 0) {
      setError('Title is required');
      setIsLoading(false);
      return;
    }
    if (formData.goal.trim().length === 0) {
      setError('Goal is required');
      setIsLoading(false);
      return;
    }
    if (formData.title.length > 50) {
      setError('Title must be 50 characters or less');
      setIsLoading(false);
      return;
    }
    if (formData.goal.length > 200) {
      setError('Goal must be 200 characters or less');
      setIsLoading(false);
      return;
    }
    if (formData.scheduled_duration < 1 || formData.scheduled_duration > 240) {
      setError('Duration must be between 1 and 240 minutes');
      setIsLoading(false);
      return;
    }

    try {
      const newSession = await sessionsAPI.createSession(formData);
      onSessionCreated(newSession);
      setFormData({ title: '', goal: '', scheduled_duration: 25 });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create session');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Create New Session</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Session Title
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            maxLength={50}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., Write documentation"
          />
          <div className="text-xs text-gray-500 mt-1">
            {formData.title.length}/50 characters
          </div>
        </div>

        <div>
          <label htmlFor="goal" className="block text-sm font-medium text-gray-700 mb-1">
            Goal
          </label>
          <textarea
            id="goal"
            name="goal"
            value={formData.goal}
            onChange={handleChange}
            required
            maxLength={200}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="What do you want to accomplish in this session?"
          />
          <div className="text-xs text-gray-500 mt-1">
            {formData.goal.length}/200 characters
          </div>
        </div>

        <div>
          <label htmlFor="scheduled_duration" className="block text-sm font-medium text-gray-700 mb-1">
            Duration (minutes)
          </label>
          <input
            type="number"
            id="scheduled_duration"
            name="scheduled_duration"
            value={formData.scheduled_duration}
            onChange={handleChange}
            required
            min="1"
            max="240"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {error && (
          <div className="text-red-600 text-sm bg-red-50 p-3 rounded-md">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Creating...' : 'Create Session'}
        </button>
      </form>
    </div>
  );
};

export default SessionForm;
