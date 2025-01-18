const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const file = fileInput.files[0];

  if (file) {
    const formData = new FormData();
    formData.append('pdfFile', file);

    // Make an API call to upload the file
    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => {
      // Handle the response from the server
      if (response.ok) {
        console.log('File uploaded successfully');
      } else {
        console.error('File upload failed');
      }
    })
    .catch(error => {
      console.error('Error uploading file:', error);
    });
  } else {
    console.error('No file selected');
  }
});