import datetime
import calendar
import mysql.connector
from mysql.connector import Error
def db():
    connection=None
    try:
        connection=mysql.connector.connect(host='localhost',user='root',passwd='Password',
                                           database='railway_ticket_management',auth_plugin='mysql_native_password')
        print('Sucessfull')
    except Error as e:
        print(e)
        return
    return connection
db_connection=db()
def get_dates(db,query):
    cursor=db.cursor()
    try:
        cursor.execute(query)
        result=cursor.fetchall()
        for i in result:
            print(i[0])
        #print(result)
    except Error as e:
        print(e)
def get_trains(db,query):
    print('Trains Available')
    cursor = db.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for i in result:
            print(i[0],i[1].replace(' ','_'))
        return [int(i[0]) for i in result]
    except Error as e:
        print(e)
def get_avaiable_dates(db,query):
    cursor = db.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for i in result:
            print(i[0],i[1],i[2])
        return [i[2] for i in result]
    except Error as e:
        print(e)
def check_seats_availability(db,query):
    cursor = db.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for i in result:
            #print(i[0], i[1], i[2])
            print('Seats Available for train {0} on {1}: {2} '.format(i[0],i[1],i[2]))
            # Verify i[2] as available category seats
            if i[2]==0:
                return None
            else:
                return i[2]
    except Error as e:
        print(e)
def update_booked_tickets(db,trainNumber,trainDate,category):
    query='update train_status set {0}_seats_Available={0}_seats_Available-1 where trainNumber="{1}" and train_date="{2}"'.format(category,trainNumber,trainDate)
    query2='update train_status set {0}_seats_booked={0}_seats_booked+1 where trainNumber="{1}" and train_date="{2}"'.format(category,trainNumber,trainDate)
    cursor = db.cursor()
    try:
        cursor.execute(query)
        cursor.execute(query2)
        db.commit()
    except Error as e:
        print(e)
def confirmTicket(db,query):
    cursor = db.cursor()
    try:
        cursor.execute(query)
        print('Ticket confirmed')
        db.commit()
    except Error as e:
        print(e)
def put_into_waitingList(db,query):
    cursor=db.cursor()
    try:
        cursor.execute(query)
        db.commit()
    except Error as e:
        print(e)
def get_waiting_list_number(db,query):
    cursor = db.cursor()
    try:
        cursor.execute(query)
        waiting_list_number=cursor.fetchall()
        print(waiting_list_number)
        print(waiting_list_number[0][0])
        # verify print statement
        try:
            if waiting_list_number[0][0]>=2:
                # Understand this condition
                return False
            elif waiting_list_number==[]:
                print('Ticket in Waiting list')
                return True
            else:
                return True
        except Exception as f:
            return True
    except Error as e:
        print(e)
def book_tickets(categoryy):
    check_seat_availability_query = 'select ts.trainNumber,ts.train_date,ts.{0}_seats_AVAILABLE from train_status ts where ts.train_date="{1}" and ts.trainNumber={2}'.format(
        categoryy,booking_date, train_number)
    SEATS_AVAILABLE = check_seats_availability(db_connection, check_seat_availability_query)
    name = input('Name: ')
    Age = int(input('Age: '))
    Gender = input('Gender: ')
    Address = input('Address: ')
    if SEATS_AVAILABLE:
        No_of_tickets = 1
        ticket_status = 'Confirmed'
        booking_details_query = 'insert into passenger(trainNumber,Booking_Date,passenger_name,age,sex,address,ticket_status,category) values({0},"{1}","{2}",{3},"{4}","{5}","{6}","{7}")'.format(
            train_number, booking_date, name, Age, Gender, Address, ticket_status, categoryy)
        confirmTicket(db_connection, booking_details_query)
        update_booked_tickets(db_connection, train_number, booking_date, categoryy)

        cursor = db_connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID()")
        print(cursor.fetchone()[0])
        ticket_details = '{0} {1} {2} {3} {4} {5} {6}'.format(name, Age, Address, ticket_status, categoryy,
                                                              train_number, booking_date)
        print(ticket_details)
    else:
        get_waiting_list_number_query = 'select count(ticket_id) from passenger where trainNumber="{0}" and booking_date="{1}" and category="{2}" and ticket_status="waiting list" group by ticket_status;'.format(
            train_number, booking_date, categoryy)
        if get_waiting_list_number(db_connection, get_waiting_list_number_query):
            ticket_status = 'waiting List'
            query = 'insert into passenger(trainNumber,Booking_Date,passenger_name,age,sex,address,ticket_status,category) values({0},"{1}","{2}",{3},"{4}","{5}","{6}","{7}")'.format(
                train_number, booking_date, name, Age, Gender, Address, ticket_status, categoryy)
            put_into_waitingList(db_connection, query)
        else:
            print('Waiting List is full. So, ticket cannot be booked.')
