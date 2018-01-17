import usb.core
import usb.util

class Keyboard:
    VENDOR_ID = 0x28da
    PRODUCT_ID = 0x1301

    PACKET_LENGTH=264
    
    def __init__(self):
        self.red_map = [0]*126
        self.green_map = [0]*126
        self.blue_map = [0]*126

    def attach(self):
        # Find the keyboard
        self.dev = usb.core.find(idVendor=self.VENDOR_ID, idProduct=self.PRODUCT_ID)

        if self.dev is None:
            raise ValueError('Device not found')


        print("Found: {}".format(usb.util.get_string(self.dev, self.dev.iProduct)))

        print(self.dev)

        print("Detaching kernel driver...")

        for cfg in self.dev:
            for intf in cfg:
                if self.dev.is_kernel_driver_active(intf.bInterfaceNumber):
                    try:
                        self.dev.detach_kernel_driver(intf.bInterfaceNumber)
                    except usb.core.USBError as e:
                        sys.exit("Could not detach kernel driver from interface({0}): {1}".format(intf.bInterfaceNumber, str(e)))

                usb.util.claim_interface(self.dev, intf.bInterfaceNumber)


        cfg = self.dev.get_active_configuration()
        print("cfg", cfg)

        for intf in cfg:
            print("intf", intf)

        self.epi = usb.util.find_descriptor(intf, custom_match= \
            lambda e: \
            e.bEndpointAddress == 0x83)

        assert self.epi is not None

    def set_color(self, key, red, green, blue):
        key = key.value
        self.red_map[key]=red;
        self.green_map[key]=green;
        self.blue_map[key]=blue;

    def write_packet(self, packet):
        bmRequestType=0x21
        bRequest=9
        wValue=0x307
        wIndex = 1
        print(len(packet))
        r=self.dev.ctrl_transfer(bmRequestType=bmRequestType, bRequest=bRequest, wValue=wValue, wIndex=wIndex, data_or_wLength=packet)
        print("r", r)
        val = self.epi.read(0x83, 1024)
        print("val", val)
       
    def pad_packet(self, packet):
        packet.extend([0] * (self.PACKET_LENGTH - len(packet)))
        return packet
                
    def create_color_packet(self, color, colors):
       packet = [0x07, 0x09, 0x01, color, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]
       packet.extend(colors)
       return self.pad_packet(packet)

    def commit(self):
        intro_packet=self.pad_packet([0x07, 0x0d])
        self.write_packet(intro_packet)
        self.write_packet(self.create_color_packet(1, self.red_map))
        self.write_packet(self.create_color_packet(2, self.green_map))
        self.write_packet(self.create_color_packet(3, self.blue_map))
        


    def close(self):
        print('bye')
        usb.util.release_interface(self.dev, 0)
        usb.util.release_interface(self.dev, 1)

        for cfg in self.dev:
            print(cfg)
            for intf in cfg:
                print("\t{}".format(intf))
                try:
                    self.dev.attach_kernel_driver(intf.bInterfaceNumber)
                except usb.core.USBError as e:
                    print("Could not attach kernel driver from interface({0}): {1}".format(intf.bInterfaceNumber, str(e)))

                usb.util.dispose_resources(self.dev)
                self.dev.reset()


if __name__ == "__main__":
    from keys import Keys
    keyboard = Keyboard()
    keyboard.attach()
    keyboard.set_color(Keys.ENTER, 0xff, 0x0, 0x0)
    keyboard.set_color(Keys.KP_ENTER, 0x0, 0xff, 0x0)
    keyboard.set_color(Keys.SPACE, 0x0, 0x0, 0xff)
    
    keyboard.set_color(Keys.V, 0xff, 0xff, 0xff)
    keyboard.set_color(Keys.I, 0xff, 0xff, 0xff)
    keyboard.set_color(Keys.C, 0xff, 0xff, 0xff)

    keyboard.commit()
    keyboard.close()
