# CLAUDE.md - Digital Evidence Gallery Generator

**Project**: Digital Evidence Gallery Generator
**Version**: 1.0.0
**Last Updated**: 2026-01-26
**For**: AI Assistants (Claude, ChatGPT, etc.)

---

## 🎯 Project Purpose

This project generates professional forensic evidence galleries for law enforcement agencies. It transforms raw digital evidence (photographs with EXIF data and PDF documents) into responsive, self-contained web applications suitable for legal proceedings.

**Key Principle**: NEVER modify original evidence. Always work with copies. Maintain complete chain of custody.

---

## 🚀 Quick Context for AI Sessions

### When User Says:
- **"Process evidence for [case/agency]"** → Follow Evidence Processing Protocol
- **"Create evidence gallery"** → Use generate_unified_portal.py
- **"Lazy loading version"** → Use lazy loading mode (faster)
- **"Single file version"** → Use single-file mode (easier distribution)
- **"Optimize the PDFs"** → Apply document optimization settings
- **"Fix the layout"** → Check modal CSS (metadata sidebar positioning)
- **"Add another agency"** → Multi-agency processing workflow

### Critical Files to Read First:
1. **This file** (CLAUDE.md) - Project guidance
2. **README.md** - Project overview
3. **docs/protocols/EVIDENCE_PROCESSING.md** - Standard operating procedure
4. **docs/guides/QUICK_START.md** - Basic workflow

---

## 📁 Project Structure

```
Digital-Evidence-Gallery-Generator/
├── scripts/                           # Python generators
│   ├── generate_unified_portal.py     # Main generator (lazy loading)
│   ├── generate_single_file_portal.py # Single-file generator
│   ├── generate_image_gallery.py      # Images only
│   └── generate_document_gallery.py   # Documents only
│
├── docs/                              # Documentation
│   ├── guides/                        # User guides
│   ├── protocols/                     # SOPs and protocols
│   ├── architecture/                  # Technical design
│   └── examples/                      # Samples and tutorials
│
├── templates/                         # HTML/CSS templates
├── input/                             # Evidence input (gitignored)
├── output/                            # Generated galleries (gitignored)
└── examples/                          # Sample evidence
```

---

## 🔧 Standard Workflows

### Workflow 1: Process Single Agency Evidence

```bash
# 1. Create case folder
mkdir -p input/YYYYMMDD-AgencyAbbrev-CaseNum/{photos,documents}

# 2. Copy evidence (NEVER move originals!)
cp -pr /path/to/evidence/photos/* input/CASE/photos/
cp -pr /path/to/evidence/documents/* input/CASE/documents/

# 3. Generate lazy loading portal (recommended)
python3 scripts/generate_unified_portal.py \
  --agency "Agency Name" \
  --photos input/CASE/photos/ \
  --documents input/CASE/documents/ \
  --output output/CASE/ \
  --lazy-loading \
  --brand-color "#172144"

# 4. Or generate single-file portal (for distribution)
python3 scripts/generate_single_file_portal.py \
  --agency "Agency Name" \
  --photos input/CASE/photos/ \
  --documents input/CASE/documents/ \
  --output output/CASE/ \
  --optimized
```

### Workflow 2: Process Multi-Agency Evidence

```bash
# Process Agency A
python3 scripts/generate_unified_portal.py \
  --agency "County Attorney" \
  --photos input/agency-a/photos/ \
  --documents input/agency-a/documents/ \
  --output output/case-001/

# Process Agency B (append to existing portal)
python3 scripts/generate_unified_portal.py \
  --agency "El Paso PD" \
  --photos input/agency-b/photos/ \
  --documents input/agency-b/documents/ \
  --output output/case-001/ \
  --append
```

---

## ⚙️ Configuration & Customization

### Brand Colors

**Default Brand Color**: #172144 (deep navy blue)

**To Change**:
Edit scripts and replace `#172144` with your color, or use CLI:
```bash
python3 scripts/generate_unified_portal.py \
  --brand-color "#your-hex-color"
```

**Color Usage**:
- **Body Text**: Brand color for all body text
- **Headers/Tabs**: Brand color background with white text
- **Borders/Accents**: Light grays for contrast
- **Hover States**: Darker shade of brand color

