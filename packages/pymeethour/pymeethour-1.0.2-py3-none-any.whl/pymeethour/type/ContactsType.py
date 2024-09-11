class ContactsType:
    def __init__ (self, 
                 exclude_hosts: int,
                 limit: int,
                 page: int):
        self.exclude_hosts = exclude_hosts
        self.limit = limit
        self.page = page
    def prepare(self):
        return {
            "exclude_hosts": self.exclude_hosts,
            "limit": self.limit,
            "page": self.page
        } 