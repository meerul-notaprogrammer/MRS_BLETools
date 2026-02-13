"""
PDF Report Generator for MRS BLE Scanner V0.2
Generates professional diagnostic reports from NetworkDiagnostics results
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import os


class PDFReportGenerator:
    """Generates PDF diagnostic reports"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Define colors
        self.color_success = colors.HexColor('#28a745')
        self.color_warning = colors.HexColor('#ffc107')
        self.color_danger = colors.HexColor('#dc3545')
        self.color_info = colors.HexColor('#17a2b8')
        self.color_header = colors.HexColor('#2c3e50')
        self.color_subheader = colors.HexColor('#34495e')
    

    def generate_report(self, diagnostic_result, report_number: int = None) -> str:
        """
        Generate PDF report from diagnostic result
        Returns: path to generated PDF file
        """
        
        # Extract last 4 digits of IMEI
        imei = diagnostic_result.device_imei
        if imei and imei != "Unknown" and len(imei) >= 4:
            last4 = imei[-4:]
        else:
            last4 = "0000"
        
        # Generate filename: R3982-13.20.pdf
        time_str = datetime.now().strftime('%H.%M')
        filename = f"R{last4}-{time_str}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )
        
        # Build content
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=self.color_header,
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=self.color_subheader,
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
        # Title
        story.append(Paragraph("🔍 NB-IoT NETWORK DIAGNOSTIC REPORT", title_style))
        story.append(Spacer(1, 10*mm))
        
        # Device Info Box
        # Generate report identifier for display
        # imei and time_str are already defined above for filename generation
        report_id = f"R{last4}-{time_str}"
        
        device_data = [
            ['Device Information', ''],
            ['IMEI:', diagnostic_result.device_imei],
            ['Report Time:', diagnostic_result.timestamp],
            ['Report Number:', report_id],
        ]
        
        if diagnostic_result.imsi:
            device_data.append(['IMSI:', diagnostic_result.imsi])
        
        device_table = Table(device_data, colWidths=[60*mm, 100*mm])
        device_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.color_info),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ]))
        
        story.append(device_table)
        story.append(Spacer(1, 8*mm))
        
        # Overall Status
        status_color = {
            'HEALTHY': self.color_success,
            'PARTIAL': self.color_warning,
            'FAILED': self.color_danger
        }.get(diagnostic_result.overall_status, colors.grey)
        
        status_icon = {
            'HEALTHY': '✅',
            'PARTIAL': '⚠️',
            'FAILED': '❌'
        }.get(diagnostic_result.overall_status, '❓')
        
        status_data = [
            ['Overall Status', f"{status_icon} {diagnostic_result.overall_status}"]
        ]
        
        status_table = Table(status_data, colWidths=[60*mm, 100*mm])
        status_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.color_header),
            ('BACKGROUND', (1, 0), (1, 0), status_color),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(status_table)
        story.append(Spacer(1, 8*mm))
        
        # Layer Status
        story.append(Paragraph("📊 Layer-by-Layer Analysis", heading_style))
        
        # Check if device successfully communicated
        device_communicated = diagnostic_result.ack_received or diagnostic_result.cipsend_success
        
        layer_data = [
            ['Layer', 'Component', 'Status', 'Details']
        ]
        
        # Only show SIM/IMSI if device didn't communicate
        # If device sent data or got ACK, SIM is obviously working!
        if not device_communicated:
            layer_data.extend([
                [
                    '1',
                    'SIM Card',
                    '✅ PASS' if diagnostic_result.sim_ready else '❌ FAIL',
                    'Ready' if diagnostic_result.sim_ready else 'Not detected'
                ],
                [
                    '1',
                    'IMSI',
                    '✅ PASS' if diagnostic_result.imsi else '⚠️ N/A',
                    diagnostic_result.imsi[:15] if diagnostic_result.imsi else 'Not visible (may be normal)'
                ]
            ])
        
        # Always show these layers
        layer_data.extend([
            [
                '2',
                'Registration',
                '✅ PASS' if diagnostic_result.cereg_registered else '❌ FAIL',
                f"{diagnostic_result.cereg_status or 'Unknown'} ({diagnostic_result.cereg_code or 'N/A'})"
            ],
            [
                '3',
                'PDP Context',
                '✅ PASS' if diagnostic_result.netopen_success else '❌ FAIL',
                'NETOPEN successful' if diagnostic_result.netopen_success else 'NETOPEN failed'
            ],
            [
                '4',
                'UDP Socket',
                '✅ PASS' if diagnostic_result.cipopen_success else '❌ FAIL',
                'CIPOPEN successful' if diagnostic_result.cipopen_success else 'CIPOPEN failed'
            ],
            [
                '4',
                'Data Send',
                '✅ PASS' if diagnostic_result.cipsend_success else '❌ FAIL',
                f'{diagnostic_result.packet_bytes} bytes sent' if diagnostic_result.packet_bytes else 'No data sent'
            ],
            [
                '4',
                'Server ACK',
                '✅ RECEIVED' if diagnostic_result.ack_received else '⚠️ NONE',
                'Server acknowledged' if diagnostic_result.ack_received else 'No acknowledgment'
            ],
        ])
        
        layer_table = Table(layer_data, colWidths=[15*mm, 40*mm, 30*mm, 75*mm])
        layer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.color_header),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ]))
        
        story.append(layer_table)
        story.append(Spacer(1, 8*mm))
        
        # Signal Quality (if available)
        if diagnostic_result.rsrp or diagnostic_result.snr:
            story.append(Paragraph("📡 Signal Quality", heading_style))
            
            signal_data = [['Metric', 'Value', 'Quality']]
            
            if diagnostic_result.rsrp:
                signal_data.append([
                    'RSRP (Signal Power)',
                    f'{diagnostic_result.rsrp} dBm',
                    diagnostic_result.rsrp_quality or 'Unknown'
                ])
            
            if diagnostic_result.snr:
                signal_data.append([
                    'SNR (Signal-to-Noise)',
                    f'{diagnostic_result.snr} dB',
                    diagnostic_result.snr_quality or 'Unknown'
                ])
            
            signal_table = Table(signal_data, colWidths=[60*mm, 50*mm, 50*mm])
            signal_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.color_info),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ]))
            
            story.append(signal_table)
            story.append(Spacer(1, 8*mm))
        
        # Server Configuration (if available)
        if diagnostic_result.server_ip or diagnostic_result.apn:
            story.append(Paragraph("🌐 Server Configuration", heading_style))
            
            server_data = [['Setting', 'Value']]
            
            if diagnostic_result.server_ip:
                server_data.append([
                    'Server IP',
                    diagnostic_result.server_ip
                ])
            
            if diagnostic_result.server_port:
                server_data.append([
                    'Server Port',
                    diagnostic_result.server_port
                ])
            
            if diagnostic_result.apn:
                server_data.append([
                    'APN',
                    diagnostic_result.apn
                ])
            
            server_table = Table(server_data, colWidths=[60*mm, 100*mm])
            server_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.color_info),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ]))
            
            story.append(server_table)
            story.append(Spacer(1, 8*mm))
        
        # Root Cause
        if diagnostic_result.failure_layer:
            story.append(Paragraph("🔴 Root Cause Analysis", heading_style))
            
            cause_data = [
                ['Failure Point', diagnostic_result.failure_layer],
                ['Diagnosis', diagnostic_result.root_cause]
            ]
            
            cause_table = Table(cause_data, colWidths=[50*mm, 110*mm])
            cause_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff3cd')),
                ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#fff3cd')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ffc107')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            story.append(cause_table)
            story.append(Spacer(1, 8*mm))
        
        # Recommendations
        story.append(Paragraph("🔧 Recommended Actions", heading_style))
        
        rec_text = "<br/>".join([f"• {rec}" for rec in diagnostic_result.recommendations])
        story.append(Paragraph(rec_text, body_style))
        story.append(Spacer(1, 8*mm))
        
        # Packet Info (if available)
        if diagnostic_result.packet_sent:
            story.append(Paragraph("📦 Packet Information", heading_style))
            
            packet_data = [
                ['Packet Data (Hex)', diagnostic_result.packet_sent[:50] + '...' if len(diagnostic_result.packet_sent) > 50 else diagnostic_result.packet_sent],
                ['Packet Size', f'{diagnostic_result.packet_bytes} bytes' if diagnostic_result.packet_bytes else 'Unknown']
            ]
            
            packet_table = Table(packet_data, colWidths=[50*mm, 110*mm])
            packet_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e9ecef')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('FONTNAME', (1, 0), (1, 0), 'Courier'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(packet_table)
            story.append(Spacer(1, 8*mm))
        
        # Footer
        story.append(Spacer(1, 10*mm))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph(
            f"Generated by MRS BLE Scanner V0.2 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            footer_style
        ))
        
        # Build PDF
        doc.build(story)
        
        return filepath
