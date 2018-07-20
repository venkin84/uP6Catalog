# Items Catalog
Ver: 1.0.0.0 | Dated: 14-Jul-18

This is an Items Catalog application done as a part of training course @Udacity. The expectation was that an Items Catalog application be developed for the provided specification and demonstrates the skills learned during the course...
This web application can be used for managing a catalog of items grouped in categories based on various user roles (RBAC)...

### Features
Overall features in this application is as follows
- User of this application can have 3 roles
    - Unidentified user
    - Identified User
    - Administrator
- An unidentified user should be able to view the items and its information organised in categories
- An identified user should be able to do all that an unidentified user does and should also be able to add categories and items in the app, as well as be able to edit or delete the categories and items the user created
- An administrator will have access to do all that an identified user does and apart from that an admin has rights to edit or delete categories and items that belong to any user
- Google Identity is the third party authencation service provider currently

### Note
- The url `http://localhost:5000/item/<itemID>/view` provides json endpoint for the application
- Currently an identified user can be made as an administrator by hardcoding in the DB. A method is provided in the dbutils `setUserAdmin("user's email address")` to do the same or use the command shown below to directly update the DB.
```
update users set role = 2 where email_address = 'user's email address';
```

### Dependencies
Dependencies to run this application are 
- Flask
- google_auth_oauthlib
- Requests
- PostreSQL
- Psycopg2
- Vagrant (for setting up the VM)

### How to Deploy
Perform the following steps one after another in the terminal from the `catalog` folder of the solution downloaded
```bash
vagrant up
vagrant ssh
cd ../../vagrant/catalog
python catalog.py
```
This would have deployed the Catalog Application in the local VM. To launch the application navigate to the URL `http://localhost:5000` in the browser

### License
This project is a public project done as part of the learning and so feel free to use it the way you want. But all the licenses related to the third part APIs used will be applicable.
