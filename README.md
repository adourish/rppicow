# Goal

Create a reference application that shows everything you need to configure a Raspberry Pi Pico W with an ePaper display using MicroPython.

-   I want to be able to place an ePaper device on my fridge which displays my todo and active tasks
-   I want to trigger events using Google Assistant
-   I want to create new tasks using Google Assistant
-   I want to make new tasks using a command line

# Outcome

A GitHub repository with an application written in MicroPython that uses all of the best practices for security, encryption, and coding standards and documents any of the blockers that I face

# Architecture

-   Google Assistant integration using IFTTT
-   Tasks application and API using Todoist
    -   See issues with MQTT and Google Tasks API
-   MicroPython Application
-   Raspberry Pi Pico W
-   2.9-inch e-paper SPI-compatible display
    -   Waveshare 2.9inch E-Ink Display Module (B07P6MJPTD)

## Logical Diagram

![Diagram Description automatically generated](media/12737869000ed826e2d3ed75d88b981b.png)

## Setup

![Graphical user interface Description automatically generated](media/045384149005245cf501e8d5d2d91a5e.jpeg)

![A picture containing indoor, office, cluttered Description automatically generated](media/1a57b104ab14c1a812b1d9c63ed355c5.png)

![Text Description automatically generated](media/ae2187e88646e823dc9583be75f8180a.png)

## Tools

-   Siglent SDS 1202X-E Oscilloscope
-   Longwei LW-K3010D Benchtop Digital Switching DC Power Supply

# Hardware

## Pico W to E-Paper mapping

-   The table below shows the pin mapping between the Pico W and the ePaper display
    -   https://www.waveshare.com/wiki/Pico-ePaper-2.9

| e-Paper | Pico | Description                                                       |
|---------|------|-------------------------------------------------------------------|
| VCC     | VSYS | Power input                                                       |
| GND     | GND  | GND                                                               |
| DIN     | GP11 | MOSI pin of SPI interface, data transmitted from Master to Slave. |
| CLK     | GP10 | SCK pin of SPI interface, clock input                             |
| CS      | GP9  | Chip select pin of SPI interface, Low active                      |
| DC      | GP8  | Data/Command control pin (High: Data; Low: Command)               |
| RST     | GP12 | Reset pin, low active                                             |
| BUSY    | GP13 | Busy pin                                                          |
| KEY0    | GP2  | User button 0                                                     |
| KEY1    | GP3  | User button 1                                                     |
| RUN     | RUN  | Reset                                                             |

## Pico W Pinouts

![Raspberry Pi Pico W: high-resolution pinout and specs – Renzo Mischianti](media/aa0d6606326a47e001ec776444b9aabc.png)

# Application

## Features (Completed)

-   Tasks service
    -   Integration with Todoist APIs
-   ePaper service
    -   Integration with ePaper display
-   Wifi Service
    -   Internal LED indicator
    -   Connect to Wifi
    -   Reconnect to Wifi
-   Settings service
-   Logging service
-   Interval timer

## Features (Active)

-   Date service
-   Logging service
-   Documentation

## Features (Todo)

-   Encryption for secrets and keys
-   Integration with Google Assistant using
-   Performance, error handling, and memory
    -   I need to handle transient errors and ensure that garbage collection gets called after each loop

## Settings

Create a config.py file with a settings object and a cipher key string to be imported by the main.py application

settings = {

'ssid': '{your ssid for wifi}',

'pw': '{your wifi password}',

'token': 'Bearer {your todoist token}',

'tasksUrl': 'https://api.todoist.com/rest/v2/tasks'

}

\# key size must be 16 or 32

\# key = uos.urandom(32)

cipherkey = b'I_am_32bytes=256bits_key_padding'

# Issues

## MQTT client library

-   I was able to get the MQTT library to work
-   The library I found had a lot of bugs and would only work 30-40% of the time
-   I abandoned using MQTT for the Pico W because it was consuming too much project time.
-   I would prefer to use MQTT for the pub/sub features of the application, but it did not seem practical given the issues with the client library

## Google Tasks API

-   There are a lot of challenges with using the Google Tasks APIs (or many Google APIs) to work in my MicroPython application
-   Most of the Google APIs are now using OAuth 2.0. There is no way to get a long-live Personal Access Token (similar to Microsoft Azure or AWS)
-   You may create a Service Account, but it will not have access to your tasks data
-   You must use the gcloud CLI to generate a short-lived token
-   You must apply to Google with a YouTube video of your project to create a short-lived token with the required Scopes for Google Tasks API
-   After some thought, the Google Tasks application is very basic compared to other options, and I have decided to move all of my tasks to Todoist
-   Todoist allows a Personal Access Token (PAT) and has many features I can use for this project, like filtering tasks, etc.

## MicroPython

-   MicroPython is impressive if you worked with Microcontrollers 10-20 years ago. You were forced to write your application using a low-level language like assembly or machine code
-   If you have worked with full features frameworks like .Net Core or Java then MicroPython can be a bit frustrating
-   I did abandon a few best practices to speed up the development of my application. One example is that you can create modules for your libraries and import them into the main application. You will see from the GitHub history that you started using import but abandoned it. If there are any errors in your code, the stack trace will mask the root error and give you a bogus error that sends on a wild goose change
