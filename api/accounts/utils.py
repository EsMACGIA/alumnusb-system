from accounts.models import User_information, User_stats 

class ErrorMessages:
    UserNotFound = {"error" : "User does not exist"}
    UnauthAccesAccount = {"error" : "Unauthorized access to another user's account"}

def defaultUserInfo(email):
    """ 
    Returns a default User_information model filled with default data and the given email. 
    
    Parameters: 
    email (string): email needed inside the default object

    Returns: 
    User_information: User_information model filled with default data and the given email
  
    """

    return User_information(First_name='',Middle_name='',
                    Last_name='',Mailing_city='',USB_alumn=0,
                    Codigo_Alumn_USB='',Mailing_country='',
                    Email=email,Mobile='',Cohorte=0,Birthdate='2020-1-1',
                    Age=1,Undergrad_degree='',Graduate_degree='',Carnet=0,
                    USB_undergrad_campus='',Graduate_campus='',Work_email='',
                    Workplace='',Donor=1,Social_networks='',Twitter_account='',
                    Instagram_account='')


def defaultUserStats(email):
    """ 
    Returns a default User_stat model filled with default data and the given email. 
    
    Parameters: 
    email (string): email needed inside the default object

    Returns: 
    User_stat: User_stat  model filled with default data and the given email
  
    """
    return User_stats(Email=email,Average_gift=0,
                    Largest_gift=0,Smallest_gift=0,Total_gifts=0,
                    Best_gift_year_total=0,Best_gift_year=0, First_gift_date='2020-1-1', Last_gift_date='2020-1-1', Total_number_of_gifts=0)
