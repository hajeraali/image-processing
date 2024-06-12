document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.blob())
      .then(blob => {
          const url = URL.createObjectURL(blob);
          document.getElementById('originalImage').src = url;
          document.getElementById('originalImage').dataset.filename = formData.get('image').name;
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

function processImage(operation, value) {
    const filename = document.getElementById('originalImage').dataset.filename;
    
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename: filename, operation: operation, value: value })
    }).then(response => response.json())
      .then(data => {
          document.getElementById('processedImage').src = data.processedImagePath;
      }).catch(error => console.error('Error:', error));
}
