import requests
from django.conf import settings


class InstagramBusinessManager:
    """Gestionnaire Instagram Business"""

    @staticmethod
    def publish_photo(instagram_id, access_token, listing, image_url):
        """Publier une photo sur Instagram"""
        try:
            # Étape 1 : Créer le conteneur média
            create_url = f"https://graph.facebook.com/v18.0/{instagram_id}/media"
            caption = f"{listing.title}\n\n{listing.description[:200]}\n\n💰 {listing.price:,.0f} FCFA\n\n🔗 Lien dans la bio"

            create_data = {
                'image_url': image_url,
                'caption': caption,
                'access_token': access_token
            }

            create_response = requests.post(create_url, data=create_data)
            container = create_response.json()

            if 'id' not in container:
                return {'success': False, 'error': container.get('error', {}).get('message', 'Erreur')}

            # Étape 2 : Publier le conteneur
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
                    'url': f"https://instagram.com/p/{result['id']}"
                }
            return {'success': False, 'error': result.get('error', {}).get('message', 'Erreur')}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def publish_story(instagram_id, access_token, listing, image_url):
        """Publier une story Instagram"""
        try:
            url = f"https://graph.facebook.com/v18.0/{instagram_id}/stories"

            data = {
                'media_url': image_url,
                'caption': f"🛍️ {listing.title} - {listing.price:,.0f} FCFA",
                'access_token': access_token
            }

            response = requests.post(url, data=data)
            result = response.json()

            if 'id' in result:
                return {'success': True, 'story_id': result['id']}
            return {'success': False, 'error': result.get('error', {}).get('message', 'Erreur')}
        except Exception as e:
            return {'success': False, 'error': str(e)}