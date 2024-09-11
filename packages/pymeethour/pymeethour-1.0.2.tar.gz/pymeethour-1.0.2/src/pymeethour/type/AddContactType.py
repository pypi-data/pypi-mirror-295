class AddContactType:
    
    def __init__ (self,
        email: str,
        firstname: str,
        lastname: str = None,
        phone: int = None,
        country_code: str = None,
        image: str = None,
        is_show_portal: bool = None,
    ):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.country_code = country_code
        self.image = image
        self.is_show_portal = is_show_portal
    def prepare(self):
        addContact = {}
        addContact.update({
            "email": self.email,
            "firstname": self.firstname
        })
        if(self.lastname != None):
                 addContact.update({"lastname": self.lastname})
        if(self.phone != None):
                 addContact.update({"phone": self.phone})
        if(self.country_code != None):
                 addContact.update({"country_code": self.country_code})
        if(self.image != None):
                 addContact.update({"image": self.image})
        if(self.is_show_portal != None):
                 addContact.update({"is_show_portal": self.is_show_portal})
        return addContact
    