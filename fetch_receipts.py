import imaplib
import email
import os
import datetime
from email.header import decode_header

# ==========================================
# CONFIGURATION
# ==========================================
# 1. Update these details with your email info
EMAIL_USER = "xxx@xxx.com"
EMAIL_PASS = "xxxxxxxxxxxxxxx"  # App Password
IMAP_SERVER = "imap.gmail.com"

# 2. Output directory for .eml files
OUTPUT_DIR = "collected_receipts"

# 3. Search Criteria
# Categories to help filter
KEYWORDS = [
    "Invoice", "Receipt", "Bill", "Order Confirmation", "Payment Processed",
    "Uber", "Deliveroo", "Just Eat", "Amazon", "Sainsbury", "Tesco"
]

# Keywords to exclude (Job spam filter)
NEGATIVE_KEYWORDS = [
    "hiring", "job", "vacancy", "internship", "career", "opportunity", 
    "apply", "role", "full time", "part time", "consultant", "interview"
]

# Date range: Last 2 years
DAYS_BACK = 730 
# ==========================================

def clean_filename(subject):
    """Sanitize the subject line to be a valid filename."""
    return "".join(c for c in subject if c.isalnum() or c in (' ', '_', '-')).strip()

def fetch_receipts():
    # Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Calculate date for search
        date_since = (datetime.date.today() - datetime.timedelta(days=DAYS_BACK)).strftime("%d-%b-%Y")
        
        print(f"Searching for emails since {date_since}...")

        total_saved = 0

        for keyword in KEYWORDS:
            if total_saved >= 200: 
                break
                
            print(f"Searching for keyword: {keyword}")
            # Search for emails with specific keyword and date
            status, messages = mail.search(None, f'(SINCE "{date_since}" BODY "{keyword}")')
            
            if status != "OK":
                continue

            email_ids = messages[0].split()
            # Get the latest ones first
            email_ids = email_ids[::-1] 

            for e_id in email_ids: # Iterate through all found, we will filter manually
                if total_saved >= 200:
                    break
                    
                res, msg_data = mail.fetch(e_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Decode subject
                        subject_header = msg["Subject"]
                        if subject_header:
                            subject, encoding = decode_header(subject_header)[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else "utf-8")
                        else:
                            subject = "No Subject"
                        
                        # FILTER: Check for negative keywords
                        if any(nk.lower() in subject.lower() for nk in NEGATIVE_KEYWORDS):
                            continue
                            
                        # Generate filename
                        filename = f"{clean_filename(subject)}.eml"
                        filepath = os.path.join(OUTPUT_DIR, filename)
                        
                        # Avoid duplicates
                        if os.path.exists(filepath):
                            continue
                        
                        # Save .eml file
                        with open(filepath, "wb") as f:
                            f.write(response_part[1])
                        
                        print(f"Saved: {filename}")
                        total_saved += 1
                        
                        # Limit per keyword to avoid one keyword dominating if we want variety, 
                        # but for "Invoice" we might want all of them. 
                        # Let's cap at 20 per keyword to keep it balanced, unless it's a very specific brand.
                        # Actually, let's just rely on the global limit for now, or a soft limit.
                        # We'll just break inner loop if we hit global limit.

        print(f"Done! Saved {total_saved} receipts to '{OUTPUT_DIR}' folder.")
        mail.close()
        mail.logout()

    except Exception as e:
        print(f"Error: {e}")
        print("Tip: If using Gmail, make sure 2FA is on and you are using an 'App Password'.")

if __name__ == "__main__":
    fetch_receipts()
