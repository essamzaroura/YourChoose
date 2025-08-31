import React, { useState } from 'react';
import axios from 'axios';

const Chat = () => {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [error, setError] = useState('');

  const handleAskAI = async () => {
    setError('');
    setResponse('');
    try {
      const res = await axios.post('/api/chat', { message });
      setResponse(res.data.reply);
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to connect to AI service';
      setError(errorMsg.includes('429') 
        ? 'Quota exceeded. Please check your plan or try again later (retry in 58s).'
        : errorMsg);
    }
  };

  return (
    <div>
      <h1>Chat with Gemini AI</h1>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {response && <div>{response}</div>}
      <div>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask something to Gemini..."
        />
        <button onClick={handleAskAI}>Ask AI</button>
      </div>
    </div>
  );
};

export default Chat;