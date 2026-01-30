import pdfplumber
import re
import json
import sys
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
import os

def extract_control_headings_and_sections(pdf_path, output_dir):
    """
    Extract control headings and save PDF sections between headings
    Works for any control family (AC, AT, AU, CM, CP, etc.)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[DOC] Processing PDF: {pdf_path}")
    print(f"[FOLDER] Output directory: {output_dir}")

    control_headings = []
    control_sections = []

    with pdfplumber.open(pdf_path) as pdf:
        print(f"[STATS] PDF has {len(pdf.pages)} pages")
        
        for page_num, page in enumerate(pdf.pages, start=1):
            print(f"[DEBUG] Processing page {page_num}...")
            
            # Extract text with font information
            chars = page.chars
            
            if not chars:
                print(f"   [WARNING] No characters found on page {page_num}")
                continue
            
            # Group characters by font size and position
            font_groups = {}
            for char in chars:
                font_size = round(char['size'], 1)
                if font_size not in font_groups:
                    font_groups[font_size] = []
                font_groups[font_size].append(char)
            
            # Sort font sizes to find the largest (likely headings)
            font_sizes = sorted(font_groups.keys(), reverse=True)
            print(f"   [INFO] Font sizes found: {font_sizes}")
            
            # Extract text from larger fonts (potential headings)
            for font_size in font_sizes:
                if font_size >= 9.0:  # Lower threshold to catch more controls
                    chars_in_font = sorted(font_groups[font_size], key=lambda x: (x['top'], x['x0']))
                    text = ''.join([char['text'] for char in chars_in_font])
                    
                    # Generic pattern for any control family: two letters-number space and words
                    # Pattern: [A-Z]{2}-\d+\s+[A-Z][A-Z\s\-—&()]+
                    control_match = re.search(r'\b([A-Z]{2}-\d+)\s+([A-Z][A-Z\s\-—&()]+?)(?=\s+[A-Z]{2}-\d+|$)', text)
                    if control_match:
                        control_code = control_match.group(1)
                        control_title = control_match.group(2).strip()
                        
                        # Clean up the title
                        control_title = re.sub(r'\s+', ' ', control_title)
                        control_title = control_title.strip()
                        
                        # Check if we already found this control
                        if not any(c['control_code'] == control_code for c in control_headings):
                            control_headings.append({
                                'control_code': control_code,
                                'control_title': control_title,
                                'font_size': font_size,
                                'start_page': page_num
                            })
                            print(f"   [OK] Found: {control_code} {control_title}")
            
            # Also try plain text extraction as backup
            text = page.extract_text()
            if text:
                # Look for controls in plain text using generic pattern
                lines = text.split('\n')
                for line in lines:
                    control_match = re.search(r'\b([A-Z]{2}-\d+)\s+([A-Z][A-Z\s\-—&()]+?)(?=\s+[A-Z]{2}-\d+|$)', line)
                    if control_match:
                        control_code = control_match.group(1)
                        control_title = control_match.group(2).strip()
                        
                        # Clean up the title
                        control_title = re.sub(r'\s+', ' ', control_title)
                        control_title = control_title.strip()
                        
                        # Check if we already found this control
                        if not any(c['control_code'] == control_code for c in control_headings):
                            control_headings.append({
                                'control_code': control_code,
                                'control_title': control_title,
                                'font_size': 'text_extraction',
                                'start_page': page_num
                            })
                            print(f"   [OK] Found (text): {control_code} {control_title}")

    print(f"[INFO] Total control headings extracted: {len(control_headings)}")

    # Sort controls by their number (works for any control family)
    def extract_number(control):
        match = re.search(r'[A-Z]{2}-(\d+)', control['control_code'])
        return int(match.group(1)) if match else 0
    
    control_headings.sort(key=extract_number)

    # Extract PDF sections between headings
    if control_headings:
        print("\n[DOC] Extracting PDF sections...")
        
        # Read the original PDF
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        
        # Group controls by their starting page to handle multiple controls on same page
        page_groups = {}
        for control in control_headings:
            start_page = control['start_page']
            if start_page not in page_groups:
                page_groups[start_page] = []
            page_groups[start_page].append(control)
        
        # Sort pages to process them in order
        sorted_pages = sorted(page_groups.keys())
        
        # Create sections based on control headings
        for i, start_page in enumerate(sorted_pages):
            controls_on_page = page_groups[start_page]
            
            # Use the first control as the main one for naming
            main_control = controls_on_page[0]
            
            # Determine end page - end BEFORE the next page with controls starts
            if i < len(sorted_pages) - 1:
                # End at the page BEFORE the next page with controls starts
                end_page = sorted_pages[i + 1] - 1
            else:
                # For the last page with controls, go to the end of the PDF
                end_page = total_pages
            
            # Ensure we don't go beyond PDF bounds
            if end_page > total_pages:
                end_page = total_pages
            
            # Convert to 0-based index for PDF operations
            start_page_idx = start_page - 1
            end_page_idx = end_page - 1
            
            # Skip if start_page > end_page (shouldn't happen but safety check)
            if start_page_idx > end_page_idx:
                print(f"   [WARNING] Skipping {main_control['control_code']} - invalid page range ({start_page} > {end_page})")
                continue
            
            # Create folder name for this control section
            safe_title = re.sub(r'[^\w\s-]', '', main_control['control_title'])
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            folder_name = f"{main_control['control_code']}_{safe_title}"
            folder_name = folder_name.replace(' ', '_')
            
            # Create the folder
            section_folder = output_dir / folder_name
            section_folder.mkdir(parents=True, exist_ok=True)
            
            # Create PDF writer for this section
            writer = PdfWriter()
            
            # Add pages to the section
            for page_num in range(start_page_idx, end_page_idx + 1):
                if page_num < total_pages:
                    writer.add_page(reader.pages[page_num])
            
            # Save the PDF section in the folder
            pdf_filename = f"{main_control['control_code']}_{safe_title}.pdf"
            pdf_filename = pdf_filename.replace(' ', '_')
            pdf_path_section = section_folder / pdf_filename
            
            with open(pdf_path_section, 'wb') as output_file:
                writer.write(output_file)
            
            # Extract text content from the PDF section for JSON
            section_text_content = []
            with pdfplumber.open(pdf_path_section) as section_pdf:
                for page_num, page in enumerate(section_pdf.pages, start=1):
                    text = page.extract_text()
                    if text:
                        section_text_content.append({
                            'page_number': page_num,
                            'content': text.strip()
                        })
            
            # Create JSON content for this section
            section_json_content = {
                'control_info': {
                    'control_code': main_control['control_code'],
                    'control_title': main_control['control_title'],
                    'start_page': start_page,
                    'end_page': end_page,
                    'total_pages_in_section': end_page - start_page + 1,
                    'controls_in_section': [c['control_code'] for c in controls_on_page],
                    'all_controls_details': controls_on_page
                },
                'pdf_file': pdf_filename,
                'extracted_content': section_text_content,
                'extraction_metadata': {
                    'extraction_date': str(Path().cwd()),
                    'source_pdf': str(pdf_path),
                    'total_pages_extracted': len(section_text_content)
                }
            }
            
            # Save JSON content in the folder
            json_filename = f"{main_control['control_code']}_content.json"
            json_path_section = section_folder / json_filename
            
            with open(json_path_section, 'w', encoding='utf-8') as json_file:
                json.dump(section_json_content, json_file, indent=4, ensure_ascii=False)
            
            # Add section info to control_sections
            control_sections.append({
                'control_code': main_control['control_code'],
                'control_title': main_control['control_title'],
                'start_page': start_page,
                'end_page': end_page,
                'folder_name': folder_name,
                'pdf_file': pdf_filename,
                'json_file': json_filename,
                'total_pages_in_section': end_page - start_page + 1,
                'controls_in_section': [c['control_code'] for c in controls_on_page]
            })
            
            # Show which controls are included in this section
            if len(controls_on_page) > 1:
                control_list = ", ".join([c['control_code'] for c in controls_on_page])
                print(f"   [OK] Created folder: {folder_name}/")
                print(f"      [DOC] PDF: {pdf_filename} (pages {start_page}-{end_page})")
                print(f"      [INFO] JSON: {json_filename} - Includes: {control_list}")
            else:
                print(f"   [OK] Created folder: {folder_name}/")
                print(f"      [DOC] PDF: {pdf_filename} (pages {start_page}-{end_page})")
                print(f"      [INFO] JSON: {json_filename}")

    # Save clean JSON with control headings and sections
    output_file = output_dir / "control_headings.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            'control_headings': control_headings,
            'control_sections': control_sections
        }, f, indent=4, ensure_ascii=False)

    # Also save as simple text file for easy reading
    text_file = output_dir / "control_headings.txt"
    with open(text_file, "w", encoding="utf-8") as f:
        for control in control_headings:
            f.write(f"{control['control_code']} {control['control_title']}\n")

    # Save sections summary
    sections_summary = output_dir / "sections_summary.txt"
    with open(sections_summary, "w", encoding="utf-8") as f:
        f.write("PDF Sections Extracted:\n")
        f.write("=" * 50 + "\n\n")
        for section in control_sections:
            f.write(f"Control: {section['control_code']} - {section['control_title']}\n")
            f.write(f"Folder: {section['folder_name']}/\n")
            f.write(f"PDF File: {section['pdf_file']}\n")
            f.write(f"JSON File: {section['json_file']}\n")
            f.write(f"Pages: {section['start_page']}-{section['end_page']} ({section['total_pages_in_section']} pages)\n")
            f.write("-" * 30 + "\n")

    print(f"[OK] Extracted {len(control_headings)} control headings")
    print(f"[OK] Created {len(control_sections)} PDF sections")
    print(f"[OK] JSON saved to: {output_file}")
    print(f"[OK] Text file saved to: {text_file}")
    print(f"[OK] Sections summary saved to: {sections_summary}")
    
    # Print summary
    print("\n[LIST] Control Headings Found:")
    for control in control_headings:
        print(f"   {control['control_code']} - {control['control_title']}")
    
    print("\n[DOC] PDF Sections Created:")
    for section in control_sections:
        print(f"   {section['folder_name']}/")
    
    return control_headings, control_sections

def process_all_pdfs_in_sections():
    """
    Process all PDF files in the extracted_sections/sections directory
    and create sub-folders within each respective folder
    """
    # Use current working directory to find extracted_sections/sections
    base_dir = Path("extracted_sections/sections")
    
    # Check if the directory exists
    if not base_dir.exists():
        print(f"[ERROR] Directory not found: {base_dir}")
        print("Please make sure the 'extracted_sections/sections' directory exists.")
        return
    
    print(f"[DEBUG] Scanning directory: {base_dir}")
    
    # Find all subdirectories in the sections folder
    subdirs = [d for d in base_dir.iterdir() if d.is_dir()]
    
    if not subdirs:
        print("[ERROR] No subdirectories found in the sections folder.")
        return
    
    print(f"[FOLDER] Found {len(subdirs)} subdirectories")
    
    # Process each subdirectory
    for subdir in subdirs:
        print(f"\n{'='*60}")
        print(f"[EMOJI] Processing subdirectory: {subdir.name}")
        print(f"{'='*60}")
        
        # Look for PDF files in this subdirectory
        pdf_files = list(subdir.glob("*.pdf"))
        
        if not pdf_files:
            print(f"   [WARNING] No PDF files found in {subdir.name}")
            continue
        
        # Process each PDF file in the subdirectory
        for pdf_file in pdf_files:
            print(f"\n[DOC] Processing PDF: {pdf_file.name}")
            
            # Create output directory within the same subdirectory
            output_dir = subdir / "extracted_controls"
            
            try:
                # Extract control headings and sections
                control_headings, control_sections = extract_control_headings_and_sections(
                    str(pdf_file), str(output_dir)
                )
                
                if control_headings:
                    print(f"[OK] Successfully processed {pdf_file.name}")
                    print(f"   [STATS] Found {len(control_headings)} controls")
                    print(f"   [FOLDER] Created {len(control_sections)} sections in {output_dir}")
                else:
                    print(f"[WARNING] No controls found in {pdf_file.name}")
                    
            except Exception as e:
                print(f"[ERROR] Error processing {pdf_file.name}: {str(e)}")
                continue
    
    print(f"\n{'='*60}")
    print("[EMOJI] Processing complete!")
    print(f"{'='*60}")

if __name__ == "__main__":
    # Check if PDF path is provided as command line argument
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        output_dir = "uploads/output_sections"
        
        if Path(pdf_path).exists():
            extract_control_headings_and_sections(pdf_path, output_dir)
        else:
            print(f"[ERROR] PDF file not found: {pdf_path}")
            print("Usage: python sub_policy_extraction.py [path_to_pdf]")
            print("Example: python sub_policy_extraction.py uploads/NIST_SP_800_53_Split/sections/016-3_2_AWARENESS_AND_TRAINING/3_2_AWARENESS_AND_TRAINING.pdf")
    else:
        # Process all PDFs in the default sections directory
        process_all_pdfs_in_sections()
