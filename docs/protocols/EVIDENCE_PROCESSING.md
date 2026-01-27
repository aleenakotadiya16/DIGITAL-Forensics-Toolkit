# Evidence Processing Protocol

**Version**: 1.0.0
**Effective Date**: 2026-01-26
**Review Frequency**: Quarterly
**Document Owner**: Digital Forensics Team

---

## 🎯 Purpose

This protocol establishes standardized procedures for processing digital evidence (photographs and documents) into forensic evidence galleries. Following this protocol ensures:

- Consistent quality across all cases
- Complete metadata preservation
- Forensic integrity maintained
- Legal admissibility standards met
- Reproducible results

---

## 📋 Standard Operating Procedure

### Phase 1: Evidence Intake (15-30 minutes)

#### 1.1 Create Case Folder
```bash
# Navigate to project
cd Digital-Evidence-Gallery-Generator

# Create case folder with standardized naming
# Format: YYYYMMDD-AgencyAbbrev-CaseNumber
mkdir -p input/20260126-EPPD-23-262207

# Create evidence subdirectories
mkdir -p input/20260126-EPPD-23-262207/photos
mkdir -p input/20260126-EPPD-23-262207/documents
```

**Naming Convention**:
- Date: YYYYMMDD format
- Agency: Standard abbreviation (EPPD, CAPD, SDSO, etc.)
- Case Number: Official case identifier

#### 1.2 Copy Evidence Files
```bash
# Copy original evidence (NEVER move - always copy)
cp -r /path/to/original/photos/* input/20260126-EPPD-23-262207/photos/
cp -r /path/to/original/documents/* input/20260126-EPPD-23-262207/documents/

# Verify file count
echo "Photos: $(ls input/20260126-EPPD-23-262207/photos/ | wc -l)"
echo "Documents: $(ls input/20260126-EPPD-23-262207/documents/*.pdf | wc -l)"
```

**Critical Rules**:
- ✅ ALWAYS copy (never move) original evidence
- ✅ Maintain original file names
- ✅ Preserve file timestamps
- ✅ Do NOT modify original files
- ❌ NEVER delete originals

#### 1.3 Document Chain of Custody
Create `input/20260126-EPPD-23-262207/CHAIN_OF_CUSTODY.txt`:
```
CHAIN OF CUSTODY LOG
Case: 23-262207
Agency: El Paso Police Department
Processing Date: 2026-01-26
Processor: [Your Name]
Original Evidence Location: /Volumes/Evidence/EPPD-23-262207
Files Copied: 19 photos, 20 PDF documents
Original File Hashes: [See checksums.txt]
Processing Purpose: Digital evidence gallery generation
Next Custodian: [Recipient Name]
```

---

### Phase 2: Evidence Validation (10-15 minutes)

#### 2.1 Verify File Integrity
```bash
# Check for corrupted files
python3 scripts/validate_evidence.py input/20260126-EPPD-23-262207/

# Generate checksums for audit trail
cd input/20260126-EPPD-23-262207/photos/
shasum -a 256 * > ../photo_checksums.txt

cd ../documents/
shasum -a 256 *.pdf > ../document_checksums.txt
```

**Validation Checks**:
- [ ] All files open without errors
- [ ] Image files contain valid EXIF data
- [ ] PDF files are readable
- [ ] No password-protected files
- [ ] File extensions match actual file types
- [ ] Checksums documented for audit trail

#### 2.2 Review Evidence Inventory
```bash
# Generate inventory report
python3 scripts/create_inventory.py input/20260126-EPPD-23-262207/
```

**Review Checklist**:
- [ ] Total file count matches expected
- [ ] File sizes within reasonable ranges
- [ ] Date ranges align with case timeline
- [ ] No duplicate files (unless intentional)
- [ ] All agencies properly identified

---

### Phase 3: Metadata Extraction (5-10 minutes)

