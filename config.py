import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class AppConfig:
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    sender_name: str
    dry_run: bool
    send_mode: str
    max_outreach_per_run: int
    input_path: str
    groq_api_key: str | None
    llm_provider: str
    llm_model: str

def load_config() -> AppConfig:
    """Loads and validates configuration from environment variables and .env file."""
    load_dotenv()
    
    # 1. SMTP settings
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com") or "smtp.gmail.com"
    
    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    except (ValueError, TypeError):
        smtp_port = 587
        
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    sender_name = os.getenv("SENDER_NAME", "")
    
    # 2. Safety settings (DRY_RUN default is True)
    dry_run_str = os.getenv("DRY_RUN", "true").lower().strip()
    if dry_run_str in ("false", "0", "no", "off"):
        dry_run = False
    else:
        dry_run = True
        
    send_mode = os.getenv("SEND_MODE", "draft").lower().strip()
    if send_mode not in ("draft", "send"):
        send_mode = "draft"
        
    try:
        max_outreach_per_run = int(os.getenv("MAX_OUTREACH_PER_RUN", "5"))
    except (ValueError, TypeError):
        max_outreach_per_run = 5
        
    # 3. Input and LLM settings
    input_path = os.getenv("INPUT_PATH", "contacts.json") or "contacts.json"
    
    groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not groq_api_key:
        groq_api_key = None
        
    llm_provider = os.getenv("LLM_PROVIDER", "groq") or "groq"
    llm_model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant") or "llama-3.1-8b-instant"
    
    return AppConfig(
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        smtp_user=smtp_user,
        smtp_password=smtp_password,
        sender_name=sender_name,
        dry_run=dry_run,
        send_mode=send_mode,
        max_outreach_per_run=max_outreach_per_run,
        input_path=input_path,
        groq_api_key=groq_api_key,
        llm_provider=llm_provider,
        llm_model=llm_model
    )
