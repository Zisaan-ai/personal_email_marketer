# AI Email Marketer & Cold Email Platform

An advanced AI-powered cold email outreach and marketing automation platform. This application allows you to manage lead lists, configure multiple SMTP sending accounts, track email opens/clicks, and automatically generate personalized email sequences using AI (Google Gemini or Groq).

## Features
- **Campaign Management**: Create and schedule email campaigns.
- **AI Integration**: Use Groq or Google Gemini to craft personalized emails and subject lines.
- **Multi-Sender Rotation**: Add multiple SMTP accounts to distribute sending load.
- **Analytics & Tracking**: Real-time open, click, and bounce tracking.
- **Webhook Support**: Integrate with Make.com, Zapier, or custom endpoints for event triggers.

## Deployment Instructions

### Backend (Python / FastAPI)
1. Upload the `backend/` folder contents to your cPanel Python App directory (e.g., `xcomic_backend`).
2. Ensure you have selected **Python 3.11** in the Setup Python App section.
3. Add the required environment variables in the `.env` file (copy from `.env.example`).
4. Install dependencies via `requirements.txt`.
5. Restart the Python App from cPanel.

### Frontend (HTML/JS/CSS)
1. Upload the `frontend/` folder contents to the public web root (e.g., `public_html` or `xcomic.xyz`).
2. Ensure the `.htaccess` file is present to route traffic to the Python backend correctly.
3. Access your domain to view the application dashboard.

## Support
If you encounter any issues, please refer to the documentation or contact support.
