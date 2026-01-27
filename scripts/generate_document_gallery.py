#!/usr/bin/env python3
import os
import json
import base64
import fitz
from PIL import Image
import io

DOCUMENT_DIR = "/Volumes/HOLE-RAID-DRIVE/Projects/Digital-Forensics/Exif-Project/El-paso-pd/Documents"
OUTPUT_FILE = "/Volumes/HOLE-RAID-DRIVE/Projects/Digital-Forensics/Analysis-Output/El-Paso-PD/el-paso-pd-documents.html"

def parse_pdf_date(date_str):
    if not date_str:
        return "Unknown"
    try:
        if isinstance(date_str, str) and date_str.startswith('D:'):
            date_str = date_str[2:8]
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}" if len(date_str) >= 8 else "Unknown"
    except:
        return "Unknown"

def pdf_page_to_base64(pdf_path, page_num, quality=85, resize_percent=1.0):
    try:
        pdf_document = fitz.open(pdf_path)
        if page_num >= pdf_document.page_count:
            return None, None
        page = pdf_document[page_num]
        mat = fitz.Matrix(300/72, 300/72)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.open(io.BytesIO(pix.tobytes("ppm")))
        
        if resize_percent < 1.0:
            new_width = int(img.width * resize_percent)
            new_height = int(img.height * resize_percent)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{b64}", img.size
    except Exception as e:
        print(f"  Error on page {page_num}: {str(e)[:50]}")
        return None, None

print("Processing El Paso PD documents...")
pdf_files = sorted([f for f in os.listdir(DOCUMENT_DIR) if f.endswith('.pdf')])
document_array = []
total_pages = 0

for idx, filename in enumerate(pdf_files):
    pdf_path = os.path.join(DOCUMENT_DIR, filename)
    try:
        pdf_doc = fitz.open(pdf_path)
        page_count = pdf_doc.page_count
        file_size = os.path.getsize(pdf_path)
        metadata = pdf_doc.metadata
        
        print(f"  [{idx+1}/{len(pdf_files)}] {filename} ({page_count} pages)")
        
        # Limit processing for very large files
        max_pages = min(page_count, 100)
        
        pages = []
        for page_num in range(max_pages):
            data_uri, _ = pdf_page_to_base64(pdf_path, page_num, quality=85)
            if data_uri:
                pages.append({'pageNumber': page_num + 1, 'dataUri': data_uri})
        
        preview_uri, _ = pdf_page_to_base64(pdf_path, 0, quality=75, resize_percent=0.25)
        
        document_array.append({
            'FileName': filename,
            'pageCount': page_count,
            'embeddedPages': len(pages),
            'previewUri': preview_uri,
            'CreationDateEmbedded': parse_pdf_date(metadata.get('creationDate') if metadata else None) if metadata else "Unknown",
            'ModificationDate': parse_pdf_date(metadata.get('modDate') if metadata else None) if metadata else "Unknown",
            'DocumentAuthor': (metadata.get('author') if metadata else None) or "Unknown",
            'DocumentCreator': (metadata.get('creator') if metadata else None) or "Unknown",
            'DocumentProducer': (metadata.get('producer') if metadata else None) or "Unknown",
            'fileSize': file_size,
            'pages': pages
        })
        
        total_pages += len(pages)
        pdf_doc.close()
    except Exception as e:
        print(f"  Error processing {filename}: {str(e)[:80]}")

# Sort by date
def sort_key(item):
    date = item['CreationDateEmbedded']
    if date == "Unknown":
        return ('z', '')
    return (date, item['FileName'])

document_array.sort(key=sort_key)