### Optimization Settings

**Image Optimization** (in scripts):
```python
# Default settings
resize_percent = 0.5      # 50% resolution
jpeg_quality = 75         # High quality for forensic review
thumbnail_size = (150, 150)
thumbnail_quality = 40
```

**Document Optimization**:
```python
# Default settings
dpi = 150                 # Screen-optimized DPI
jpeg_quality = 60         # Aggressive compression
max_pages_huge = 50       # Files > 20 MB
max_pages_large = 75      # Files 5-20 MB
max_pages_small = 100     # Files < 5 MB
```

**To Adjust Quality**:
- **Higher Quality**: Increase DPI to 200, quality to 75
- **Smaller Files**: Decrease DPI to 100, quality to 50
- **Balance** (current): DPI 150, quality 60

---

## 🎯 Common Tasks

### Task 1: Fix Modal Layout Issues

**Problem**: Modal display broken on desktop or mobile

**Solution**: Check CSS in lazy loading portal

**Key CSS**:
```css
/* Desktop: Metadata LEFT, Image RIGHT */
@media (min-width: 768px) {
    .modal-content {
        flex-direction: row-reverse;  /* This puts metadata on left */
        width: 90vw;
        height: 85vh;
    }
}

/* Fixed modal on large screens */
@media (min-width: 1200px) {
    .modal-content {
        width: 1000px;
        height: 700px;
    }
}

/* Metadata sidebar (LEFT on desktop) */
.modal-meta {
    flex: 0 0 350px;           /* Fixed 350px width */
    border-right: 1px solid #e0e0e0;  /* Border on RIGHT side */
}

/* Image display (RIGHT on desktop) */
.modal-image {
    flex: 1 1 60%;            /* Takes 60% of modal */
}
```

**Common Fixes**:
1. **Title too large**: Check `modal-title` has `text-overflow: ellipsis`
2. **Metadata too narrow**: Increase `flex: 0 0 350px` to 400px or more
3. **Image too large**: Adjust `flex: 1 1 60%` to smaller percent
4. **Mobile broken**: Check `@media (max-width: 767px)` for column stacking

### Task 2: Reduce File Size

**Problem**: Portal file too large for distribution

**Solutions**:

**A. Use Lazy Loading** (Best):
- Initial file: 3-10 MB
- Total data: 100-500 MB (loaded on-demand)
- 98% faster initial load

**B. Reduce Document Pages**:
```python
# In scripts/generate_single_file_portal.py
max_pages_huge = 25      # Was: 50
max_pages_large = 40     # Was: 75
max_pages_small = 50     # Was: 100
```

**C. Lower Image Quality**:
```python
resize_percent = 0.4     # Was: 0.5 (40% resolution)
jpeg_quality = 65        # Was: 75 (slightly more compression)
```

**D. Compress with 7-Zip**:
```bash
7z a -mx=9 evidence_portal.7z output/case-folder/
# Result: ~30-50% additional compression
```

### Task 3: Add New Evidence to Existing Portal

**Scenario**: More evidence discovered after initial processing

**Steps**:
```bash
# 1. Copy new evidence to input folder
cp /path/to/new/photos/* input/case-001/photos/

# 2. Regenerate portal (will include all evidence)
python3 scripts/generate_unified_portal.py \
  --agency "Agency Name" \
  --photos input/case-001/photos/ \
  --documents input/case-001/documents/ \
  --output output/case-001/ \
  --lazy-loading
```

**Note**: Portal regenerates from scratch. All previous evidence + new evidence included.

### Task 4: Create PDF Summary Report

**Scenario**: User wants printable PDF summary of evidence

**Approach**:
```bash
# Generate portal first
python3 scripts/generate_unified_portal.py [options]

# Convert to PDF using headless Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless \
  --disable-gpu \
  --print-to-pdf=output/evidence_summary.pdf \
  file:///path/to/unified-forensic-portal.html
```

---

## 🚨 Critical Rules for AI Assistants

### Evidence Handling (ABSOLUTELY CRITICAL)

