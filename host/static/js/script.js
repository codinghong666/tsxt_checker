document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const resultContent = document.getElementById('resultContent');
    const newUploadBtn = document.getElementById('newUpload');
    
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('studentId', document.getElementById('studentId').value);
        formData.append('projectFile', document.getElementById('projectFile').files[0]);
        
        // Show loading, hide form
        uploadForm.classList.add('hidden');
        loadingDiv.classList.remove('hidden');
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                resultContent.textContent = data.results;
            } else {
                resultContent.textContent = 'Error: ' + data.message;
            }
            
            // Show results, hide loading
            loadingDiv.classList.add('hidden');
            resultsDiv.classList.remove('hidden');
        })
        .catch(error => {
            resultContent.textContent = 'Error: ' + error.message;
            loadingDiv.classList.add('hidden');
            resultsDiv.classList.remove('hidden');
        });
    });
    
    newUploadBtn.addEventListener('click', function() {
        // Reset form and show it again
        uploadForm.reset();
        resultsDiv.classList.add('hidden');
        uploadForm.classList.remove('hidden');
    });
});