#### 3.1 Extract Image Metadata
```bash
cd input/20260126-EPPD-23-262207/

# Extract EXIF data
exiftool -csv photos/*.JPG photos/*.JPEG > metadata_images.csv

# Verify extraction
echo "Metadata records: $(wc -l < metadata_images.csv)"
```

**EXIF Fields Extracted**:
- DateTimeOriginal (critical for timeline)
- Make and Model (camera identification)
- ISO, FNumber, ShutterSpeed (technical details)
- FocalLength (lens information)
- ImageWidth, ImageHeight (resolution)
- GPSLatitude, GPSLongitude (if available)

#### 3.2 Extract Document Metadata
```bash
# Extract PDF metadata
exiftool -csv documents/*.pdf > metadata_documents.csv

# Verify extraction
echo "Document metadata records: $(wc -l < metadata_documents.csv)"
```

**PDF Fields Extracted**:
- CreationDate (document creation timestamp)
- ModDate (last modification date)
- Author (document creator)
- Creator (application used)
- Producer (PDF generator)
- PageCount (total pages)

---

### Phase 4: Portal Generation (10-20 minutes)

#### 4.1 Choose Portal Type

**Decision Matrix**:

| Requirement | Portal Type | File Size | Load Time |
|-------------|-------------|-----------|-----------|
| Team investigation | Lazy Loading | 3-10 MB | 1-3 sec |
| USB distribution | Single-File Optimized | 50-200 MB | 5-15 sec |
| Court evidence | Single-File Optimized | 50-200 MB | 5-15 sec |
| Archival (max quality) | Single-File Original | 200-800 MB | 15-30 sec |

#### 4.2 Generate Lazy Loading Portal (Recommended)
```bash
python3 scripts/generate_unified_portal.py \
  --agency "El Paso Police Department" \
  --photos input/20260126-EPPD-23-262207/photos/ \
  --documents input/20260126-EPPD-23-262207/documents/ \
  --output output/20260126-EPPD-23-262207/ \
  --lazy-loading \
  --brand-color "#172144"
```

**Output Files**:
- `unified-forensic-portal-lazy.html` (3-10 MB)
- `images-data.json` (5-15 MB)
- `documents-data.json` (50-150 MB)
- `thumbnails-data.json` (2-5 MB)

#### 4.3 OR Generate Single-File Portal
```bash
python3 scripts/generate_unified_portal.py \
  --agency "El Paso Police Department" \
  --photos input/20260126-EPPD-23-262207/photos/ \
  --documents input/20260126-EPPD-23-262207/documents/ \
  --output output/20260126-EPPD-23-262207/ \
  --single-file \
  --optimized \
  --brand-color "#172144"
```

**Output Files**:
- `unified-forensic-portal-optimized.html` (50-200 MB)

---

### Phase 5: Quality Assurance (5-10 minutes)

#### 5.1 Visual Review Checklist
Open the generated portal and verify:

**Gallery View**:
- [ ] All thumbnails display correctly
- [ ] Agency badges show correct agency names
- [ ] File count matches input evidence
- [ ] Gallery grid is responsive
- [ ] Filter buttons work (All, Agency A, Agency B)

**Image Detail View**:
- [ ] Images display at good quality
- [ ] EXIF metadata is complete and accurate
- [ ] Date/time stamps are correct
- [ ] Camera information matches expectations
- [ ] Previous/Next navigation works
- [ ] Keyboard shortcuts work (arrow keys, Escape)

**Document Detail View**:
- [ ] Document pages render clearly
- [ ] Text is readable (test zooming)
- [ ] PDF metadata is complete
- [ ] Page counter is accurate
- [ ] Navigation buttons work
- [ ] Keyboard shortcuts work

#### 5.2 Technical Validation
```bash
# Run automated QA tests
python3 scripts/qa_validation.py output/20260126-EPPD-23-262207/

# Check output
# ✅ All metadata fields populated
# ✅ No broken image links
# ✅ File size within expected range
# ✅ HTML validates without errors
```

