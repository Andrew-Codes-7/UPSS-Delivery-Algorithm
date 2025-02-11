#Author: Andrew Vigil
#Student ID: 4120979

import csv
import datetime
import truck
import package
from hash import CreateHash
from package import Package


with open("address_data.csv") as address_CSV:
    AddressCSV = csv.reader(address_CSV)
    AddressCSV = list(AddressCSV)

with open("distance_data.csv") as distance_CSV:
    DistanceCSV = csv.reader(distance_CSV)
    DistanceCSV = list(DistanceCSV)

with open("package_data.csv") as package_CSV:
    PackageCSV = csv.reader(package_CSV)
    PackageCSV = list(PackageCSV)



#Create pack objects from CSV
#Load packs into hash table
def load_package_data(filename, package_hash_table):
    with open(filename) as package_info:
        package_data = csv.reader(package_info, delimiter=',')
        next (package_data)
        for package in package_data:
            pID = int(package[0])
            # print(pID)
            pStreet = package[1]
            # print(pStreet)
            pCity = package[2]
            # print(pCity)
            pState = package[3]
            # print(pState)
            pZipCode = package[4]
            # print(pZipCode)
            pDeadline = package[5]
            # print(pDeadline)
            pWeight = package[6]
            # print(pWeight)
            pNotes = package[7]
            # print(pNotes)
            pStatus = "At Hub"
            # print(pStatus)

            #Package Object
            p = Package(pID, pStreet, pCity, pState, pZipCode, pDeadline, pWeight, pNotes, pStatus)

            #Insert
            package_hash_table.insert(pID, p)

#Create hash table
packageHash = CreateHash()

load_package_data("package_data.csv", packageHash)


#Method for finding distance between two locations
def between_address(address1, address2):
    distance = DistanceCSV[address1][address2]
    if distance == '':
        distance = DistanceCSV[address2][address1]
    return float(distance)

def extract_address(address):
    for row in AddressCSV:
        if address in row[2]:
            return int(row[0])



#Create Truck Object and Manually Load
truck1 = truck.Truck(16, 18, 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8), [13,14,15,16,19,20,30,31,34,40,24,26,37,39,29])

for pack in truck1.packages:
    obj = packageHash.search_hash(pack)
    obj.truck = "Truck 1"


truck2 = truck.Truck(16,18,0.0,"4001 South 700 East",
                     datetime.timedelta(hours=9.25), [6,25,3,18,36,2,1,32,33,38])

for pack in truck2.packages:
    obj = packageHash.search_hash(pack)
    obj.truck = "Truck 2"

truck3 = truck.Truck(16,18,0.0,"4001 South 700 East",
                     datetime.timedelta(hours=12), [10,23,35,27,4,5,7,8,9,11,12,17,21,22,28])
for pack in truck3.packages:
    obj = packageHash.search_hash(pack)
    obj.truck = "Truck 3"




#Delivering packages using algorithm
def deliver_packages(truck):
    #Creates a list for all the packages not delivered yet
    not_delivered = []
    #puts packages from the hash table into the not delivered list
    for packageID in truck.packages:
        package = packageHash.search_hash(packageID)
        not_delivered.append(package)

    #Clear the package list of a given truck
    truck.packages.clear()

    #cycle through list of not delivered until none
    #Adds the nearest package into the truck.packages list one by one
    while len(not_delivered) > 0:
        next_address = 2000
        next_package = None
        for package in not_delivered:
            # if package.ID == 6:
            #     next_package = package

            if between_address(extract_address(truck.current_location), extract_address(package.street)) <= next_address:
                next_address = between_address(extract_address(truck.current_location), extract_address(package.street))
                next_package = package

        truck.packages.append(next_package.ID)

        not_delivered.remove(next_package)

        truck.mileage += next_address

        truck.current_location = next_package.street

        truck.time += datetime.timedelta(hours=next_address / 18)

        next_package.deliveryTime = truck.time
        next_package.status = "Delivered"
        next_package.departureTime = truck.depart_time


deliver_packages(truck1)
deliver_packages(truck2)

#Makes sure that the 3rd truck doesn't leave before another one gets back.
truck3.depart_time = min(truck1.time, truck2.time)
deliver_packages(truck3)

