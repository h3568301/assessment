import json
import os
from src.processor import process_all_tickets
from config.settings import (
    PRIORITY_LEVEL,
    REQUIRED_FIELDS,
    CATEGORY_ROUTING,
    CATEGORY_KEYWORDS,
    DEFAULT_CATEGORY,
    OUTPUT_FOLDER,
    OUTPUT_FILENAME
)

# Load tickets from JSON file.
# Args: filepath (str): Path to JSON file
# Returns: list: List of ticket dictionaries
def load_tickets(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)


# Save processed results to JSON file.
# Args: data (dict): Data to save, filepath (str): Output file path
def save_results(data, filepath):
    # Create output folder if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nResults saved to: {filepath}")


# Print formatted details for a single ticket.
# Args: ticket (dict): Processed ticket data
def print_ticket_details(ticket):
    print(f"\n{'='*50}")
    print(f"Ticket: {ticket.get('ticket_id', 'Unknown')}")
    print(f"Title: {ticket.get('title', 'No title') or 'No title'}")
    print(f"{'='*50}")
    print(f"Category: {ticket.get('category', 'Unknown')} {'(auto)' if ticket.get('auto_categorised') else ''}")
    print(f"Route to: {ticket.get('routing_team', 'Unknown')}")
    print(f"Priority: {ticket.get('priority', 'Unknown')}")
    print(f"Priority Status: {ticket['pri']['status'].upper()} ({ticket['pri']['days_open']} days open, threshold: {ticket['pri']['threshold']} days)")
    
    if ticket['validation']['is_valid']:
        print(f"Valid: Yes")
    else:
        print(f"Valid: No - Missing: {', '.join(ticket['validation']['missing_fields'])}")
    
    print(f"Needs Attention: {'YES' if ticket.get('needs_attention') else 'No'}")


# Print overall processing summary.
# Args: summary (dict): Summary statistics
def print_summary(summary):
    print(f"\n{'#'*50}")
    print("OVERALL SUMMARY")
    print(f"{'#'*50}")
    print(f"Total Tickets: {summary['total']}")
    print(f"Valid: {summary['valid']} | Invalid: {summary['invalid']}")
    print(f"Overdue: {summary['overdue']} | At Risk: {summary['at_risk']} | Within time: {summary['within_time']}")
    
    print(f"\nBy Category:")
    for category, count in summary['by_category'].items():
        print(f"  - {category}: {count}")
    
    print(f"\nBy Team:")
    for team, count in summary['by_team'].items():
        print(f"  - {team}: {count}")


def main():
    print("Ticket Processing Automation")    
    # Build configuration dictionary
    config = {
        "pri_thresholds": PRIORITY_LEVEL,
        "required_fields": REQUIRED_FIELDS,
        "category_routing": CATEGORY_ROUTING,
        "category_keywords": CATEGORY_KEYWORDS,
        "default_category": DEFAULT_CATEGORY
    }
    
    # Load sample tickets
    tickets = load_tickets("data/sample_tickets.json")
    print(f"Loaded {len(tickets)} tickets")
    
    # Process all tickets
    results = process_all_tickets(tickets, config)
    
    # Print individual ticket details
    for ticket in results["processed_tickets"]:
        print_ticket_details(ticket)
    
    # Print overall summary
    print_summary(results["summary"])
    
    # Save results to JSON
    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)
    save_results(results, output_path)


if __name__ == "__main__":
    main()