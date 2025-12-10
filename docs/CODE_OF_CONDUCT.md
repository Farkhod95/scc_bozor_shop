# Code of Conduct for TMS mono

#### Language: python 3.9

#### Description: This document outlines the set of coding policies that must be followed by developers in order to ensure consistent developer experience.

## 1. URL naming conventions

### 1.1 Names used in APIs should be in correct American English

### 1.2 Use intuitive, familiar terminology where possible (`delete` is preferred over `erase`, `clear`, `destroy`)

### 1.3 Use the same name or term for the same concept, including for concepts shared across APIs

```
Bad example:
- /api/v1/orders/bulk-delete/
- /api/v1/customers/delete/

Good example:
- /api/v1/orders/bulk-delete/
- /api/v1/customers/bulk-delete/
```

### 1.4 Use plural to indicate a collection type

```
Bad example:
- /api/v1/customer/

Good example:
- /api/v1/customers/
```

### 1.5 Use hyphens (-) to improve the readability of URIs

```
Bad example:
- /api/v1/orders/{id}/getTracking/
- /api/v1/orders/{id}/gettracking/
- /api/v1/orders/{id}/GetTracking/
- /api/v1/orders/{id}/get_tracking/

Good example:
- /api/v1/orders/{id}/get-tracking/
```

### 1.6 Use CRUD function names in URIs

```
Good example:
- GET /api/v1/orders/{id}/detail/
- GET /api/v1/orders/list/
- POST /api/v1/orders/create/
- PUT /api/v1/orders/{id}/update/
- PATCH /api/v1/orders/{id}/partial-update/
```

### 1.7 Provide unique URI for a resource when performing an action on it

```
Bad example:
- /api/v1/orders/{id}/trips/add-stop/ body: {"trip_id": 1, ...}

Good example:
- /api/v1/orders/{orderId}/trips/{tripId}/add-stop/
```

## 2. App structure

```
└── order
    ├──  __init__.py
    └──  migrations
    └──  models
                ├── __init__.py
                ├── order.py
                ├── trip.py
    └──  views
                ├── __init__.py
                ├── create_order.py
                ├── update_order.py
    └──  services
                ├── __init__.py
                ├── create_order.py
                ├── update_order.py
    ├──  admin.py
    ├──  apps.py
    ├──  urls.py
```

### 2.1 Serializers

#### 2.1.1 Naming conventions should be in VerbNoun form, and it should uniquely identify that serializer.

Compose serializer's name with the name of the corresponding view class, add `Request`, `Response` keywords as in the
example.

Bad example:

```python
class OrderCreateSerializer(Serializer):
    pass


class CreateOrderView(APIView):
    pass
```

Good example:

```python
class CreateOrderRequestSerializer(Serializer):
    pass


class CreateOrderResponseSerializer(Serializer):
    pass


class CreateOrderView(APIView):
    pass
```

#### 2.1.2 Use Serializer as a base class. Avoid using ModelSerializer.

Any Serializer definition should inherit from `apps.core.serializer.Serializer` class which returns immutable dictionary

Bad example:

```python
from rest_framework import serializers


class CreateOrderRequestSerializer(serializers.Serializer):
    pass


from rest_framework import serializers


class DetailOrderResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = (
            "created_datetime",
            "modified_datetime",
        )
```

Good example:

```python
from apps.core.serializer import Serializer


class CreateOrderRequestSerializer(Serializer):
    pass
```

#### 2.1.3 Serializers should be in their simplest form. They should not contain any validation except basic field validations.

Bad example:

```python
class CreateOrderRequestSerializer(Serializer):
    number = serializers.CharField(required=True)

    def validate_number(self, value):
        if self.instance and self.instance.number == value:
            return value
        if Order.objects.filter(number=value).exists():
            raise serializers.ValidationError("Order number already exists.")
        return value
```

Good example:

```python
class CreateOrderRequestSerializer(Serializer):
    number = serializers.CharField(required=True)
```

#### 2.1.4 Provide default values for not required fields (except in PATCH APIs)

