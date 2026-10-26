from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology",
         "country": "Japan"},
        {"name": "Mercedes", "description": "Great cars. German technology",
         "country": "Germany"},
        {"name": "Audi", "description": "Great cars. German technology",
         "country": "Germany"},
        {"name": "Kia", "description": "Great cars. Korean technology",
         "country": "South Korea"},
        {"name": "Toyota", "description": "Great cars. Japanese technology",
         "country": "Japan"},
    ]

    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(CarMake.objects.create(**data))

    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "make": 0},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "make": 0},
        {"name": "XTRAIL", "type": "SUV", "year": 2023, "make": 0},
        {"name": "A-Class", "type": "SUV", "year": 2023, "make": 1},
        {"name": "C-Class", "type": "SUV", "year": 2023, "make": 1},
        {"name": "E-Class", "type": "SUV", "year": 2023, "make": 1},
        {"name": "A4", "type": "SUV", "year": 2023, "make": 2},
        {"name": "A5", "type": "SUV", "year": 2023, "make": 2},
        {"name": "A6", "type": "SUV", "year": 2023, "make": 2},
        {"name": "Sorrento", "type": "SUV", "year": 2023, "make": 3},
        {"name": "Carnival", "type": "SUV", "year": 2023, "make": 3},
        {"name": "Cerato", "type": "SEDAN", "year": 2023, "make": 3},
        {"name": "Corolla", "type": "SEDAN", "year": 2023, "make": 4},
        {"name": "Camry", "type": "SEDAN", "year": 2023, "make": 4},
        {"name": "Kluger", "type": "SUV", "year": 2023, "make": 4},
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data["name"],
            car_make=car_make_instances[data["make"]],
            type=data["type"],
            year=data["year"],
        )
