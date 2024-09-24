from django.core.files.uploadedfile import SimpleUploadedFile


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
