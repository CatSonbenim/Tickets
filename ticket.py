"""Program by @CatSonbenim (Lisa Bulala) 24.10.2018"""

from datetime import datetime as dt


class Event:

    def get_price(self):
        return self.price

    def get_discount_info(self):
        return self.d_info

    def get_event_name(self):
        return self.name_of_event

    def get_date(self):
        return self.date

    def s_tickets(self):
        return self.sold_tickets

    def a_tickets(self):
        return self.all_tickets

    def __str__(self):
        return '\nEvent: ' + self.get_event_name() + '\nDate of event: ' + str(self.get_date().day) + '.' \
               + str(self.get_date().month) + '.' + str(self.get_date().year)


class Event1(Event):

    sold_tickets = 0

    def __new__(cls, *args, **kwargs):
        if cls.sold_tickets + 1 > cls.all_tickets:
            raise MemoryError('All tickets were sold!')
        else:
            cls.sold_tickets += 1
            return super(Event1, cls).__new__(cls)

    price = 10
    name_of_event = 'EpamCourse'
    date = dt(2018, 10, 30)
    d_info = ''
    all_tickets = 25


class Event2(Event):

    sold_tickets = 0

    def __new__(cls, *args, **kwargs):
        if cls.sold_tickets + 1 > cls.all_tickets:
            raise MemoryError('All tickets were sold!')
        else:
            cls.sold_tickets += 1
            return super(Event2, cls).__new__(cls)

    price = 15
    name_of_event = 'ExcadelCourse'
    date = dt(2018, 12, 15)
    d_info = ''
    all_tickets = 0


class Event3(Event):

    sold_tickets = 0

    def __new__(cls, *args, **kwargs):
        if cls.sold_tickets + 1 > cls.all_tickets:
            raise MemoryError('All tickets were sold!')
        else:
            cls.sold_tickets += 1
            return super(Event3, cls).__new__(cls)

    price = 25
    name_of_event = 'CiklumCourse'
    date = dt(2019, 2, 24)
    d_info = ''
    all_tickets = 50


class Decorator(Event):

    def __init__(self, event):
        self.event = event

    def get_price(self):
        return self.event.get_price() + self.event.get_price() * Event.get_price(self)

    def get_discount_info(self):
        return self.event.get_discount_info() + Event.get_discount_info(self)

    def get_event_name(self):
        return self.event.get_event_name()

    def get_date(self):
        return self.event.get_date()

    def a_tickets(self):
        return self.event.a_tickets()

    def s_tickets(self):
        return self.event.s_tickets()


class StudentTicket(Decorator):

    price = -0.5

    d_info = ' Student Ticket.'

    def __init__(self, event):
        Decorator.__init__(self, event)


class AdvanceTicket(Decorator):

    price = -0.4
    d_info = 'Advance Ticket (ticket bought more then 60 days before event).'

    def __init__(self, event):
        Decorator.__init__(self, event)


class LateTicket(Decorator):

    price = 0.1
    d_info = 'Late Ticket (ticket bought less then 10 days before event).'

    def __init__(self, event):
        Decorator.__init__(self, event)


class Ticket:

    numbers = [i for i in range(1000, 9999)]
    ind = 0

    def __init__(self, *, name, surname, event):
        self.visitor = name + ' ' + surname
        self.event = event
        self.st = Ticket.numbers[Ticket.ind]
        Ticket.ind += 1

    def __str__(self):
        return 'Ticket #' + str(self.st) + str(self.event) + '\nVisitor: ' + self.visitor + '\nTicket price: '\
               + str(self.event.get_price()) + '$' + '\nDiscount info: ' + self.event.get_discount_info()


def creating_ticket(event):
    if (event.get_date() - dt.today()).days >= 60:
        event = AdvanceTicket(event)
    elif (event.get_date() - dt.today()).days <= 10:
        event = LateTicket(event)

    student = input('If you are a student press enter. Else enter eny key.')
    if student == '':
        while True:
            try:
                st_tick = input('Enter your student ticket series: ')
                if not st_tick[:2:].isalpha() and st_tick[2::].isdigit():
                    raise SyntaxError
                if not len(st_tick) != 9:
                    raise Warning
                break
            except SyntaxError:
                print('Student ticket series must look like AA000000.')
            except Warning:
                print('Len of student ticket series has to be 8.')
        event = StudentTicket(event)
        event.d_info = event.d_info + '\nStudent ticket series: ' + st_tick

    return event


def new_ticket(event):

    while True:
        try:
            name_of_visitor = input('Enter name of visitor of event: ').title()
            if not name_of_visitor.isalpha():
                raise Warning
            break
        except (ValueError, Warning):
            print('Incorrect input. Retry Entering!')

    while True:
        try:
            surname_of_visitor = input('Enter surname of visitor of event: ').title()
            if not surname_of_visitor.isalpha():
                raise Warning
            break
        except (ValueError, Warning):
            print('Incorrect input. Retry Entering!')

    return Ticket(name=name_of_visitor, surname=surname_of_visitor, event=creating_ticket(event))


def choosing_event(all_events):
    print('All events')
    for i in range(len(all_events)):
        all_events[i].sold_tickets -= 1
        print('Event #', i+1, '\nInfo:', all_events[i](), '\n')

    while True:
        try:
            choose = int(input('Enter number of event: '))-1
            if choose not in range(len(all_events)):
                raise Warning
            break
        except Warning:
            print('Your input is out of range. Retry entering.')
        except ValueError:
            print('Incorrect input. Retry entering!')

    return all_events[choose]()


def searching(tickets):

    while True:
        try:
            searched = int(input('\nEnter a number of searched ticket'))
            if searched not in range(1000, 9999):
                raise Warning
            break
        except (ValueError, Warning):
            print('Incorrect input. Retry entering.')

    for i in tickets:
        if i.st == searched:
            return i
    return None


def main():

    all_eve = [Event1, Event2, Event3]
    all_tickets = []
    esc = False

    while True:
        while True:
            try:
                ticket = new_ticket(choosing_event(all_eve))
                break
            except MemoryError:
                print('All tickets for chosen event were sold')
                while True:
                    try:
                        inp = input('\nDo you want to buy ticket for another event? Enter yes or no: ').lower()
                        if inp != 'yes' and inp != 'no':
                            raise Warning
                        break
                    except (ValueError, Warning):
                        print('Incorrect input. Retry Entering!')
                if inp == 'yes':
                    pass
                elif inp == 'no':
                    esc = True
                    break

        if esc:
            break

        while True:
            try:
                inp = input('\nDo you want to print your ticket? Enter yes or no: ').lower()
                if inp == 'yes':
                    print(ticket)
                    break
                elif inp == 'no':
                    break
                else:
                    raise Warning
            except (ValueError, Warning):
                print('Incorrect input. Retry Entering!')

        while True:
            try:
                inp = input('\nDo you want to buy one more ticket? Enter yes or no: ').lower()
                if inp != 'yes' and inp != 'no':
                    raise Warning
                break
            except (ValueError, Warning):
                print('Incorrect input. Retry Entering!')

        all_tickets.append(ticket)
        if inp == 'yes':
            pass
        elif inp == 'no':
            break

    while True:
        try:
            inp = input('\nDo you want to search ticket by number? Enter yes or no: ').lower()
            if inp == 'yes':
                fouded = searching(all_tickets)
                if fouded is None:
                    print('There is no such ticket!')
                else:
                    print(fouded)
                break
            elif inp == 'no':
                break
            else:
                raise Warning
        except (ValueError, Warning):
            print('Incorrect input. Retry Entering!')


if __name__ == '__main__':
    main()
