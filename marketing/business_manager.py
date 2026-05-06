import requests
from datetime import datetime
from django.conf import settings
from django.contrib import messages


class IntegratedBusinessManager:
    """Business Manager intégré dans OCALM"""

    @staticmethod
    def get_facebook_login_url():
        """URL pour connecter Facebook Business"""
        app_id = settings.FACEBOOK_APP_ID
        redirect_uri = settings.FACEBOOK_REDIRECT_URI
        permissions = 'pages_manage_posts,pages_read_engagement,pages_read_user_content'

        return f"https://www.facebook.com/v18.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope={permissions}"

    @staticmethod
    def exchange_facebook_code(code):
        """Échanger le code contre un token"""
        app_id = settings.FACEBOOK_APP_ID
        app_secret = settings.FACEBOOK_APP_SECRET
        redirect_uri = settings.FACEBOOK_REDIRECT_URI

        url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            'client_id': app_id,
            'redirect_uri': redirect_uri,
            'client_secret': app_secret,
            'code': code
        }

        response = requests.get(url, params=params)
        return response.json()

    @staticmethod
    def get_user_pages(access_token):
        """Récupérer les pages Facebook du vendeur"""
        url = f"https://graph.facebook.com/v18.0/me/accounts?access_token={access_token}"
        response = requests.get(url)
        return response.json().get('data', [])

    @staticmethod
    def publish_to_facebook(page_id, page_token, listing):
        """Publier automatiquement sur Facebook"""
        try:
            url = f"https://graph.facebook.com/v18.0/{page_id}/feed"

            message = f"""🛍️ {listing.title}

{listing.description[:400]}

💰 Prix: {listing.price:,.0f} FCFA
🚚 Livraison: {listing.delivery_fee:,.0f} FCFA

🔒 Paiement sécurisé OCALM
✅ Livraison garantie

👉 Acheter: http://127.0.0.1:8000/listing/{listing.id}/

#OCALM #Shopping #Afrique #Vente"""

            payload = {
                'message': message,
                'access_token': page_token
            }

            response = requests.post(url, data=payload)
            result = response.json()

            if 'id' in result:
                return {
                    'success': True,
                    'post_id': result['id'],
                    'post_url': f"https://facebook.com/{result['id']}"
                }
            return {'success': False, 'error': result.get('error', {}).get('message', 'Erreur')}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_post_stats(post_id, access_token):
        """Récupérer les statistiques d'un post Facebook"""
        try:
            url = f"https://graph.facebook.com/v18.0/{post_id}/insights"
            params = {
                'metric': 'post_impressions,post_reactions,post_comments,post_shares',
                'access_token': access_token
            }
            response = requests.get(url, params=params)
            data = response.json()

            stats = {}
            for item in data.get('data', []):
                if item['name'] == 'post_impressions':
                    stats['views'] = item['values'][0]['value']
                elif item['name'] == 'post_reactions':
                    stats['likes'] = item['values'][0]['value']
                elif item['name'] == 'post_comments':
                    stats['comments'] = item['values'][0]['value']
                elif item['name'] == 'post_shares':
                    stats['shares'] = item['values'][0]['value']

            return stats
        except:
            return {'views': 0, 'likes': 0, 'comments': 0, 'shares': 0}

    @staticmethod
    def publish_to_instagram(instagram_id, access_token, listing, image_url):
        """Publier automatiquement sur Instagram"""
        try:
            # Créer le conteneur média
            container_url = f"https://graph.facebook.com/v18.0/{instagram_id}/media"
            caption = f"{listing.title}\n\n{listing.description[:200]}\n\n💰 {listing.price:,.0f} FCFA\n\n🔗 Lien dans la bio"

            container_data = {
                'image_url': image_url,
                'caption': caption,
                'access_token': access_token
            }

            container_response = requests.post(container_url, data=container_data)
            container = container_response.json()

            if 'id' not in container:
                return {'success': False, 'error': container.get('error', {}).get('message', 'Erreur')}

            # Publier
            publish_url = f"https://graph.facebook.com/v18.0/{instagram_id}/media_publish"
            publish_data = {
                'creation_id': container['id'],
                'access_token': access_token
            }

            publish_response = requests.post(publish_url, data=publish_data)
            result = publish_response.json()

            if 'id' in result:
                return {
                    'success': True,
                    'post_id': result['id'],
                    'post_url': f"https://instagram.com/p/{result['id']}"
                }
            return {'success': False, 'error': result.get('error', {}).get('message', 'Erreur')}
        except Exception as e:
            return {'success': False, 'error': str(e)}