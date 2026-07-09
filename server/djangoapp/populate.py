from .models import CarMake, CarModel

def initiate():
    car_make_data = [
        {"name": "Toyota", "description": "Toyota Motor Corporation"},
        {"name": "Ford", "description": "Ford Motor Company"},
        {"name": "Honda", "description": "Honda Motor Company"},
        {"name": "Nissan", "description": "Nissan Motor Co., Ltd."},
        {"name": "Chevrolet", "description": "Chevrolet Division of General Motors"},
    ]

    car_make_instances = []
    for data in car_make_data:
        car_make, created = CarMake.objects.get_or_create(
            name=data["name"],
            defaults={"description": data["description"]}
        )
        car_make_instances.append(car_make)

    car_model_data = [
        {"name": "Corolla", "type": "SEDAN", "year": 2020, "car_make": car_make_instances[0]},
        {"name": "Camry", "type": "SEDAN", "year": 2021, "car_make": car_make_instances[0]},
        {"name": "RAV4", "type": "SUV", "year": 2022, "car_make": car_make_instances[0]},
        {"name": "F-150", "type": "SUV", "year": 2021, "car_make": car_make_instances[1]},
        {"name": "Mustang", "type": "COUPE", "year": 2020, "car_make": car_make_instances[1]},
        {"name": "Civic", "type": "SEDAN", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "Accord", "type": "SEDAN", "year": 2022, "car_make": car_make_instances[2]},
        {"name": "CR-V", "type": "SUV", "year": 2021, "car_make": car_make_instances[2]},
        {"name": "Altima", "type": "SEDAN", "year": 2020, "car_make": car_make_instances[3]},
        {"name": "Rogue", "type": "SUV", "year": 2022, "car_make": car_make_instances[3]},
        {"name": "Silverado", "type": "SUV", "year": 2021, "car_make": car_make_instances[4]},
        {"name": "Malibu", "type": "SEDAN", "year": 2023, "car_make": car_make_instances[4]},
    ]

    for data in car_model_data:
        CarModel.objects.get_or_create(
            name=data["name"],
            type=data["type"],
            year=data["year"],
            car_make=data["car_make"]
        )

    print("Database populated successfully.")
