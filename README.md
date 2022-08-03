###  Joycontrol Bot Designer

![Joycontrol Bot Designer UI](/images/joycontrol_bot_designer_example_smaller.png)

Joycontrol Bot Designer is built upon the greatness [joycontrol](https://github.com/mart1nro/joycontrol), [joycontrol_rest_api](https://github.com/choss/joycontrol_rest_api) with inspiration from [RasCon](https://github.com/SkyoKen/RasCon_NS).

The project is guided the goal of making boting (automating) fun and easy so you'll be interested in learning to code or just improve your existing coding skills.

- Quality matters!!  If you happen to find a bug please [Report it](https://github.com/dentedghost/joycontrol_bot_designer/issues)
- Have a great idea or feature request?  Please [Share it](https://github.com/dentedghost/joycontrol_bot_designer/issues")

## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


## About The Project

Automation is a passion of mine.  I previously taught a Bot Programming course as part of a Quality Assurance degree at [Niacc.edu](https://www.niacc.edu/).  From that course I was inspired to write the book [Bot Programming: Intelligent Automation For Windows Applications And Games](https://www.amazon.com/Bot-Programming-Intelligent-Automation-Applications/dp/1453855963).

While playing some games on Nintendo switch,  I had the itch of "oh I wonder if I can automate this"?  Lucky for me other's have done all the heavy lifting.

The next question was how can I leverage this project to help others.  Just like when I taught Bot Programming,  some times the hardest part of education is to give someone a reason to learn that inspires them with a burning passion.  Being able to create Bots for some is exactly that nudge need to learn.

### Built With

* [Python 3.8.0](https://www.python.org/downloads/release/python-380/?ref=codebldr)
* [Flask 1.0.2](https://pypi.org/project/Flask/)
* [Raspbian GNU/Linux 10 (buster)](https://www.raspberrypi.org/blog/buster-the-new-version-of-raspbian/)


## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Install awesome projects that enabled Joycontrol Bot Designer:
* [joycontrol](https://github.com/mart1nro/joycontrol#installation)
* [joycontrol_rest_api](https://github.com/choss/joycontrol_rest_api#package-requirements)

Install libraries, In addition to the joycontrol and joycontrol_rest_api packages:

```sh
sudo pip3 install pycurl flask
```
If you have issues installing pycurl try installing this first

```sh
sudo apt install libcurl4-openssl-dev libssl-dev
```
```sudo pip3 install python3-xlib
sudo pip3 install pyautogui
```
### Installation
 
1. Clone the joycontrol_bot_designer
```sh
git clone https://github.com/dentedghost/joycontrol_bot_designer.git
```

## Steps to get up and running
1. Start joycontrol_rest_api
* cd joycontrol_rest_api
* sudo python3 rest.py

2. Start joycontrol_bot_designer webpage UI (Note Virtual Joy Controller works with Bot running)
* cd joycontrol_bot_designer
* sudo python3 web.py

3. Start joycontrol_bot_designer bot engine
* cd joycontrol_bot_designer
* sudo python3 bot.py

## Boting Basics

PRINT- Individually press a button (Capitalization is ignore)
a
X
A

PRINT - This is how you print/display something to the screen

PRINT - Wait a specific amount in milliseconds (1000 = 1 second)
1000

PRINT - Wait a random about of time between to values (Simulates real users)
waitrandom 1000 2000

PRINT - Do the same thing over and over a specific amount of times in a loop
FOR 5
waitrandom 500 750
Y
NEXT

PRINT - Nest loops.  Outer loop will run X amount of times and inner loop will loop Y each time X runs
PRINT - Outer 5 times and Inner 5*2=10 times
FOR 5
PRINT Outer
For 2
PRINT Inner
NEXT
NEXT


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/dentedghost/joycontrol_bot_designer/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Your Name - [@ghostcanoe](https://twitter.com/ghostcanoe)

Project Link: [https://github.com/github_username/repo](https://github.com/github_username/repo)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Nintendo Switch Reverse Engineering](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering)
* [joycontrol](https://github.com/mart1nro/joycontrol)
* [joycontrol_rest_api](https://github.com/choss/joycontrol_rest_api)
* [RasCon](https://github.com/SkyoKen/RasCon_NS)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [Markdown Editor](https://markdown-editor.github.io/)

