// JavaScript to preview the image when a file is selected
document.getElementById('formFile').addEventListener('change', function(event) {
  var reader = new FileReader();
  
  reader.onload = function() {
    var imagePreview = document.getElementById('imagePreview');
    imagePreview.src = reader.result;  // Set the image preview source to the file
    imagePreview.style.display = 'block'; // Display the image preview
  }

  reader.readAsDataURL(this.files[0]);  // Read the selected file as a data URL
});