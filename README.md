# Open Channel Hydraulics
Python modules to use in solving hydraulic elements of an open channel. This uses the Manning's equation in solving the hydraulic elements.

This project aims to create bits of modules for hydraulics engineering and later to be combined as one package for easier distribution. It aims to create an open source software for this subject to help both engineering students and instructors if they ever find this useful to them.

There are three types of open channel classes in this module <u>openchannel</u>, _rectangular_, _trapezoidal_ and _circular_.

Here are the checklist for this module:<br/>
- [x] Rectangular
- [x] Trapezoidal
- [x] Circular
- [ ] Irregular

All those unchecked are yet to be written.

## Notes:

- In the circular pipe class in the module open channel, I haven't incorporated yet the unit conversion. All units are assumed to be in metric. Although it's easy to incorporate it if you are to use it by subclassing it and override the getter and setter functions.

## Additions:
### 08/03/2016
- Uploaded a module irrig_channel. This module will calculate the discharge-elevation rating curve. Note that this module is not yet incorporated as a class in <b>Open Channel</b> module. This is a separate file for separate use.

Anyone who want to contribute, just contact me at alexius.academia@gmail.com
