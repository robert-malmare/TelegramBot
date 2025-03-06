from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext
from telegram.helpers import escape_markdown
import os

# Token-ul primit de la BotFather
TOKEN = os.getenv("TOKEN", "7322765836:AAE4oVnSEUeoqjsdwWxvhoeh_szmkbBjLC0")

# Dicționarele tale (rămân neschimbate)
SQLSugar = {
    "sql_last_users": "SELECT id, user_name, date_modified, modified_user_id FROM users ORDER BY date_modified DESC LIMIT 10;",
    # ... (restul dicționarului SQLSugar)
    "sql_create_user": "UPDATE users\nSET user_hash = '$2y$10$Racn2ZN1JR1.pGVxICeW5O9O4gDWMznHkX90e8KOJ2G8jAiWLro9G'\nWHERE user_name = 'admin';"
}

NOTITE_BUG = {
    "bug_template": "Environment:\nSugar 14.0 instance:\nCredentials: wsysdev/ for password see wcreds or 1Password\nPackage name and version:\nSteps to reproduce:\nExpected results:\nActual results:\nPlease see the attached image/video",
    "db_port": "LocalForward 9884 10.3.1.67:22\nLocalForward 9883 10.3.1.169:22\nLocalForward 8998 10.3.2.20:3306\nLocalForward 8991 10.3.2.80:3306\nLocalForward 8990 10.3.2.119:3306\nHOST:127.0.0.1"
}

NOTITE_TEAMWORK = {
    "tw_deploy_message": "Hi,\nThe package [] version [] was successfully deployed on [x] production.\nAfter the package was installed in production, I ran a QRR and cleared cache.\nBest Regards,",
    "tw_title_template": "QA Issue [package name]: Titlu bug\nQA Feature [package name]: Titlu feature"
}

NOTITE_GIT = {
    "git_readme": "test(Readme): < Update Readme>\n[ QA Badge; QA Summary; Configuration ; Create Release]\nTW: <teamwork_task_url>",
    "git_readme_documentation": "Readme.MD updates !\nLa Documentation\nRequirements/User Guide: <link catre specs/user guide pt standalone>\nEstimated: Yes/No"
}

NOTITE_VSCODE = {
    "vscode_shortcuts": "✅ **VS Code Shortcuts:**\n- `Cmd + Shift + P` → Open Command Palette\n- `Cmd + B` → Toggle Sidebar\n- `Cmd + K + C` → Comment Code",
}

# Funcții
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = escape_markdown("👋 Bun venit, QA Team!\nSunt asistentul tău digital, gata să îți faciliteze munca de zi cu zi. Tastează /notite_list în chat pentru a explora comenzile disponibile și a vedea cum te pot sprijini în procesul de testare și validare!\nDacă vrei informații despre SQL, tastează: /sqlots.\nDacă vrei informații despre cum să creezi un template pentru un bug, tastează: /notite_bug.\nDacă vrei informații despre taskuri în Teamwork, tastează: /notite_teamwork.\nDacă vrei informații despre ReadMe în Git, tastează: /notite_git.", version=2)
    await update.message.reply_text(text, parse_mode="MarkdownV2")

async def notite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        text = escape_markdown("⚠️ Folosește comanda astfel: `/notite <categorie>`. Ex: `/notite sql_last_users`", version=2)
        await update.message.reply_text(text, parse_mode="MarkdownV2")
        return
    
    cheie = context.args[0].lower()
    for notite_dict in [SQLSugar, NOTITE_BUG, NOTITE_TEAMWORK, NOTITE_GIT, NOTITE_VSCODE]:
        if cheie in notite_dict:
            escaped_text = escape_markdown(notite_dict[cheie], version=2)
            await update.message.reply_text(escaped_text, parse_mode="MarkdownV2")
            return
    text = escape_markdown("❌ Notița nu există! Folosește `/notite_list` pentru a vedea toate opțiunile.", version=2)
    await update.message.reply_text(text, parse_mode="MarkdownV2")

async def notite_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lista_mesaje = escape_markdown("📌 **Lista de notițe disponibile:**\n", version=2)
    for notite_dict in [SQLSugar, NOTITE_BUG, NOTITE_TEAMWORK, NOTITE_GIT, NOTITE_VSCODE]:
        lista_mesaje += "\n".join([f"🔹 `{escape_markdown(cheie, version=2)}`" for cheie in notite_dict.keys()]) + escape_markdown("\n", version=2)
    
    footer = escape_markdown("\n👉 Folosește `/notite <cheie>` pentru a vedea detalii. Ex: `/notite sql_last_users`", version=2)
    await update.message.reply_text(f"{lista_mesaje}{footer}", parse_mode="MarkdownV2")

