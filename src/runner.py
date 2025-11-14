thonpython
import json
import logging
from pathlib import Path

from extractors.email_parser import extract_emails_from_text
from extractors.filters import EmailFilters
from outputs.exporters import export_results

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

CONFIG_PATH = Path(__file__).parent / "config" / "settings.example.json"
DATA_SAMPLE = Path(__file__).parent.parent / "data" / "sample.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def load_input_data():
    with open(DATA_SAMPLE, "r") as f:
        return json.load(f)

def main():
    logging.info("Starting Amazon Email Scraper...")

    config = load_config()
    filters = EmailFilters(
        allowed_countries=config.get("allowedCountries", []),
        location_keyword=config.get("locationKeyword"),
        allowed_domain=config.get("allowedEmailDomain"),
    )

    raw_records = load_input_data()
    results = []

    for item in raw_records:
        text = item.get("content", "")
        keyword = item.get("keyword", "")
        country = item.get("country", "")
        location = item.get("location", "")
        source_url = item.get("sourceUrl", "")

        emails = extract_emails_from_text(text)
        for email in emails:
            if filters.apply(email=email, country=country, location=location):
                results.append({
                    "email": email,
                    "sourceUrl": source_url,
                    "keyword": keyword,
                    "location": location,
                    "country": country,
                    "emailType": email.split("@")[-1],
                })

    # Deduplicate by email
    deduped = {entry["email"]: entry for entry in results}.values()

    output_path = Path(__file__).parent.parent / "data" / "output.csv"
    export_results(list(deduped), output_path)

    logging.info(f"Scraping completed. Saved results to: {output_path}")

if __name__ == "__main__":
    main()