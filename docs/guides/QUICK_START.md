# Quick Start Guide - Digital Evidence Gallery Generator

**Time to First Portal**: 5-10 minutes
**Difficulty**: Beginner-friendly

---

## 🎯 Overview

This guide will walk you through creating your first forensic evidence gallery in just a few steps.

---

## Prerequisites

Before you begin, ensure you have:
- [ ] Python 3.10 or higher installed
- [ ] Evidence files ready (JPG photos and/or PDF documents)
- [ ] 500 MB+ free disk space
- [ ] Modern web browser installed

---

## Step 1: Install Dependencies (2 minutes)

### macOS
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install exiftool
brew install exiftool

# Install Python packages
pip3 install Pillow PyMuPDF
```

### Linux (Debian/Ubuntu)
```bash
# Install exiftool
sudo apt-get update
sudo apt-get install libimage-exiftool-perl

# Install Python packages
pip3 install Pillow PyMuPDF
```

### Windows
```powershell
# Download exiftool from: https://exiftool.org/
# Extract and add to PATH

# Install Python packages
pip install Pillow PyMuPDF
```

---

## Step 2: Prepare Your Evidence (3 minutes)

### Create Evidence Folders

```bash
cd Digital-Evidence-Gallery-Generator

# Create folders for your case
mkdir -p input/my-case-name/photos
mkdir -p input/my-case-name/documents
```

### Copy Evidence Files

```bash
# Copy photographs (JPG, JPEG, PNG)
cp /path/to/evidence/photos/*.JPG input/my-case-name/photos/

# Copy documents (PDF)
cp /path/to/evidence/documents/*.pdf input/my-case-name/documents/
```

---

## Step 3: Generate Your Portal (2 minutes)

### Option A: Lazy Loading (Fastest Load Time) ⭐ Recommended

```bash
python3 scripts/generate_unified_portal.py \
  --agency "My Agency Name" \
  --photos input/my-case-name/photos/ \
  --documents input/my-case-name/documents/ \
  --output output/my-case/ \
  --lazy-loading
```

**Result**: 3.4 MB main file + separate data files
**Load Time**: 1-3 seconds
**Requires**: Web server for deployment

### Option B: Single-File (Easy Distribution)

```bash
python3 scripts/generate_unified_portal.py \
  --agency "My Agency Name" \
  --photos input/my-case-name/photos/ \
  --documents input/my-case-name/documents/ \
  --output output/my-case/ \
  --single-file
```

**Result**: Single HTML file (~50-200 MB depending on evidence)
**Load Time**: 5-15 seconds
**Requires**: Nothing (just open in browser)

---

## Step 4: View Your Portal (30 seconds)

### Lazy Loading Portal
```bash
# Start a simple web server
cd output/my-case/
python3 -m http.server 8000

# Open in browser: http://localhost:8000/unified-forensic-portal-lazy.html
```

### Single-File Portal
```bash
# Just open the file
open output/my-case/unified-forensic-portal.html
```

---

## 🎉 You're Done!

You now have a professional forensic evidence gallery with:
- ✅ All photographs with complete EXIF metadata
- ✅ All documents with page-by-page navigation
- ✅ Responsive design for any device
- ✅ Professional appearance
- ✅ Complete metadata preservation

---

## 🔄 Next Steps

### Customize Your Portal
- Edit `templates/config.json` to change colors
- Adjust optimization settings for quality vs. size
- Add agency logos or branding elements

### Process Multiple Agencies
```bash
# Process Agency A
python3 scripts/generate_unified_portal.py \
  --agency "Agency A" \
  --photos input/agency-a/photos/ \
  --documents input/agency-a/documents/ \
  --output output/case-001/

# Process Agency B
python3 scripts/generate_unified_portal.py \
  --agency "Agency B" \
  --photos input/agency-b/photos/ \
  --documents input/agency-b/documents/ \
  --output output/case-001/ \
  --append
```

### Learn Advanced Features
- Read [Evidence Processing Protocol](../protocols/EVIDENCE_PROCESSING.md)
- Review [System Design](../architecture/SYSTEM_DESIGN.md)
- Explore [Use Cases](../examples/USE_CASES.md)

---

## 🆘 Common Issues

### "exiftool: command not found"
**Solution**: Install exiftool (see Step 1)

### "No module named 'PIL'"
**Solution**: `pip3 install Pillow`

### "No module named 'fitz'"
**Solution**: `pip3 install PyMuPDF`

### Portal won't load in browser
**Solution**:
- For lazy loading: Must use web server (see Step 4)
- For single-file: Try different browser or drag file to browser window

### PDFs not displaying
**Solution**: Check that PDF files aren't corrupted. Run:
```bash
python3 scripts/validate_evidence.py input/my-case-name/documents/
```

---

## 📊 Example Output

### Command Line Output
```
================================================================================
UNIFIED FORENSIC EVIDENCE PORTAL GENERATOR
================================================================================

Processing evidence from: Agency Name

Extracting metadata...
  ✅ Image metadata extracted (23 photos)
  ✅ PDF metadata extracted (15 documents)

Processing images...
  ✅ County Attorney: 23 images processed

Processing documents...
  ✅ County Attorney: 15 documents, 342 pages embedded

Generating HTML portal with lazy loading...

✅ Portal created!
  Main HTML: 3.4 MB
  Images Data: 5.2 MB
  Documents Data: 87.3 MB
  Total: 95.9 MB

🎯 Access: output/my-case/unified-forensic-portal-lazy.html
================================================================================
```

---

## 💡 Pro Tips

1. **Organize evidence by agency** - Keep separate folders for multi-agency cases
2. **Use descriptive names** - Name evidence folders by case number
3. **Test with samples first** - Use the examples/ folder to test before processing real evidence
4. **Keep originals** - Never delete original evidence files
5. **Document everything** - Add notes in output folders about processing dates
6. **Version control** - Git commit after each case processed

---

## 🎓 What's Next?

**Learn the full workflow**:
→ Read [Evidence Processing Protocol](../protocols/EVIDENCE_PROCESSING.md)

**Understand the system**:
→ Review [System Design](../architecture/SYSTEM_DESIGN.md)

**See real examples**:
→ Explore [Sample Workflow](../examples/SAMPLE_WORKFLOW.md)

---

**Need help?** See [Troubleshooting Guide](TROUBLESHOOTING.md) or review the [Protocol Documentation](../protocols/)

---

*Quick Start Guide - Digital Evidence Gallery Generator v1.0.0*
