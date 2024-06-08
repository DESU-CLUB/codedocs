import React, { useState } from 'react';
import './App.css';
import { downloadNotebook } from './axios';

function App() {
  // State for the main input box
  const [topicInput, setTopicInput] = useState('');

  // Separate state for the speech bubble input box
  const [descriptionInput, setDescriptionInput] = useState('');

  // Handler for the main input box
  const handleTopicChange = (event) => {
    setTopicInput(event.target.value);
  };

  // Handler for the speech bubble input box
  const handleDescriptionChange = (event) => {
    setDescriptionInput(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault(); // This stops the form from triggering a page reload
    // This function will be called when the user clicks the "Generate" button
    // It should fetch the documentation for the URL in the main input box
    // and display it in the speech bubble
    if (topicInput && descriptionInput) {
      downloadNotebook();
    } else {
      // Add your code or statement here
      alert('Please enter a URL and description to learn about the topic');
    }
  };

  return (
    <div className="app">
      <form onSubmit={handleSubmit}>

      <header className="header">
        <h1>DocFinder.com <span className="beta">BETA</span></h1>
        <p>
          This helps you find documentation on various topics quickly. 
          Input a URL you want to learn about.
        </p>
        <input 
          type="text" 
          placeholder="Enter URL:"
          className="input-box"
          value={topicInput}
          onChange={handleTopicChange}
        />
        <button className="generate-button">Generate</button>
      </header>
     
      <div className="image-section">
        <img src="comical-doc-image.webp" alt="Comical documentation theme" />
        <div className = 'speech-bubble-container'>
        <div className="speech-bubble">
        <input 
          type="text" 
          placeholder="Enter description of topic to learn"
          className="description-input"
          value={descriptionInput}
          onChange={handleDescriptionChange}
        />
        </div>
      </div>
      </div>
      </form>
    </div>
  );
}

export default App;