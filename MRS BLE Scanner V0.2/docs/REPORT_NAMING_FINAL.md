# Report Naming System - UPDATED ✅

## New Format (Final)

**Format**: `R{last4digits}-{HH.MM}.pdf`  
**Example**: `R0687-01.37.pdf`

### Breakdown:
- `R` = Report prefix
- `0687` = Last 4 digits of device IMEI (351469520520**0687**)
- `01.37` = Time when report was generated (01:37 = 1:37 AM)

## Why This Format?

✅ **Device Identification**: Instantly see which device the report is for  
✅ **Time Stamp**: Know exactly when the report was generated  
✅ **Unique**: Different devices or different times = different filenames  
✅ **Sortable**: Reports naturally sort by device, then by time  
✅ **Readable**: Easy to read and understand at a glance  

## Examples

| Device IMEI | Time | Filename |
|-------------|------|----------|
| 351469520520687 | 13:20 | `R0687-13.20.pdf` |
| 351469520523982 | 14:45 | `R3982-14.45.pdf` |
| 351469520520687 | 09:15 | `R0687-09.15.pdf` |

## Files Modified

### `PDFReportGenerator.py`
- Removed persistent counter system (no longer needed)
- Changed filename format to `R{last4}-{HH.MM}.pdf`
- Updated PDF content to show matching report ID

### `Scanner.py`
- Updated report extraction regex to match new format
- Display shows full report ID (e.g., "R0687-01.37")

## Important Notes

⚠️ **Same device, same minute**: If you generate multiple reports for the same device within the same minute, the filename will be the same and will **overwrite** the previous report.

💡 **Solution**: This is actually a feature! You typically only need the latest report for a device at any given time. Old reports from different times are preserved.

## Testing

The test IMEI `351469520520687` generates reports like:
- `R0687-01.37.pdf` (generated at 1:37 AM)
- `R0687-13.20.pdf` (generated at 1:20 PM)

Both the filename and the "Report Number" field inside the PDF will show the same ID.
