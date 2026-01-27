import lxml.etree as ET
from django.db import transaction

from apps.bazars.models import BazarSection, Place
from apps.uploads.models import File


def create_bazar_section(bazar_id, name, file, user):
    svg_obj = File.objects.create(file=file)
    section = BazarSection.objects.create(
        bazar_id=bazar_id,
        name=name,
        svg=svg_obj,
        created_by=user
    )

    place_created_count = _create_places_from_svg(svg_obj.file, section.id, bazar_id)

    return {
        "id": section.id,
        "name": section.name,
        "svg": section.svg.file.url,
        "place_created_count": place_created_count
    }

def _create_places_from_svg(svg_file, section_id, bazar_id):
    svg_file.seek(0)

    try:
        parser = ET.XMLParser(recover=True, remove_comments=True)
        tree = ET.parse(svg_file, parser=parser)
        root = tree.getroot()
    except Exception as e:
        return {"error": f"SVG faylni o'qishda xatolik: {str(e)}"}

    ns = {'svg': 'http://www.w3.org/2000/svg'}

    prefix = 'svg:' if 'http://www.w3.org/2000/svg' in root.tag else ''

    places_to_create = []

    groups = root.xpath(f'.//{prefix}g/{prefix}g[@id]', namespaces=ns)

    for g_tag in groups:
        g_id = g_tag.get('id')

        for rect in g_tag.xpath(f'.//{prefix}rect[@prilavok_id]', namespaces=ns):
            prilavok_id = rect.get('prilavok_id')

            full_slug = f"{g_id}_{prilavok_id}"

            try:
                place_number = int(prilavok_id.split('_')[-1])
            except (ValueError, IndexError):
                place_number = 0

            places_to_create.append(
                Place(
                    slug=full_slug,
                    bazar_id=bazar_id,
                    section_id=section_id,
                    number=place_number,
                )
            )

    with transaction.atomic():
        created_instances = Place.objects.bulk_create(
            places_to_create,
            ignore_conflicts=True
        )

    return len(places_to_create)