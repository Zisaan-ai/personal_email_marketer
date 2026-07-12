with open('frontend/index.html', encoding='utf-8') as f:
    text = f.read()

modal_html = '''
    <!-- Image Gallery Modal -->
    <div id="gallery-modal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(15,23,42,0.6);z-index:9999;align-items:center;justify-content:center;backdrop-filter:blur(4px);">
        <div style="background:#fff;width:800px;max-width:90%;height:600px;max-height:90vh;border-radius:12px;display:flex;flex-direction:column;box-shadow:0 10px 25px rgba(0,0,0,0.15);">
            <div style="padding:20px;border-bottom:1px solid #e2e8f0;display:flex;justify-content:space-between;align-items:center;">
                <h3 style="margin:0;font-size:18px;color:#1e293b;"><i class="fa-solid fa-images"></i> Image Gallery</h3>
                <button onclick="closeGalleryModal()" style="background:none;border:none;font-size:20px;color:#64748b;cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div style="padding:20px;border-bottom:1px solid #e2e8f0;display:flex;gap:10px;">
                <input type="file" id="gallery-upload-input" accept="image/*" style="display:none;" onchange="handleGalleryUpload(event)">
                <button onclick="document.getElementById('gallery-upload-input').click()" class="primary-btn" style="padding:8px 16px;"><i class="fa-solid fa-upload"></i> Upload Image</button>
                <span id="gallery-upload-status" style="align-self:center;font-size:14px;color:#64748b;display:none;"><i class="fa-solid fa-spinner fa-spin"></i> Uploading...</span>
            </div>
            <div id="gallery-grid" style="flex:1;overflow-y:auto;padding:20px;display:grid;grid-template-columns:repeat(auto-fill, minmax(150px, 1fr));gap:15px;align-content:start;">
                <!-- Images will be loaded here -->
            </div>
        </div>
    </div>
'''

if 'id="gallery-modal"' not in text:
    text = text.replace('</body>', modal_html + '\n</body>')
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added gallery modal to index.html')
else:
    print('Gallery modal already exists')
