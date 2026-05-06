import requests
from django.conf import settings
from django.contrib import messages


class FacebookBusinessManager:
    """Gestionnaire Facebook Business"""

    @staticmethod
    def get_login_url():
        """URL pour connecter Facebook"""
        app_id = settings.FACEBOOK_APP_ID
        redirect_uri = settings.FACEBOOK_REDIRECT_URI
        permissions = 'pages_manage_posts,pages_read_engagement,pages_manage_metadata'

        url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope={permissions}"
        return url

    @staticmethod
    def exchange_code_for_token(code):
        """Échanger le code contre un token"""
        app_id = settings.FACEBOOK_APP_ID
        app_secret = settings.FACEBOOK_APP_SECRET
        redirect_uri = settings.FACEBOOK_REDIRECT_URI

        url = f"https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            'client_id': app_id,
            'redirect_uri': redirect_uri,
            'client_secret': app_secret,
            'code': code
        }

        response = requests.get(url, params=params)
        return response.json()

    @staticmethod
    def get_page_access_token(user_access_token):
        """Obtenir le token de la page"""
        url = f"https://graph.facebook.com/v18.0/me/accounts?access_token={user_access_token}"
        response = requests.get(url)
        data = response.json()

        if 'data' in data and len(data['data']) > 0:
            return data['data'][0]['access_token'], data['data'][0]['id']
        return None, None

    @staticmethod
    def publish_to_page(page_id, page_token, listing, image_url=None):
        """Publier automatiquement sur la page Facebook"""
        try:
            url = f"https://graph.facebook.com/v18.0/{page_id}/feed"

            message = f"""🛍️ {listing.title}

{listing.description[:300]}

💰 Prix: {listing.price:,.0f} FCFA
🚚 Livraison: {listing.delivery_fee:,.0f} FCFA

🔒 Paiement sécurisé OCALM
✅ Livraison garantie

👉 Acheter: http://127.0.0.1:8000/listing/{listing.id}/"""

            payload = {
                'message': message,
                'access_token': page_token
            }

            if image_url:
                payload['link'] = image_url

            response = requests.post(url, data=payload)
            result = response.json()

            if 'id' in result:
                return {
                    'success': True,
                    'post_id': result['id'],
                    'url': f"https://facebook.com/{result['id']}"
                }
            return {'success': False, 'error': result.get('error', {}).get('message', 'Erreur')}
        except Exception as e:
            return {'success': False, 'error': str(e)}