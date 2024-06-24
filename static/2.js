document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.blob())
      .then(blob => {
          const url = URL.createObjectURL(blob);
          document.getElementById('processedImage').src = url;
          document.getElementById('processedImage').dataset.filename = formData.get('image').name;
      }).catch(error => console.error('Error:', error));
});

document.getElementById('blurSlider').addEventListener('input', function() {
    processImage('blur', this.value);
});

document.getElementById('contrastSlider').addEventListener('input', function() {
    processImage('contrast', this.value);
});

document.getElementById('sharpenSlider').addEventListener('input', function() {
    processImage('sharpen', this.value);
});

document.getElementById('invertSlider').addEventListener('input', function() {
    processImage('invert', this.value);
});

// New function to handle 'detect_white' operation
document.getElementById('detectWhiteCheckbox').addEventListener('change', function() {
    if (this.checked) {
        processImage('detect_white', 0); // Pass a dummy value, as threshold value is not used
    }
});

function processImage(operation, value) {
    const processedFilename = document.getElementById('processedImage').dataset.filename;

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename: processedFilename, operation: operation, value: value })
    }).then(response => response.json())
      .then(data => {
          document.getElementById('processedImage').src = data.processedImagePath;
          document.getElementById('processedImage').dataset.filename = data.newProcessedFilename;
      }).catch(error => console.error('Error:', error));
}
