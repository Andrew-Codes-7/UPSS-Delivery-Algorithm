class Truck:
    def __init__(self, capacity, speed, mileage, current_location, depart_time, packages):
        self.capacity = capacity
        self.speed = speed
        self.mileage = mileage
        self.current_location = current_location
        self.time = depart_time
        self.depart_time = depart_time
        self.packages = packages


    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.packages, self.speed, self.mileage, self.time, self.depart_time,
                                           self.current_location)
