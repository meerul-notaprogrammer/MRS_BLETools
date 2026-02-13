# Report Naming & Numbering System - FIXED ✅

## Changes Made

### 1. **New Report Naming Format**
- **Old Format**: `Network_Report_{IMEI}_{timestamp}_#{number}.pdf`
  - Example: `Network_Report_520687_20260212_170757_#001.pdf`
  - Hard to identify which report is which
  
- **New Format**: `R{number}_{timestamp}.pdf`
  - Example: `R007_20260214_003539.pdf`
  - Clean, simple, easy to identify
  - Report number comes first for easy sorting

### 2. **Persistent Report Counter**
- **Problem**: Report counter reset to 001 every time the app restarted
- **Solution**: Counter now stored in `reports/.report_counter` file
- **Behavior**: 
  - Counter automatically increments across app restarts
  - First report = R001, second = R002, etc.
  - Never resets unless you manually delete the counter file

### 3. **Consistent Numbering in PDF**
- Report number inside the PDF now matches the filename
- Format changed from `#001` to `R001` in the PDF content
- Example: File `R007_20260214_003539.pdf` shows "Report Number: R007" inside

## Files Modified

### `PDFReportGenerator.py`
1. Added `counter_file` path in `__init__`
2. Added `_get_next_report_number()` method to handle persistent counter
3. Changed filename format from `Network_Report_{imei}_{timestamp}_#{number}` to `R{number}_{timestamp}`
4. Updated PDF content to show `R001` instead of `#001`
5. Made report_number parameter optional (auto-increments if not provided)

### `Scanner.py`
1. Removed manual `report_count` tracking (no longer needed)
2. Updated `generate_diagnostic_report()` to use auto-increment
3. Extracts report number from filename for display
4. Removed report count from stats display

## How It Works

### Counter File System
```
reports/
├── .report_counter          # Contains: "7" (next report will be R007)
├── R001_20260214_003446.pdf
├── R002_20260214_003446.pdf
├── R003_20260214_003446.pdf
└── ...
```

### Auto-Increment Logic
1. When generating a report, `_get_next_report_number()` is called
2. Reads current value from `.report_counter` (or starts at 0)
3. Increments by 1
4. Saves new value back to file
5. Returns the number for the current report

### Example Flow
```python
# First run of the app
pdf_gen.generate_report(result)  # Creates R001_20260214_120000.pdf
pdf_gen.generate_report(result)  # Creates R002_20260214_120030.pdf

# App restarts (counter persists!)
pdf_gen.generate_report(result)  # Creates R003_20260214_130000.pdf
pdf_gen.generate_report(result)  # Creates R004_20260214_130030.pdf
```

## Testing

Run `test_report_naming.py` to verify:
```bash
python test_report_naming.py
```

This will:
- Show current counter value
- Generate 3 test reports
- Display all reports in the directory
- Verify counter increments correctly

## Benefits

✅ **Easy to identify**: `R007` is much clearer than `Network_Report_520687_20260212_170757_#001`  
✅ **Persistent counting**: Numbers never reset across app restarts  
✅ **Consistent**: Filename and PDF content match (both show R007)  
✅ **Sortable**: Reports sort naturally by number (R001, R002, R003...)  
✅ **Timestamp preserved**: Still includes timestamp for exact generation time  

## Migration

Old reports with the old naming format are still in the `reports/` folder and will continue to work. New reports will use the new format starting from where the counter left off.

If you want to reset the counter to start from R001 again, simply delete the `.report_counter` file.
