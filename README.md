# Amiibo RESTful API

[![Heroku App Status](http://heroku-shields.herokuapp.com/amiiboapi)](http://amiiboapi.com)
![Hits](https://hitcounter.pythonanywhere.com/count/tag.svg?url=https%3A%2F%2Fgithub.com%2FN3evin%2FAmiiboAPI)
[![discod](https://img.shields.io/badge/Join-Discord-orange.svg?colorB=7289DA&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAPUAAADwCAMAAADvotLkAAAAM1BMVEUAAAD%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2B3leKCAAAAEHRSTlMAQIAQv%2B%2Bfz2Aw3yBwUK%2BPD%2FW3OwAABYNJREFUeAHt3deWqzAPhuHPljtN93%2Bzf8kasktWHLPHgBj0nk956NVA0zRN0zRN0zRN0zRN07Q%2BkTFWSKMxOKIpFJZVXDJ2jcbCEosJ%2BzUVllo02CeaWXIL9ihHlp2jHdCepRe7s4cVfSc2Rb5CM7q28DUa0THDF8kP6FfkqxTQrYmv04BeOb5OCzo18IUq6NTIVyqjTzNfKYs%2BFb5SM%2FrElyqiS5mvFbpkVK1qVata1apWtapVrWpVq1rVqlY1VK1qVata1apWtapVrWpVR2et9VytWLu4%2BEPUJaQMAMhz0%2B32PIZycXUcBzyagucP%2BTABqzxeVl1Wcl48N%2BVDxlfDUq6odgaPKMUXnPstz38UE%2BGr5K6mDsM6y35TOWetMXjJGLv80vsw4CvjrqR2%2BcscVomz04B6w2RXZDB1t0R1MX%2Ba5zGjNbPEP6YbkPwl1JYAABTWDfPGhnH%2BfR0BLfLVMePR6OvkajRGZm9p%2FQ%2BKcPVCz5dEXCL8ezn456oCmkWrHR7ZdUP8nSiVdSICRbLaAMAQiyX0KLmS8SgJVjsAMDGhW8YlPCpy1QZATuhaMgCAJFYdsWNFqjphx6xQdcGekZeptti1IFNN2LUsUh2wc06i2mDnkkB1we55eeoRuxfkqQfsXhannnFARZo64YBGaWrCAQ3C1DMOKcpSJxzSKEtNOKRBlHrGQUVJ6oSDWiSpBxxUFqSOOCwvR21xWEGO2uCwkhi1x4eGZK01hGrGWpsGfIjEqGdUM8%2Fb0u9NZH3jYHxRinpEJQr8zL8jGd88OtsiRZ3bxwhLDStrrLInKeqmbW6FnbfsCEmI2m2ZM57wUtm0Jywy1HbTvxgadkae8L4gQz1tWgl9y8wb8b5RhprwttAwkfLGlcaIUPuNO1fbcrSFSiLUDu9rOaaxW0%2FiogS13ah2LWqD980S1GkPdcb7rAS12Xg2vLQgUMlIUG8dBi81%2FP6CSlmAuqDS2LKh8ltHmhSgdhsPml3LTj2jVjlfHTaeF5qGi9wO1dz5aotaVBomkt04WvByvjptGm09UsOB64R69ny1wQa2I%2BAT239CI8lXg54kbxs%2BL%2BEGfMqcr8bnhtE57%2BZEqJSC89HZDFxfvUt0SzVOV7tbq1VtB%2FRrMnipSFTnMqJTg5vxmpOoRuIyoUNkOdJl1EjMznzf7Fe0ePXKbnZXzCtakLp%2Bm2LyzFwSfeOFxbeH7YM%2FW81z9XtePhhsjlKsnsRGPl3Ny4cTwrJkbGkdeKKY%2Bg2Vc9Wc8KbseIUbNEUrmb0l2Xf3ODWcQPp5%2FCQ31vFaGPCmkYWoK2xMjn%2FlltEQXiMzhsjP%2FDJc4ckrDnjt7cgn0c32fyWT7P8KLvIfzal6hUKQmh3hfVQ6fTsvRxalrl7tCp2%2BwzN6eW%2BxzUOfbz5NlT2CJPWapR4jj%2FgMvDYEse%2Faezt0%2BBJnpIpZlnptnr7%2FJU6HP6Lk5I%2BN40MiPAvf%2FHjekObLjHlVgjW5enOm4bAnGzuXC45lVxz%2FY67oGJWqVrWqVa1qVata1apWdbdUrWpVq1rVqla1qlWtalWrWtWqzrdUg0%2FOxzPUhU%2FOxBPUM5%2FcSPF4deKTc0A4XE18drSFjZ%2ByiE8AwtFqwycXAGA8WA3H51b2Hyte4oFK3sBGtyyf24hHkz9UjXj6vutR9oeq6WQ2tbPRsVz4zKb2%2FwP4MXM7tP8f6BotfF4FzWx0zhQ%2BrdzMRvdS5JMam995wQ5l6%2FiMYvObJNipwZwQWtn4wdlbqpFuqUa6pRrJ31GN7O%2BoRo53VIPiHdWgcEc1EG6pxnhLNdIt1cj%2Bjmrkckc1KN5RDZrvqAbCLdUYb6lGuqUa2d9RjVzuqAbFO6pBM%2BOOLdA0TdM0TdM0TdM0TdO0b%2FZfegfWFMciUSwAAAAASUVORK5CYII%3D)](https://discord.gg/myxnvvc)


A RESTful API that was created for retriving amiibo information.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Features
- always updated
- JSON format
- could be used with any platform

### Usage
Full amiibo: [https://www.amiiboapi.com/api/amiibo](https://www.amiiboapi.com/api/amiibo) 

Specific Amiibo (Mario): [https://www.amiiboapi.com/api/amiibo?name=mario](https://www.amiiboapi.com/api/amiibo?name=mario)

When searching for amiibo, you can use the key or amiibo name. Key must be in hexdecimal example `0x1D0`

More APIs can be found here: [https://www.amiiboapi.com](https://www.amiiboapi.com) 

### Requirements (if you want to host)
- Python 2.X or 3.X
- [Flask](http://flask.pocoo.org/)
- [Flask-Cors](https://flask-cors.readthedocs.io/en/latest/)

### Manually Setup (if you want to host)
1. Run `app.py` to start the webservice.
2. Put in the information required in the spreadsheet boxes.

### Heroku Setup (if you want to host)
Click on the `Deploy to Heroku` button and you are good to go!

### Credit
- [JSON script source](https://script.google.com/d/143u0RLuppsmYJ0B3wzo6i0jZYSfIFV2NLJMHPM-Sqczpr9bLwdffc-Wx/edit?usp=sharing)
- [Amiibo Database](https://docs.google.com/spreadsheets/d/19E7pMhKN6x583uB6bWVBeaTMyBPtEAC-Bk59Y6cfgxA)
- [Amiibo images](http://amiibo.life)