This way you can directly access the key inside dict object returned by serializer, instead of checking for the key
or using `.get()` method which improves code readability and consistency.

Bad example:

```python
class CreateOrderRequestSerializer(Serializer):
    number = serializers.CharField(required=True)
    city = serializers.CharField(required=False)
    discount = serializers.DecimalField(required=False)


data.get('discount', 0)
```

Good example:

```python
class CreateOrderRequestSerializer(Serializer):
    number = serializers.CharField(required=True)
    city = serializers.CharField(required=False, default=None)
    discount = serializers.DecimalField(required=False, default=0)
    pass


data['discount']
```

#### 2.1.5 Define serializers in their corresponding view files (No need to separate them).

Bad example:

##### views/order.py:

```python
from .serializers import OrderSerializer, OrderListSerializer, OrderDetailSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    list_serializer_class = OrderListSerializer
    detail_serializer_class = OrderDetailSerializer

    def create(self, request, *args, **kwargs):
        pass
```

Good example:

##### views/create_order.py:

```python
class CreateOrderRequestSerializer(Serializer):
    pass


class CreateOrderResponseSerializer(Serializer):
    pass


class CreateOrderView(APIView):
    def post(self, request):
        pass
```

### 2.2 Services

#### 2.2.1 Structure your service files in immediate services/ folder, avoid nesting unless it makes sense.

Bad example:

```
services/order/create_order.py
services/trip/create_trip.py
services/ifta/create_ifta.py
```

Good example:

```
services/create_order.py
services/create_trip.py
services/create_ifta.py
```

#### 2.2.2 Follow Single Responsibility Principle, each service should be responsible for only one action

Bad example:

##### order.py:

```python
def create_order(*args, **kwargs):
    pass


def update_order(*args, **kwargs):
    pass
```

Good example:

##### create_order.py:

```python
def create_order(*args, **kwargs):
    pass
```

##### update_order.py:

```python
def update_order(*args, **kwargs):
    pass
```

#### 2.2.3 Use verb_noun naming convention on services

Bad example:

##### order_create.py:

```python
def order_create(*args, **kwargs):
    pass
```

Good example:

##### create_order.py:

```python
def create_order(*args, **kwargs):
    pass
```

#### 2.2.4 Use additional `protected` functions inside a service when required

That means only main function must be exposed, and protected functions must be used only inside that service.

Bad example:

##### create_order.py:

```python
def create_order(*args, **kwargs):
    validate()
    notify_driver()


def validate(*args, **kwargs)
    pass


def notify_driver():
    pass
```

Good example:

##### create_order.py:

```python
def create_order(*args, **kwargs):
    _validate()
    _notify_driver()


def _validate(*args, **kwargs)
    pass


def _notify_driver():
    pass
```

### 2.3 Views

#### 2.3.1 Use VerbNoun form in naming Views.

Bad example:

```python
class OrderCreateView(APIView):
    def post(self, request):
        pass
```

Good example:

```python
class CreateOrderView(APIView):
    def post(self, request):
        pass
```

#### 2.3.2 Use verb_noun form in naming view files.

Bad example:

```
views/order_create_view.py
views/order_create.py
```

Good example:

```
views/create_order.py
```

#### 2.3.3 Structure your view files in immediate views/ folder, avoid nesting unless necessary.

Bad example:

```
views/order/create_order.py
views/trip/create_trip.py
views/ifta/create_ifta.py
```

Good example:

```
views/create_order.py
views/create_trip.py
views/create_ifta.py
```

#### 2.3.4 Avoid using ViewSets and function views, instead use CBV(Class-Based Views) that are highly-customizable.

Bad example:

##### views/order.py:

```python
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    list_serializer_class = OrderListSerializer
    detail_serializer_class = OrderDetailSerializer

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass
```

Good example:

##### views/create_order.py:

```python
class CreateOrderView(APIView):
    def post(self, request):
        pass
```

##### views/update_order.py:

```python
class UpdateOrderView(APIView):
    def put(self, request):
        pass
```

