from accounts.models import UserInformation, UserStats 
from enum import Enum

# THIS SECTION IS USEFUL TO SAVE ERROR MSGS 
class ErrorMessages:
    UserNotFound = {"error" : "User does not exist"}
    UnauthAccesAccount = {"error" : "Unauthorized access to another user's account"}

# THIS SECTION IS USEFUL TO ADMINISTRATE TYPES OF ACHIEVEMENTS
class AchievementsData:
    def __init__(self, type, goal):
        self.type = type # String that represents what kind of achievement is
        self.goal = goal # Number that represents the goal the achievement is trying to reach

class AchievementsType(Enum):
    UNKNOWN = 0
    TOTAL_NUMBER_OF_DONATIONS = 1
    TOTAL_SUM_DONATIONS = 2
    LARGEST_DONATION = 3
    

AchievementsDic = {
    "Donante" : AchievementsData(AchievementsType.TOTAL_NUMBER_OF_DONATIONS, 1),
    "Numero donaciones bronce" : AchievementsData(AchievementsType.TOTAL_NUMBER_OF_DONATIONS, 5),
    "Numero donaciones plata" : AchievementsData(AchievementsType.TOTAL_NUMBER_OF_DONATIONS, 10),
    "Numero donaciones oro" : AchievementsData(AchievementsType.TOTAL_NUMBER_OF_DONATIONS, 20),
    "Numero donaciones platino" : AchievementsData(AchievementsType.TOTAL_NUMBER_OF_DONATIONS, 50),
    "Numero donaciones diamante" : AchievementsData(AchievementsType.TOTAL_NUMBER_OF_DONATIONS, 100),
    "Total donaciones bronce" : AchievementsData(AchievementsType.TOTAL_SUM_DONATIONS, 100),
    "Total donaciones plata" : AchievementsData(AchievementsType.TOTAL_SUM_DONATIONS, 500),
    "Total donaciones oro" : AchievementsData(AchievementsType.TOTAL_SUM_DONATIONS, 1500),
    "Total donaciones platino" : AchievementsData(AchievementsType.TOTAL_SUM_DONATIONS, 3000),
    "Total donaciones diamante" : AchievementsData(AchievementsType.TOTAL_SUM_DONATIONS, 5000),
    "Donacion estrella bronce" : AchievementsData(AchievementsType.LARGEST_DONATION, 5),
    "Donacion estrella plata" : AchievementsData(AchievementsType.LARGEST_DONATION, 20),
    "Donacion estrella oro" : AchievementsData(AchievementsType.LARGEST_DONATION, 50),
    "Donacion estrella platino" : AchievementsData(AchievementsType.LARGEST_DONATION, 100),
    "Donacion estrella diamante" : AchievementsData(AchievementsType.LARGEST_DONATION, 500),
    "Donante recurrente": AchievementsData(AchievementsType.UNKNOWN, -1)
}

# THIS SECTION IS USEFUL TO CREATE DEFAULT INFORMATION
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
