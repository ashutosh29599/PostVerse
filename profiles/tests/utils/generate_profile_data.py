from django.core.files.uploadedfile import SimpleUploadedFile


def generate_profile_data(user_id, first_name='Test', last_name='User', bio='This is the test bio!', photo=None):
    profile_data = {
        'user': user_id,
        'first_name': first_name,
        'last_name': last_name,
        'bio': bio,
    }

    if photo:
        with open(f'tests/images/{photo}.png', 'rb') as image:
            profile_data['photo'] = SimpleUploadedFile(
                name=f'{photo}.png',
                content=image.read(),
                content_type='image/png')

    return profile_data