async def sqlots(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = escape_markdown("🔹 **Comenzi SQL disponibile pentru SugarCRM:**\n" +
                           "- `/notite sql_last_users` - Ultimii useri activi pe o instanta\n" +
                           "- `/notite sql_user_change_details` - ID,User cu status Admin despre care a facut schimbari pe o instanta\n" +
                           "- `/notite sql_active_users` - Utilizatori activi din instanta de Sugar\n" +
                           "- `/notite sql_available_modules` - Module disponibile dintr-o instanta\n" +
                           "- `/notite sql_api_modifications` - Ce API a facut modificari pe instanta\n" +
                           "- `/notite sql_user_modifications` - Userul care a facut modificari asupra unui utilizator\n" +
                           "- `/notite sql_account_changes` - Modificari facute de client pe Accounts\n" +
                           "- `/notite sql_sugar_errors` - Ultimele erori Sugar log\n" +
                           "- `/notite sql_users_roles` - Useri și rolurile lor\n" +
                           "- `/notite sql_users_no_roles` - Useri fără roluri\n" +
                           "- `/notite sql_module_changes` - Modificări într-un modul pe o instanta\n" +
                           "- `/notite sql_field_changed` - Schimbări recente pe un field\n" +
                           "- `/notite sql_api_created_records` - Înregistrări create prin API\n" +
                           "- `/notite sql_active_workflows` - Workflow-uri active\n" +
                           "- `/notite sql_sugar_errors_extended` - Erori Sugar \n" +
                           "- `/notite sql_temp_tables` - Tabele temporare\n" +
                           "- `/notite sql_temp_tables_creation` - Verificarea tabelelor temporare dintr-o baza de date\n" +
                           "- `/notite sql_temp_table_data` - Date dintr-un tabel temporar\n" +
                           "- `/notite sql_sugar_temp_tables` - Tabele temporare Sugar\n" +
                           "- `/notite sql_active_processes` - Procese active\n" +
                           "- `/notite sql_import_job_status` - Starea job-urilor de import\n" +
                           "- `/notite sql_recent_temp_tables` - Tabele temporare recente\n" +
                           "- `/notite sql_create_user` - Creare un user nou cu parola Welcome1\n" +
                           "- `/notite sql_recent_job_modifications` - Modificări recente job-uri", version=2)
    await update.message.reply_text(text, parse_mode="MarkdownV2")

async def notite_bug(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = escape_markdown("🔹 **Comenzi Bug disponibile:**\n" +
                           "- `/notite bug_template` - Template pentru Teamwork raportare bug\n" +
                           "- `/notite db_port` - Porturi pentru forwarding local pe care sa il folosesti cu Host = 127.0.0.1", version=2)
    await update.message.reply_text(text, parse_mode="MarkdownV2")

async def notite_teamwork(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = escape_markdown("🔹 **Comenzi Teamwork disponibile:**\n" +
                           "- `/notite tw_deploy_message` - Mesaj de deploy pe producție pentru Teamwork\n" +
                           "- `/notite tw_title_template` - Template pentru task-uri si change-uri in Teamwork", version=2)
    await update.message.reply_text(text, parse_mode="MarkdownV2")

async def notite_git(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = escape_markdown("🔹 **Comenzi Git disponibile:**\n" +
                           "- `/notite git_readme` - Mesaj pentru update Readme\n" +
                           "- `/notite git_readme_documentation` - Documentație pentru Readme.MD", version=2)
    await update.message.reply_text(text, parse_mode="MarkdownV2")

async def notite_vscode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = escape_markdown("🔹 **Comenzi VS Code disponibile:**\n" +
                           "- `/notite vscode_shortcuts` - Scurtături utile în VS Code", version=2)
    await update.message.reply_text(text, parse_mode="MarkdownV2")

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Eroare: {context.error}")

# Webhook server
from aiohttp import web

async def webhook_handler(request):
    update = Update.de_json(await request.json(), app.bot)
    await app.process_update(update)
    return web.Response(text="OK")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("notite", notite))
app.add_handler(CommandHandler("notite_list", notite_list))
app.add_handler(CommandHandler("sqlots", sqlots))
app.add_handler(CommandHandler("notite_bug", notite_bug))
app.add_handler(CommandHandler("notite_teamwork", notite_teamwork))
app.add_handler(CommandHandler("notite_git", notite_git))
app.add_handler(CommandHandler("notite_vscode", notite_vscode))
app.add_error_handler(error_handler)

async def main():
    port = int(os.getenv("PORT", 8443))
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    await app.bot.set_webhook(url=webhook_url)
    
    web_app = web.Application()
    web_app.router.add_post('/webhook', webhook_handler)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Botul rulează pe port {port} cu webhook {webhook_url}")
    await app.initialize()
    await app.start()
    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="/webhook",
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())