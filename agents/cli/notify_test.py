#!/usr/bin/env python3

import click
import json
from pathlib import Path
from typing import Dict
import sys
import os

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config.humanlayer_config import NotificationConfig
from data_store.store import SimpleStore

# Sample notification templates
TEMPLATES = {
    "new_case": {
        "title": "New Case Intake",
        "description": "New foreclosure case requires review",
        "content": {
            "case_type": "Foreclosure Defense",
            "priority": "High",
            "deadline": "48 hours",
            "documents_needed": [
                "Notice of Foreclosure",
                "Loan Documents",
                "Payment History"
            ]
        }
    },
    "risk_alert": {
        "title": "High Risk Alert",
        "description": "Critical timeline in foreclosure case",
        "content": {
            "risk_level": "Critical",
            "reason": "Sale date within 10 days",
            "recommended_actions": [
                "File TRO",
                "Request Emergency Hearing"
            ]
        }
    },
    "doc_request": {
        "title": "Document Request",
        "description": "Missing critical documents for case",
        "content": {
            "case_id": "FC-2025-123",
            "missing_documents": [
                "Proof of Service",
                "Chain of Title"
            ],
            "impact": "Cannot file response without these documents"
        }
    }
}

@click.group()
def cli():
    """Test notification system for legal case management"""
    pass

@cli.command()
@click.option('--template', type=click.Choice(TEMPLATES.keys()), 
              help='Notification template to use')
@click.option('--custom-data', type=str, 
              help='Custom JSON data for notification')
def send(template: str, custom_data: str):
    """Send a test notification"""
    try:
        # Initialize notification config
        config = NotificationConfig()
        
        # Get notification data
        if template:
            data = TEMPLATES[template]
        elif custom_data:
            data = json.loads(custom_data)
        else:
            click.echo("Error: Either --template or --custom-data must be provided")
            return
            
        # Send notification
        workflow_id = config.create_approval_workflow(data)
        
        # Store in data store
        store = SimpleStore(Path(os.getenv("DATA_STORE_PATH", "./data")))
        store.save("notifications", workflow_id, {
            "type": template if template else "custom",
            "data": data
        })
        
        click.echo(f"✅ Notification sent! Workflow ID: {workflow_id}")
        
    except Exception as e:
        click.echo(f"❌ Error sending notification: {str(e)}")

@cli.command()
@click.argument('workflow_id')
def status(workflow_id: str):
    """Check status of a notification workflow"""
    try:
        config = NotificationConfig()
        status = config.check_approval_status(workflow_id)
        
        # Pretty print status
        click.echo("📊 Workflow Status:")
        click.echo(json.dumps(status, indent=2))
        
    except Exception as e:
        click.echo(f"❌ Error checking status: {str(e)}")

@cli.command()
def list_templates():
    """List available notification templates"""
    click.echo("📝 Available Templates:")
    for name, template in TEMPLATES.items():
        click.echo(f"\n{name}:")
        click.echo("-" * len(name))
        click.echo(json.dumps(template, indent=2))

if __name__ == "__main__":
    cli()
