import datetime


class Package:
    def __init__(self, ID, street, city, state, zipcode, deadline, weight, notes, status):
        self.ID = ID
        self.truck = None
        self.status = status
        self.departureTime = None
        self.deliveryTime = None
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes

    def __str__(self):
        return ("ID: %s, %s, Status: %s, Departed: %s, Delivered: %s, Address: %s, %s, %s, %s, Deadline: %s, Weight: %s,"
                " Notes: %s" %
                (self.ID, self.truck, self.status, self.departureTime, self.deliveryTime, self.street, self.city,
                 self.state, self.zipcode, self.deadline, self.weight, self.notes))


