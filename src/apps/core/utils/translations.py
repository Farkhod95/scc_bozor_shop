def translate_response(obj, fields: list[str], lang: str, is_admin: bool) -> dict:
    data = {"id": obj.id}

    for field in fields:
        if is_admin:
            data[field] = getattr(obj, field, None)
            data[f"{field}_uz"] = getattr(obj, f"{field}_uz", None)
            data[f"{field}_ru"] = getattr(obj, f"{field}_ru", None)
            data[f"{field}_en"] = getattr(obj, f"{field}_en", None)
            data[f"{field}_kr"] = getattr(obj, f"{field}_kr", None)

        else:
            translated_field = f"{field}_{lang}"
            value = getattr(obj, translated_field, None) or getattr(obj, field, None)
            data[field] = value

    return data

