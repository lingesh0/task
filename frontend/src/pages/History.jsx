import React from 'react';
import SessionHistory from '../components/SessionHistory';

const History = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Session History</h1>
          <p className="text-gray-600">View all your deep work sessions and track your productivity</p>
        </div>
        
        <SessionHistory />
      </div>
    </div>
  );
};

export default History;
