import json
import os
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from googletrans import Translator
from apps.locations.models import City, Region

class Command(BaseCommand):
    help = 'Region va Tumanlarni 4 tilda bazaga yuklash'

    def handle(self, *args, **kwargs):
        translator = Translator()

        regions_path = os.path.join(settings.BASE_DIR, 'regions.json')
        districts_path = os.path.join(settings.BASE_DIR, 'districts.json')

        def translate_to_en(text_uz):
            try:
                res = translator.translate(text_uz, src='uz', dest='en')
                return res.text
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Tarjima xatosi ({text_uz}): {e}"))
                return text_uz

        if os.path.exists(regions_path):
            with open(regions_path, 'r', encoding='utf-8') as f:
                regions = json.load(f)

            self.stdout.write("Viloyatlar yuklanmoqda...")
            for r in regions:
                name_en = translate_to_en(r['name_uz'])
                time.sleep(0.2)

                Region.objects.update_or_create(
                    id=r['id'],
                    defaults={
                        'code': str(r['soato_id']),
                        'name_uz': r['name_uz'],
                        'name_en': name_en,
                        'name_ru': r['name_ru'],
                        'name_uz_cyrl': r['name_oz'],
                    }
                )
                self.stdout.write(f"V: {r['name_uz']} -> {name_en}")

        if os.path.exists(districts_path):
            with open(districts_path, 'r', encoding='utf-8') as f:
                districts = json.load(f)

            self.stdout.write("\nTumanlar yuklanmoqda (bu biroz vaqt oladi)...")
            for d in districts:
                try:
                    region_obj = Region.objects.get(id=d['region_id'])
                    name_en = translate_to_en(d['name_uz'])
                    time.sleep(0.3)

                    City.objects.update_or_create(
                        id=d['id'],
                        defaults={
                            'region': region_obj,
                            'code': str(d['soato_id']),
                            'name_uz': d['name_uz'],
                            'name_en': name_en,
                            'name_ru': d['name_ru'],
                            'name_uz_cyrl': d['name_oz'],
                        }
                    )
                except Region.DoesNotExist:
                    continue

            self.stdout.write(self.style.SUCCESS("\nBarcha ma'lumotlar 4 tilda saqlandi!"))