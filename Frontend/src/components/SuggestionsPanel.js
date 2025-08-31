// src/components/SuggestionsPanel.js
import React from 'react';
import { Box, Typography, Card, CardMedia, CardActions, Button } from '@mui/material';

function SuggestionsPanel({ suggestions = [], onLike, onExplore }) {
  return (
    <Box>
      <Typography variant="h6" sx={{ mb: 2 }}>Categories</Typography>
      
      {suggestions.map((item, index) => (
        <Box key={index} sx={{ mb: 3 }}>
          <Typography variant="subtitle1" sx={{ mb: 1 }}>{item.category}</Typography>
          <Card sx={{ mb: 1 }}>
            <CardMedia
              component="img"
              height="140"
              image={item.image}
              alt={item.title}
            />
            <CardActions sx={{ justifyContent: 'space-between' }}>
              <Button size="small" onClick={() => onExplore(item)}>Explore</Button>
              <Button size="small" onClick={() => onLike(item)}>Like</Button>
            </CardActions>
          </Card>
          <Typography variant="body2">{item.description}</Typography>
        </Box>
      ))}
    </Box>
  );
}

export default SuggestionsPanel;
