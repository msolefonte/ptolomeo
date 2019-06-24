# Ptolomeo

Functional example of a serverless conversational bot.

## Introduction

Ptolomeo is a conversational bot that follows the proper patterns of the serverless architecture. To achieve this, cloud
computing tools provided by Amazon Web Services have been used, as well as the Dialogflow development environment. 
Dialogflow is a suite executed on Google Cloud that allows to facilitate the human-computer interaction offering a 
simple and effective development with which to interpret the natural language. The application’s back-end, a weather 
consultant, has been designed to be fully executed on the Amazon cloud. The code, mostly written in Python, but also in 
Javascript, is executed through Lambda functions and invoked thanks to the Gateway API. On the other hand, the 
front-end, developed using the Vue.js framework, is stored in S3 and allows authentication through Cognito. As a result 
of the work, it has been obtained an application that allows deepening on the creation of conversational bots, as well 
as exploiting the use of serverless architectures to obtain efficient results at low cost.

## Contributing

Feel free to add issues or to create pull requests. Help is always welcome.

## Versioning

[SemVer](http://semver.org/) is used for versioning. For the changelog, see [CHANGELOG.md](CHANGELOG.md). 

## Authors

* **Marc Solé Fonte** - *Initial work* - [msolefonte](https://github.com/msolefonte)

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* Thanks to [World Weather Online](https://www.worldweatheronline.com/developer/api/), as Ptolomeo AWS Serverless code 
uses their free api to work.
* Thanks to the authors of 
[Dialogflow Fulfillment Weather Sample Python (Flask)](https://github.com/dialogflow/fulfillment-weather-python) as some
code related to the World Weather Online API has been based on their project.
* Thanks to [Peter Joles](https://github.com/jolzee) for his indirect help and for keeping open source project 
[Leopard Chat UI](https://github.com/jolzee/chat-teneo-vue).
