import requests
from django.conf import settings


class TikTokBusinessManager:
    """Gestionnaire TikTok Business"""

    @staticmethod
    def get_login_url():
        """URL pour connecter TikTok"""
        app_key = settings.TIKTOK_APP_KEY
        redirect_uri = settings.TIKTOK_REDIRECT_URI

        url = f"https://www.tiktok.com/v2/auth/authorize/?client_key={app_key}&response_type=code&scope=user.info.basic,video.upload&redirect_uri={redirect_uri}"
        return url

    @staticmethod
    def get_access_token(code):
        """Obtenir le token d'accès TikTok"""
        app_key = settings.TIKTOK_APP_KEY
        app_secret = settings.TIKTOK_APP_SECRET
        redirect_uri = settings.TIKTOK_REDIRECT_URI

        url = "https://open-api.tiktok.com/oauth/access_token/"

        data = {
            'app_key': app_key,
            'app_secret': app_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }

        response = requests.post(url, data=data)
        return response.json()

    @staticmethod
    def publish_video(access_token, open_id, listing, video_url):
        """Publier une vidéo sur TikTok"""
        try:
            url = "https://open-api.tiktok.com/video/upload/"

            description = f"{listing.title}\n💰 {listing.price:,.0f} FCFA\n{listing.description[:200]}\n\n#OCALM #Shopping #Afrique"

            data = {
                'access_token': access_token,
                'open_id': open_id,
                'video_url': video_url,
                'description': description
            }

            response = requests.post(url, data=data)
            result = response.json()

            if result.get('data', {}).get('video_id'):
                return {
                    'success': True,
                    'video_id': result['data']['video_id'],
                    'share_url': f"https://www.tiktok.com/@user/video/{result['data']['video_id']}"
                }
            return {'success': False, 'error': result.get('error', {}).get('message', 'Erreur')}
        except Exception as e:
            return {'success': False, 'error': str(e)}