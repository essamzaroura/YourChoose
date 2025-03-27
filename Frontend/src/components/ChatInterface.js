// src/components/ChatInterface.js
import React, { useState, useRef, useEffect } from 'react';
import { Box, TextField, IconButton, Typography, Paper } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

function ChatInterface({ onSendMessage }) {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = (e) => {
    e.preventDefault();
    if (input.trim()) {
      const newMessage = { type: 'user', text: input };
      setMessages([...messages, newMessage]);
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
        {messages.map((msg, index) => (
          <Box 
            key={index}
            sx={{
              display: 'flex',
              justifyContent: msg.type === 'user' ? 'flex-end' : 'flex-start',
              mb: 2
            }}
          >
            <Paper 
              elevation={1}
              sx={{ 
                p: 2, 
                maxWidth: '70%',
                bgcolor: msg.type === 'user' ? '#e3f2fd' : '#f1f1f1'
              }}
            >
              <Typography>{msg.text}</Typography>
            </Paper>
          </Box>
        ))}
        <div ref={messagesEndRef} />
      </Box>
      
      <Box component="form" onSubmit={handleSend} sx={{ p: 2, borderTop: '1px solid #eee' }}>
        <Box sx={{ display: 'flex' }}>
          <TextField
            fullWidth
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            variant="outlined"
            size="small"
          />
          <IconButton type="submit" color="primary" disabled={!input.trim()}>
            <SendIcon />
          </IconButton>
        </Box>
      </Box>
    </Box>
  );
}

export default ChatInterface;