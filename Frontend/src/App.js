// App.js (Main navigation logic with 3 tabs: Home, Chat, Menu)
import React, { useState } from 'react';
import { Box, IconButton } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import ChatIcon from '@mui/icons-material/Chat';
import MenuIcon from '@mui/icons-material/Menu';
import HomePage from './pages/Home';
import ChatPage from './pages/Chat';
import MenuPage from './pages/Menu';

function App() {
  const [page, setPage] = useState('home');
  
  const renderPage = () => {
    switch (page) {
      case 'chat':
        return <ChatPage />;
      case 'menu':
        return <MenuPage />;
      default:
        return <HomePage />;
    }
  };
  
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <Box sx={{ flexGrow: 1, overflow: 'auto' }}>{renderPage()}</Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-around', padding: 2, borderTop: '1px solid #ddd' }}>
        <IconButton color={page === 'home' ? 'primary' : 'default'} onClick={() => setPage('home')}>
          <HomeIcon />
        </IconButton>
        <IconButton color={page === 'chat' ? 'primary' : 'default'} onClick={() => setPage('chat')}>
          <ChatIcon />
        </IconButton>
        <IconButton color={page === 'menu' ? 'primary' : 'default'} onClick={() => setPage('menu')}>
          <MenuIcon />
        </IconButton>
      </Box>
    </Box>
  );
}

export default App;