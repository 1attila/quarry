from quarry.types.buffer import Buffer1_20_4


class Buffer1_21(Buffer1_20_4):
    
    def unpack_login_start(self):
        # 1.21: Name + UUID
        name = self.unpack_string()
        uuid = self.unpack_uuid()
        return name, uuid

    def pack_login_start(self, name, uuid):
        return self.pack_string(name) + self.pack_uuid(uuid)

    # --- SERVER -> CLIENT (Il colpevole dell'errore game_profile) ---
    def unpack_login_success(self):
        # 1.21: UUID (16 byte) + Name (String) + Properties (Array)
        uuid = self.unpack_uuid()
        name = self.unpack_string()

        # Dobbiamo consumare le "Properties" (Skin, ecc) per svuotare il buffer
        # Altrimenti rimangono byte e Quarry pensa che il pacchetto sia corrotto
        count = self.unpack_varint()
        for _ in range(count):
            self.unpack_string() # Name
            self.unpack_string() # Value
            if self.unpack_boolean(): # Is Signed?
                self.unpack_string() # Signature

        return uuid, name

    # FIX: Login Success (Server -> Client)
    def pack_login_success_1_21(self, uuid, name):
        return (
            self.pack_uuid(uuid) + 
            self.pack_string(name) + 
            self.pack_varint(0) +     # Numero proprietà (0)
            self.pack_boolean(True)   # <--- ECCOLO! Strict Error Handling
        )

    # --- CHAT ---
    def unpack_chat_command(self):
        return self.unpack_string()
