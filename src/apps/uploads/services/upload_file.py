from apps.uploads.models import File


def create_file(file, user=None):
    new_file = File.objects.create(file=file)
    return {"file": new_file.file.url}