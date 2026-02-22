# Email Receipt Fetcher

This project contains a Python script, `fetch_receipts.py`, designed to automate the process of "scraping" or fetching specific emails (like receipts, invoices, and order confirmations) from an email account using the IMAP protocol.

## Overview

The script connects to your email provider (e.g., Gmail), searches for emails matching specific financial keywords (e.g., "Invoice", "Uber", "Sainsbury"), and filters out unwanted emails (like job alerts). Matched emails are then downloaded and saved as `.eml` files locally.

## Features

*   **Automated Search:** Scans your inbox for keywords such as "Invoice", "Receipt", "Bill", "Order Confirmation", and specific vendors like "Uber" or "Deliveroo".
*   **Smart Filtering:** Excludes emails containing negative keywords (e.g., "hiring", "job", "apply") to avoid false positives from job boards or recruiters.
*   **Date Filtering:** Fetches emails from the last 2 years (configurable).
*   **Duplicate Prevention:** Checks if a file already exists before saving to avoid duplicates.
*   **Sanitized Filenames:** Saves files using the email subject line, cleaned of special characters.

## Prerequisites

*   Python 3.x installed on your system.
*   An email account with IMAP access enabled (e.g., Gmail).

## Configuration

Before running the script, you must configure your credentials in `fetch_receipts.py`:

1.  Open `fetch_receipts.py` in a text editor.
2.  Locate the **CONFIGURATION** section at the top of the file.
3.  Update the following variables:

    ```python
    EMAIL_USER = "your_email@example.com"
    EMAIL_PASS = "your_app_password"  # Do NOT use your regular login password
    IMAP_SERVER = "imap.gmail.com"      # Update if not using Gmail
    ```

### Important: Security Note for Gmail Users

If you are using Gmail, you **cannot** use your standard login password due to security restrictions. You must use an **App Password**:

1.  Go to your [Google Account Security settings](https://myaccount.google.com/security).
2.  Enable **2-Step Verification** if it isn't already.
3.  Search for "App passwords" in the account search bar.
4.  Create a new App Password (custom name: e.g., "Python Receipt Scraper").
5.  Copy the 16-character code and paste it into the `EMAIL_PASS` variable in the script.

## Usage

1.  Navigate to the project directory:
    ```bash
    cd /home/arjunaberdeen/job/upwork
    ```
2.  Run the script:
    ```bash
    python3 fetch_receipts.py
    ```

## Output

The script will create a folder named `collected_receipts` (if it doesn't exist) and populate it with `.eml` files.

*   **Output Directory:** `./collected_receipts/`
*   **File Format:** `.eml` (standard email format, readable by most email clients like Outlook, Thunderbird, or Apple Mail).

## Customization

You can modify the script to change:
*   **`KEYWORDS`**: Add or remove search terms to target different types of emails.
*   **`NEGATIVE_KEYWORDS`**: Add terms to exclude specific types of spam or irrelevant emails.
*   **`DAYS_BACK`**: Change how far back in time the script searches (default is 730 days / 2 years).
