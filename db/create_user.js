db = db.getSiblingDB("db_name");

db.createUser(
    {
        user: "db_user",
        pwd: "db_password",
        roles: [
            {
                role: "readWrite",
                db: "db_name"
            }
        ]
    }
);