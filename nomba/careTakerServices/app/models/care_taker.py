from datetime import datetime


class CareTaker:
    def __init__(self, id: str, name: str, phone_number: str, care_taker_email: str, password: str, flat_no: str, date: datetime):
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.care_taker_email = care_taker_email
        self.password = password
        self.flat_no = flat_no
        self.date = datetime.strftime(date, "%Y-%m-%d")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        self._phone_number = phone_number

    @property
    def care_taker_email(self):
        return self._care_taker_email

    @care_taker_email.setter
    def care_taker_email(self, care_taker_email):
        self._care_taker_email = care_taker_email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def flat_no(self):
        return self._flat_no

    @flat_no.setter
    def flat_no(self, flat_no):
        self._flat_no = flat_no

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    def __eq__(self, other):
        if not isinstance(other, CareTaker):
            return False
        return (self.id == other.id and
                self.name == other.name and
                self.phone_number == other.phone_number and
                self.flat_no == other.flat_no)
