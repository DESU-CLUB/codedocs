import axios from 'axios';

function downloadNotebook(urlToPost) {
    axios({
        url: 'http://localhost:5000/create_notebook', // Adjust the URL based on your Flask app's URL
        method: 'POST',
        responseType: 'blob',  // Important: specifies that the response should be treated as a Blob
        data: {
            url: urlToPost  // JSON object containing the URL you want to post
        },
        headers: {
            'Content-Type': 'application/json'
        }
    }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'example_notebook.ipynb'); //or any other extension
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
        window.URL.revokeObjectURL(url);
    }).catch(error => console.error('Download error:', error));
}

export default downloadNotebook;
