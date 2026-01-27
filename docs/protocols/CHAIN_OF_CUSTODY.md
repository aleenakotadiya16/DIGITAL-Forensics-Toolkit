# Chain of Custody Protocol

**Version**: 1.0.0
**Effective Date**: 2026-01-26
**Document Type**: Standard Operating Procedure
**Classification**: Law Enforcement Sensitive

---

## 🎯 Purpose

This protocol establishes procedures for maintaining complete chain of custody when processing digital evidence using the Digital Evidence Gallery Generator. Proper chain of custody documentation is critical for legal admissibility and forensic integrity.

---

## 📋 Chain of Custody Requirements

### Legal Framework

**Federal Rules of Evidence (FRE 901)**:
"To satisfy the requirement of authenticating or identifying an item of evidence, the proponent must produce evidence sufficient to support a finding that the item is what the proponent claims it is."

**This Requires**:
1. Identity of evidence established
2. Continuous custody documented
3. Handling procedures documented
4. No unauthorized modifications

### Digital Evidence Standards

**SWGDE (Scientific Working Group on Digital Evidence)**:
- Original evidence preserved unchanged
- All processing steps documented
- Hash values for integrity verification
- Audit trail maintained

---

## 🔒 Protocol Steps

### Step 1: Evidence Receipt & Documentation

#### A. Initial Receipt Log
When receiving evidence, create: `EVIDENCE_RECEIPT_LOG.txt`

```
EVIDENCE RECEIPT LOG
====================
Case Number: 23-262207
Date Received: 2026-01-26 09:15:00
Received By: Detective John Smith, Badge #4523
Received From: Crime Scene Unit, Officer Jane Doe
Agency: El Paso Police Department

Evidence Description:
  - Digital photos from crime scene (SD card)
  - Witness statement PDFs (email attachment)
  - Medical examiner report (encrypted PDF)

Physical Custody:
  - SD Card Serial: SN1234567890
  - Email Date: 2026-01-25 14:32:00
  - Email From: evidence@eppd.gov

Chain of Custody Form: Attachment A (signed)
Evidence Seal Numbers: ES-2026-00123, ES-2026-00124
```

#### B. Generate File Checksums
```bash
# Create checksums BEFORE any processing
cd /original/evidence/location/

# SHA-256 hashes for all files
shasum -a 256 photos/*.JPG > photo_checksums_original.txt
shasum -a 256 documents/*.pdf > document_checksums_original.txt

# MD5 for additional verification (if required)
md5 photos/*.JPG > photo_checksums_md5.txt
md5 documents/*.pdf > document_checksums_md5.txt
```

**Purpose**: Prove evidence unchanged from receipt to processing

---

### Step 2: Evidence Copying

#### A. Create Working Copy
```bash
# Navigate to project
cd Digital-Evidence-Gallery-Generator

# Create case folder
mkdir -p input/20260126-EPPD-23-262207

# COPY (never move) original evidence
cp -pr /original/evidence/photos input/20260126-EPPD-23-262207/
cp -pr /original/evidence/documents input/20260126-EPPD-23-262207/

# Preserve timestamps with -p flag
```

**Critical Requirements**:
- ✅ Use `cp -pr` to preserve timestamps
- ✅ NEVER move original files
- ✅ Verify copy success before proceeding
- ❌ NEVER modify files in original location

#### B. Verify Copy Integrity
```bash
# Generate checksums of copied files
cd input/20260126-EPPD-23-262207/photos/
shasum -a 256 * > ../photo_checksums_copy.txt

cd ../documents/
shasum -a 256 *.pdf > ../document_checksums_copy.txt

# Compare to original checksums
diff /original/evidence/photo_checksums_original.txt ../photo_checksums_copy.txt
# Output should be empty (no differences)
```

**If Differences Found**:
1. Stop processing immediately
2. Document the discrepancy
3. Recopy affected files
4. Investigate cause (disk error, corruption, etc.)
5. Do not proceed until integrity confirmed

---

### Step 3: Processing Documentation

#### A. Create Processing Log
Create: `input/20260126-EPPD-23-262207/PROCESSING_LOG.txt`

