from app.enums.landUseType import LandUseType


class LandLord:
    def __init__(self, land_lord_name: str, password: str, email: str, phone_number: str, residential_address: str,
                 property_address: str, land_use_type: LandUseType, certificate_of_occupancy: str, plot_number: int,
                 virtual_account_number: str = None):
        self.land_lord_name = land_lord_name
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.residential_address = residential_address
        self.property_address = property_address
        self.land_use_type = land_use_type
        self.certificate_of_occupancy = certificate_of_occupancy
        self.plot_number = plot_number
        self.virtual_account_number = virtual_account_number

    @property
    def land_lord_name(self):
        return self._land_lord_name

    @land_lord_name.setter
    def land_lord_name(self, land_lord_name: str):
        self._land_lord_name = land_lord_name

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = password

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        self._email = email

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number: str):
        self._phone_number = phone_number

    @property
    def residential_address(self):
        return self._residential_address

    @residential_address.setter
    def residential_address(self, residential_address: str):
        self._residential_address = residential_address

    @property
    def property_address(self):
        return self._property_address

    @property_address.setter
    def property_address(self, property_address: str):
        self._property_address = property_address

    @property
    def land_use_type(self):
        return self._land_use_type

    @land_use_type.setter
    def land_use_type(self, land_use_type: str):
        self._land_use_type = land_use_type

    @property
    def certificate_of_occupancy(self):
        return self._certificate_of_occupancy

    @certificate_of_occupancy.setter
    def certificate_of_occupancy(self, certificate_of_occupancy: str):
        self._certificate_of_occupancy = certificate_of_occupancy

    @property
    def plot_number(self):
        return self._plot_number

    @plot_number.setter
    def plot_number(self, plot_number: int):
        self._plot_number = plot_number

    @property
    def virtual_account_number(self):
        return self._virtual_account_number

    @virtual_account_number.setter
    def virtual_account_number(self, virtual_account_number: str):
        self._virtual_account_number = virtual_account_number