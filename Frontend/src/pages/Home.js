// frontend/src/Home.js
import React, { useEffect, useState } from 'react';
import { Typography, CircularProgress, Grid, Card, CardContent, CardMedia, Link as MuiLink, Box } from '@mui/material';

const HomePage = () => {
  const [deals, setDeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // console.log('HomePage: useEffect triggered to fetch deals.'); // Uncomment for debugging
    setLoading(true);
    fetch('http://localhost:5000/api/deals')
      .then((res) => {
        if (!res.ok) {
          return res.json().then(errData => { // Try to parse error message from backend
            throw new Error(`HTTP error! status: ${res.status}, message: ${errData.error || 'Unknown server error'}`);
          }).catch(() => { // Fallback if error response is not JSON
            throw new Error(`HTTP error! status: ${res.status}`);
          });
        }
        return res.json();
      })
      .then((data) => {
        // console.log('HomePage: Deals data received:', data); // Uncomment for debugging
        if (data && Array.isArray(data)) {
          if (data.length > 0) {
            setDeals(data);
            setError('');
          } else {
            setError('No deals available at the moment from the source.');
            setDeals([]);
          }
        } else if (data && data.error) { // Handle structured error from API
          setError(`API Error: ${data.error}`);
          setDeals([]);
        } else { // Unexpected data format
          setError('Received unexpected data format from server.');
          setDeals([]);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('HomePage: Failed to fetch deals:', err);
        setError(`Failed to fetch deals: ${err.message}`);
        setLoading(false);
        setDeals([]);
      });
  }, []);

  if (loading) {
    return <CircularProgress sx={{ display: 'block', mx: 'auto', mt: 5, mb: 2 }} />;
  }

  if (error) {
    return <Typography align="center" color="error" variant="h6" mt={5} mb={2}>{error}</Typography>;
  }

  if (!deals.length) {
    return <Typography align="center" variant="h6" mt={5} mb={2}>No deals found currently. Please check back later!</Typography>;
  }

  // --- FIX: Dynamic grid sizing based on number of deals ---
  let xs = 12; // Full width on extra-small screens
  let sm = 12; // Default to full width on small screens
  let md = 12; // Default to full width on medium screens

  if (deals.length === 1) {
    // md can be 12, or less if you want it centered but not full width on larger screens
    // For 100% width even on md for a single item:
    sm = 12; md = 12; // Or keep md more constrained e.g. md = 8, offset = 2 for centering
  } else if (deals.length === 2) {
    sm = 6; // 50% width on small screens and up
    md = 6; // 50% width on medium screens and up
  } else if (deals.length >= 3) {
    sm = 6; // 2 items per row on small screens
    md = 4; // 3 items per row on medium screens and up
  }
  // For more complex centering of a single item, you might need additional Grid items or styling.
  // This setup ensures that if there's 1 item, it takes full width on small/medium.

  return (
    <Grid container spacing={3} sx={{ p: 3 }} justifyContent="center"> {/* Added justifyContent for centering items if row is not full */}
      {deals.map((deal, index) => (
        <Grid item xs={xs} sm={sm} md={md} key={deal.link_url || deal.destination + '-' + index}>
          <Card sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <MuiLink href={deal.link_url || '#'} target="_blank" rel="noopener noreferrer" underline="none">
              {deal.image && deal.image.startsWith('http') ? (
                <CardMedia
                  component="img"
                  image={deal.image}
                  alt={`Deal image for ${deal.destination || 'deal'}`}
                  sx={{
                    height: 190,
                    objectFit: 'cover', 
                    cursor: deal.link_url ? 'pointer' : 'default'
                  }}
                  onError={(e) => { e.target.alt = 'Image failed to load'; }}
                />
              ) : (
                <Box sx={{ height: 190, display: 'flex', alignItems: 'center', justifyContent: 'center', borderBottom: '1px solid lightgray', backgroundColor: '#f0f0f0' }}>
                  <Typography variant="caption" color="text.secondary">
                    (Image not available)
                  </Typography>
                </Box>
              )}
            </MuiLink>
            <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
              <Typography variant="h6" component="div" gutterBottom noWrap title={deal.destination}>
                <MuiLink href={deal.link_url || '#'} target="_blank" rel="noopener noreferrer" color="inherit" underline="hover">
                  {deal.destination || 'N/A Destination'}
                </MuiLink>
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1, height: '3.6em', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' }} title={deal.details}>
                <strong>Details:</strong> {deal.details || 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary" noWrap title={deal.hotel_name}>
                <strong>Hotel:</strong> {deal.hotel_name || 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                <strong>Dates:</strong> {deal.dates || 'N/A'}
              </Typography>
              
              <Box sx={{ marginTop: 'auto' }}> {/* Pushes price to the bottom */}
                <Typography variant="h6" color="primary" component="div">
                  {/* Display the 'price' which is new_price or fallback to old_price */}
                  Price: {deal.price && deal.price !== "N/A" ? deal.price : "N/A"}
                </Typography>
                {/* Display old_price separately if it's different from the main 'price' and valid */}
                {deal.old_price && deal.old_price !== "N/A" && deal.old_price !== deal.price && (
                  <Typography variant="body2" color="text.secondary" sx={{ textDecoration: 'line-through' }}>
                    Old: {deal.old_price}
                  </Typography>
                )}
              </Box>
            </CardContent>
            {deal.link_url && (
                 <Box sx={{ p: 1, textAlign: 'center', borderTop: '1px solid #eee', mt: 'auto' }}> {/* Ensure button is at bottom */}
                    <MuiLink href={deal.link_url} target="_blank" rel="noopener noreferrer" variant="button">
                        View Deal on Blik
                    </MuiLink>
                </Box>
            )}
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default HomePage;