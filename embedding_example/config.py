from configparser import ConfigParser

def connection_credentials(filename = r"database.ini file" , section = "postgresql") :
    parser = ConfigParser()     #Create a parser
    parser.read(filename)       #Read config file

    db = {}

    if parser.has_section(section) :
        params = parser.items(section)

        for param in params :
            db[param[0]] = param[1]

    else :
        raise Exception("Section {0} is not found in the {1} file".format(section , filename))

    # print(db)
    return db