---

### Phase 6: Documentation & Delivery (10-15 minutes)

#### 6.1 Generate Delivery Package
```bash
# Create delivery documentation
python3 scripts/create_delivery_docs.py \
  --case-folder output/20260126-EPPD-23-262207/ \
  --case-number "23-262207" \
  --agency "El Paso Police Department" \
  --recipient "District Attorney's Office"
```

**Documents Created**:
- `README.md` - User guide
- `DELIVERY_SUMMARY.txt` - Technical specifications
- `EVIDENCE_INVENTORY.txt` - Complete file listing
- `PROCESSING_LOG.txt` - Processing details and timestamps

#### 6.2 Create Distribution Package
```bash
# For USB distribution
python3 scripts/package_for_distribution.py \
  --case-folder output/20260126-EPPD-23-262207/ \
  --format usb

# For email distribution (compressed)
python3 scripts/package_for_distribution.py \
  --case-folder output/20260126-EPPD-23-262207/ \
  --format email \
  --compress
```

---

## 📊 Example Workflow Timeline

**Complete Case Processing**: 40-75 minutes

| Phase | Time | Activity |
|-------|------|----------|
| **Setup** | 2 min | Install dependencies (one-time) |
| **Intake** | 15-30 min | Create folders, copy evidence, document chain |
| **Validation** | 10-15 min | Verify integrity, generate checksums |
| **Extraction** | 5-10 min | Extract EXIF and PDF metadata |
| **Generation** | 10-20 min | Generate portal (varies by evidence size) |
| **QA** | 5-10 min | Review output, test functionality |
| **Delivery** | 10-15 min | Create docs, package for distribution |

---

## 🎯 Real-World Example

### Scenario: Traffic Accident Investigation

**Evidence Received**:
- 23 photographs from officer's camera
- 5 witness statements (PDF)
- 2 medical reports (PDF)
- 1 accident reconstruction report (PDF)

**Processing Steps**:
```bash
# 1. Setup (3 min)
mkdir -p input/20260115-EPPD-ACC-12345/{photos,documents}

# 2. Copy evidence (5 min)
cp /Volumes/Evidence/ACC-12345/photos/*.JPG input/20260115-EPPD-ACC-12345/photos/
cp /Volumes/Evidence/ACC-12345/documents/*.pdf input/20260115-EPPD-ACC-12345/documents/

# 3. Generate portal (15 min)
python3 scripts/generate_unified_portal.py \
  --agency "El Paso Police Department" \
  --photos input/20260115-EPPD-ACC-12345/photos/ \
  --documents input/20260115-EPPD-ACC-12345/documents/ \
  --output output/ACC-12345/ \
  --single-file \
  --optimized

# 4. QA Review (5 min)
open output/ACC-12345/unified-forensic-portal-optimized.html
# Visual review, test navigation

# 5. Package for DA (5 min)
python3 scripts/create_delivery_docs.py \
  --case-folder output/ACC-12345/ \
  --case-number "ACC-12345" \
  --recipient "District Attorney"

# 6. Copy to USB (2 min)
cp -r output/ACC-12345/* /Volumes/USB-EVIDENCE/

# Total time: ~35 minutes
```

**Result**:
- Professional evidence gallery
- Complete metadata preservation
- Ready for legal proceedings
- Easy to distribute to DA, defense counsel

---

## 🔄 Updating an Existing Portal

If you need to add more evidence to an existing portal:

```bash
# Add new evidence to input folder
cp /path/to/new/evidence/*.JPG input/20260126-EPPD-23-262207/photos/

# Regenerate portal (use --append flag)
python3 scripts/generate_unified_portal.py \
  --agency "El Paso Police Department" \
  --photos input/20260126-EPPD-23-262207/photos/ \
  --documents input/20260126-EPPD-23-262207/documents/ \
  --output output/20260126-EPPD-23-262207/ \
  --lazy-loading \
  --append
```

