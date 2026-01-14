# Level of priority
PRIORITY_LEVEL = {
    "high": 1,
    "medium": 3,
    "low": 7
}

# Required fields for a complete ticket
REQUIRED_FIELDS = [
    "ticket_id",
    "title",
    "requester",
    "created_date",
    "category"
]

# Category routing rules
CATEGORY_ROUTING = {
    "data_amendment": "Development Team",
    "system_access": "IT Team",
    "how_to_question": "Operations Team",
    "new_starter": "HR Team + IT Team",
    "technical_issue": "IT Team",
    "lending_query": "Product Team",
    "other": "Operations Team"
}

# Keywords for auto-categorisation
CATEGORY_KEYWORDS = {
    "data_amendment": ["update email", "change address", "amend record", "incorrect data"],
    "system_access": ["access request", "permission", "login issue", "password reset"],
    "how_to_question": ["how do i", "how to", "where can i find", "pricing matrix", "funding calculator"],
    "new_starter": ["new starter", "new joiner", "onboarding", "new employee"],
    "technical_issue": ["error", "bug", "not working", "system down", "crash"],
    "lending_query": ["lending criteria", "loan", "mortgage", "ltv", "interest rate"]
}

# Default response when no category matches
DEFAULT_CATEGORY = "other"

# Output settings
OUTPUT_FOLDER = "output"
OUTPUT_FILENAME = "processed_tickets.json"