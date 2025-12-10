# Layers

## Introduction

![img.png](img.png)

## Views

Views should focus solely on handling HTTP requests and responses. They should avoid complex business logic, serving primarily to convert incoming request data into a specific format using serializers.

### Serializer

Serializers are responsible for validating and transforming data but should not contain business logic or database queries. Their primary purpose is to ensure that the data conforms to expected formats and rules.

### Example Implementation

Here’s an example of how to implement a view and serializer for creating a user:

```python
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from app.services import create_user

class CreateUserSerializerRequest(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=255)
    last_name = serializers.CharField(required=True, max_length=255)
    is_active = serializers.BooleanField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=128)

class CreateUserSerializerResponse(serializers.Serializer):
    id = serializers.IntegerField()

@api_view(["POST"])
def create_user_handler(request):
    # Validate incoming data using the request serializer
    request_serializer = CreateUserSerializerRequest(data=request.data)
    request_serializer.is_valid(raise_exception=True)

    # Create the user using the validated data
    user = create_user(request.user, request_serializer.validated_data)

    # Prepare the response serializer with the newly created user's ID
    response_serializer = CreateUserSerializerResponse({'id': user.id})

    # Return a successful response with the user's ID
    return Response(status=status.HTTP_201_CREATED, data=response_serializer.data)
```

### Key Points:
- **Views**: Designed to handle HTTP requests and responses, keeping the logic minimal and clean.
- **Serializers**: Focused on simple data validation and transformation, ensuring that input data meets the required criteria.
- **Example Implementation**: Provides a clear demonstration of how to create a user, validate input data, and return a structured response.

By maintaining clear separation between views and serializers, the application remains modular and easier to maintain.