---

## 📝 Best Practices

### Evidence Handling
1. **Never modify originals** - Always work with copies
2. **Document everything** - Chain of custody, processing steps
3. **Verify integrity** - Checksums before and after
4. **Test thoroughly** - QA review before delivery
5. **Keep backups** - Multiple copies in different locations

### File Organization
1. **Consistent naming** - Use YYYYMMDD-Agency-CaseNum format
2. **Separate by agency** - Different folders for multi-agency cases
3. **Clear structure** - photos/ and documents/ subdirectories
4. **Documentation** - README and processing logs in each case folder

### Quality Control
1. **Visual inspection** - Open every image and document
2. **Metadata verification** - Spot-check EXIF/PDF data accuracy
3. **Functionality testing** - Test all navigation and filtering
4. **Browser testing** - Test in Chrome, Firefox, Safari
5. **Mobile testing** - Verify responsive behavior

---

## ⚖️ Legal Considerations

### Admissibility Requirements

**Federal Rules of Evidence (FRE 901)**:
- Evidence must be authenticated
- Chain of custody documented
- Original files preserved
- Processing methods documented

**This Protocol Ensures**:
✅ Complete chain of custody documentation
✅ Original file preservation (never modified)
✅ Metadata extraction and retention
✅ Processing methodology documented
✅ Audit trail created

### Discovery Obligations

**Prosecution**:
- Provide complete evidence to defense
- Include all exculpatory evidence
- Document enhancement or modification
- Maintain original files

**Defense**:
- Review all provided evidence
- Verify metadata authenticity
- Request originals if needed
- Document any discrepancies

**This Protocol Supports**:
✅ Complete evidence disclosure
✅ Metadata transparency
✅ Original file availability
✅ Processing documentation

---

## 🔐 Security & Privacy

### Handling Sensitive Evidence

**Personally Identifiable Information (PII)**:
- Review evidence for PII before distribution
- Redact when necessary (create redacted version)
- Document redaction methodology
- Maintain unredacted version for court

**Victim Privacy**:
- Consider victim privacy in evidence sharing
- Protective orders may limit distribution
- Consult with prosecutors on sensitive cases
- Use encrypted channels for distribution

**Confidential Informants**:
- Redact identifying information
- Separate CI-related evidence
- Coordinate with prosecutors
- Document redactions

### Data Security
```bash
# Encrypt sensitive evidence packages
7z a -p -mhe=on evidence_package.7z output/case-folder/

# Secure file deletion of unencrypted copies
srm -v output/case-folder-unencrypted/
```

---

## 📊 Quality Assurance Checklist

### Pre-Processing QA
- [ ] All evidence files accessible and readable
- [ ] File integrity verified (not corrupted)
- [ ] Checksums documented
- [ ] Chain of custody documented
- [ ] Evidence count verified
- [ ] Duplicate files identified

### Post-Processing QA
- [ ] All input files processed successfully
- [ ] File count matches (input = output)
- [ ] Metadata extraction complete (100% success rate)
- [ ] Visual quality acceptable
- [ ] Navigation functions correctly
- [ ] Responsive design works on all devices
- [ ] Browser compatibility verified
- [ ] Documentation complete

### Pre-Delivery QA
- [ ] Final visual review completed
- [ ] All metadata verified accurate
- [ ] README and delivery docs created
- [ ] File sizes within expected range
- [ ] Portal tested by second person
- [ ] Chain of custody updated
- [ ] Delivery package assembled

---

## 🎓 Training Requirements

### Personnel Qualifications
**Required**:
- Basic computer literacy
- Understanding of digital evidence
- Familiarity with command line
- Knowledge of chain of custody requirements

**Recommended**:
- Digital forensics certification
- Legal evidence handling training
- Web technology basics
- Photography/imaging fundamentals

