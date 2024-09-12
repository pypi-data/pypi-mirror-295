<!-- vim: set fenc=utf-8 ts=2 sw=0 sts=0 sr et si tw=0 fdm=marker fmr={{{,}}}: -->
# `weather4bar` — Weather for your status bar

<!-- {{{ What -->
## What
This is a Python script that shows weather info for the current location.

It's useful for putting into your window manager bar, or just for calling it
from your terminal.
<!-- }}} -->

<!-- {{{ Why -->
## Why
I wrote this because I simply could not find anything else that did the job 100%
right. The internet is full of shell scripts that `curl` the weather page of
AccuWeather, or a similar service, and manually parse out the HTML file to get
the needed values, most don't even autodetect your location and they make you
pass command-line arguments or set variables for your latitude and longitude,
or, even worse, manually edit the shell script to put those in.
<!-- }}} -->

<!-- {{{ How -->
## How
This Python script uses the [requests](https://github.com/psf/requests) library
to create HTTP requests, first, to [IP-API](https://ip-api.com/), to get IP
geolocation data, and then to [Open-Meteo](https://open-meteo.com/),to get the
weather information.

Then, it parses the data in a nice way, with icons and formatting, and it can be
used either as a script to get weather in your terminal, or be put inside of
Waybar as a custom module.

Right now, I only made formatting for a Waybar tooltip as it's the only bar I've
used yet.
<!-- }}} -->

<!-- {{{ Usage -->
## Usage
<!-- {{{ Help (click to expand) -->
<details>
  <summary><h3>Help (click to expand)</h3></summary>

  ```console
  $ weather4bar --help
  usage: weather4bar [-h] [-o {stdout,waybar}] [-t {celsius,fahrenheit}] [-w {kmh,ms,mph,kn}] [-p {mm,inch}] [-T {iso8601,unixtime}]

  options:
    -h, --help            show this help message and exit
    -o {stdout,waybar}, --output {stdout,waybar}
                          Output made for stdout or for parsing by Waybar
    -t {celsius,fahrenheit}, --temp-unit {celsius,fahrenheit}
                          Change the unit used for temperature
    -w {kmh,ms,mph,kn}, --wind-unit {kmh,ms,mph,kn}
                          Change the unit used for wind speed
    -p {mm,inch}, --precipitation-unit {mm,inch}
                          Change the unit used for precipitation
    -T {iso8601,unixtime}, --time-unit {iso8601,unixtime}
                          Change the unit used for time
  ```
</details>
<!-- }}} -->

To get weather in your terminal, simply use:
```console
$ weather4bar

17.6°C
Nowhere

Slight rain
Feels like 19.4°C
```

If you want to use this in Waybar, you need to create a custom module. You can
look at my dotfiles for an example:
- [Waybar `config` file](https://github.com/Andy3153/hyprland-rice/blob/master/dotconfig/waybar/config-3#L262-L267)
- [Waybar `style.css` file](https://github.com/Andy3153/hyprland-rice/blob/master/dotconfig/waybar/style-3.css#L262-L296)
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
This script is available in PyPi [here](https://pypi.org/project/weather4bar/).
To install it using `pip`, run:
```console
$ pip install weather4bar
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
- [Open-Meteo API documentation](https://open-meteo.com/en/docs)
- [IP-API API documentation](https://ip-api.com/docs/api:json)
<!-- }}} -->
