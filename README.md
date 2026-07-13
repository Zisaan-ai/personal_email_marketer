# AI Email Marketer & Cold Email Platform

An advanced AI-powered cold email outreach and marketing automation platform. This application allows you to manage lead lists, configure multiple SMTP sending accounts, track email opens/clicks, and automatically generate personalized email sequences using AI (Google Gemini or Groq).

## Features
- **Campaign Management & Pacing**: Create campaigns with precise "Max Emails Per Day" limits and "Daily Ramp Up" for organic deliverability growth.
- **AI Integration**: Use Groq or Google Gemini to craft personalized emails, subject lines, and auto-reply sequences.
- **Smart Inbox & Health Monitor**: Multi-sender rotation with an automated health monitor that dynamically lowers daily limits based on account bounce rates.
- **Visual Sequence Builder**: Create drag-and-drop cold mail sequences with automated delays and multi-step follow-ups.
- **Analytics & Tracking**: Real-time open, click, bounce, and unsubscribe tracking.
- **Automated Replied Detection**: Auto-cancels follow-up steps if a lead replies.
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
