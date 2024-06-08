import React from 'react';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="header">
        <h1>DocFinder.com <span className="beta">BETA</span></h1>
        <p>
          This helps you find documentation on various topics quickly. 
          Replace the API key with a URL you want to learn about.
        </p>
        <input 
          type="text" 
          placeholder="Enter the topic you want to learn about"
          className="input-box"
        />
        <button className="generate-button">Generate</button>
      </header>
      <div className="image-section">
        <img src="comical-doc-image.webp" alt="Comical documentation theme" />
      </div>
    </div>
  );
}

export default App;
