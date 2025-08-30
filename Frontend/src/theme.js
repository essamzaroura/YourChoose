import { createTheme } from '@mui/material/styles';

// Matching the logo colors (teal/cyan gradient and dark background)
const theme = createTheme({
  palette: {
    primary: {
      main: '#00BFA5', // Teal color from logo
      light: '#5DF2D6',
      dark: '#008E76',
      contrastText: '#fff',
    },
    secondary: {
      main: '#0088CC', // Blue color from logo
      light: '#35BFFF',
      dark: '#00599A',
      contrastText: '#fff',
    },
    background: {
      default: '#ffffff',
      paper: '#ffffff',
      dark: '#121212', // Dark background like in the logo
    },
    text: {
      primary: '#212121',
      secondary: '#757575',
    }
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h6: {
      fontWeight: 600,
    },
    subtitle1: {
      fontWeight: 600,
    }
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
        },
        contained: {
          boxShadow: 'none',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0px 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
          }
        }
      }
    },
    MuiTab: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
        }
      }
    }
  },
});

export default theme;