#### 2.3.5 Keep views simple.
Views should focus solely on handling HTTP requests and responses. They should avoid complex business logic, serving primarily to convert incoming request data into a specific format using serializers.

Bad example:

##### views/update_order.py:

```python
class UpdateOrderView(APIView):
    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = UpdateOrderRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = update_order(order, serializer.data)
        notify_customer(order)

        serializer = UpdateOrderResponseSerializer(order)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
```

Good example:

##### views/update_order.py:

```python
class UpdateOrderView(APIView):
    def put(self, request, pk):
        serializer = UpdateOrderRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = update_order(pk, serializer.data)

        serializer = UpdateOrderResponseSerializer(order)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
```

### 2.4 Models

#### 2.4.1 Define foreign key relationship in quotes

Bad example:

```python
class Trip(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
```

Good example:

```python
class Trip(BaseModel):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
```

#### 2.4.2 Avoid placing any logic in model definition, all the logic should be in service layer

Bad example:

```python
class TripExpenses(BaseModel):
    quantity = models.DecimalField(max_digits=21, decimal_places=2)
    rate = models.DecimalField(max_digits=21, decimal_places=2)
    total_amount = models.DecimalField(max_digits=21, decimal_places=2)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.total_amount = self.quantity * self.rate
        super(TripExpenses, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
```

##### services/create_trip_expenses.py:

```python
TripExpenses.objects.create(quantity=quantity, rate=rate)
```

Good example:

```python
class TripExpenses(BaseModel):
    quantity = models.DecimalField(max_digits=21, decimal_places=2)
    rate = models.DecimalField(max_digits=21, decimal_places=2)
    total_amount = models.DecimalField(max_digits=21, decimal_places=2)
```

##### services/create_trip_expenses.py:

```python
TripExpenses.objects.create(quantity=quantity, rate=rate, total_amount=quantity * rate)
```

#### 2.4.3 Define Enums in model definition and use singular naming convention

Bad example:

```python
class OrderStatuses(models.TextChoices):
    BOOKED = "booked", "Booked"
    IN_TRANSIT = "in_transit", "In Transit"
    DELIVERED = "delivered", "Delivered"


class Order(BaseModel):
    status = models.CharField(max_length=35, choices=OrderStatuses.choices, default=Status.BOOKED)
```

Good example:

```python
class Order(BaseModel):
    class Status(models.TextChoices):
        BOOKED = "booked", "Booked"
        IN_TRANSIT = "in_transit", "In Transit"
        DELIVERED = "delivered", "Delivered"

    status = models.CharField(max_length=35, choices=Status.choices, default=Status.BOOKED)
```

#### 2.4.4 Use json field when applicable

Bad example:

```python
class Customer(BaseModel):
    billing_type = models.CharField(max_length=20, choices=TYPES, default=NONE)
    billing_terms_days = models.IntegerField(default=30, validators=[MaxValueValidator(99), MinValueValidator(1)])
    billing_payment_method = models.CharField(max_length=20, choices=BILLING_PAYMENT_METHOD_TYPES, default=OTHER)
    billing_email = models.EmailField(max_length=255, null=True, blank=True)
    billing_address1 = models.CharField(max_length=255, null=True, blank=True)
    billing_address2 = models.CharField(max_length=255, null=True, blank=True)
    billing_city = models.CharField(max_length=255, null=True, blank=True)
    billing_state = models.CharField(max_length=255, null=True, blank=True)
    billing_zip_code = models.CharField(max_length=255, null=True, blank=True)
```

Good example:

```python
class Customer(BaseModel):
    class BillingAddress(TypedDict):
        type: str
        terms_days: int
        payment_method: str
        email: str
        address1: str
        address2: str
        city: str
        state: str
        zip_code: str

    billing_address: BillingAddress = models.JSONField()
```

## 3. Testing

### 3.1 Structure

### 3.1.1 Test module structure