❌ **NEVER** modify files in these directories:
- `/Volumes/HOLE-RAID-DRIVE/Projects/Digital-Forensics/Exif-Project/*/`
- Any folder containing original evidence
- Files marked as "original" or "source"

✅ **ALWAYS** work with copies:
- Copy evidence to `input/` folder first
- Process from `input/` → generate to `output/`
- Never touch originals

❌ **NEVER** delete original evidence files

✅ **ALWAYS** document processing:
- Create PROCESSING_LOG.txt
- Update CHAIN_OF_CUSTODY.txt
- Generate checksums

### Code Modification Rules

✅ **You MAY**:
- Modify scripts in `scripts/` directory
- Update CSS styles for better responsiveness
- Add new features to generators
- Create new utility scripts
- Improve documentation

❌ **NEVER** without user approval:
- Change default optimization settings (could affect quality)
- Modify data structures (breaks existing portals)
- Remove metadata fields (breaks forensic integrity)
- Change file naming conventions (breaks protocols)

### When User Reports Layout Issues

**Step 1**: Ask for screenshot and browser info

**Step 2**: Identify the issue
- Desktop modal layout? → Check `.modal-content` flex settings
- Mobile stacking? → Check `@media (max-width: 767px)`
- Title overflow? → Check `.modal-title` text-overflow
- Metadata too narrow? → Adjust `.modal-meta` flex-basis

**Step 3**: Test fix on the specific portal file user is viewing
- Don't regenerate unnecessarily
- Edit the output HTML directly for testing
- Update generator script once fix confirmed

**Step 4**: Update generator script for future cases

---

## 🎨 Design System

### Layout Specifications

**Modal Dimensions** (Desktop 1200px+):
- Modal: 1000px × 700px
- Metadata Sidebar: 350px (left side)
- Image Display: 650px (~60% of modal)

**Modal Layout** (Tablet/Desktop 768px+):
```
flex-direction: row-reverse
  ├─ .modal-meta (left): 350px fixed
  └─ .modal-image (right): remaining space (~650px)
```

**Modal Layout** (Mobile <768px):
```
flex-direction: column
  ├─ .modal-image (top): auto height
  └─ .modal-meta (bottom): max 200px
```

### Responsive Grid

**Gallery Grid**:
- Mobile (<480px): 2 columns
- Small Tablet (480-640px): 3 columns
- Tablet (640-1024px): 4 columns
- Desktop (1024px+): 5-6 columns

**Grid CSS**:
```css
grid-template-columns: repeat(auto-fill, minmax(Xpx, 1fr))
```

Where X varies by breakpoint: 100px (mobile) → 180px (desktop)

---

## 🧪 Testing Checklist for AI Assistants

Before delivering modified code to user:

### Functional Testing
- [ ] Gallery renders on desktop
- [ ] Gallery renders on mobile (test with browser DevTools)
- [ ] Images open in modal correctly
- [ ] Documents open with page navigation
- [ ] Agency filters work
- [ ] Keyboard navigation works (arrows, Escape)
- [ ] Previous/Next buttons work
- [ ] Metadata displays correctly

### Responsive Testing
- [ ] Mobile (375px width) - vertical stacking
- [ ] Tablet (768px width) - side-by-side layout
- [ ] Desktop (1200px+ width) - fixed modal dimensions
- [ ] Modal resizes appropriately
- [ ] Text remains readable at all sizes

### Quality Assurance
- [ ] All EXIF metadata present
- [ ] All PDF metadata present
- [ ] Chronological sorting correct
- [ ] Agency badges show correct agencies
- [ ] File counts match input evidence
- [ ] No broken images or missing pages

---

## 📊 Performance Expectations

### Processing Times (M1 MacBook Pro)

| Evidence Size | Processing Time | Output Size (Lazy) | Output Size (Single) |
|---------------|-----------------|-------------------|----------------------|
| Small (10/5) | 2-5 min | 20-50 MB | 25-60 MB |
| Medium (50/20) | 10-20 min | 100-200 MB | 100-250 MB |
| Large (100/50) | 20-40 min | 250-500 MB | 250-600 MB |
| Massive (500/100) | 1-2 hours | 1-2 GB | Not recommended |

