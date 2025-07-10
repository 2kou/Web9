import logging
import os
import shutil
from telethon import events
from datetime import datetime

logger = logging.getLogger(__name__)

async def handle_deploy(event, client):
    """
    Handle deployment command - sends the complete Railway package
    Premium feature for licensed users
    """
    try:
        user_id = event.sender_id
        
        # Check if user has premium access
        if not await is_premium_user(user_id):
            await event.respond("❌ **Accès premium requis**\n\nCette fonctionnalité est réservée aux utilisateurs premium.\nUtilisez `/valide` pour activer votre licence.")
            return
        
        await event.respond("📦 **Préparation du package Render complet...**\n\n⏳ Création du package avec corrections PostgreSQL et Telethon...")
        
        # Create the Render package
        import subprocess
        result = subprocess.run(['python', 'create_render_package.py'], capture_output=True, text=True, cwd='.')
        zip_path = 'TeleFeed_Render_Complete_Deploy.zip'
        
        if os.path.exists(zip_path):
            # Get file size for verification
            file_size = os.path.getsize(zip_path)
            size_kb = file_size / 1024
            
            # Send the ZIP file
            await client.send_file(
                user_id,
                zip_path,
                caption=f"""
🌐 **Package Render.com COMPLET - {size_kb:.1f} KB**

📁 **Contenu du package :**
• Configuration Render complète (render.yaml, main_render.py)
• Corrections erreurs PostgreSQL et Telethon intégrées
• Système de communication automatique Render ↔ Replit ↔ Bot
• Session manager avec fallback JSON
• Variables d'environnement préconfigurées
• Documentation complète avec instructions

🚀 **Prêt pour déploiement Render.com**

📋 **Instructions :**
1. Décompressez le fichier ZIP
2. Uploadez sur GitHub
3. Déployez sur Render.com (Web Service)
4. Configurez les variables d'environnement
5. Recevez automatiquement la notification de succès !

✅ **Erreurs PostgreSQL et Telethon corrigées**
✅ **Communication automatique silencieuse - Pas de messages "réveil toi"**
                """,
                attributes=[],
                force_document=True
            )
            
            logger.info(f"Complete Render package sent to user {user_id} - Size: {size_kb:.1f} KB")
            
        else:
            await event.respond("❌ **Package non disponible**\n\nLe package Render n'est pas encore généré. Veuillez réessayer.")
            
    except Exception as e:
        logger.error(f"Error in deploy handling: {e}")
        await event.respond("❌ Erreur lors du traitement du déploiement. Veuillez réessayer.")

async def is_premium_user(user_id):
    """Check if user has premium access"""
    # For now, allow admin user
    ADMIN_ID = int(os.getenv('ADMIN_ID', '1190237801'))
    return user_id == ADMIN_ID