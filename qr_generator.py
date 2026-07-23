"""
QR Code Generator for Clinic Registration Links
Generates QR codes that can be printed and displayed at clinic reception
"""

import qrcode
from io import BytesIO
import base64


def generate_clinic_qr(clinic_slug: str, base_url: str = "https://swasthai-2tv5.onrender.com") -> str:
    """
    Generate a QR code for a clinic's registration page.
    
    Args:
        clinic_slug: The unique slug identifier for the clinic
        base_url: The base URL of the application
    
    Returns:
        Base64 encoded PNG image of the QR code
    """
    # Construct the clinic-specific registration URL
    registration_url = f"{base_url}/c/{clinic_slug}"
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,  # Controls size (1 is smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4,
    )
    
    # Add data
    qr.add_data(registration_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in HTML
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_base64}"


def generate_clinic_qr_file(clinic_slug: str, output_path: str, base_url: str = "https://swasthai-2tv5.onrender.com"):
    """
    Generate a QR code and save it to a file.
    
    Args:
        clinic_slug: The unique slug identifier for the clinic
        output_path: Path where the QR code image will be saved
        base_url: The base URL of the application
    """
    registration_url = f"{base_url}/c/{clinic_slug}"
    
    # Create QR code instance with larger size for printing
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=15,
        border=4,
    )
    
    qr.add_data(registration_url)
    qr.make(fit=True)
    
    # Create and save image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    
    print(f"QR code saved to: {output_path}")
    print(f"URL: {registration_url}")


def get_clinic_url(clinic_slug: str, base_url: str = "https://swasthai-2tv5.onrender.com") -> str:
    """
    Get the full registration URL for a clinic.
    
    Args:
        clinic_slug: The unique slug identifier for the clinic
        base_url: The base URL of the application
    
    Returns:
        Full clinic registration URL
    """
    return f"{base_url}/c/{clinic_slug}"


if __name__ == "__main__":
    # Example usage - generate QR for clinic
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python qr_generator.py <clinic_slug> [output_file] [base_url]")
        print("Example: python qr_generator.py sample-clinic sample-clinic-qr.png https://swasthai-2tv5.onrender.com")
        sys.exit(1)
    
    clinic_slug = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"{clinic_slug}-qr.png"
    base_url = sys.argv[3] if len(sys.argv) > 3 else "https://swasthai-2tv5.onrender.com"
    
    generate_clinic_qr_file(clinic_slug, output_file, base_url)