def update_canceld_tickets(db,trainNumber,train_date,category):
    cursor=db.cursor()
    query1='update train_status set {0}_seats_booked={0}_seats_booked-1 where trainNumber="{1}" and train_date="{2}"'.format(category,trainNumber,train_date)
    query2='update train_status set {0}_seats_available={0}_seats_available+1 where trainNumber="{1}" and train_date="{2}"'.format(category,trainNumber,train_date)
    try:
        cursor.execute(query1)
        cursor.execute(query2)
        db.commit()
        return
    except Error as e:
        print(e)
def check_for_wintingList_candidates(db,query):
    cursor=db.cursor()
    try:
        cursor.execute(query)
        result=cursor.fetchall()
        print(result[0][0],'Count type',type(result[0][0]))
        if result[0][0]:
            return True
        else:
            return False
    except Error as E:
        print(E)
def change_from_waiting_status_to_confirm(db,query):
    cursor=db.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return
    except Error as E:
        pass


def canceling_of_waiting_ticket(db,query):
    cursor=db.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0][7]
    except Error as E:
        pass



def cancel_tickets(db,ticket_id):
    cancel_ticket_query='delete from passenger where ticket_id={0};'.format(ticket_id)
    cursor=db.cursor()
    try:
        cancel_waiting_ticket_query = 'select * from passenger where ticket_id={0};'.format(ticket_id)
        cancel_waiting = canceling_of_waiting_ticket(db_connection,cancel_waiting_ticket_query)
        print(cancel_waiting,'---')
        if cancel_waiting == 'waiting List':
            cursor.execute(cancel_ticket_query)
            print('Ticket Cancalled Successfully')
            db.commit()
        else:

            train_and_category_query='select * from passenger where ticket_id={0};'.format(ticket_id)

            # When we are canceling waiting list ticket then Status table should not get updated ( booked -1 and available +1 )


            cursor.execute(train_and_category_query)
            result=cursor.fetchall()

            check_for_wintingList_candidates_query='select count(ticket_id) from passenger where ticket_status="waiting List" and trainNumber="{0}" and booking_date="{1}" and category="{2}"'.format(result[0][1],result[0][2],result[0][8])
            if check_for_wintingList_candidates(db,check_for_wintingList_candidates_query):
                change_from_waiting_status_to_confirm_query='update passenger p set p.ticket_status="Confirmed" where p.ticket_id=(select p.ticket_id where p.ticket_status="waiting List" and p.trainNumber="{0}" and p.booking_date="{1}" and p.category="{2}" limit 1)'.format(result[0][1],result[0][2],result[0][8])
                change_from_waiting_status_to_confirm(db,change_from_waiting_status_to_confirm_query)
            else:
                update_canceld_tickets(db, result[0][1], result[0][2], result[0][8])
                cursor.execute(cancel_ticket_query)

            db.commit()
            print('Ticket Cancelled Succesfully.')
    except Error as e:
        print(e)
Decision=int(input('1: Book a ticket\n2: Cancel Ticket\nChoice: '))
if Decision==1:
    get_trains_query='select tl.trainNumber,tl.trainName from trainList tl;'
    trainList = get_trains(db_connection, get_trains_query)
    train_number=int(input('Train Number: '))
    while train_number not in trainList:
        print("enter valid number")
        train_number = int(input('Train Number: '))
    get_train_dates_query=r'select * from available_days where trainNumber={0}'.format(train_number)
    date_lists= get_avaiable_dates(db_connection,get_train_dates_query)
    ##BOOKING AND CATEGORIY
    booking_date=input('Please enter the booking date in the format shown above: ')
    while booking_date not in date_lists:
        print("enter valid date")
        booking_date = input('Please enter correct booking date:')

    category=input('AC or GEN: ')
    while category.upper() not in ('AC','GEN'):    #Change 1
        print('Please enter valid category')
        category = input('AC or GEN: ')
    if category.upper()=='AC':
        category='AC'
        book_tickets(category)
    elif category.upper()=='GEN':
        category = 'GEN'
        book_tickets(category)
elif Decision==2:
    ticket_id=input('Enter Ticket Id: ')
    cancel_tickets(db_connection,ticket_id)