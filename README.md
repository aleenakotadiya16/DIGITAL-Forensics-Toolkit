# Digital Evidence Gallery Generator

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-production--ready-success)

**Version**: 1.0.0
**Created**: 2026-01-26
**Status**: Production Ready
**License**: MIT
**Repository**: [github.com/Jobikinobi/DIGITAL-Forensics-Toolkit](https://github.com/Jobikinobi/DIGITAL-Forensics-Toolkit)

A professional-grade toolkit for generating responsive, self-contained forensic evidence galleries from law enforcement digital evidence (photographs and documents).

---

## 🎯 Overview

The **Digital Evidence Gallery Generator** creates beautiful, responsive web applications for reviewing digital evidence from investigations. It processes photographs and PDF documents, preserving complete metadata while creating portable, professional galleries suitable for legal proceedings.

### Key Features

✅ **Multi-Agency Support** - Process evidence from multiple agencies in unified portal
✅ **Complete Metadata Preservation** - Full EXIF and PDF metadata retained
✅ **Responsive Design** - Works on desktop, tablet, and mobile devices
✅ **Lazy Loading** - 98% faster initial load with on-demand data fetching
✅ **Offline Capable** - No internet required, completely self-contained
✅ **Professional Branding** - Customizable color schemes
✅ **Forensically Sound** - Chain of custody maintained, audit-ready format
✅ **Legal-Ready** - Professional formatting for court proceedings

---

## 📊 What It Creates

### Evidence Portals
Transform folders of raw evidence into professional web applications:

**Input**:
```
Evidence/
├── photos/
│   ├── IMG_001.JPG (with EXIF data)
│   ├── IMG_002.JPG
│   └── ...
└── documents/
    ├── report.pdf
    ├── statement.pdf
    └── ...
```

**Output**:
```
unified-forensic-portal.html
  ├─ 📸 Images Tab
  │   ├─ Gallery with thumbnails
  │   ├─ Agency filtering
  │   ├─ Detail modal with EXIF
  │   └─ Keyboard navigation
  └─ 📄 Documents Tab
      ├─ Document gallery
      ├─ Page-by-page viewer
      ├─ PDF metadata display
      └─ Navigation controls
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ with PIL/Pillow and PyMuPDF (fitz)
- exiftool for metadata extraction
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

```bash
# Clone from GitHub
git clone https://github.com/Jobikinobi/DIGITAL-Forensics-Toolkit.git
cd DIGITAL-Forensics-Toolkit

# Install Python dependencies
pip3 install Pillow PyMuPDF

# Install exiftool (macOS)
brew install exiftool

# Or download from: https://exiftool.org/

# Verify installation
python3 --version  # Should be 3.10+
exiftool -ver      # Should be 12.0+
```

### Basic Usage

```bash
# 1. Place evidence in input directories
cp -r /path/to/photos ./input/agency-name/photos/
cp -r /path/to/documents ./input/agency-name/documents/

# 2. Run the generator
python3 scripts/generate_unified_portal.py \
  --agency "Agency Name" \
  --photos ./input/agency-name/photos/ \
  --documents ./input/agency-name/documents/ \
  --output ./output/

# 3. Open the generated portal
open ./output/unified-forensic-portal-lazy.html
```

---

## 📁 Project Structure

```
Digital-Evidence-Gallery-Generator/
├── README.md                          # This file - project overview
├── LICENSE                            # MIT License
├── CHANGELOG.md                       # Version history
├── .gitignore                         # Git ignore patterns
│
├── scripts/                           # Processing scripts
│   ├── generate_unified_portal.py     # Main generator (lazy loading)
│   ├── generate_single_file_portal.py # Single-file generator (optimized)
│   ├── extract_metadata.py            # Metadata extraction utilities
│   └── optimize_pdfs.py               # PDF optimization tools
│
├── templates/                         # HTML/CSS templates
│   ├── portal_template.html           # Base portal template
│   ├── styles.css                     # Shared stylesheets
│   └── config.json                    # Configuration options
│
├── docs/                              # Documentation
│   ├── guides/
│   │   ├── QUICK_START.md             # Getting started guide
│   │   ├── INSTALLATION.md            # Detailed setup instructions
│   │   └── TROUBLESHOOTING.md         # Common issues and solutions
│   ├── protocols/
│   │   ├── EVIDENCE_PROCESSING.md     # Standard operating procedures
│   │   ├── QUALITY_ASSURANCE.md       # QA checklist
│   │   └── CHAIN_OF_CUSTODY.md        # Forensic integrity guidelines
│   ├── architecture/
│   │   ├── SYSTEM_DESIGN.md           # Technical architecture
│   │   ├── OPTIMIZATION_STRATEGY.md   # Performance optimization details
│   │   └── DATA_FORMAT.md             # Data structure specifications
│   └── examples/
│       ├── SAMPLE_WORKFLOW.md         # Example processing workflow
│       └── USE_CASES.md               # Real-world use cases
│
├── input/                             # Evidence input (gitignored)
│   └── .gitkeep
│
├── output/                            # Generated galleries (gitignored)
│   └── .gitkeep
│
└── examples/                          # Sample evidence and outputs
    ├── sample-photos/
    ├── sample-documents/
    └── sample-output/
```

---

## 🔧 Features

### Evidence Processing
- **Image Processing**: EXIF extraction, resolution optimization, JPEG compression
- **Document Processing**: PDF page rendering, metadata extraction, adaptive page limiting
- **Metadata Preservation**: Complete EXIF and PDF metadata retained
- **Chronological Sorting**: Evidence organized by original capture/creation dates

### Portal Features
- **Responsive Design**: Mobile-first with desktop optimization
- **Agency Filtering**: Toggle between multiple agencies or view all
- **Lazy Loading**: Fast initial load, on-demand data fetching
- **Keyboard Navigation**: Arrow keys for navigation, Escape to close
- **Touch-Friendly**: Optimized for mobile and tablet interaction
- **Professional Branding**: Customizable color schemes

### Optimization
- **Image Optimization**: 50% resolution reduction, JPEG quality 75
- **Document Optimization**: 150 DPI rendering, JPEG quality 60
- **Smart Page Limiting**: Adaptive limits based on PDF file size
- **Lazy Loading**: 98% of data loaded on-demand for fast initial load

---

## 📖 Documentation

### Quick Start Guides
- [Quick Start Guide](docs/guides/QUICK_START.md) - Get started in 5 minutes
- [Installation Guide](docs/guides/INSTALLATION.md) - Detailed setup instructions
- [Troubleshooting](docs/guides/TROUBLESHOOTING.md) - Common issues and solutions

### Protocols & Procedures
- [Evidence Processing Protocol](docs/protocols/EVIDENCE_PROCESSING.md) - Standard operating procedures
- [Quality Assurance Checklist](docs/protocols/QUALITY_ASSURANCE.md) - QA before delivery
- [Chain of Custody Guidelines](docs/protocols/CHAIN_OF_CUSTODY.md) - Forensic integrity

### Technical Documentation
- [System Design](docs/architecture/SYSTEM_DESIGN.md) - Architecture overview
- [Optimization Strategy](docs/architecture/OPTIMIZATION_STRATEGY.md) - Performance details
- [Data Format Specification](docs/architecture/DATA_FORMAT.md) - Data structures

---

## 🎯 Use Cases

### Law Enforcement Investigations
- Process crime scene photographs with EXIF timestamps
- Organize case documents chronologically
- Create portable evidence packages
- Share with prosecutors and defense attorneys

### Legal Proceedings
- Present evidence in court with professional formatting
- Provide complete metadata for verification
- Maintain forensic chain of custody
- Generate discovery materials for opposing counsel

### Digital Forensics
- Preserve original metadata throughout processing
- Create audit-ready evidence packages
- Document evidence handling procedures
- Generate expert witness materials

---

## 🔐 Security & Forensic Integrity

### Metadata Preservation
✅ Complete EXIF data from photographs preserved
✅ Complete PDF metadata extracted and retained
✅ Original file names and timestamps maintained
✅ No data modification during processing

### Chain of Custody
✅ Self-contained format prevents unauthorized modification
✅ Base64 encoding creates audit trail
✅ No external dependencies that could be altered
✅ Timestamped generation records

### Legal Compliance
✅ Professional formatting for legal proceedings
✅ Complete metadata for verification and authentication
✅ Chronological organization for timeline reconstruction
✅ High-quality rendering for detailed review

---

## 📦 Output Formats

### Lazy Loading Portal (Recommended)
- **Main File**: 3.4 MB (thumbnails + UI)
- **Data Files**: images-data.json (9.6 MB), documents-data.json (125.7 MB)
- **Total**: ~142 MB
- **Load Time**: 1-3 seconds initial, instant navigation after
- **Deployment**: Requires web server (Python, Node, Apache, nginx)
- **Best For**: Local investigation, team collaboration

### Optimized Single-File Portal
- **File**: Single HTML file (~135 MB)
- **Load Time**: 5-10 seconds
- **Deployment**: Works from file system, no server needed
- **Best For**: Distribution, court evidence, USB drives

### Original High-Quality Portal
- **File**: Single HTML file (~617 MB)
- **Quality**: 300 DPI documents, highest quality
- **Best For**: Archival, maximum detail requirements

---

## 🛠️ Configuration

### Customization Options

**Brand Colors** (`templates/config.json`):
```json
{
  "primaryColor": "#172144",
  "textColor": "#172144",
  "headerBackground": "#172144",
  "headerText": "#ffffff"
}
```

**Optimization Settings**:
```json
{
  "images": {
    "resolutionPercent": 0.5,
    "jpegQuality": 75
  },
  "documents": {
    "dpi": 150,
    "jpegQuality": 60,
    "maxPages": {
      "huge": 50,
      "large": 75,
      "small": 100
    }
  }
}
```

---

## 🔄 Version History

### v1.0.0 (2026-01-26) - Initial Release
- Multi-agency evidence portal
- Lazy loading implementation
- Responsive design (mobile, tablet, desktop)
- Custom brand color support
- Complete metadata preservation
- Smart PDF optimization
- Comprehensive documentation

---

## 📞 Support & Contributing

### Reporting Issues
Found a bug or issue? [Create an issue on GitHub](https://github.com/Jobikinobi/DIGITAL-Forensics-Toolkit/issues/new) with:
- Evidence type and size
- Error messages
- Expected vs actual behavior
- Screenshots if applicable
- System information (OS, Python version, browser)

### Feature Requests
Have an idea for improvement? [Open a feature request](https://github.com/Jobikinobi/DIGITAL-Forensics-Toolkit/issues/new) with:
- Describe the use case
- Explain current limitations
- Suggest implementation approach
- Expected benefits

### Contributing
Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**For major changes**, please open an issue first to discuss what you'd like to change.

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

Built for law enforcement agencies and legal professionals to streamline digital evidence review and presentation.

**Technologies Used**:
- Python 3.10+ (PIL/Pillow, PyMuPDF)
- exiftool for metadata extraction
- HTML5, CSS3, Vanilla JavaScript
- Responsive web design principles

---

## 🚀 Getting Started

**New to this project?** Start here:
1. Read [Quick Start Guide](docs/guides/QUICK_START.md)
2. Review [Evidence Processing Protocol](docs/protocols/EVIDENCE_PROCESSING.md)
3. Run the sample workflow in [examples/](examples/)
4. Process your first case!

---

**For detailed documentation, see the [docs/](docs/) directory.**

**Ready to process evidence? See [Quick Start Guide](docs/guides/QUICK_START.md)**

---

*Digital Evidence Gallery Generator - Professional forensic evidence review made simple*

*Last Updated: 2026-01-26 | Version 1.0.0*
