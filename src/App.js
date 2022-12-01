import React from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom'
import NavBar from "./components/NavBar.js"
import HomeRender from './pages/HomeRender.js';
import './App.css';


function App() {
  return (
    <>
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" exact element={<HomeRender/>}/>
      </Routes>
    </Router>
    </>
  );
}

export default App;