```
tests
    └── order
            └──  fixtures
                        └── test_create_order
                        └── test_update_order
            ├──  __init__.py
            ├──  test_create_order.py
            ├──  test_update_order.py
```

### 3.1.2 Avoid nesting unless it makes sense

Bad example:

```
tests
    └── order
            └──  fixtures
                        └── test_create_order
            ├──  __init__.py
            ├──  test_create_order.py
            └── trip
                   └──  fixtures
                                └── test_create_trip
                   ├──  __init__.py
                   ├──  test_create_trip.py
```

Good example:

```
tests
    └── order
            └──  fixtures
                        └── test_create_order
                        └── test_create_trip
            ├──  __init__.py
            ├──  test_create_order.py
            ├──  test_create_trip.py
```

### 3.1.3 Use test_verb_noun convention in naming test files.

Bad example:
`test_order_create.py`

Good example:
`test_create_order.py`

### 3.2 Test

### 3.2.1 Avoid mixing different endpoint tests inside single test file

Bad example:

##### tests/order/test_order.py:

```python
class TestOrder(APITestCase):
    def test_create_order(self):
        url = "/api/v1/orders/create/"

    def test_update_order(self):
        url = "/api/v1/orders/1/update/"
```

Good example:

##### tests/order/test_create_order.py:

```python
class TestCreateOrder(APITestCase):
    def test_create_order(self):
        url = "/api/v1/orders/create/"
```

##### tests/order/test_update_order.py:

```python
class TestUpdateOrder(APITestCase):
    def test_update_order(self):
        url = "/api/v1/orders/1/update/"
```

### 3.2.2 Use separate fixtures for separate test files and name fixture folder same as the name of the corresponding test file

Bad example:

##### tests/order/test_create_order.py:

```python
class TestCreateOrder(APITestCase):
    fixtures = [
        "tests/order/fixtures/test_order/*"
    ]

    def test_create_order(self):
        url = "/api/v1/orders/create/"
```

##### tests/order/test_update_order.py:

```python
class TestUpdateOrder(APITestCase):
    fixtures = [
        "tests/order/fixtures/test_order/*"
    ]

    def test_update_order(self):
        url = "/api/v1/orders/1/update/"
```

Good example:

##### tests/order/test_create_order.py:

```python
class TestCreateOrder(APITestCase):
    fixtures = [
        "tests/order/fixtures/test_create_order/*"
    ]

    def test_create_order(self):
        url = "/api/v1/orders/create/"
```

##### tests/order/test_update_order.py:

```python
class TestUpdateOrder(APITestCase):
    fixtures = [
        "tests/order/fixtures/test_update_order/*"
    ]

    def test_update_order(self):
        url = "/api/v1/orders/1/update/"
```

### 3.2.3 Avoid overloading tests with unnecessary fixtures

1. Do not write/include any fixture that doesn't play any role in testing except if it is a required foreign key.
2. Do not just copy&paste fixtures from other test fixtures, check and modify them to fully cover your case and delete
   unnecessary fixtures before using.

### 3.2.4 Use generic name and docstring in test functions to specify test case

Do not try to indicate a test's purpose fully in function name, that might lead to long and unclear test definitions.

Instead, use following naming style and write full explanation of the case as docstring in the test function.

Bad example:

```python
def test_cancel_order_in_booked_status(self):
    pass


def test_cancel_order_whose_settlement_is_in_paid_status(self):
    pass
```

Good example:

```python
def test_cancel_order_case_1(self):
    """
    Case: Attempt to cancel booked order
    Expected: Success
    """
    pass


def test_cancel_order_case_2(self):
    """
    Case: Attempt to cancel an order whose settlement is in paid status
    Expected: Failure
    """
    pass
```

### 3.2.5 Use model name as fixture model

Bad example:

```
[
  {
    "model": "order.orderstop",
    "pk": 1,
    "fields": {},
  }
]
```

Good example:

```
[
  {
    "model": "order.OrderStop",
    "pk": 1,
    "fields": {},
  }
]
```

### 3.2.6 Avoid mixing different fixtures into single file

Bad example:

