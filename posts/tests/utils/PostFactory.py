from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


class PostFactory:
    @staticmethod
    def generate_post_data(text='This is a test post!', photo=None):
        data = {}

        if text:
            data['text'] = text

        if photo:
            with open(f'tests/images/{photo}.png', 'rb') as image:
                data["photo"] = SimpleUploadedFile(
                    name=f'{photo}.png',
                    content=image.read(),
                    content_type='image/png')

        return data

    @staticmethod
    def create_a_post(client, text=None, photo=None):
        data = PostFactory.generate_post_data(text=text, photo=photo)

        return client.post(reverse('post-list'), data=data, format='multipart')
