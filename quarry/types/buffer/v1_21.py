from quarry.types.buffer import Buffer1_20_4


class Buffer1_21(Buffer1_20_4):
    
    def unpack_login_start(self):
        name = self.unpack_string()
        uuid = self.unpack_uuid()
        return name, uuid

    def pack_login_start(self, name, uuid):
        return self.pack_string(name) + self.pack_uuid(uuid)

    # Server -> Client (IMPORTANTE per evitare il crash "game_profile")
    def unpack_login_success(self):
        uuid = self.unpack_uuid()
        name = self.unpack_string()
        
        # Legge le proprietà (Skin, ecc) per svuotare il buffer, anche se non le usiamo
        count = self.unpack_varint()
        for _ in range(count):
            self.unpack_string() # Name
            self.unpack_string() # Value
            if self.unpack_boolean(): # Has Signature
                self.unpack_string() # Signature
                
        return uuid, name

    # Fallback per i comandi
    def unpack_chat_command(self):
        return self.unpack_string()
