from database_class import database

class Person:
    
    db = None
    
    
    def __init__(self, db):
        self.db = db
    
    def getFriends(self, id):
        
        friends = self.db.fetchAll('SELECT `u`.`id`, `u`.`first_name`,\
                                         `u`.`last_name`, `u`.`avatar`\
                                         FROM `users_friends` `f` INNER JOIN `users` `u`\
                                         ON `u`.`id` = `f`.`users1_id` or `u`.`id` = `f`.`users2_id`\
                                         WHERE `f`.`is_active` = 1 AND `u`.`id` != %s AND \
                                         (`f`.`users1_id` = %s or `f`.`users2_id` = %s)' % (id, id, id))
        return {'friends' : friends}
    
    
    def getPersonById(self, id):
        person = self.db.fetchOne('SELECT first_name, last_name, avatar, birthday, job, email, phone\
                                   FROM users WHERE id = %s' % (id))
        return person


    def fetchProfile(self, id):  
          
        some_friends = self.db.fetchMany('SELECT `u`.`id`, `u`.`first_name`,\
                                         `u`.`last_name`, `u`.`avatar`\
                                         FROM `users_friends` `f` INNER JOIN `users` `u`\
                                         ON `u`.`id` = `f`.`users1_id` or `u`.`id` = `f`.`users2_id`\
                                         WHERE `f`.`is_active` = 1 AND `u`.`id` != %s AND \
                                         (`f`.`users1_id` = %s or `f`.`users2_id` = %s) ORDER BY RAND()' 
                                         % (id, id, id), 3)
    
        count = int(self.db.fetchOne('SELECT FOUND_ROWS()')['FOUND_ROWS()'])
    
        return {'some_friends' : some_friends,'count' : count }