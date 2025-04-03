import React, { useState } from 'react';
import { Box, Typography, TextField, InputAdornment, IconButton, Tabs, Tab, Card, CardMedia, CardActions, Button } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import HomeIcon from '@mui/icons-material/Home';
import ChatIcon from '@mui/icons-material/Chat';
import HistoryIcon from '@mui/icons-material/History';
import BarChartIcon from '@mui/icons-material/BarChart';

function Home() {
  const [tabValue, setTabValue] = useState('categories');
  const [suggestions, setSuggestions] = useState([
    {
      category: 'Travel',
      image: 'https://source.unsplash.com/random/400x200/?puppy',
      description: 'Take your furry friend out to the park and let them play with other dogs too!'
    },
    {
      category: 'Food',
      image: 'https://source.unsplash.com/random/400x200/?mansion',
      description: 'Explore a mansion and indulge in luxury and opulence with your loved ones.'
    }
  ]);
  
  const updateSuggestions = () => {
    setSuggestions([...suggestions, { category: 'New', image: 'https://source.unsplash.com/random/400x200/?beach', description: 'Enjoy a beach trip!' }]);
  };
  
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleLike = (item) => {
    console.log('Liked:', item);
  };

  const handleExplore = (item) => {
    console.log('Exploring:', item);
  };

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column', bgcolor: '#ffffff' }}>
      {/* Header - matching mockup */}
      <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>Home</Typography>
        <IconButton>
          <BarChartIcon />
        </IconButton>
      </Box>
      
      {/* Search - matching mockup */}
      <Box sx={{ px: 2, pb: 2 }}>
        <TextField
          fullWidth
          placeholder="Search for suggestions..."
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
          variant="outlined"
          size="small"
          sx={{ 
            bgcolor: '#f5f5f5',
            '& .MuiOutlinedInput-root': {
              borderRadius: 3,
            }
          }}
        />
      </Box>
      <Button onClick={updateSuggestions} variant="contained" sx={{ mx: 2, mb: 2 }}>Add Suggestion</Button>
      
      {/* Categories Tab - matching mockup */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs 
          value={tabValue} 
          onChange={handleTabChange}
          variant="fullWidth"
          sx={{
            '& .MuiTabs-indicator': {
              backgroundColor: '#0088CC',
              height: 3
            },
            '& .Mui-selected': {
              color: '#0088CC !important',
              fontWeight: 'bold'
            }
          }}
        >
          <Tab value="categories" label="Categories" />
        </Tabs>
      </Box>
      
      {/* Content Area - matching mockup */}
      <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
        {tabValue === 'categories' && suggestions.map((item, index) => (
          <Box key={index} sx={{ mb: 3 }}>
            <Typography variant="subtitle1" sx={{ mb: 1, fontWeight: 'bold' }}>{item.category}</Typography>
            <Card sx={{ mb: 1, borderRadius: 2, overflow: 'hidden' }}>
              <CardMedia
                component="img"
                height="160"
                image={item.image}
                alt={item.category}
              />
              <CardActions sx={{ justifyContent: 'space-between', p: 1 }}>
                <Button 
                  size="small" 
                  variant="outlined" 
                  onClick={() => handleExplore(item)}
                  sx={{ 
                    borderRadius: 4,
                    fontSize: '0.7rem',
                    bgcolor: '#ffffff'
                  }}
                >
                  Explore
                </Button>
                <Button 
                  size="small" 
                  variant="outlined" 
                  onClick={() => handleLike(item)}
                  sx={{ 
                    borderRadius: 4,
                    fontSize: '0.7rem',
                    bgcolor: '#ffffff'
                  }}
                >
                  Like
                </Button>
              </CardActions>
            </Card>
            <Typography variant="body2" align="center">{item.description}</Typography>
          </Box>
        ))}
      </Box>
      
      {/* Bottom Navigation - matching mockup */}
      <Box 
        sx={{ 
          borderTop: '1px solid #eee', 
          p: 1, 
          display: 'flex', 
          justifyContent: 'space-around',
          bgcolor: '#ffffff'
        }}
      >
        <IconButton color="primary">
          <HomeIcon />
        </IconButton>
        <IconButton>
          <ChatIcon />
        </IconButton>
        <IconButton>
          <HistoryIcon />
        </IconButton>
      </Box>
    </Box>
  );
}

export default Home;