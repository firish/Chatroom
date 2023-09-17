import logo from './logo.svg';
import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginSignup from './LoginSignup'; 
import Chatroom from './Chatroom';       

function App() {
  return (
    <div className="App">
      <Router>
            <Routes>
                <Route path="/login" element={<LoginSignup />} />
                <Route path="/chatroom" element={<Chatroom />} />
                <Route path="/" element={<LoginSignup />} />
            </Routes>
        </Router>
    </div>
  );
}

export default App;
