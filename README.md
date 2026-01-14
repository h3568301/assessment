# Ticket Processing & Automation System

A Python-based ticket processing system that automates the categorization, validation, and routing of incoming support tickets. Built as a demonstration of clean coding principles for the KSEYE technical assessment.

## Features

- **Ticket Validation** - Validates tickets against required fields
- **Auto-Categorization** - Intelligent keyword-based category assignment
- **Smart Routing** - Maps categories to appropriate teams (Dev, IT, HR, Operations, Product)
- **SLA Tracking** - Calculates priority status (overdue, at_risk, within_time_limit)
- **Attention Flagging** - Marks tickets needing human review
- **Summary Reports** - Generates actionable statistics

## Project Structure

```
Automation/
├── main.py                 # Entry point - orchestrates the workflow
├── config/
│   └── settings.py         # Configuration & business rules
├── src/
│   ├── __init__.py
│   └── processor.py        # Core processing logic
├── data/
│   └── sample_tickets.json # Input test data
└── output/
    └── processed_tickets.json # Generated output results
```

## Requirements

- Python 3.x
- No external dependencies (uses only Python standard library)

## Usage

Run the system from the `Automation/` directory:

```bash
cd Automation
python main.py
```

The system will:
1. Load tickets from `data/sample_tickets.json`
2. Validate and enrich each ticket
3. Print individual ticket details to console
4. Display summary statistics
5. Save results to `output/processed_tickets.json`

## Configuration

All business rules are centralized in `config/settings.py`:

| Setting | Description |
|---------|-------------|
| `PRIORITY_LEVEL` | SLA thresholds by priority (high: 1 day, medium: 3 days, low: 7 days) |
| `REQUIRED_FIELDS` | Fields required for ticket validation |
| `CATEGORY_ROUTING` | Maps categories to team assignments |
| `CATEGORY_KEYWORDS` | Keywords for auto-categorization |

## Supported Categories

| Category | Description | Routed To |
|----------|-------------|-----------|
| `data_amendment` | Email/address updates | Operations Team |
| `system_access` | Access/permission requests | IT Team |
| `how_to_question` | User guidance queries | Operations Team |
| `new_starter` | Onboarding requests | HR Team |
| `technical_issue` | System errors/bugs | Dev Team |
| `lending_query` | Financial/lending questions | Product Team |
| `other` | Default category | Operations Team |

## Data Model

### Input Ticket
```json
{
  "ticket_id": "TKT001",
  "title": "Please update customer email address",
  "description": "...",
  "requester": "John Smith",
  "created_date": "2026-01-05",
  "priority": "high",
  "category": null,
  "status": "open"
}
```

### Output (Enriched Ticket)
```json
{
  "ticket_id": "TKT001",
  "title": "Please update customer email address",
  "validation": {"is_valid": true, "missing_fields": []},
  "auto_categorised": true,
  "category": "data_amendment",
  "routing_team": "Operations Team",
  "pri": {"days_open": 9, "threshold": 1, "status": "overdue"},
  "needs_attention": true
}
```

## Code Quality

This project follows clean code best practices:

- **Single Responsibility** - Each function has one clear purpose
- **Clear Naming** - Descriptive function and variable names
- **Documentation** - Docstrings explaining purpose, arguments, and returns
- **Configuration Over Hardcoding** - Business rules externalized to settings
- **Modular Design** - Logic separated into distinct modules
- **No External Dependencies** - Uses only Python standard library for portability

## Extensibility

The system is designed for easy extension:

- **Add categories** - Update `CATEGORY_KEYWORDS` in settings
- **Modify routing** - Update `CATEGORY_ROUTING` mapping
- **Change validation** - Adjust `REQUIRED_FIELDS` list
- **API integration** - Processor logic is isolated for easy integration
- **AI enhancement** - Replace keyword matching with ML model
- **Database connection** - Replace file I/O with database operations

## License

This project was created for the KSEYE technical assessment.
