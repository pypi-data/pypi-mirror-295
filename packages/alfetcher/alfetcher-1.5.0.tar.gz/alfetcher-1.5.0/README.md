# alfetcher

A simple library to help you fetch data from AniList

## Description

Welcome to my first python project!
This library is aimed at people who might be interested in automatizing their anime library.

## Getting Started

### Dependencies

* Python(tested on the latest ver.)
* An AniList account
* An AniList developer app

### Installing

* Clone this repo
```
git clone https://github.com/prochy-exe/alfetcher /path/to/desired/folder
```
* Install it using pip
```
pip install alfetcher
```
* Install it using pip locally
```
cd /path/to/desired/folder
pip install .
```
* If you want to make modifications to the library install it in the edit mode:
```
cd /path/to/desired/folder
pip install -e .
```

### Using the library

* To import the library into your code use:
```
import alfetcher
```
* When importing this library for the first time, you will be taken through the setup process

### Setting up the AniList developer app

* When the setup process starts, you will be automatically taken to required pages. This process is really simple.
* When asked for the Client ID, you will be taken to the account developer page.
* If not logged in, log in first.
* Then create a new client
* Choose whatever name you fancy, and for the redirect URL use http://localhost:8888/auth
* After you save the client, copy the ID and paste it into the terminal
* After entering the ID you will be taken to an auth page, where you need to allow the app to access your account.
* Afterwards you will be taken to a redirect page that will automatically send the token to the library.
* After that the library is successfully set-up and ready for use.

## Help

If you encounter any issues, feel free to open a new issue. If you have any new ideas or fixes, please open a pull request, they are more than welcome!

## Version History
* [1.5.0](https://github.com/prochy-exe/alfetcher/releases/tag/v1.5.0)
    * [guard against excessive updates](https://github.com/prochy-exe/alfetcher/commit/260bd7e9529582531820af3b9f0066e9b0b6c883)
    * [make sure the id is a str](https://github.com/prochy-exe/alfetcher/commit/1756332241e7937ac5b1482c3bb9a5f9a5c1c5b7)
    * [simply function and variable names](https://github.com/prochy-exe/alfetcher/commit/8d6560c28c8c2c02c7ad966acd662b8a126bf134)
* [1.4.0](https://github.com/prochy-exe/malfetcher/releases/tag/v1.4.0)
    * [add env to minimize output](https://github.com/prochy-exe/alfetcher/commit/4d0c90af39c6f6bd39c9199005ea1447ad303fc5)
* [1.3.0](https://github.com/prochy-exe/malfetcher/releases/tag/v1.3.0)
    * [don't cache empty searches](https://github.com/prochy-exe/alfetcher/commit/76c822ad2b1df430f27edf6245dde2c124b3b18e)
* [1.2.0](https://github.com/prochy-exe/alfetcher/releases/tag/v1.2.0)
    * [fix authenticated requests](https://github.com/prochy-exe/alfetcher/commit/bc9b7448145d2d0f4aa3c636fdd0d124e2f6390a)
* [1.1.0](https://github.com/prochy-exe/alfetcher/releases/tag/v1.1.0)
    * [fix typo](https://github.com/prochy-exe/alfetcher/commit/dbf3d14e90c4cfeebcef51503a884efd1e1178b5)
    * [allow some functions to not require user token](https://github.com/prochy-exe/alfetcher/commit/f3e58106709d5b1626b65384977fe22a05c7d647)
    * [use local ip address instead of localhost](https://github.com/prochy-exe/alfetcher/commit/9d6500229980faf68b20fe4a559a8d2bc08fed1b)
    * [print list name when no anime found](https://github.com/prochy-exe/alfetcher/commit/efca221b8f78ac0848aaa7d8813b6b5c36e89c28)
    * [drop user list caching](https://github.com/prochy-exe/alfetcher/commit/954fe02ef643e228561a2c3e845e18b431947652)
    * [add function to update progress in users list](https://github.com/prochy-exe/alfetcher/commit/c040d8836efb44352dd2f1339305cb9c5296f97d)
    * [add function to convert from al to mal id](https://github.com/prochy-exe/alfetcher/commit/278805356c25dcabb4029b01e337c40f83b135ac)
    * [dates: Make sure they are not None](https://github.com/prochy-exe/alfetcher/commit/92db92773cea64ec7e8c8f12bcf4bc624c2400b2)
    * [Formatting changes](https://github.com/prochy-exe/alfetcher/commit/b4a96be729ab23cff87fe00c2e0deab7d6b742f7)
* [1.0.0](https://github.com/prochy-exe/alfetcher/releases/tag/v1.0.0)
    * [Initial Release](https://github.com/prochy-exe/alfetcher/commit/4b67b1d8719d183012446a065c5b6c941ec6518e)

## Acknowledgments

Huge thanks to AniList team for their great page and database:
* [AniList](https://anilist.co/home)
* [AniList GraphQL](https://anilist.co/graphiql)