### Initial Training Checklist
- [ ] Complete Quick Start Guide tutorial
- [ ] Process sample evidence (examples/ folder)
- [ ] Review all protocol documentation
- [ ] Shadow experienced processor for 2-3 cases
- [ ] Process supervised case independently
- [ ] Pass competency assessment

---

## 🔄 Continuous Improvement

### Monthly Review
- Review processing times and identify bottlenecks
- Collect user feedback from prosecutors/investigators
- Update documentation based on lessons learned
- Test new browser versions for compatibility

### Quarterly Audit
- Review 10% of cases for protocol compliance
- Verify metadata accuracy
- Check chain of custody documentation
- Update procedures based on findings

### Annual Review
- Full protocol review and update
- Technology stack assessment
- Training material refresh
- Performance metrics analysis

---

## 📞 Support & Escalation

### Tier 1: Self-Service
- Review Quick Start Guide
- Check Troubleshooting documentation
- Search examples/ folder for similar cases

### Tier 2: Technical Support
- Contact digital forensics team
- Provide error logs and screenshots
- Share sample evidence files (if not sensitive)

### Tier 3: Development Team
- Complex technical issues
- Feature requests
- Protocol modifications
- System architecture changes

---

## 📋 Appendix A: Evidence Type Matrix

| Evidence Type | Supported | Metadata Extracted | Notes |
|---------------|-----------|-------------------|-------|
| JPEG photos | ✅ Yes | EXIF complete | Primary format |
| PNG images | ✅ Yes | Limited EXIF | Some metadata may be missing |
| HEIC images | ✅ Yes | EXIF complete | iPhone photos |
| PDF documents | ✅ Yes | Complete | All versions supported |
| TIFF images | ⚠️ Partial | EXIF complete | Large file sizes |
| Videos (MP4) | ❌ No | N/A | Not supported (future feature) |
| Audio files | ❌ No | N/A | Not supported |
| RAW photos | ❌ No | N/A | Convert to JPEG first |

---

## 📋 Appendix B: File Size Guidelines

### Expected Output Sizes

**Small Case** (10 photos, 5 documents):
- Lazy Loading: 2-5 MB main + 20-50 MB data
- Single-File: 25-60 MB
- Processing Time: 5-10 minutes

**Medium Case** (50 photos, 20 documents):
- Lazy Loading: 5-15 MB main + 80-200 MB data
- Single-File: 100-250 MB
- Processing Time: 15-30 minutes

**Large Case** (100+ photos, 50+ documents):
- Lazy Loading: 10-30 MB main + 200-500 MB data
- Single-File: 250-600 MB
- Processing Time: 30-60 minutes

**Massive Case** (500+ photos, 100+ documents):
- Lazy Loading: 30-100 MB main + 1-2 GB data
- Single-File: May exceed practical limits (use lazy loading)
- Processing Time: 1-3 hours

---

## 📋 Appendix C: Browser Compatibility

| Browser | Version | Status | Notes |
|---------|---------|--------|-------|
| Chrome | 90+ | ✅ Excellent | Best performance |
| Firefox | 88+ | ✅ Excellent | Full compatibility |
| Safari | 14+ | ✅ Excellent | macOS/iOS optimized |
| Edge | 90+ | ✅ Excellent | Chromium-based |
| Internet Explorer | Any | ❌ Not supported | Use modern browser |

---

## 🎯 Success Criteria

A successfully processed case meets all of these criteria:

- [x] All evidence files processed without errors
- [x] 100% metadata extraction success rate
- [x] Visual quality meets standards (readable, professional)
- [x] Navigation works on desktop and mobile
- [x] Browser compatibility verified (3+ browsers)
- [x] Chain of custody documented
- [x] Delivery documentation complete
- [x] QA checklist signed off
- [x] Recipient acknowledgment received

---

**This protocol ensures consistent, professional, forensically-sound evidence processing for all cases.**

---

*Evidence Processing Protocol v1.0.0 - Digital Evidence Gallery Generator*
*Last Updated: 2026-01-26*
