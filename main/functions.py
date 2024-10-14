import math

OFFICE_LAT = '42.8738439'
OFFICE_LON = '74.5765609'


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    delta_phi = math.radians(float(lat2) - float(lat1))
    delta_lambda = math.radians(float(lon2) - float(lon1))

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  
    return distance

def check_employee_in_office(lat_employee, lon_employee, radius=100):
    distance = haversine(lat_employee, lon_employee, OFFICE_LAT, OFFICE_LON)
    return distance <= radius
 