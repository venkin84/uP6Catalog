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
- An identified user should be able to do all that an identified user does and should also be able to add or edit categories and items in the app
- An administrator will have access to do all that an identified user does but also has the access to delete a category or an item from the catalog
- Google Identity is the third party authencation service provider currently and other service providers can be added

### Note
- The url `http://localhost:5000/item/<itemID>/view` provides json endpoint for the application
- Currently an identified user can be made as an administrator by hardcoding in the DB (a method is provided in the dbutils to do the same)

### Dependencies
Dependencies to run this application are 
- Flask
- google_auth_oauthlib
- Requests
- PostreSQL
- Psycopg2
- Vagrant (for setting up the VM)

### How to Deploy
Perform the following steps from the `catalog` folder of the solution downloaded in the terminal
```bash
vagrant up
vagrant ssh
cd ../../vagrant/catalog
python catalog.py
```

### License
This project is a public project done as part of the learning and so feel free to use the way you want.
