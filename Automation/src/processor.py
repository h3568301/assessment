from datetime import datetime

# Check if ticket has all required fields populated.
# Args: ticket (dict): Ticket data, required_fields (list): List of required field names
# Returns: dict: Validation result with is_valid flag and missing fields
def validate_ticket(ticket, required_fields):
        missing_fields = []
    
        for field in required_fields:
            if field not in ticket or not ticket[field]:
                missing_fields.append(field)
        
        return {
            "is_valid": len(missing_fields) == 0,
            "missing_fields": missing_fields
        }

# Validate that date string is in correct format (YYYY-MM-DD).
# Args: date_string (str): Date to validate
# Returns: bool: True if valid, False otherwise
def validate_date_format(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False
    

# Automatically assign category based on title and description keywords.
# Args: ticket (dict): Ticket data, category_keywords (dict): Keywords for each category, 
# default_category (str): Default if no match found
# Returns: str: Matched category or default
def auto_categorise(ticket, category_keywords, default_category):
    # Combine title and description for searching
    text_to_search = f"{ticket.get('title', '')} {ticket.get('description', '')}".lower()
    
    # Check each category's keywords
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in text_to_search:
                return category
    
    return default_category

# Get the team responsible for handling this category
# Args: ticket (dict): category (str): Ticket category, category_routing (dict): Category to team mapping
# Returns: str: Team name(s) responsible
def get_routing_team(category, category_routing):
    return category_routing.get(category, "Operations Team")

    
# Calculate how many days a ticket has been open.
# Args: created_date (str): Date ticket was created (YYYY-MM-DD)
# Returns: int: Number of days open, or -1 if date invalid
def calculate_days_open(created_date):
    if not validate_date_format(created_date):
        return -1
    
    created = datetime.strptime(created_date, "%Y-%m-%d")
    today = datetime.now()
    delta = today - created
    
    return delta.days

# Check if ticket is within the time, at risk, or overdue.
# Args: ticket (dict): Ticket data, priority_level (dict): days by priority
# Returns: dict: status with days_open, threshold, and status
def check_priority_status(ticket, priority_level):
    days_open = calculate_days_open(ticket.get("created_date", ""))
    priority = ticket.get("priority", "medium")
    threshold = priority_level.get(priority, 3)
    
    # Determine priority status
    if days_open < 0:
        status = "unknown"
    elif days_open > threshold:
        status = "overdue"
    elif days_open == threshold:
        status = "at_risk"
    else:
        status = "within_time"
    return {
        "days_open": days_open,
        "threshold": threshold,
        "status": status
    }

# Process a single ticket: validate, categorise, check priority, and route.
# Args: ticket (dict): Raw ticket data, config (dict): Configuration settings
# Returns: dict: Processed ticket with all enrichments
def process_ticket(ticket, config):
    result = ticket.copy()
    
    # Step 1: Validate completeness
    result["validation"] = validate_ticket(ticket, config["required_fields"])
    
    # Step 2: Auto-categorise if no category assigned
    if not ticket.get("category"):
        result["category"] = auto_categorise(
            ticket,
            config["category_keywords"],
            config["default_category"]
        )
        result["auto_categorised"] = True
    else:
        result["auto_categorised"] = False
    
    # Step 3: Assign routing team
    result["routing_team"] = get_routing_team(
        result["category"],
        config["category_routing"]
    )
    
    # Step 4: Check status
    result["pri"] = check_priority_status(ticket, config["pri_thresholds"])
    
    # Step 5: Set attention flag
    result["needs_attention"] = (
        not result["validation"]["is_valid"] or
        result["pri"]["status"] in ["overdue", "at_risk"]
    )
    
    return result

# Process a list of tickets and generate summary.
# Args: tickets (list): List of ticket dictionaries, config (dict): Configuration settings
# Returns: dict: Processing results with all tickets and summary stats
def process_all_tickets(tickets, config):
    processed = []
    summary = {
        "total": len(tickets),
        "valid": 0,
        "invalid": 0,
        "overdue": 0,
        "at_risk": 0,
        "within_time": 0,
        "by_category": {},
        "by_team": {}
    }
    
    for ticket in tickets:
        result = process_ticket(ticket, config)
        processed.append(result)
        
        # Update validation counts
        if result["validation"]["is_valid"]:
            summary["valid"] += 1
        else:
            summary["invalid"] += 1
        
        # Update priority counts
        pri_status = result["pri"]["status"]
        if pri_status in summary:
            summary[pri_status] += 1
        
        # Update category counts
        category = result["category"]
        summary["by_category"][category] = summary["by_category"].get(category, 0) + 1
        
        # Update team counts
        team = result["routing_team"]
        summary["by_team"][team] = summary["by_team"].get(team, 0) + 1
    
    return {
        "processed_tickets": processed,
        "summary": summary
    }