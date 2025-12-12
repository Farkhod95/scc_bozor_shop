from modeltranslation.translator import translator


def translate_response(obj, fields: list[str], lang: str, is_admin: bool) -> dict:
    data = {"id": obj.id}

    for field in fields:
        if is_admin:
            data[field] = getattr(obj, field, None)
            data[f"{field}_uz"] = getattr(obj, f"{field}_uz", None)
            data[f"{field}_ru"] = getattr(obj, f"{field}_ru", None)
            data[f"{field}_en"] = getattr(obj, f"{field}_en", None)
            data[f"{field}_uz_cyrl"] = getattr(obj, f"{field}_uz_cyrl", None)
        else:
            translated_field = f"{field}_{lang}"
            value = getattr(obj, translated_field, None) or getattr(obj, field, None)
            data[field] = value
    return data



LANGS = ["uz", "ru", "en", "uz_cyrl"]

def expand_translated_fields(model, search_fields):
    opts = translator.get_options_for_model(model)
    translated_fields = opts.fields

    expanded = []

    for field in search_fields:
        base = field.split("__")[0]

        if base in translated_fields:
            for lang in LANGS:
                expanded.append(field.replace(base, f"{base}_{lang}"))
        else:
            expanded.append(field)

    return expanded