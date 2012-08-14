from database_class import database

class Person:
    
    db = None
    
    
    def __init__(self, db):
        self.db = db
    
    
    def getNewFriends(self, id):
        friends = self.db.fetchAll('SELECT `u`.`id`, `u`.`first_name`,\
                                     `u`.`last_name`, `u`.`avatar`\
                                     FROM `users_friends` `f` INNER JOIN `users` `u`\
                                     ON `u`.`id` = `f`.`users2_id`\
                                     WHERE `f`.`is_active` = 0 AND `u`.`id` != %s AND \
                                     `f`.`users2_id` = %s' % (id, id))
        return friends
       
    
    def getFriends(self, id, is_friend = 1):
        friends = self.db.fetchAll('SELECT `u`.`id`, `u`.`first_name`,\
                                     `u`.`last_name`, `u`.`avatar`\
                                     FROM `users_friends` `f` INNER JOIN `users` `u`\
                                     ON `u`.`id` = `f`.`users1_id` OR `u`.`id` = `f`.`users2_id`\
                                     WHERE `f`.`is_active` = %d AND `u`.`id` != %s AND \
                                     (`f`.`users1_id` = %s OR `f`.`users2_id` = %s)' % (is_friend, id, id, id))
        return friends
    
    
    def getPersonById(self, id):
        person = self.db.fetchOne('SELECT id, first_name, last_name,\
                                   avatar, birthday, job, email, phone\
                                   FROM users WHERE id = %s' % (id))
        return person


    def addFriend(self, id, user_id):
        self.db.action('INSERT INTO users_friends\
                        VALUES (NULL,%s, %s, 0)' % (user_id, id)) 
    

    def fetchProfile(self, id, user_id):  
        is_friend = False
        
        friends = self.getFriends(id)
        
        for f in friends:
            if user_id == int(f['id']):
                is_friend = True
                break
        
        some_friends = friends[0:4]
        
        count = int(self.db.fetchOne('SELECT FOUND_ROWS()')['FOUND_ROWS()'])
    
        return {'some_friends' : some_friends,
                'count' : count,
                'is_friend': is_friend}