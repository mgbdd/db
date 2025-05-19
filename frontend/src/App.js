import React from 'react';
import { Routes, Route } from 'react-router-dom';
import RoleSelection from './components/RoleSelection';
import TablesList from './components/TablesList';
import TableView from './components/TableView';
import Header from './components/Header';
import './App.css';

function App() {
  return (
    <div className="app">
      <Header />
      <div className="container">
        <Routes>
          <Route path="/" element={<RoleSelection />} />
          <Route path="/tables/:role" element={<TablesList />} />
          <Route path="/tables/:role/:table" element={<TableView />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
