# Hacking the G.Skill Ripjaws KM-570 RGB

## About
This is my attempt to bring some level of support for G.Skill's RIPJAWS KM-570 RGB gaming keyboard to Linux.

I'm running G.Skill's software under a Windows 7 guest on Linux, and capturing its USB traffic with Wireshark.

## Warning
I take no responsibility for damage this may cause to your keyboard.

## Firmware
G.Skill's software will try to update the firmware if necessary. I had no luck updating the firmware under VirtualBox. It bricked the keyboard. Luckily, it's relatively easy to recover. They keyboard has a small hole under one of the feet. Pressing it wilth a paper clip while plugging the keyboard into the USB port will make it appear as a storage device containing the firmware image as a file. Ideally, you should be able to remove that file and copy the new firmware image over. My attempts at doing this under Linux and Windows guest were not successful.  Luckily, my daughter's laptop can dual boot into Linux and Windows. I was able to update the firmware under a real Windows install.

## Progress
I've figured out some of the protocol, but so far, I am only able to reliably set static colors for the keys.  This assumes that the keyboard is already in that mode, and that no Lighting Effect is enabled.

I've also started to replicate G.Skill's software.  I haven't posted that yet because it uses some assets from their software, and I haven't asked permission to use them.

## Dependencies
PyUSB
