import axios from 'axios';

function downloadNotebook(urlToPost) {
    return new Promise((resolve, reject) => { // Return a Promise
        axios.post('http://localhost:5000/create_notebook',
            {
                url: urlToPost
            },
            {
                responseType: 'blob',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        ).then((response) => {
            // Create a URL for the blob
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'example_notebook.ipynb');
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
            window.URL.revokeObjectURL(url);

            resolve(); // Resolve the Promise after successful download
        }).catch(error => {
            console.error('Download error:', error);
            alert('Download failed, please try again.');
            reject(error); // Reject the Promise on error
        });
    });
}

export default downloadNotebook;
