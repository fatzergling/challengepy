# Penn Labs Server Challenge

General Description:
This project is a program that scrapes data from the Online Clubs with Penn and stores them with the JSON file. Additionally, it contains an API that can add new clubs and favorite clubs by specific users. The API requires users to login in order to access: otherwise, access is denied. New users can register if interested. Finally, the program stores the information of all users and clubs in JSON files, although one must manually save the clubs if they have modified it before closing the server.

The project is composed of 4 python files: User, Club, Scrapper, and Index
The User file contains the User class, which has 5 variables:
String username, String password, string list favorites(stores favorites), string list clubs(stores clubs that the person is in) and authentication (used for login purposes. The password is stored as a hash for maximum security.
The Club file contains the Club class, which has 4 variables: string club name, string list tags (contains tags), string description, string list favorites (stores users that favorited it)
The scrapper scrapes the data from the Online Clubs with Penn website and stores it in a JSON format based off the Club class.
Keep in mind that except for the /api/clubs post (which takes a JSON file), all other posts use request.form to activate. 
Routes (for the server):
- /: Welcome message for Penn Club Review
- /api: Welcome message for Penn Club Review’s API
- /api/clubs: The ‘GET’ method returns the list of clubs. The ‘POST’ method takes a JSON file similar to the existing clubs and appends the club into the list of clubs.
- /api/user/:username: Obtain the information of a user, including favorited clubs and clubs joined. 
- /api/favorite: Allows a user to favorite a specific club. It returns the amount of times the club has been favorited. 
- /api/unfavorite: Allows a user to unfavorite a specific club.  It returns the amount of times the club has been favorited after the removal
- /api/save: Allows a user to save the club information in case the server shuts down
- /api/load: Allows a user to load the club information
- /login: Login into your user with a password. 
- /logout: Logout of the system.
- /register: Register a new user into the system.
For trial user jen, she is part of Arun Fan Club and her password is password.
I added an unfavorite system as well as a secure login system to the API.