class Main:
    # User Interface
    # Upon running the program, the below message will appear.

    while True:

        print("Western Governors University Parcel Service (WGUPS)")
        print("Select from the 4 options below:")
        print("1. Package Statuses and Total Miles for All 3 Trucks")
        print("2. Package Statuses at a specific time")
        print("3. Get single package status for a specific time")
        print("4. Exit the program")
        selection = int(input("Input selection: "))


        # Condition for choosing to just see the trucks total mileage
        if selection == 1:
            mile = truck1.mileage + truck2.mileage + truck3.mileage
            print()
            print(f"*** Total Miles for 3 Trucks: {mile} ***")
            print()
            for packageID in range(1,41):
                package = packageHash.search_hash(packageID)
                print(package)
            print()



        #     Condition for choosing to see info on ALL packages
        elif selection == 2:
            try:
                userTime2 = input("Please enter a time for which you'd like to see the status of all packages. Format: (24)HH:MM : ")
                (h, m) = userTime2.split(":")
                timeChange = datetime.timedelta(hours=int(h), minutes=int(m))

                for packageID in range(1,41):
                    package = packageHash.search_hash(packageID)

                    DelT = package.deliveryTime
                    str(DelT)
                    DepT = package.departureTime
                    str(DepT)

                    pack9address = "300 State St, Salt Lake City, UT 84103"
                    pack9time = "10:20"
                    (h, m) = pack9time.split(":")
                    pack9change = datetime.timedelta(hours=int(h), minutes=int(m))
                    stat = ""

                    if timeChange < DepT:
                        stat = "At Hub"
                        if packageID == 9:
                            print("ID:", package.ID, ", ", package.truck, ", Status:", stat, ", Address:",
                                  pack9address, ", Deadline:", package.deadline, ", Notes:",
                                  package.notes)
                        else:
                            print("ID:", package.ID, ", ",package.truck, ", Status:", stat, ", Address:", package.street,
                              package.state, package.zipcode, ", Deadline:", package.deadline, ", Notes:", package.notes)
                    elif timeChange < DelT:
                        stat = "En Route"
                        if packageID == 9:
                            if timeChange < pack9change:
                                print("ID:", package.ID, ", ",package.truck, ", Status:", stat, ", Departure:",
                                      package.departureTime, ", Address:", pack9address, ", Deadline:", package.deadline, ", Notes:",
                                      package.notes)
                            else:
                                print("ID:", package.ID, ", ",package.truck, ", Status:", stat, ", Departure:",
                                      package.departureTime, ", Address:", package.street,
                                      package.state, package.zipcode, ", Deadline:", package.deadline, ", Notes:",
                                      package.notes)
                        else:
                            print("ID:", package.ID, ", ",package.truck, ", Status:", stat, ", Departure:", package.departureTime, ", Address:", package.street,
                              package.state, package.zipcode, ", Deadline:", package.deadline, ", Notes:", package.notes)
                    else:
                        stat = "Delivered"
                        print("ID:", package.ID, ", ",package.truck, ", Status:", stat, ", Departure:", package.departureTime,
                              ", Delivery:", package.deliveryTime, ", Address:", package.street,
                              package.state, package.zipcode, ", Deadline:", package.deadline, ", Notes:", package.notes)

            except ValueError:
                print("Invalid Entry. Program Closing.")

        #Condition to see the status for A SINGLE package
        elif selection == 3:
            try:
                userTime = input("Please enter a time for which you'd like to see the status of a package. Format: HH:MM: ")
                (h, m) = userTime.split(":")
                timeChange = datetime.timedelta(hours=int(h), minutes=int(m))
                singleEntry = [int(input("Enter the package ID: "))]
            except ValueError:
                singleEntry = range(1, 41)
            for packageID in singleEntry:
                package = packageHash.search_hash(packageID)
                DelT = package.deliveryTime
                DepT = package.departureTime
                pack9address = "300 State St, Salt Lake City, UT 84103"
                pack9time = "10:20"
                (h, m) = pack9time.split(":")
                pack9change = datetime.timedelta(hours=int(h), minutes=int(m))
                stat = ""
                print()
                if timeChange < DepT:
                    stat = "At Hub"
                    if packageID == 9:
                        print("ID:", package.ID,  ", ",package.truck, ", Status:", stat, ", Address:",
                              pack9address, ", Deadline:", package.deadline, ", Notes:",
                              package.notes)
                    else:
                        print("ID:", package.ID, ", ",package.truck, ", Status:", stat, ", Address:",
                              package.street,
                              package.state, package.zipcode, ", Deadline:", package.deadline, ", Notes:",
                              package.notes)
                elif timeChange < DelT:
                    stat = "En Route"
                    if packageID == 9:
                        if timeChange < pack9change:
                            print("ID:", package.ID, ", ",package.truck, ", Status:", stat, ", Departure:",
                                  package.departureTime, ", Address:", pack9address, ", Deadline:", package.deadline,
                                  ", Notes:",
                                  package.notes)
                        else:
                            print("ID:", package.ID, ", ",package.truck, ", Status:", stat, ", Departure:",
                                  package.departureTime, ", Address:", package.street,
                                  package.state, package.zipcode, ", Deadline:", package.deadline, ", Notes:",
                                  package.notes)
                    else:
                        print("ID:", package.ID, ", ",package.truck, ", Status:", stat, ", Departure:",
                              package.departureTime, ", Address:", package.street,
                              package.state, package.zipcode, ", Deadline:", package.deadline, ", Notes:",
                              package.notes)
                else:
                    stat = "Delivered"
                    print("ID:", package.ID, ", ",package.truck, ", Status:", stat, ", Departure:",
                          package.departureTime,
                          ", Delivery:", package.deliveryTime, ", Address:", package.street,
                          package.state, package.zipcode, ", Deadline:", package.deadline, ", Notes:", package.notes)
                print()
        elif selection == 4:
            exit()

        else:
            exit()
