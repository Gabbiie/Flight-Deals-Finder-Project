class FlightData:
    """Contains details about a flight"""
    def __init__(self, origin_city, origin_code, destination_city, destination_code, price, departure_date,
                 return_date, stop_overs=0, via_city=""):
        self.origin_city = origin_city
        self.origin_code = origin_code
        self.destination_city = destination_city
        self.destination_code = destination_code
        self.price = price
        self.departure_date = departure_date
        self.return_date = return_date
        self.stop_overs = stop_overs
        self.via_city = via_city
