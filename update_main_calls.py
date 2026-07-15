import codecs
import re

# Update main.py
main_path = 'backend/main.py'
with codecs.open(main_path, 'r', 'utf-8') as f:
    main_content = f.read()

main_content = main_content.replace(
    'response = ai_core.chat_with_assistant(req.message, history_dict, current_user.groq_api_key)',
    'response = ai_core.chat_with_assistant(req.message, history_dict, current_user)'
)
main_content = main_content.replace(
    'result = ai_core.generate_email_content(req.prompt, current_user.groq_api_key)',
    'result = ai_core.generate_email_content(req.prompt, current_user)'
)
main_content = main_content.replace(
    'result = ai_core.optimize_subject(req.subject, current_user.groq_api_key)',
    'result = ai_core.optimize_subject(req.subject, current_user)'
)
main_content = main_content.replace(
    'result = ai_core.generate_icebreakers(req.leads_csv, current_user.groq_api_key)',
    'result = ai_core.generate_icebreakers(req.leads_csv, current_user)'
)
main_content = main_content.replace(
    'result = ai_core.generate_autopilot_campaign(req.prompt, current_user.groq_api_key)',
    'result = ai_core.generate_autopilot_campaign(req.prompt, current_user)'
)
main_content = main_content.replace(
    'draft = ai_core.draft_reply_to_email(reply.body or "", current_user.groq_api_key)',
    'draft = ai_core.draft_reply_to_email(reply.body or "", current_user)'
)

with codecs.open(main_path, 'w', 'utf-8') as f:
    f.write(main_content)

print("Successfully updated backend/main.py")
