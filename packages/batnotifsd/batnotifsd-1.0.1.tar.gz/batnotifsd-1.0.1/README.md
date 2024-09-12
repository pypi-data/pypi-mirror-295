<!-- vim: set fenc=utf-8 ts=2 sw=0 sts=0 sr et si tw=0 fdm=marker fmr={{{,}}}: -->
# `batnotifsd` — Battery notifications daemon

<!-- {{{ What -->
## What
This is a Python script that sends notifications about the battery's status
(charger plugged in/unplugged, low/critical battery levels).

It's useful for window managers where you don't get this functionality out of
the box like in a desktop environment.
<!-- }}} -->

<!-- {{{ Why -->
## Why
I wrote this because I simply could not find anything else that did the job 100%
right. The internet is full of shell scripts that just tap into
`/sys/class/power_supply` and take info from that in a `while true` loop with a
`sleep`, most don't even autodetect the laptop's battery and they make you set a
variable for the right battery for you, or, even worse, manually edit the shell
script to put it in.
<!-- }}} -->

<!-- {{{ How -->
## How
This Python script uses the [pydbus](https://github.com/LEW21/pydbus) library to
get information directly from [UPower](https://upower.freedesktop.org/) through
[DBus](https://dbus.freedesktop.org/), and then send it back through DBus using
the `org.freedesktop.Notifications` bus, all in a
[GLib](https://pygobject.gnome.org/) loop.

Also, it automatically detects the first battery that
classifies as a laptop battery[^1].
<!-- }}} -->

<!-- {{{ Usage -->
## Usage
<!-- {{{ Help (click to expand) -->
<!--<details>
  <summary><h3>Help (click to expand)</h3></summary>

  ```console
  $ batnotifsd --help
  ```
</details>-->
<!-- }}} -->

To start the daemon, simply use:
```console
$ batnotifsd
```

You probably want to add it to the autostart of your window manager, check with
your WM's documentation for that.
<!-- }}} -->

<!-- {{{ Packages -->
## Packages
<!-- {{{ Packages -->
### NixOS
A derivation for this package is available inside
[my Nix package collection](https://github.com/Andy3153/my-nixpkgs/).
Just follow
[my-nixpkgs/Usage](https://github.com/Andy3153/my-nixpkgs/?tab=readme-ov-file#usage)
to add the flake to your config and to add the program to your
`environment.systemPackages`.

Right now I'm the only person actually using this program, so it's only
available in the repo with my personal Nix derivations. If there's going to be
any interest in it, I'll upstream a derivation into Nixpkgs.

Feel free to just take out the derivation from the
[pkgs/](https://github.com/Andy3153/my-nixpkgs/tree/master/pkgs) folder and
stick it in your configuration, if you know what you're doing.
<!-- }}} -->

<!-- {{{ PyPi -->
### PyPi
This script is available in PyPi [here](https://pypi.org/project/batnotifsd/).
To install it using `pip`, run:
```console
$ pip install batnotifsd
```
<!-- }}} -->
<!-- }}} -->

<!-- {{{ About the flake -->
## About the flake
The Nix flake present in this repo is just the development shell I use to test
this script.
<!-- }}} -->

<!-- {{{ More info -->
## More info
- [pydbus documentation](https://pydbus.readthedocs.io/)
- [pydbus tutorial](https://pydbus.readthedocs.io/en/latest/legacydocs/tutorial.html)
(teaches how to actually take values out of DBus)
- [pydbus notification example](https://pydbus.readthedocs.io/en/latest/legacydocs/shortexamples.html?highlight=notifi#send-a-desktop-notification)
(teaches how to send notifications using DBus)
- [`org.freedesktop.UPower.device`](https://upower.freedesktop.org/docs/Device.html)
specification in the UPower Manual (teaches what UPower properties are there and
what they mean)
<!-- }}} -->

<!-- {{{ Footnotes -->
[^1]: *If the value is set to "Battery", you will need to verify that the
property power-supply has the value "true" before considering it as a laptop
battery. Otherwise it will likely be the battery for a device of an unknown
type.* —
[`org.freedesktop.UPower.device`](https://upower.freedesktop.org/docs/Device.html)
specification in the UPower Manual
<!-- }}} -->
