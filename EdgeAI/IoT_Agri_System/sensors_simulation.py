import random, time

def read_soil_moisture(): return random.uniform(30, 90)
def read_temperature(): return random.uniform(18, 35)
def read_humidity(): return random.uniform(40, 90)
def read_light(): return random.uniform(200, 1200)
def read_npk(): return {"N": random.uniform(10,50),"P": random.uniform(5,30),"K": random.uniform(10,40)}

def simulate_sensor_data():
    while True:
        data = {
            "soil_moisture": read_soil_moisture(),
            "temperature": read_temperature(),
            "humidity": read_humidity(),
            "light": read_light(),
            "npk": read_npk(),
        }
        print(data)
        time.sleep(2)

if __name__ == "__main__":
    simulate_sensor_data()