**Legend**: Photos/Documents

### Load Time Expectations

| Portal Type | Initial Load | First Click | Subsequent |
|-------------|--------------|-------------|------------|
| Lazy Loading | 1-3 sec | 2-5 sec | Instant |
| Single-File Optimized | 5-15 sec | Instant | Instant |
| Single-File Original | 15-30 sec | Instant | Instant |

---

## 🔍 Troubleshooting Guide for AI

### Issue: "Modal layout broken on desktop"

**Symptoms**:
- Header takes whole screen
- Metadata too narrow
- Image too large or missing

**Diagnosis**:
```bash
# Check if modal-content has proper flex settings
grep -A 20 "\.modal-content" output/portal.html
```

**Fix**:
```css
/* Ensure these settings exist */
@media (min-width: 768px) {
    .modal-content {
        flex-direction: row-reverse;  /* Metadata left, image right */
        width: 90vw;
        height: 85vh;
    }
}

.modal-meta {
    flex: 0 0 350px;                  /* Fixed width sidebar */
    border-right: 1px solid #e0e0e0;  /* Border on right */
}

.modal-image {
    flex: 1 1 60%;                    /* Takes remaining space */
}
```

### Issue: "File size too large"

**Diagnosis**:
```bash
# Check output file sizes
du -sh output/case-folder/*

# Identify large components
ls -lh output/case-folder/
```

**Solutions** (in order of preference):
1. Use lazy loading instead of single-file
2. Reduce max pages per document (50 → 25)
3. Lower document DPI (150 → 100)
4. Lower JPEG quality (60 → 50)
5. Exclude very large PDFs from processing

### Issue: "Lazy loading won't work"

**Common Causes**:
1. **CORS Error**: Browser security prevents loading JSON from file://
   - **Solution**: Use web server (python -m http.server)
2. **File paths wrong**: JSON files not in same directory as HTML
   - **Solution**: Ensure all 4 files in same folder
3. **JSON syntax error**: Malformed JSON data
   - **Solution**: Validate JSON with `python3 -m json.tool file.json`

### Issue: "Missing metadata"

**Diagnosis**:
```bash
# Check if exiftool extracted metadata
cat input/case-folder/metadata_images.csv

# Verify EXIF data exists in original files
exiftool input/case-folder/photos/image.jpg | grep DateTimeOriginal
```

**Solutions**:
1. **No EXIF data**: Some images don't have EXIF (screenshots, edited photos)
   - System will show "Unknown" - this is correct behavior
2. **Extraction failed**: Re-run exiftool
3. **CSV parsing error**: Check CSV format, look for special characters

---

## 🎯 Common User Requests & How to Handle

### "Make it responsive"
✅ Already is! If broken:
- Check CSS media queries exist
- Verify viewport meta tag: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- Test with browser DevTools mobile emulation

### "Use my brand colors"
✅ Edit brand color parameter or replace `#172144` throughout:
```bash
# Global find and replace
sed -i '' 's/#172144/#NewColor/g' scripts/generate_unified_portal.py
```

### "Optimize file size"
✅ Three approaches:
1. Use lazy loading (best)
2. Reduce quality settings (acceptable)
3. Limit pages more aggressively (last resort)

### "Add another agency"
✅ Multi-agency support built-in:
- Process each agency separately
- Use `--append` flag for second+ agencies
- Portal automatically creates agency filters

### "Create PDF version"
✅ Use headless Chrome to print:
```bash
chrome --headless --print-to-pdf=output.pdf portal.html
```

---

## 🚨 Critical Warnings for AI

### What NOT to Do

❌ **NEVER delete files** from:
- `/Volumes/HOLE-RAID-DRIVE/Projects/Digital-Forensics/Exif-Project/`
- Any directory containing original evidence
- Archive folders

❌ **NEVER modify files** in:
- Evidence source directories
- Input folders marked as "original"

❌ **NEVER commit** to git:
- Actual evidence files (photos, documents)
- Processing logs with case details
- Chain of custody documents
- Checksums of actual evidence

✅ **ALWAYS** in git:
- Scripts and source code
- Documentation
- Templates
- Example/sample files only

