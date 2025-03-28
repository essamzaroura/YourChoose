import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './theme';
import Login from './pages/Login';
import Home from './pages/Home';
import PrivateRoute from './components/PrivateRoute';
// import { registerSW } from './serviceWorkerRegistration';


function App() {
  registerSW();

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div style={{ textAlign: "center", padding: "10px" }}>
        <img src="/logo.png" alt="YourChoose Logo" style={{ width: "100px", height: "auto" }} />
          <h1>Welcome to YourChoose</h1>
        </div>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={
            <PrivateRoute>
              <Home />
            </PrivateRoute>
          } />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}
fetch("/manifest.json")
  .then(response => response.json())
  .then(data => console.log(data));

export default App;
