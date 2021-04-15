
CREATE TABLE Student(
    student_id varchar(8),
    password varchar(1024),
    email varchar(1024),
    first_name varchar(64),
    last_name varchar(64),
    branch varchar(64),
    primary key (student_id)
    
);


'''
CREATE TABLE Club(
    name varchar(128),
    admin varchar(128), 
    description varchar(1024), 
    image_url varchar(2000),
    primary key (name),
    foreign key (admin) references Student (student_id)
    
);
'''
'''
CREATE TABLE followers(
    student_id varchar(128),
    club_id int,
    foreign key (student_id) references Student (student_id),
    foreign key (club_id) references Club (name)
    
);
'''
'''
CREATE TABLE members(
    student_id varchar(128),
    club_id int,
    foreign key (student_id) references Student (student_id),
    foreign key (club_id) references Club (name)
);
'''


'''
CREATE TABLE member_request(
    student varchar(128),
    club int, 
    date_time datetime, 
    foreign key (club) references Club (name),
    foreign key (student) references Student (student_id)
    
);
'''





'''
CREATE TABLE Event(
    event_id int,
    title varchar(128),
    description varchar(2048), 
    details varchar(2048),
    date_time datetime,
    organiser int,
    open_to_all bool,
    image_url varchar(2000),
    primary key(event_id),
    foreign key (organiser) references Club (name)
    
);
'''
'''
CREATE TABLE interested(
    student_id varchar(128),
    event_id int,
    foreign key (student_id) references Student (student_id),
    foreign key (event_id) references Event (event_id)
    
);
'''
'''
CREATE TABLE participants(
    student_id varchar(128),
    event_id int,
    foreign key (student_id) references Student (student_id),
    foreign key (event_id) references Event (event_id)
    
);
'''
'''
CREATE TABLE participation_request(
    student_id varchar(128),
    event_id int,
    date_time date,
    foreign key (student_id) references Student (student_id),
    foreign key (event_id) references Event (event_id)
    
    
);
'''

'''
CREATE TABLE Comment(
    comment_id int,
    comment_txt varchar(2048),
    student_id varchar(128),
    event_id int,
    date_time date,
    primary key(comment_id),
    foreign key (student_id) references Student (student_id),
    foreign key (event_id) references Event (event_id)
    
);
'''
