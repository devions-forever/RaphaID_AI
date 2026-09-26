"""
Inline SVG Icons — Medically Accurate Icons for RaphaID AI
All icons are self-contained inline SVGs (24x24 viewBox, stroke="currentColor")
with zero external dependencies.
"""

ICONS = {
    # Brand / Insignia
    "brand": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v5M12 17v5"/><path d="M2 12h5l2-4 3 8 2-4h8"/></svg>''',
    
    # Primary Navigation & Console
    "dashboard": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>''',
    "home": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>''',
    "detection": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18h8"/><path d="M3 21h18"/><circle cx="12" cy="7" r="3"/><path d="M12 10v4"/><path d="M8 14h8"/><path d="M16 18a4 4 0 0 0-8 0"/></svg>''',
    "radiology": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></svg>''',
    "chatbot": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v2h6V5a3 3 0 0 0-3-3z"/><rect x="4" y="7" width="16" height="12" rx="3"/><circle cx="9" cy="12" r="1.5" fill="currentColor"/><circle cx="15" cy="12" r="1.5" fill="currentColor"/><path d="M9 16h6M2 13h2M20 13h2"/></svg>''',
    "assistant": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v2h6V5a3 3 0 0 0-3-3z"/><rect x="4" y="7" width="16" height="12" rx="3"/><circle cx="9" cy="12" r="1.5" fill="currentColor"/><circle cx="15" cy="12" r="1.5" fill="currentColor"/><path d="M9 16h6M2 13h2M20 13h2"/></svg>''',
    
    # Blood Pathology Submodules (Medically Accurate)
    # Malaria: Erythrocyte with intra-cellular Plasmodium ring trophozoite and chromatin dot
    "malaria": '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="12" rx="9" ry="7"/><circle cx="12" cy="12" r="3.5"/><circle cx="14" cy="10.5" r="1" fill="currentColor"/></svg>''',
    
    # Sickle Cell: Distinctive crescent / sickle-shaped red blood cell
    "sickle_cell": '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3a10 10 0 0 0 10 18 10 10 0 0 1-5-17.5A10 10 0 0 0 7 3z"/></svg>''',
    
    # Acute Lymphoblastic Leukemia: Large abnormal lymphoblast with prominent nucleus
    "all": '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9.5 8a3.5 3.5 0 0 1 5 1.5c.8 1.4.3 3.2-.8 4-1.2.9-2.5 2.5-4 1.5-1.4-.9-1.8-3.2-1.2-4.8.4-1.1.5-1.7 1-2.2z"/></svg>''',
    
    # Iron Deficiency: Microcytic hypochromic erythrocyte with enlarged central pallor
    "iron_deficiency": '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5" stroke-dasharray="2 2"/><circle cx="12" cy="12" r="2"/></svg>''',
    
    # Radiology Submodules (Medically Accurate)
    # MRI: Cylindrical scanner bore with axial head profile
    "mri": '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="4"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/><path d="M12 2v2M12 20v2"/></svg>''',
    
    # CT: Axial computed tomography ring detector with cross-sectional beams
    "ct": '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M7.05 7.05l9.9 9.9M7.05 16.95l9.9-9.9"/><circle cx="12" cy="12" r="3"/></svg>''',
    
    # Chest X-Ray: Radiographic thorax rib cage silhouette
    "xray": '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 6v12M8 8c2 .8 6 .8 8 0M8 11c2 .8 6 .8 8 0M8 14c2 .8 6 .8 8 0M9 17c1.5.5 4.5.5 6 0"/></svg>''',
    "xray_icon": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 6v12M8 8c2 .8 6 .8 8 0M8 11c2 .8 6 .8 8 0M8 14c2 .8 6 .8 8 0M9 17c1.5.5 4.5.5 6 0"/></svg>''',
    
    # System Status & Hardware Telemetry
    # Neural network model weights
    "models": '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="2"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="18" cy="18" r="2"/><circle cx="12" cy="12" r="2"/><path d="M8 7l4 4M8 17l4-4M16 7l-4 4M16 17l-4-4"/></svg>''',
    
    # Workstation / CPU device
    "device": '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M1 9h3M1 15h3M20 9h3M20 15h3"/></svg>''',
    
    # RAM memory module
    "ram": '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="1"/><line x1="6" y1="18" x2="6" y2="15"/><line x1="10" y1="18" x2="10" y2="15"/><line x1="14" y1="18" x2="14" y2="15"/><line x1="18" y1="18" x2="18" y2="15"/><circle cx="6" cy="10" r="1"/><circle cx="12" cy="10" r="1"/><circle cx="18" cy="10" r="1"/></svg>''',
    
    # Air-gapped / offline
    "offline": '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="1" y1="1" x2="23" y2="23"/><path d="M16.72 11.06A10.94 10.94 0 0 1 19 12.55"/><path d="M5 12.55a10.94 10.94 0 0 1 5.17-2.39"/><path d="M10.71 5.05A16 16 0 0 1 22.58 9"/><path d="M1.42 9a15.91 15.91 0 0 1 4.7-2.88"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>''',
    
    # Capabilities & Facts
    "microchip": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M1 9h3M1 15h3M20 9h3M20 15h3"/></svg>''',
    "bacterium": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="9" width="12" height="6" rx="3"/><path d="M6 12H3M21 12h-3M9 9V6M15 9V6M9 15v3M15 15v3"/></svg>''',
    "robot": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="12" x="3" y="6" rx="2"/><path d="M12 6V2"/><circle cx="12" cy="2" r="1"/><path d="M2 12h1"/><path d="M21 12h1"/><circle cx="8" cy="11" r="1" fill="currentColor"/><circle cx="16" cy="11" r="1" fill="currentColor"/><path d="M9 15h6"/></svg>''',
    "bolt": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>''',
    "memory": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="1"/><line x1="6" y1="18" x2="6" y2="15"/><line x1="10" y1="18" x2="10" y2="15"/><line x1="14" y1="18" x2="14" y2="15"/><line x1="18" y1="18" x2="18" y2="15"/><circle cx="6" cy="10" r="1"/><circle cx="12" cy="10" r="1"/><circle cx="18" cy="10" r="1"/></svg>''',
    "shield": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>''',
    "file_medical": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M12 11v6M9 14h6"/></svg>''',
    "file_medical_2": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M12 11v6M9 14h6"/></svg>''',
    
    # Clinical Workflow
    "vial": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2h12M9 2v3h6V2M7 5h10v12a5 5 0 0 1-10 0V5z"/><line x1="7" y1="10" x2="12" y2="10"/></svg>''',
    "magnifying_glass_chart": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><path d="M8 11h6M11 8v6"/></svg>''',
    "brain": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A4.5 4.5 0 0 0 5 6.5c0 1.2.5 2.3 1.3 3.1A4.5 4.5 0 0 0 5 13c0 1.9 1.2 3.6 3 4.2V20a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-2.8c1.8-.6 3-2.3 3-4.2 0-1.4-.6-2.6-1.5-3.4.8-.8 1.3-1.9 1.3-3.1A4.5 4.5 0 0 0 14.5 2c-1.4 0-2.6.6-3.4 1.5A4.5 4.5 0 0 0 9.5 2z"/></svg>''',
    "user_doctor": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="7" r="4"/><path d="M5.5 21v-2a6.5 6.5 0 0 1 13 0v2"/><path d="M10 13v2a2 2 0 0 0 4 0v-2"/><circle cx="12" cy="18" r="1"/></svg>''',
    "warning": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>''',
    "check": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>''',
}


def get_icon(icon_key: str, color: str = None, width: str = None, height: str = None) -> str:
    """Get SVG icon with optional color and size styling."""
    svg = ICONS.get(icon_key, ICONS.get("brand", ICONS["dashboard"]))
    
    if color:
        svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
        svg = svg.replace('fill="currentColor"', f'fill="{color}"')
    
    if width or height:
        w_val = width or "24"
        h_val = height or "24"
        for orig_dim in ("24", "20", "18"):
            svg = svg.replace(f'width="{orig_dim}"', f'width="{w_val}"')
            svg = svg.replace(f'height="{orig_dim}"', f'height="{h_val}"')
    
    return svg