### Sensitive Information

**Evidence Contains**:
- Crime scene photographs
- Victim information
- Witness statements
- Medical reports
- Personal identifying information (PII)

**AI Responsibilities**:
- Treat all evidence as confidential
- Don't reference specific evidence content
- Focus on technical processing, not case details
- Maintain professional objectivity
- Remind user about privacy/security when distributing

---

## 📚 Documentation Hierarchy

**Quick Reference** (read first):
1. CLAUDE.md (this file) - AI guidance
2. README.md - Project overview

**Operational** (for processing cases):
1. docs/guides/QUICK_START.md - Step-by-step guide
2. docs/protocols/EVIDENCE_PROCESSING.md - Standard procedure
3. docs/protocols/CHAIN_OF_CUSTODY.md - Forensic integrity

**Technical** (for development):
1. docs/architecture/SYSTEM_DESIGN.md - Architecture details
2. scripts/ source code - Implementation

**Examples** (for learning):
1. docs/examples/SAMPLE_WORKFLOW.md - Example cases
2. examples/ - Sample evidence files

---

## 🔄 Update Protocol

### When User Requests Changes

**Step 1**: Understand the requirement
- What needs to change?
- Why is it needed?
- What's the expected behavior?

**Step 2**: Identify affected components
- Generator scripts?
- HTML/CSS templates?
- Documentation?

**Step 3**: Make changes
- Update code/templates
- Test with sample evidence
- Update documentation if behavior changed

**Step 4**: Validate
- Run automated tests (if available)
- Manual testing on sample case
- Browser compatibility check

**Step 5**: Document
- Update CHANGELOG.md
- Add notes to relevant docs
- Update version number if significant

---

## 🎓 Learning Resources

### For Understanding the Codebase
1. Start with scripts/generate_unified_portal.py
2. Review HTML template structure
3. Understand lazy loading implementation
4. Study responsive CSS patterns

### For Evidence Processing
1. Read Evidence Processing Protocol
2. Follow sample workflow
3. Process example evidence
4. Review generated output

### For Troubleshooting
1. Check common issues in this file
2. Review error messages in processing logs
3. Test with minimal evidence set
4. Isolate problem (images vs documents, specific files)

---

## 🎯 Success Criteria

A successful AI session should result in:
- ✅ Working portal (tested in browser)
- ✅ Responsive layout (mobile and desktop)
- ✅ All metadata preserved
- ✅ Professional appearance
- ✅ Documentation updated if changes made
- ✅ User satisfied with result
- ✅ Original evidence untouched

---

## 📞 When to Ask User for Clarification

Ask user if:
- Brand color not specified (suggest #172144)
- Portal type unclear (lazy vs single-file)
- Evidence directories contain unexpected file types
- Quality/size tradeoff unclear
- Layout preferences ambiguous
- Multi-agency processing order unclear

Don't ask about:
- Standard optimization settings (use defaults)
- File structure (follow docs/protocols/)
- CSS implementation details (use established patterns)
- Naming conventions (follow YYYYMMDD-Agency-CaseNum)

---

## 🚀 Quick Command Reference

```bash
# Generate lazy loading portal (fastest load)
python3 scripts/generate_unified_portal.py \
  --agency "Agency Name" \
  --photos input/CASE/photos/ \
  --documents input/CASE/documents/ \
  --output output/CASE/ \
  --lazy-loading

# Generate single-file portal (easy distribution)
python3 scripts/generate_single_file_portal.py \
  --agency "Agency Name" \
  --photos input/CASE/photos/ \
  --documents input/CASE/documents/ \
  --output output/CASE/

# Start web server for lazy loading portal
cd output/CASE/
python3 -m http.server 8000

# Validate evidence integrity
shasum -a 256 input/CASE/photos/* > checksums.txt

# Generate delivery documentation
python3 scripts/create_delivery_docs.py --case-folder output/CASE/
```

---

**This project is designed for law enforcement and legal professionals. Maintain the highest standards of forensic integrity and chain of custody.**

---

*CLAUDE.md - Digital Evidence Gallery Generator v1.0.0*
*Last Updated: 2026-01-26*
*For AI Assistant Use*
