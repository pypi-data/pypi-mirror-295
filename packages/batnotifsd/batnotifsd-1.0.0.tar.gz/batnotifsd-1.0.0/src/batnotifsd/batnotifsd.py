#!/usr/bin/env python3
# vim: set fenc=utf-8 ts=4 sw=0 sts=0 sr et si tw=0 fdm=marker fmr={{{,}}}:

# {{{ Imports
import pydbus
from gi.repository import GLib
# }}}

# {{{ Variables
# {{{ Basic
sysBus        = pydbus.SystemBus()
upowerBusName = "org.freedesktop.UPower"
# }}}

# {{{ Get battery path
upowerObject  = sysBus.get(upowerBusName, "/org/freedesktop/UPower")
upowerDevices = upowerObject.EnumerateDevices()

for devicePath in upowerDevices:                # go through all devices on dbus from upower
    bat = sysBus.get(upowerBusName, devicePath) # create a device to test its properties
    if bat.Type == 2:                           # if "Type" property is `2` (`"Battery"`)
        if bat.PowerSupply:                     # if "PowerSupply" property is `True`
            batteryPath = devicePath            # set battery path to that device path
# }}}
# }}}

# {{{ Functions
# {{{ Convert seconds to time remaining
def convertSeconds(totalSeconds):
    hours,   remainder = divmod(totalSeconds, 3600)
    minutes, seconds   = divmod(remainder, 60)
    return f"{int(hours)} h {int(minutes)} min"
# }}}

# {{{ Handle property changes
def handlePropChanges(interface, changedProperties, invalidatedProperties):
    if "State" in changedProperties or "WarningLevel" in changedProperties:
        # Refresh the values going into the notifications
        batPercentage      = int(bat.Percentage)
        roundBatPercentage = round(batPercentage, -1)

        timeToEmpty = convertSeconds(bat.TimeToEmpty)

        chargingIcon    = f"battery-level-{roundBatPercentage}-charging-symbolic"
        dischargingIcon = f"battery-level-{roundBatPercentage}-symbolic"

    if "State" in changedProperties:
        match changedProperties["State"]:
            case 1: notify(**notiMsg["Charging"])
            case 2: notify(**notiMsg["Discharging"])
            case 4: notify(**notiMsg["Charged"])

    if "WarningLevel" in changedProperties:
        match changedProperties["WarningLevel"]:
            case 3: notify(**notiMsg["Low"])
            case 4: notify(**notiMsg["Critical"])
# }}}
# }}}

# {{{ Defining the main elements
bat  = sysBus.get(upowerBusName, batteryPath)
loop = GLib.MainLoop()

# {{{ Notification function
def notify(appName="Battery", title="No title", message="No message body", duration=-1, icon="battery-level-100-symbolic"):
    bus      = pydbus.SessionBus()
    notifs   = bus.get(".Notifications")
    duration *= 1000

    notifs.Notify(appName, 0, icon, title, message, [], {}, duration)
# }}}
# }}}

# {{{ Notification messages
# {{{ Initialize variables that'll be refreshed in the main loop
batPercentage      = int(bat.Percentage)
roundBatPercentage = round(batPercentage, -1)

timeToEmpty = convertSeconds(bat.TimeToEmpty)

chargingIcon    = f"battery-level-{roundBatPercentage}-charging-symbolic"
dischargingIcon = f"battery-level-{roundBatPercentage}-symbolic"
# }}}

notiMsg ={
    # {{{ Fully charged
    "Charged": {
        "appName":  "Battery",
        "title":    "Fully charged",
        "message":  "Battery is fully charged. You may unplug your charger.",
        "icon":     "battery-level-100-charged-symbolic",
    },
    # }}}

    # {{{ Charging
    "Charging": {
        "appName":  "Battery",
        "title":    "Charging",
        "message":  "Charger plugged in.",
        "icon":     chargingIcon,
    },
    # }}}

    # {{{ Discharging
    "Discharging": {
        "appName":  "Battery",
        "title":    "Discharging",
        "message":  "Charger unplugged.",
        "icon":     dischargingIcon,
    },
    # }}}

    # {{{ Low
    "Low": {
        "appName":  "Battery",
        "title":    "Low battery",
        "message":  f"Battery is at {batPercentage}%. Please plug in a charger.\n{timeToEmpty} remaining.",
        "icon":     "battery-caution-symbolic",
    },
    # }}}

    # {{{ Critical
    "Critical": {
        "appName":  "Battery",
        "title":    "Critically low battery",
        "message":  f"Battery is at {batPercentage}%. Plug in a charger immediately or save your work and shut down.\n{timeToEmpty} remaining.",
        "duration": 20,
        "icon":     "battery-empty-symbolic",
    }
    # }}}
}
# }}}

bat.PropertiesChanged.connect(handlePropChanges)
loop.run()
