// Chat.js (ChatGPT-like AI chat with session history)
import React, { useState } from 'react';
import { Box, TextField, Button, Typography, List, ListItem, ListItemText } from '@mui/material';

function Chat() {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState([]);
  const [sessionId, setSessionId] = useState(Date.now());

  const handleAskAI = () => {
    if (!input.trim()) return;

    // Simulate AI response (you can connect this to Gemini API)
    const reply = `AI: ${input} 🤖`;

    const newHistory = [...history, { session: sessionId, question: input, answer: reply }];
    setHistory(newHistory);
    setInput('');
  };

  const newSession = () => {
    setSessionId(Date.now());
    setHistory([]);
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" sx={{ fontWeight: 'bold' }}>Chat with Gemini AI</Typography>
      <Button variant="outlined" sx={{ mt: 1, mb: 2 }} onClick={newSession}>New Session</Button>

      <List sx={{ maxHeight: '60vh', overflow: 'auto', mb: 2 }}>
        {history.map((msg, i) => (
          <ListItem key={i} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
            <ListItemText primary={`You: ${msg.question}`} />
            <ListItemText secondary={msg.answer} />
          </ListItem>
        ))}
      </List>

      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          value={input}
          placeholder="Ask something like Gemini..."
          onChange={(e) => setInput(e.target.value)}
        />
        <Button variant="contained" onClick={handleAskAI}>Ask AI</Button>
      </Box>
    </Box>
  );
}

export default Chat;
