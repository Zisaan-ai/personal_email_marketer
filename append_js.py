with open('frontend/assets/app.js', 'a', encoding='utf-8') as f:
    f.write('''
// ============================================================
// IMAGE GALLERY
// ============================================================
let currentGalleryInputId = null;

window.openGalleryModal = function(inputId) {
    currentGalleryInputId = inputId;
    document.getElementById('gallery-modal').style.display = 'flex';
    fetchGalleryImages();
};

window.closeGalleryModal = function() {
    document.getElementById('gallery-modal').style.display = 'none';
    currentGalleryInputId = null;
};

window.fetchGalleryImages = function() {
    const grid = document.getElementById('gallery-grid');
    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:20px;color:#64748b;"><i class="fa-solid fa-spinner fa-spin"></i> Loading...</div>';
    
    fetch('/api/gallery', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    .then(res => res.json())
    .then(data => {
        if (!Array.isArray(data)) {
            grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:20px;color:red;">Failed to load images.</div>';
            return;
        }
        if (data.length === 0) {
            grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:20px;color:#64748b;">No images found. Upload one to get started!</div>';
            return;
        }
        
        grid.innerHTML = data.map(media => `
            <div style="position:relative;border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;cursor:pointer;aspect-ratio:1;background:#f8fafc;" onclick="selectGalleryImage('${media.url}')">
                <img src="${media.url}" style="width:100%;height:100%;object-fit:contain;">
                <button onclick="event.stopPropagation(); deleteGalleryImage('${media.id}')" style="position:absolute;top:5px;right:5px;background:rgba(255,0,0,0.8);color:white;border:none;border-radius:4px;width:24px;height:24px;display:flex;align-items:center;justify-content:center;cursor:pointer;"><i class="fa-solid fa-trash"></i></button>
            </div>
        `).join('');
    })
    .catch(err => {
        grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:20px;color:red;">Error loading gallery.</div>';
    });
};

window.handleGalleryUpload = function(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const status = document.getElementById('gallery-upload-status');
    status.style.display = 'inline-block';
    
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('/api/gallery/upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        status.style.display = 'none';
        event.target.value = '';
        if (data.status === 'success') {
            fetchGalleryImages();
        } else {
            alert('Upload failed: ' + (data.detail || 'Unknown error'));
        }
    })
    .catch(err => {
        status.style.display = 'none';
        alert('Upload error');
    });
};

window.deleteGalleryImage = function(id) {
    if(!confirm('Delete this image?')) return;
    fetch('/api/gallery/' + id, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    .then(() => fetchGalleryImages());
};

window.selectGalleryImage = function(url) {
    if (currentGalleryInputId) {
        const input = document.getElementById(currentGalleryInputId);
        if (input) {
            input.value = url;
            // Trigger change event to update the preview
            const event = new Event('input', { bubbles: true });
            input.dispatchEvent(event);
        }
    }
    closeGalleryModal();
};
''')
