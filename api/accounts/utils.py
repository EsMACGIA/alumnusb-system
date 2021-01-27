from accounts.models import User_information, User_stats 

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
    "Donacion estrella diamante" : AchievementsData(AchievementsType.LARGEST_DONATION, 500)
}

# THIS SECTION IS USEFUL TO CREATE DEFAULT INFORMATION
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
