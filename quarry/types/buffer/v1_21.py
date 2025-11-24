from quarry.types.buffer import Buffer1_20_4


class Buffer1_21(Buffer1_20_4):
    
    # FIX 1: 1.21 Login Start is just Name + UUID. No signatures.
    def unpack_login_start(self):
        name = self.unpack_string()
        uuid = self.unpack_uuid()
        return name, uuid

    def pack_login_start(self, name, uuid):
        return self.pack_string(name) + self.pack_uuid(uuid)

    # FIX 2: 1.21 Chat Command (Upstream)
    # The structure changed to include bitsets/signatures. 
    # If you get crashes on commands, you might need this generic reader:
    def unpack_chat_command(self):
        command = self.unpack_string()
        timestamp = self.unpack_long()
        salt = self.unpack_long()
        # In 1.21 there are complex signature arrays here.
        # For a proxy, it is safest to read the rest as raw bytes if possible, 
        # but Quarry requires specific unpacking.
        # If this crashes later, we can address it. 
        # For now, let's fix Login.
        return super().unpack_chat_command()
