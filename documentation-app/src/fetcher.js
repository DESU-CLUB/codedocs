import axios from 'axios';

function downloadNotebook(urlToPost) {
    axios.post('http://localhost:5000/create_notebook', // The URL where the POST request is sent
        {
            url: urlToPost  // JSON object containing the URL you want to post
        },
        {
            responseType: 'blob',  // Important: specifies that the response should be treated as a Blob
            headers: {
                'Content-Type': 'application/json'
            }
        }
    ).then((response) => {
        // Create a URL for the blob
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'example_notebook.ipynb'); // Set the download attribute to a default filename
        document.body.appendChild(link);
        link.click(); // Programmatically trigger the link to download
        link.parentNode.removeChild(link); // Remove the link from the DOM
        window.URL.revokeObjectURL(url); // Clean up the URL object
    }).catch(error => {
        console.error('Download error:', error);
        alert('Download failed, please try again.');
    });
}

export default downloadNotebook;
