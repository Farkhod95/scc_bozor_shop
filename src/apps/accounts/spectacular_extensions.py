from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing  import build_bearer_security_scheme_object

class JWTTokenScheme(OpenApiAuthenticationExtension):
    target_class = 'apps.core.auth.authentication.JWTAuthentication'
    name = 'JWTAuth'

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            token_prefix='Bearer',
            header_name='Authorization',
        )
