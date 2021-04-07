db = db.getSiblingDB('airbnb')

db.createUser(
    {
        user: "airbnb-user",
        pwd: "pass",
        roles: [
            {
                role: "readWrite",
                db: "airbnb"
            }
        ]
    }
);