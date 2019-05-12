from couchdb import Server


main_connection = Server('http://user:user@localhost:5984/')
server = main_connection['images']