```
DIGITAL EVIDENCE PROCESSING LOG
================================
Case Number: 23-262207
Processing Date: 2026-01-26 10:00:00
Processor: Detective John Smith, Badge #4523
Agency: El Paso Police Department
System: Digital Evidence Gallery Generator v1.0.0

Original Evidence Location:
  /Volumes/Evidence-Storage/EPPD/2026/01-January/23-262207/

Evidence Copied To:
  Digital-Evidence-Gallery-Generator/input/20260126-EPPD-23-262207/

File Inventory:
  Photos: 19 JPEG files (total: 42.3 MB)
  Documents: 20 PDF files (total: 289.4 MB)

Integrity Verification:
  SHA-256 checksums generated: YES
  Checksums match original: YES
  Files readable: YES
  EXIF data present: YES (19/19 photos)
  PDF metadata present: YES (20/20 documents)

Processing Method:
  Tool: Digital Evidence Gallery Generator v1.0.0
  Image Optimization: 50% resolution, JPEG quality 75
  Document Optimization: 150 DPI, JPEG quality 60, max 50-100 pages
  Output Format: Lazy Loading Portal
  Brand Color: #172144

Processing Started: 2026-01-26 10:05:00
Processing Completed: 2026-01-26 10:23:00
Duration: 18 minutes

Output Files Generated:
  unified-forensic-portal-lazy.html (3.4 MB)
  images-data.json (5.2 MB)
  documents-data.json (87.3 MB)
  thumbnails-data.json (3.4 MB)
  Total: 99.3 MB

Quality Assurance:
  Visual review completed: YES
  Navigation tested: YES
  Metadata accuracy verified: YES
  Browser compatibility tested: Chrome, Firefox, Safari
  Mobile testing completed: iOS Safari, Chrome Mobile

Original Evidence Status: UNCHANGED, PRESERVED
Original Evidence Location: /Volumes/Evidence-Storage/EPPD/2026/01-January/23-262207/
Original Evidence Checksums: See photo_checksums_original.txt, document_checksums_original.txt

Processed By: _____________________  Date: __________
Reviewed By: ______________________  Date: __________
```

---

### Step 4: Output Validation

#### A. Post-Processing Checksums
```bash
# Generate checksums for output files
cd output/20260126-EPPD-23-262207/

shasum -a 256 unified-forensic-portal-lazy.html > portal_checksum.txt
shasum -a 256 images-data.json >> portal_checksum.txt
shasum -a 256 documents-data.json >> portal_checksum.txt
```

**Purpose**: Document output file integrity for delivery

#### B. Automated Validation
```bash
# Run automated QA script
python3 scripts/qa_validation.py output/20260126-EPPD-23-262207/

# Expected output:
# ✅ All metadata fields populated
# ✅ No broken data URIs
# ✅ File count matches input
# ✅ Chronological sorting verified
# ✅ HTML structure valid
```

---

### Step 5: Delivery Documentation

#### A. Create Delivery Package
```bash
# Generate complete delivery documentation
python3 scripts/create_delivery_docs.py \
  --case-folder output/20260126-EPPD-23-262207/ \
  --case-number "23-262207" \
  --agency "El Paso Police Department" \
  --recipient "District Attorney's Office" \
  --processor "Detective John Smith"
```

**Documents Created**:
1. `README.md` - User guide for portal
2. `DELIVERY_SUMMARY.txt` - Technical specifications
3. `EVIDENCE_INVENTORY.txt` - Complete file listing
4. `CHAIN_OF_CUSTODY_UPDATE.txt` - Transfer documentation

#### B. Chain of Custody Update
The delivery documentation includes chain of custody update:

```
CHAIN OF CUSTODY - TRANSFER RECORD
===================================
Transfer Date: 2026-01-26 11:00:00
Transferred From: Detective John Smith, EPPD Badge #4523
Transferred To: ADA Sarah Johnson, District Attorney's Office
Transfer Method: Hand delivery (USB drive)

Evidence Transferred:
  Format: Digital Evidence Gallery Portal
  Files: 4 files (99.3 MB total)
  Processing: Digital Evidence Gallery Generator v1.0.0
  Original Evidence: Preserved unchanged at original location

Checksums:
  unified-forensic-portal-lazy.html: [SHA-256 hash]
  images-data.json: [SHA-256 hash]
  documents-data.json: [SHA-256 hash]
  thumbnails-data.json: [SHA-256 hash]

Custody Transfer:
  Releasing Officer: ___________________ Date: _______
  Receiving Party: ______________________ Date: _______
  Witness: ___________________________ Date: _______

Purpose: Discovery disclosure, case review, trial preparation
Next Expected Custody Transfer: Court admission as exhibit
```

---

### Step 6: Archival & Retention

#### A. Archive Original Evidence
```bash
# Create archival package
mkdir -p /Volumes/Evidence-Archive/2026/EPPD/23-262207/

# Copy originals to archive
cp -pr /original/evidence/* /Volumes/Evidence-Archive/2026/EPPD/23-262207/original/

# Copy processing outputs
cp -pr output/20260126-EPPD-23-262207/* /Volumes/Evidence-Archive/2026/EPPD/23-262207/processed/

# Copy all documentation
cp input/20260126-EPPD-23-262207/PROCESSING_LOG.txt /Volumes/Evidence-Archive/2026/EPPD/23-262207/
cp input/20260126-EPPD-23-262207/*_checksums*.txt /Volumes/Evidence-Archive/2026/EPPD/23-262207/
```

#### B. Retention Schedule
| Item | Retention Period | Disposal Method |
|------|------------------|-----------------|
| Original evidence files | Indefinite | Per agency policy |
| Processing logs | 7 years minimum | Secure shred |
| Checksums | 7 years minimum | Secure shred |
| Portal outputs | 7 years minimum | Secure delete |
| Delivery documentation | 7 years minimum | Secure shred |

