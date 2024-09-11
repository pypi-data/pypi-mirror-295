class EditContactType:
    def __init__(
            self,
            contact_id: int,
            country_code: int,
            email: str,
            firstname: str,
            image: str  ,
            is_show_portal: bool,
            lastname: str,
            phone: int):
        self.contact_id = contact_id
        self.country_code = country_code
        self.email = email
        self.firstname =firstname
        self.lastname = lastname
        self.image =image
        self.is_show_portal = is_show_portal
        self.phone = phone
    def prepare(self):
        return {
            "contact_id": self.contact_id,
            "country_code": self.country_code,
            "email": self.email,
            "firstname":self.firstname,
            "lastname": self.lastname,
            "image": self.image,
            "is_show_portal": self.is_show_portal,
            "phone": self.phone
        } 