print(f"Generating HTML for {len(document_array)} documents ({total_pages} pages)...")

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>El Paso PD - Forensic Document Analyzer</title>
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
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 12px;
        }
        @media (min-width: 640px) {
            .gallery {
                grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
                gap: 15px;
            }
        }
        @media (min-width: 1024px) {
            .gallery {
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 20px;
            }
        }
        .gallery-item {
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s;
            min-height: 180px;
        }
        .gallery-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            border-color: #172144;
        }
        .gallery-preview {
            width: 100%;
            height: 140px;
            object-fit: cover;
            background: #f0f0f0;
        }
        .gallery-info {
            padding: 10px;
        }
        .gallery-title {
            font-size: clamp(12px, 2vw, 13px);
            font-weight: 600;
            color: #172144;
            margin-bottom: 6px;
            word-break: break-word;
        }
        .gallery-pages {
            font-size: 11px;
            color: #999;
            background: #f5f5f5;
            padding: 4px 8px;
            border-radius: 3px;
            display: inline-block;
        }
        .divider {
            display: flex;
            align-items: center;
            margin: 20px 0;
            color: #999;
        }
        .divider::before, .divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: #e0e0e0;
        }
        .divider span {
            padding: 0 12px;
            font-size: 12px;
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.7);
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
            overflow: auto;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            background: #f5f5f5;
            border-bottom: 1px solid #e0e0e0;
            position: sticky;
            top: 0;
            flex-wrap: wrap;
            gap: 10px;
        }
        .modal-title {
            font-size: clamp(14px, 3vw, 16px);
            font-weight: 600;
            color: #172144;
            flex: 1;
        }
        .modal-controls {
            display: flex;
            gap: 8px;
            align-items: center;
            flex-wrap: wrap;
        }
        .modal-button {
            background: #172144;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            min-height: 44px;
            font-size: 13px;
            white-space: nowrap;
        }
        .modal-button:hover {
            background: #0f1630;
        }
        .modal-button:active {
            transform: scale(0.98);
        }
        .modal-button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .page-counter {
            font-size: 12px;
            color: #172144;
            padding: 8px;
            min-width: 60px;
            white-space: nowrap;
        }
        .close-btn {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            padding: 5px;
            min-width: 44px;
            min-height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .modal-page {
            padding: clamp(10px, 3vw, 20px);
            text-align: center;
        }
        .modal-page img {
            max-width: 100%;
            max-height: calc(90vh - 150px);
            object-fit: contain;
        }
        .metadata-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        @media (max-width: 640px) {
            .metadata-grid {
                grid-template-columns: 1fr;
            }
        }
        .metadata-card {
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 12px;
        }
        .metadata-title {
            font-weight: 600;
            color: #172144;
            margin-bottom: 10px;
            font-size: 14px;
        }
        .metadata-field {
            margin-bottom: 8px;
            font-size: 13px;
        }
        .metadata-label {
            color: #999;
            font-size: 11px;
            text-transform: uppercase;
        }
        .metadata-value {
            color: #172144;
            word-break: break-word;
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
                grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
                gap: 10px;
            }
            .modal-header {
                padding: 12px;
            }
            .modal-controls {
                width: 100%;
                justify-content: space-between;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 El Paso PD - Forensic Document Analyzer</h1>
            <p style="font-size: 14px; opacity: 0.9;">Police Department evidence documents with page-by-page viewer</p>
        </div>
        <div class="tabs">
            <button class="tab-button active" onclick="switchTab('gallery')">Document Gallery</button>
            <button class="tab-button" onclick="switchTab('metadata')">Document Metadata</button>
        </div>
        <div id="gallery" class="tab-content active"></div>
        <div id="metadata" class="tab-content"></div>
    </div>
    
    <div id="pageModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title" id="pageModalTitle"></div>
                <div class="modal-controls">
                    <button class="modal-button" id="prevBtn" onclick="previousPage()">← Prev</button>
                    <div class="page-counter" id="pageCounter"></div>
                    <button class="modal-button" id="nextBtn" onclick="nextPage()">Next →</button>
                    <button class="close-btn" onclick="closePageModal()">✕</button>
                </div>
            </div>
            <div class="modal-page" id="pageContainer"></div>
        </div>
    </div>
    
    <script>
        const documentData = DOCUMENT_DATA_PLACEHOLDER;
        let currentDocumentIndex = null;
        let currentPageIndex = 0;
        
        function renderGallery() {
            const galleryDiv = document.getElementById('gallery');
            let html = '';
            const datedDocs = documentData.filter(d => d.CreationDateEmbedded !== 'Unknown');
            const undatedDocs = documentData.filter(d => d.CreationDateEmbedded === 'Unknown');
            
            datedDocs.forEach((doc) => {
                const actualIndex = documentData.indexOf(doc);
                html += `<div class="gallery-item" onclick="openDocument(${actualIndex})">
                    ${doc.previewUri ? `<img src="${doc.previewUri}" class="gallery-preview">` : ''}
                    <div class="gallery-info">
                        <div class="gallery-title">${escapeHtml(doc.FileName)}</div>
                        <div class="gallery-pages">${doc.pageCount} pages</div>
                    </div></div>`;
            });
            
            if (undatedDocs.length > 0) {
                html += '<div class="divider"><span>⚠️ DOCUMENTS WITHOUT ORIGINAL DATES</span></div>';
                undatedDocs.forEach((doc) => {
                    const actualIndex = documentData.indexOf(doc);
                    html += `<div class="gallery-item" onclick="openDocument(${actualIndex})" style="opacity: 0.7;">
                        ${doc.previewUri ? `<img src="${doc.previewUri}" class="gallery-preview">` : ''}
                        <div class="gallery-info">
                            <div class="gallery-title">${escapeHtml(doc.FileName)}</div>
                            <div class="gallery-pages">${doc.pageCount} pages</div>
                        </div></div>`;
                });
            }
            const container = document.createElement('div');
            container.className = 'gallery';
            container.innerHTML = html;
            galleryDiv.innerHTML = '';
            galleryDiv.appendChild(container);
        }
        
        function renderMetadata() {
            const metadataDiv = document.getElementById('metadata');
            let html = '';
            documentData.forEach(doc => {
                html += `<div class="metadata-card">
                    <div class="metadata-title">${escapeHtml(doc.FileName)}</div>
                    <div class="metadata-field"><div class="metadata-label">Original Date</div><div class="metadata-value">${doc.CreationDateEmbedded}</div></div>
                    <div class="metadata-field"><div class="metadata-label">Total Pages</div><div class="metadata-value">${doc.pageCount}</div></div>
                    <div class="metadata-field"><div class="metadata-label">Embedded Pages</div><div class="metadata-value">${doc.embeddedPages}</div></div>
                    <div class="metadata-field"><div class="metadata-label">File Size</div><div class="metadata-value">${(doc.fileSize / (1024 * 1024)).toFixed(2)} MB</div></div>
                    <div class="metadata-field"><div class="metadata-label">Author</div><div class="metadata-value">${doc.DocumentAuthor}</div></div>
                </div>`;
            });
            metadataDiv.innerHTML = `<div class="metadata-grid">${html}</div>`;
        }
        
        function openDocument(index) {
            currentDocumentIndex = index;
            currentPageIndex = 0;
            displayPage();
            document.getElementById('pageModal').classList.add('active');
        }
        
        function closePageModal() {
            document.getElementById('pageModal').classList.remove('active');
        }
        
        function displayPage() {
            const doc = documentData[currentDocumentIndex];
            const page = doc.pages[currentPageIndex];
            document.getElementById('pageModalTitle').textContent = escapeHtml(doc.FileName);
            document.getElementById('pageCounter').textContent = `Page ${currentPageIndex + 1} of ${doc.embeddedPages}`;
            document.getElementById('pageContainer').innerHTML = `<img src="${page.dataUri}">`;
            document.getElementById('prevBtn').disabled = currentPageIndex === 0;
            document.getElementById('nextBtn').disabled = currentPageIndex === doc.pages.length - 1;
        }
        
        function previousPage() {
            if (currentPageIndex > 0) { currentPageIndex--; displayPage(); }
        }
        
        function nextPage() {
            if (currentPageIndex < documentData[currentDocumentIndex].pages.length - 1) { currentPageIndex++; displayPage(); }
        }
        
        function switchTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            if (tabName === 'metadata') renderMetadata();
        }
        
        function escapeHtml(text) {
            const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
            return String(text).replace(/[&<>"']/g, m => map[m]);
        }
        
        document.addEventListener('keydown', (e) => {
            if (document.getElementById('pageModal').classList.contains('active')) {
                if (e.key === 'ArrowLeft') previousPage();
                if (e.key === 'ArrowRight') nextPage();
                if (e.key === 'Escape') closePageModal();
            }
        });
        
        renderGallery();
    </script>
</body>
</html>'''

html_content = html_template.replace('DOCUMENT_DATA_PLACEHOLDER', json.dumps(document_array, ensure_ascii=False))

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
print(f"✅ Document app created: {OUTPUT_FILE}")
print(f"   Size: {file_size_mb:.1f} MB")
print(f"   Documents: {len(document_array)}")
print(f"   Pages embedded: {total_pages}")
