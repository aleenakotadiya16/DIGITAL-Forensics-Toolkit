#!/usr/bin/env python3
import os
import csv
import json
import base64
from PIL import Image
import io
from pathlib import Path

IMAGE_DIR = "/Volumes/HOLE-RAID-DRIVE/Projects/Digital-Forensics/Exif-Project/El-paso-pd/images:videos"
METADATA_FILE = "/tmp/el_paso_images_exif.csv"
OUTPUT_FILE = "/Volumes/HOLE-RAID-DRIVE/Projects/Digital-Forensics/Analysis-Output/El-Paso-PD/el-paso-pd-images.html"

def get_image_metadata():
    """Extract metadata from exiftool CSV"""
    metadata_map = {}
    try:
        with open(METADATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row:
                    filename = row.get('FileName', '').split('/')[-1] if row.get('FileName') else ''
                    if filename:
                        metadata_map[filename] = {
                            'DateTimeOriginal': row.get('DateTimeOriginal', 'Unknown'),
                            'Make': row.get('Make', 'Unknown'),
                            'Model': row.get('Model', 'Unknown'),
                            'ISO': row.get('ISO', 'Unknown'),
                            'FNumber': row.get('FNumber', 'Unknown'),
                            'FocalLength': row.get('FocalLength', 'Unknown'),
                            'ShutterSpeed': row.get('ShutterSpeed', 'Unknown'),
                            'ImageWidth': row.get('ImageWidth', 'Unknown'),
                            'ImageHeight': row.get('ImageHeight', 'Unknown'),
                        }
    except Exception as e:
        print(f"Warning: Could not read metadata file: {e}")
    return metadata_map

def image_to_base64(image_path, quality=75, resize_percent=0.5):
    """Convert image to base64 JPEG at specified quality and resolution"""
    try:
        img = Image.open(image_path)
        # Skip non-image files
        if img.format not in ['JPEG', 'PNG', 'HEIC']:
            return None, None
        
        # Resize if needed
        if resize_percent < 1.0:
            new_width = int(img.width * resize_percent)
            new_height = int(img.height * resize_percent)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Compress to JPEG
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{b64}", img.size
    except Exception as e:
        print(f"  Error processing {os.path.basename(image_path)}: {e}")
        return None, None

def generate_image_app():
    """Generate image analyzer"""
    print("Loading image metadata...")
    metadata_map = get_image_metadata()
    
    # Get all JPG files
    image_files = sorted([f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    
    if not image_files:
        print("No images found!")
        return
    
    print(f"Processing {len(image_files)} images...")
    
    image_array = []
    total_size = 0
    original_size = 0
    
    for idx, filename in enumerate(image_files):
        print(f"  [{idx+1}/{len(image_files)}] {filename}")
        image_path = os.path.join(IMAGE_DIR, filename)
        
        # Get original size
        original_size += os.path.getsize(image_path)
        
        # Convert to base64
        data_uri, dims = image_to_base64(image_path, quality=75, resize_percent=0.5)
        
        if data_uri:
            # Get metadata
            meta = metadata_map.get(filename, {})
            
            image_array.append({
                'FileName': filename,
                'DateTimeOriginal': meta.get('DateTimeOriginal', 'Unknown'),
                'Make': meta.get('Make', 'Unknown'),
                'Model': meta.get('Model', 'Unknown'),
                'ISO': meta.get('ISO', 'Unknown'),
                'FNumber': meta.get('FNumber', 'Unknown'),
                'FocalLength': meta.get('FocalLength', 'Unknown'),
                'ShutterSpeed': meta.get('ShutterSpeed', 'Unknown'),
                'ImageWidth': meta.get('ImageWidth', 'Unknown'),
                'ImageHeight': meta.get('ImageHeight', 'Unknown'),
                'dataUri': data_uri,
                'fileSize': os.path.getsize(image_path)
            })
    
    # Sort by date
    def sort_key(img):
        date = img['DateTimeOriginal']
        if date == 'Unknown':
            return ('z', '')
        return (date, img['FileName'])
    
    image_array.sort(key=sort_key)
    
    # Create HTML
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>El Paso PD - Forensic Image Analyzer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
            min-height: 100vh;
            padding: 10px;
            color: #172144;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .header {
            background: #172144;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            font-size: clamp(24px, 5vw, 32px);
            margin-bottom: 5px;
        }
        .header p {
            font-size: clamp(12px, 3vw, 14px);
            opacity: 0.9;
        }
        .tabs {
            display: flex;
            background: #f5f5f5;
            border-bottom: 1px solid #ddd;
            flex-wrap: wrap;
        }
        .tab-button {
            flex: 1;
            min-width: 120px;
            padding: 12px 10px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: clamp(13px, 2vw, 16px);
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
        }
        .tab-button.active {
            background: white;
            color: #172144;
            border-bottom: 3px solid #172144;
        }
        .tab-content {
            display: none;
            padding: clamp(15px, 4vw, 30px);
        }
        .tab-content.active {
            display: block;
        }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 12px;
        }
        @media (min-width: 640px) {
            .gallery {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 15px;
            }
        }
        @media (min-width: 1024px) {
            .gallery {
                grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
                gap: 15px;
            }
        }
        .gallery-item {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s;
            min-height: 140px;
        }
        .gallery-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            border-color: #172144;
        }
        .gallery-thumb {
            width: 100%;
            height: 120px;
            object-fit: cover;
            background: #f0f0f0;
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 10px;
        }
        .modal.active {
            display: flex;
        }
        .modal-content {
            background: white;
            border-radius: 8px;
            max-width: 95vw;
            max-height: 90vh;
            display: flex;
            overflow: hidden;
            flex-direction: column;
        }
        @media (min-width: 768px) {
            .modal-content {
                flex-direction: row;
            }
        }
        .modal-image {
            flex: 1;
            min-height: 300px;
            padding: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f9f9f9;
        }
        .modal-image img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }
        .modal-meta {
            flex: 1;
            padding: 15px;
            background: white;
            overflow-y: auto;
            min-height: 300px;
            border-left: 1px solid #e0e0e0;
        }
        @media (max-width: 767px) {
            .modal-meta {
                border-left: none;
                border-top: 1px solid #e0e0e0;
            }
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }
        .modal-title {
            font-size: clamp(14px, 3vw, 16px);
            font-weight: 600;
            color: #172144;
            word-break: break-word;
            flex: 1;
        }
        .close-btn {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: #999;
            padding: 5px;
            min-width: 44px;
            min-height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .modal-nav {
            display: flex;
            gap: 8px;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        .nav-btn {
            background: #172144;
            color: white;
            border: none;
            padding: 10px 12px;
            border-radius: 4px;
            cursor: pointer;
            min-height: 44px;
            font-size: 14px;
            flex: 1;
            min-width: 80px;
        }
        .nav-btn:hover {
            background: #0f1630;
        }
        .nav-btn:active {
            transform: scale(0.98);
        }
        .nav-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .counter {
            font-size: 12px;
            color: #172144;
            padding: 8px;
            white-space: nowrap;
        }
        .meta-field {
            margin-bottom: 12px;
        }
        .meta-label {
            font-size: 11px;
            color: #999;
            text-transform: uppercase;
            font-weight: 600;
        }
        .meta-value {
            font-size: 13px;
            color: #172144;
            margin-top: 3px;
            word-break: break-word;
        }
        .divider {
            margin: 15px 0;
            border-top: 1px solid #e0e0e0;
        }
        @media (max-width: 480px) {
            .container {
                border-radius: 4px;
            }
            .header {
                padding: 15px;
            }
            .tab-button {
                padding: 10px 8px;
                font-size: 13px;
            }
            .tab-content {
                padding: 12px;
            }
            .gallery {
                grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📸 El Paso PD - Forensic Image Analyzer</h1>
            <p>Police Department evidence images with EXIF metadata</p>
        </div>
        <div class="tabs">
            <button class="tab-button active" onclick="switchTab('gallery')">Image Gallery</button>
        </div>
        <div id="gallery" class="tab-content active"></div>
    </div>
    
    <div id="imageModal" class="modal">
        <div class="modal-content">
            <div class="modal-image">
                <img id="modalImg" src="" alt="Image">
            </div>
            <div class="modal-meta">
                <div class="modal-header">
                    <div>
                        <button class="close-btn" onclick="closeModal()">✕</button>
                    </div>
                </div>
                <div class="modal-title" id="modalTitle"></div>
                <div class="divider"></div>
                <div id="metaContent"></div>
                <div class="divider"></div>
                <div class="modal-nav">
                    <button class="nav-btn" id="prevBtn" onclick="previousImage()">← Prev</button>
                    <div class="counter"><span id="counter"></span></div>
                    <button class="nav-btn" id="nextBtn" onclick="nextImage()">Next →</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const imageData = IMAGE_DATA_PLACEHOLDER;
        let currentImageIndex = 0;
        
        function renderGallery() {
            const galleryDiv = document.getElementById('gallery');
            let html = '';
            imageData.forEach((img, idx) => {
                html += `<div class="gallery-item" onclick="openImage(${idx})">
                    <img src="${img.dataUri}" class="gallery-thumb" alt="${escapeHtml(img.FileName)}">
                </div>`;
            });
            const container = document.createElement('div');
            container.className = 'gallery';
            container.innerHTML = html;
            galleryDiv.innerHTML = '';
            galleryDiv.appendChild(container);
        }
        
        function openImage(idx) {
            currentImageIndex = idx;
            displayImage();
            document.getElementById('imageModal').classList.add('active');
        }
        
        function closeModal() {
            document.getElementById('imageModal').classList.remove('active');
        }
        
        function displayImage() {
            const img = imageData[currentImageIndex];
            document.getElementById('modalImg').src = img.dataUri;
            document.getElementById('modalTitle').textContent = escapeHtml(img.FileName);
            document.getElementById('counter').textContent = `${currentImageIndex + 1} / ${imageData.length}`;
            
            let meta = '<div class="meta-field"><div class="meta-label">Date/Time</div><div class="meta-value">' + escapeHtml(img.DateTimeOriginal) + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Camera</div><div class="meta-value">' + escapeHtml(img.Make) + ' ' + escapeHtml(img.Model) + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">ISO</div><div class="meta-value">' + escapeHtml(img.ISO) + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Aperture</div><div class="meta-value">' + escapeHtml(img.FNumber) + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Shutter Speed</div><div class="meta-value">' + escapeHtml(img.ShutterSpeed) + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Focal Length</div><div class="meta-value">' + escapeHtml(img.FocalLength) + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Resolution</div><div class="meta-value">' + escapeHtml(img.ImageWidth) + ' × ' + escapeHtml(img.ImageHeight) + '</div></div>';
            
            document.getElementById('metaContent').innerHTML = meta;
            document.getElementById('prevBtn').disabled = currentImageIndex === 0;
            document.getElementById('nextBtn').disabled = currentImageIndex === imageData.length - 1;
        }
        
        function previousImage() {
            if (currentImageIndex > 0) {
                currentImageIndex--;
                displayImage();
            }
        }
        
        function nextImage() {
            if (currentImageIndex < imageData.length - 1) {
                currentImageIndex++;
                displayImage();
            }
        }
        
        function switchTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        function escapeHtml(text) {
            const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
            return String(text).replace(/[&<>"']/g, m => map[m]);
        }
        
        document.addEventListener('keydown', (e) => {
            if (document.getElementById('imageModal').classList.contains('active')) {
                if (e.key === 'ArrowLeft') previousImage();
                if (e.key === 'ArrowRight') nextImage();
                if (e.key === 'Escape') closeModal();
            }
        });
        
        renderGallery();
    </script>
</body>
</html>'''
    
    html_content = html_template.replace(
        'IMAGE_DATA_PLACEHOLDER',
        json.dumps(image_array, ensure_ascii=False)
    )
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"✅ Image app created: {OUTPUT_FILE}")
    print(f"   Size: {file_size_mb:.1f} MB")
    print(f"   Images: {len(image_array)}")

if __name__ == '__main__':
    generate_image_app()
