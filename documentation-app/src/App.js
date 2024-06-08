import React, { useState } from 'react';
import './App.css';
import downloadNotebook from './fetcher';


function App() {
  // State for the main input box
  const [topicInput, setTopicInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Handler for the main input box
  const handleTopicChange = (event) => {
    setTopicInput(event.target.value);
  };

  // Handler for the speech bubble input box

  const isValidUrl = (url) => {
    try {
      new URL(url);
      return true;
    } catch (e) {
      return false;
    }
  };


const handleSubmit = (event) => {
  event.preventDefault();
  if (topicInput && isValidUrl(topicInput)) {
    setIsLoading(true);
    downloadNotebook(topicInput)
      .then(() => {
        setIsLoading(false);
      })
      .catch((error) => {
        console.error('Download error:', error);
        alert('Failed to fetch the documentation. Please try again.');
        setIsLoading(false);
      });
  } else {
    alert('Please enter a valid URL to learn about the topic');
  }
};


  return (
    <div className="app">
      <form onSubmit={handleSubmit}>

      <header className="header">
        <h1>DocPuzzles.com <span className="beta">ALPHA</span></h1>
        <p>
          This helps you find documentation on various topics and turn them into code quickly. 
          Input a URL you want to learn about.
        </p>
        <input 
          type="text" 
          placeholder="Enter URL:"
          className="input-box"
          value={topicInput}
          onChange={handleTopicChange}
        />
<button className="generate-button" disabled={isLoading}>
  {isLoading ? 'Loading...' : 'Generate'}
</button>

      </header>
     
      <div className="image-section">
        <img src="comical-doc-image.webp" alt="Comical documentation theme" />
      </div>
      </form>
      <footer class = 'footers'>
        Powered by <a href = 'https://groq.com/'>Groq</a> and <a href = "https://relevanceai.com/">Relevance AI</a>
      </footer>
    </div>
  );
}

export default App;
