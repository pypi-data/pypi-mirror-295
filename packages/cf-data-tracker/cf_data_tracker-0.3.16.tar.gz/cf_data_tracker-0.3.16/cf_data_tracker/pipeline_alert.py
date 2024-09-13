import os
import boto3
from botocore.exceptions import ClientError
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

logger = logging.getLogger(__name__)

class PipelineAlert:
    """
    A class to manage pipeline alerts and send email reports.

    This class provides functionality to collect reports from different stages of a data pipeline
    and send a consolidated email report using Amazon SES.

    Attributes:
        ses_client (boto3.client): Amazon SES client for sending emails.
        sender_email (str): Email address used to send alerts.
        recipient_emails (list): List of email addresses to receive alerts.
        pipeline_name (str): Name of the pipeline, used in email subject and body.
        reports (dict): Dictionary to store reports from different pipeline stages.

    Environment Variables:
        AWS_REGION: AWS region for SES client (default: 'eu-west-2')
        SENDER_EMAIL: Email address to send alerts from
        RECIPIENT_EMAILS: JSON-formatted list of email addresses to receive alerts
        PIPELINE_NAME: Name of the pipeline for reporting
    """

    def __init__(self):
        """
        Initialize the PipelineAlert instance.

        Sets up the SES client and loads configuration from environment variables.
        """
        self.ses_client = boto3.client('ses', region_name=os.environ.get('AWS_REGION', 'eu-west-2'))
        self.sender_email = os.environ.get('SENDER_EMAIL', 'rami.reddy@carnallfarrar.com')
        self.pipeline_name = os.environ.get('PIPELINE_NAME', 'Data Ingestion Pipeline')
        self.reports = {}

        # Parse recipient emails
        try:
            recipient_emails = os.environ.get('RECIPIENT_EMAILS', '["rami.reddy@carnallfarrar.com"]')
            logger.debug(f"Recipient emails before parsing: {recipient_emails}")
            parsed_emails = json.loads(recipient_emails)
            logger.debug(f"Parsed emails: {parsed_emails}")
            if not isinstance(parsed_emails, list):
                raise ValueError("RECIPIENT_EMAILS must be a JSON array of strings")
            self.recipient_emails = parsed_emails
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing RECIPIENT_EMAILS: {e}")
            logger.info("Using default email: rami.reddy@carnallfarrar.com")
            self.recipient_emails = ["rami.reddy@carnallfarrar.com"]
        except ValueError as e:
            logger.error(f"Invalid RECIPIENT_EMAILS format: {e}")
            logger.info("Using default email: rami.reddy@carnallfarrar.com")
            self.recipient_emails = ["rami.reddy@carnallfarrar.com"]

    def add_report(self, pipeline_stage, report_type, message):
        """
        Add a report message for a specific pipeline stage and report type.

        Args:
            pipeline_stage (str): The stage of the pipeline (e.g., 'Raw', 'Clean').
            report_type (str): Type of the report ('ingestion' or 'error').
            message (str): The report message to be added.
        """
        if pipeline_stage not in self.reports:
            self.reports[pipeline_stage] = {'ingestion': [], 'error': []}
        
        if report_type in ['ingestion', 'error']:
            self.reports[pipeline_stage][report_type].append(message)

    def send_email_alert(self):
        """
        Compile and send the email alert with all collected reports.

        This method formats the email body in both HTML and plain text,
        and sends it using Amazon SES.

        Raises:
            ClientError: If there's an error sending the email via Amazon SES.
        """
        subject = f"{self.pipeline_name} Report"
        body_html = self._format_email_body_html()
        body_text = self._format_email_body_text()

        try:
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = ', '.join(self.recipient_emails)

            part1 = MIMEText(body_text, 'plain')
            part2 = MIMEText(body_html, 'html')

            message.attach(part1)
            message.attach(part2)

            response = self.ses_client.send_raw_email(
                Source=self.sender_email,
                Destinations=self.recipient_emails,
                RawMessage={'Data': message.as_string()}
            )
        except ClientError as e:
            logger.error(f"An error occurred while sending email: {e.response['Error']['Message']}")
        else:
            logger.info(f"Email sent! Message ID: {response['MessageId']}")

    def _format_email_body_html(self):
        """
        Format the email body in HTML.

        Returns:
            str: The formatted HTML body of the email.
        """
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; }}
                .pipeline {{ margin-bottom: 20px; }}
                .report {{ margin-left: 20px; }}
                .error {{ color: #e74c3c; }}
            </style>
        </head>
        <body>
            <h1>{self.pipeline_name} Report</h1>
        """
        
        for pipeline_stage, reports in self.reports.items():
            html += f"""
            <div class="pipeline">
                <h2>{pipeline_stage} Stage</h2>
                <div class="report">
                    <h3>Ingestion Report:</h3>
                    <ul>
                        {"".join(f"<li>{msg}</li>" for msg in reports['ingestion']) if reports['ingestion'] else "<li>No ingestion activity.</li>"}
                    </ul>
                    <h3>Error Report:</h3>
                    <ul class="error">
                        {"".join(f"<li>{msg}</li>" for msg in reports['error']) if reports['error'] else "<li>No errors reported.</li>"}
                    </ul>
                </div>
            </div>
            """
        
        html += "</body></html>"
        return html

    def _format_email_body_text(self):
        """
        Format the email body in plain text.

        Returns:
            str: The formatted plain text body of the email.
        """
        body = f"{self.pipeline_name} Report:\n\n"
        
        for pipeline_stage, reports in self.reports.items():
            body += f"{pipeline_stage} Stage:\n"
            body += "Ingestion Report:\n"
            body += "\n".join(f"- {msg}" for msg in reports['ingestion']) if reports['ingestion'] else "- No ingestion activity.\n"
            body += "\nError Report:\n"
            body += "\n".join(f"- {msg}" for msg in reports['error']) if reports['error'] else "- No errors reported.\n"
            body += "\n\n"
        
        return body

# Usage example:
"""
# Initialize the PipelineAlert
pipeline_alert = PipelineAlert()

# Add reports for different stages
pipeline_alert.add_report("Raw", "ingestion", "Processed 5 files successfully")
pipeline_alert.add_report("Raw", "error", "Failed to download 1 file")
pipeline_alert.add_report("Clean", "ingestion", "Cleaned and uploaded 3 files")

# Send the email alert
pipeline_alert.send_email_alert()
"""

# Note: Ensure that the necessary environment variables are set before using this class:
# - AWS_REGION
# - SENDER_EMAIL
# - RECIPIENT_EMAILS (as a JSON-formatted list)
# - PIPELINE_NAME