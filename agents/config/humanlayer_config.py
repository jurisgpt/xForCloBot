from humanlayer import HumanLayer, ApprovalWorkflow, Channel
from pathlib import Path
import os
from typing import Dict, Any

class NotificationConfig:
    """HumanLayer notification configuration"""
    
    def __init__(self):
        # Initialize HumanLayer with API key
        self.human_layer = HumanLayer(
            api_key=os.getenv("HUMANLAYER_API_KEY", "your-api-key")
        )
        
        # Configure channels
        self.channels = {
            "slack": {
                "channel": os.getenv("SLACK_CHANNEL", "#legal-notifications"),
                "workspace": os.getenv("SLACK_WORKSPACE", "your-workspace")
            },
            "email": {
                "to": os.getenv("NOTIFICATION_EMAIL", "legal-team@example.com")
            }
        }
        
    def create_approval_workflow(self, data: Dict[str, Any]) -> str:
        """Create a new approval workflow"""
        workflow = ApprovalWorkflow(
            title=data.get("title", "Legal Document Review Required"),
            description=data.get("description", ""),
            channels=[
                Channel.slack(
                    channel=self.channels["slack"]["channel"],
                    workspace=self.channels["slack"]["workspace"]
                ),
                Channel.email(
                    to=self.channels["email"]["to"]
                )
            ]
        )
        
        # Add workflow steps/content
        workflow.add_content(data.get("content", {}))
        
        # Submit workflow
        return self.human_layer.submit_workflow(workflow)
        
    def check_approval_status(self, workflow_id: str) -> Dict[str, Any]:
        """Check the status of an approval workflow"""
        return self.human_layer.get_workflow_status(workflow_id)
