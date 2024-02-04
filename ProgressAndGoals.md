## Tasks (Completed)

- Created a REST API server with several endpoints:
  #MENUS
    MAIN_MENU = '/MainMenu'
    MAIN_MENU_NM = "Welcome to Food Finder!"
    LOGIN_PAGE = '/LoginPage'
    LOGIN_SCREEN_MSG = 'Please Login or Register'

  # ENDPOINTS
    LOGIN_SYSTEM = '/LoginSystem'
    REGISTRATION_SYSTEM = '/RegistrationSystem'

  # RESTAURANT_RELATED ENDPOINTS
    RESTAURANT_REGISTRATION = '/Restaurant_Registration'
    ADD_RESTAURANT_MENUITEM = '/Add_Restaurant_MenuItem'
    REMOVE_RESTAURANT = '/Remove_Restaurant'
    REMOVE_RESTAURANT_RESERVATIONS = '/Remove_Restaurant_Reservations'
    REMOVE_RESTAURANT_MENUITEM = '/Remove_Restaurant_MenuItem'
    SET_RESTAURANT_HOURS = '/Set_Restaurant_Hours'
    GET_RESTAURANT_REVIEWS = '/Get_Restaurant_Reviews'
    SET_RESTAURANT_OPTIONS = '/Set_Restaurant_Options'
    RESTAURANT_SPECIAL_MEALS = '/Restaurant_Special_Meals'


  # CLIENT_RELATED ENDPOINTS
    GET_RESTAURANT_LIST = '/Get_Restaurant_List'
    GET_TRENDING_RESTAURANT_LIST = '/Get_Trending_Restaurant_List'
    PROVIDE_REVIEW = '/Provide_Review'
    GET_RESTAURANT_INFO = '/Get_Restaurant_Info'
    MAKE_RESERVATION = '/Make_Reservation'


    ADD_RESTAURANT = '/restaurant/register'
    RESTAURANT_EP = '/restaurant'
    RESTAURANT_ALL = '/restaurant/all'
    Menu_EP = '/menu'
    REVIEW_EP = '/review'
    HOUR_EP = '/hour'

    TYPE = 'Type'
    DATA = 'Data'
    TITLE = 'Title'
    RETURN = 'Return'
    MENU = 'menu'

    USER_MENU_EP = '/user_menu'
    MAIN_MENU_EP = '/MainMenu'
(put down the endpoints later)

- Created and connected our REST API server to MongoDB Cloud
and hosted our server on PythonAnywhere
@@ -56,9 +12,6 @@ MongoDB Cloud integration
## Goals 
- Develop an interactive frontend -> using good practices and testing procedures as part
  of our automated testing requirement
- Regularly update README files, document code, and provide clearer updates for developers involved with the project.
  This will be done using feedback from constant testing of the application.
- Communicate more with the individuals involved in the group, which will help us achive our milestones.