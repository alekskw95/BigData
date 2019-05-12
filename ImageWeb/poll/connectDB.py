from couchdb import Server


main_connection = Server('http://userola:userola@localhost:5984/')
server = main_connection['images']