##### fixtures/order.json:

```
[
  {
    "model": "order.Order",
    "pk": 1,
    "fields": {
      "customer": 1,
      "mc_number": 1,
      "created_datetime": "2024-11-06T23:14:01+00:00",
      "modified_datetime": "2024-11-06T23:14:01+00:00"
    }
  },
  {
    "model": "order.Trip",
    "pk": 1,
    "fields": {
      "order": 1,
      "pickup": 1,
      "delivery": 2,
      "created_datetime": "2024-11-06T23:14:01+00:00",
      "modified_datetime": "2024-11-06T23:14:01+00:00"
    }
  },
]
```

Good example:

##### fixtures/order.json:

```
[
  {
    "model": "order.Order",
    "pk": 1,
    "fields": {
      "customer": 1,
      "mc_number": 1,
      "created_datetime": "2024-11-06T23:14:01+00:00",
      "modified_datetime": "2024-11-06T23:14:01+00:00"
    }
  }
]
```

##### fixtures/trip.json:

```
[
  {
    "model": "order.Trip",
    "pk": 1,
    "fields": {
      "order": 1,
      "pickup": 1,
      "delivery": 2,
      "created_datetime": "2024-11-06T23:14:01+00:00",
      "modified_datetime": "2024-11-06T23:14:01+00:00"
    }
  },
]
```

### 3.2.7 When writing assert statements, use the value in place of expected field instead of a variable

Bad example:

```python
self.assertEqual(order.status, data["status"])
self.assertEqual(order.note, data["note"])
```

Good example:

```python
self.assertEqual(order.status, Order.BOOKED)
self.assertEqual(order.note, "Lorem ipsum dolor sit amet")
```

### 3.2.8 Pass query params as an argument in request

Bad example:

```python
def test_list_orders(self):
    response = self.client.get("/api/v1/orders/list/?page=1&page_size=20")
```

Good example:

```python
def test_list_orders(self):
    query_params = {
        "page": 1,
        "page_size": 20,
    }
    response = self.client.get("/api/v1/orders/list/", query_params)
```

## 3.3 Mocking

### 3.3.1 Use mock_{mocked function/method name} as a naming convention

Bad example:

```python
class TestCancelOrder(APITestCase):
    @mock.patch.object(SuperDispatchClient, "cancel_paid_order")
    def test_cancel_order(self, mock_cancel: Mock):
        pass
```

Good example:

```python
class TestCancelOrder(APITestCase):
    @mock.patch.object(SuperDispatchClient, "cancel_paid_order")
    def test_cancel_order(self, mock_cancel_paid_order: Mock):
        pass
```

### 3.3.2 Avoid mocking internal functions, mock only external calls

Bad example:

```python
class TestCancelOrder(APITestCase):
    @mock.patch("order.services.notify_customer")
    def test_cancel_order(self, mock_notify_customer: Mock):
        response = self.client.post("/api/v1/orders/1/cancel/")
        mock_notify_customer.assert_called_once()
```

Good example:

```python
class TestCancelOrder(APITestCase):
    @mock.patch.object(EmailClient, "send")
    def test_cancel_order(self, mock_send: Mock):
        response = self.client.post("/api/v1/orders/1/cancel/")
        mock_send.assert_called_once()
        # Assert arguments being passed to mock function as well if there is any
```

### 3.3.3 Use mocking in datetime-dependent tests

Bad example:

```python
class TestListWeeklyOrders(APITestCase):
    def test_list_weekly_orders(self):
        Order.objects.filter(pk__in=[1, 2]).update(created_datetime=datetime.now())
        response = self.client.get("/api/v1/orders/list-weekly-orders/")
```

Good example:

```python
class TestListWeeklyOrders(APITestCase):
    @mock.patch("django.utils.timezone.now")
    def test_list_weekly_orders(self, mock_now: Mock):
        mock_now.return_value = timezone.datetime(2024, 1, 5, tzinfo=timezone.utc)

        response = self.client.get("/api/v1/orders/list-weekly-orders/")
```
