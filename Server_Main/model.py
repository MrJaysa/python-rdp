class Devices:
    def __init__(self, sid, rid, pwd, typ):
        self.sid  = sid
        self.rid  = rid
        self.pwd  = pwd
        self.typ  = typ

class Users:
    def __init__(self):
        self.users = []
    
    def create(self, sid, rid, pwd, typ):
        self.users.append(Devices(sid, rid, pwd, typ))

    def update_sid(self, id, sid):
        dev = self.get_devices_by_rid(id)
        if dev:
            dev.sid = sid

    def remove_by_sid(self, id):
        dev = self.get_devices_by_sid(id)
        if dev:
            self.users.remove(dev)

    def remove_by_rid(self, id):
        dev = self.get_devices_by_rid(id)
        if dev:
            self.users.remove(dev)

    def get_devices_by_rid(self, id):
        dev = [dev for dev in self.users if dev.rid == id]
        if dev:
            return dev[0]
        return False

    def get_devices_by_sid(self, id):
        dev = [dev for dev in self.users if dev.sid == id]
        if dev:
            return dev[0]
        return False

    
    def return_desktop_type(self):
        values = [vars(x) for x in list(filter(lambda item: item.typ == 'desktop', self.users))]
        return values

    def get_all_users(self):
        values = [vars(x) for x in self.users]
        return values

    def check_user(self, rid, pwd):
        dev = [dev for dev in self.users if dev.rid == rid and dev.pwd == pwd]
        if dev:
            return dev[0]
        return False
    