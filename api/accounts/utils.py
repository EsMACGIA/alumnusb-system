from accounts.models import UserInformation, UserStats 

class ErrorMessages:
    UserNotFound = {"error" : "User does not exist"}
    UnauthAccesAccount = {"error" : "Unauthorized access to another user's account"}

def defaultUserInfo(email):
    """ 
    Returns a default UserInformation model filled with default data and the given email. 
    
    Parameters: 
    email (string): email needed inside the default object

    Returns: 
    UserInformation: UserInformation model filled with default data and the given email
  
    """

    return UserInformation(first_name='',middle_name='',
                    last_name='',mailing_city='',usb_alumn=0,
                    codigo_alumn_usb='',mailing_country='',
                    email=email,mobile='',cohorte=0,birthdate='2020-1-1',
                    age=1,undergrad_degree='',graduate_degree='',carnet=0,
                    usb_undergrad_campus='',graduate_campus='',work_email='',
                    workplace='',donor=1,social_networks='',twitter_account='',
                    instagram_account='')


def defaultUserStats(email):
    """ 
    Returns a default User_stat model filled with default data and the given email. 
    
    Parameters: 
    email (string): email needed inside the default object

    Returns: 
    User_stat: User_stat  model filled with default data and the given email
  
    """
    return UserStats(email=email,average_gift=0,
                    largest_gift=0,smallest_gift=0,total_gifts=0,
                    best_gift_year_total=0,best_gift_year=0, first_gift_date='2020-1-1', last_gift_date='2020-1-1', total_number_of_gifts=0)
