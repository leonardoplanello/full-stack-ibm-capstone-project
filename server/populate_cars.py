import os
import django
from djangoapp.models import CarMake, CarModel  # noqa: E402

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
django.setup()

# Create car makes
car_makes_data = [
    ('Audi', 'German luxury car manufacturer'),
    ('BMW', 'German luxury car manufacturer'),
    ('Mercedes-Benz', 'German luxury car manufacturer'),
    ('Toyota', 'Japanese automotive manufacturer'),
    ('Honda', 'Japanese automotive manufacturer'),
    ('Ford', 'American automotive manufacturer'),
    ('Chevrolet', 'American automotive manufacturer'),
    ('Nissan', 'Japanese automotive manufacturer'),
]

for name, description in car_makes_data:
    car_make, created = CarMake.objects.get_or_create(
        name=name,
        defaults={'description': description}
    )
    if created:
        print(f'Created CarMake: {name}')
    else:
        print(f'CarMake already exists: {name}')

# Create some car models
car_models_data = [
    ('Audi', 'A4', 'Sedan', 2020),
    ('Audi', 'Q5', 'SUV', 2021),
    ('BMW', '3 Series', 'Sedan', 2020),
    ('BMW', 'X5', 'SUV', 2021),
    ('Mercedes-Benz', 'C-Class', 'Sedan', 2020),
    ('Mercedes-Benz', 'GLE', 'SUV', 2021),
    ('Toyota', 'Camry', 'Sedan', 2020),
    ('Toyota', 'RAV4', 'SUV', 2021),
    ('Honda', 'Accord', 'Sedan', 2020),
    ('Honda', 'CR-V', 'SUV', 2021),
]

for make_name, model_name, car_type, year in car_models_data:
    try:
        car_make = CarMake.objects.get(name=make_name)
        car_model, created = CarModel.objects.get_or_create(
            car_make=car_make,
            name=model_name,
            defaults={'type': car_type, 'year': year}
        )
        if created:
            print(f'Created CarModel: {make_name} {model_name}')
    except CarMake.DoesNotExist:
        print(f'CarMake not found: {make_name}')

print(f'\nTotal CarMakes: {CarMake.objects.count()}')
print(f'Total CarModels: {CarModel.objects.count()}')