**Note**: Retention periods vary by jurisdiction and case type. Consult agency policy and legal counsel.

---

## ⚠️ Critical Reminders

### NEVER Do This:
❌ Modify original evidence files
❌ Delete original files before archival
❌ Process evidence without documentation
❌ Skip integrity verification steps
❌ Distribute without chain of custody update
❌ Forget to backup original evidence

### ALWAYS Do This:
✅ Copy (never move) original files
✅ Generate checksums before and after
✅ Document every step in processing log
✅ Verify integrity at each stage
✅ Update chain of custody for transfers
✅ Maintain multiple backups

---

## 📋 Chain of Custody Checklist

Use this checklist for every case:

### Evidence Intake
- [ ] Evidence received and logged
- [ ] Chain of custody form signed
- [ ] Original evidence sealed and stored
- [ ] Checksums generated for originals
- [ ] Evidence inventory created

### Processing
- [ ] Working copy created (originals untouched)
- [ ] Copy integrity verified (checksums match)
- [ ] Processing log initiated
- [ ] System and version documented
- [ ] Processing parameters documented

### Quality Assurance
- [ ] Output validation completed
- [ ] Visual review passed
- [ ] Metadata accuracy verified
- [ ] Browser testing completed
- [ ] QA checklist signed

### Delivery
- [ ] Delivery documentation created
- [ ] Chain of custody updated
- [ ] Recipient acknowledgment obtained
- [ ] Transfer checksums generated
- [ ] Delivery method documented

### Archival
- [ ] Originals archived securely
- [ ] Outputs archived with documentation
- [ ] Retention schedule documented
- [ ] Multiple backup locations
- [ ] Archive checksums generated

---

## 🔍 Audit Trail

Every case processed creates a complete audit trail:

```
input/20260126-EPPD-23-262207/
├── photos/ (original copied files)
├── documents/ (original copied files)
├── EVIDENCE_RECEIPT_LOG.txt
├── PROCESSING_LOG.txt
├── CHAIN_OF_CUSTODY.txt
├── photo_checksums_original.txt
├── document_checksums_original.txt
├── photo_checksums_copy.txt
├── document_checksums_copy.txt
├── metadata_images.csv
└── metadata_documents.csv

output/20260126-EPPD-23-262207/
├── unified-forensic-portal-lazy.html
├── images-data.json
├── documents-data.json
├── thumbnails-data.json
├── portal_checksum.txt
├── README.md
├── DELIVERY_SUMMARY.txt
├── EVIDENCE_INVENTORY.txt
└── CHAIN_OF_CUSTODY_UPDATE.txt
```

**This audit trail demonstrates**:
- When evidence was received
- Who handled it
- What processing occurred
- Integrity verification results
- Delivery chain
- Retention information

---

## 🎓 Training Requirements

### Chain of Custody Training

**All personnel must complete**:
1. Digital Evidence Handling 101
2. Chain of Custody Fundamentals
3. Evidence Processing Protocol training
4. System-specific training (this tool)
5. Legal admissibility requirements
6. Competency assessment

**Annual Refresher**:
- Review protocol updates
- Case study analysis
- New features training
- Legal updates review

---

## 📞 Escalation Procedures

### Chain of Custody Breaks

**If chain of custody is broken**:
1. **Stop all processing immediately**
2. **Document the break**:
   - What happened
   - When it occurred
   - Who was involved
   - What evidence affected
3. **Notify supervisor immediately**
4. **Consult with legal counsel**
5. **Determine if evidence is still admissible**
6. **Document remediation steps**

**Examples of Breaks**:
- Evidence files modified (timestamps changed)
- Checksums don't match
- Unauthorized access to evidence
- Missing documentation
- Gap in custody log

---

## 🎯 Best Practices

### Documentation
- Use templates for all logs (consistent format)
- Sign and date every log entry
- Be specific (exact times, not "morning")
- Include witness signatures when possible
- Photograph evidence seals and storage

### Evidence Handling
- Use write-protected storage for originals
- Never work directly on originals
- Verify integrity at every transfer
- Document every person who handles evidence
- Limit access to authorized personnel only

### System Security
- Access logs for evidence storage
- Encrypted storage for sensitive cases
- Secure deletion of temporary files
- Network isolation during processing
- Physical security of processing workstation

---

## 📋 Appendix: Sample Forms

### Form A: Evidence Receipt Log
[See template in templates/forms/]

### Form B: Processing Log
[See template in templates/forms/]

### Form C: Chain of Custody Transfer
[See template in templates/forms/]

### Form D: Delivery Acknowledgment
[See template in templates/forms/]

---

**Strict adherence to this protocol ensures forensic integrity and legal admissibility of all processed evidence.**

---

*Chain of Custody Protocol v1.0.0 - Digital Evidence Gallery Generator*
*Last Updated: 2026-01-26*
