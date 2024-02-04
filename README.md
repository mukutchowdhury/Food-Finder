# **FOOD FINDER**

---

## Progress & Goals

[a link](https://github.com/mukutchowdhury/Food-Finder/blob/master/ProgressAndGoals.md)

---

## Project Description

Food Finder is a platform designed to help users discover and explore local restaurants and food establishments. It promises to provide a great user experience by offering up-to-date menus and establishment ratings. Users are also able to create an account for themselves to keep track of restaurants, ratings, dashboards, bookings, and more!

---

## User Interactions and Features: [High-level]
- **Signup**: On this page, users will provide their full name: first name and last name. This pages would check if the formatting of the registration is clear so no fake name with numbers or emojis. Will give a sucessfull message in the end once the user is done filling out the information.
- **Login**: The login page would reguire users to enter their email address and password. This page is user-friendly and would have another confirmation password section where the user has to re-enter their password so its the same throughout the time they are using the food-finder services. Will display a sucessfull message when its done. 
- **Restaurant Discovery**: Assist users in discovering nearby restaurants and food places. Includes map views with pins and location ordering.
- **Menu Access**: Provide users with access to up-to-date menus for selected establishments.
- **Rating and Social System**: Enhance user experience through establishment scoring via a rating feature and allow users to interact with other ratings.
- **Business Exposure**: Offer local establishments exposure through front-page and food category advertisements. 
- **User support**: Create a feedback mechanism within the app for users to report issues or suggest improvements. Offer customer support channels to address user inquiries and concerns.
- **Restaurant Dashboard**: Provide restaurant owners with a dashboard where they can update their menus, respond to customer reviews, and manage their business information.
- **Reservations & Booking**: Incorporate a reservation and booking system to allow users to reserve tables or order food for pick-up or delivery directly through the app. Partner with local restaurants to facilitate online reservations.
- **Personalization**: Personalized restaurant recommendations based on user preferences and past interactions. Machine learning algorithms to improve recommendations over time.
- **Search & filter**: Keyword search for restaurant names or cuisines. Filter options for location, price range, ratings, and dietary preferences (e.g., vegetarian, vegan, gluten-free). Sorting options for distance, popularity, ratings, and price.
- **Timing**: Breaks down into Breakfast, Lunch, Dinner, and other special categories. User is able to select the preferred timing and the list of options in Brooklyn.
- **Payment Integration**: Secure payment processing for in-app purchases, reservations, and food orders.

## System Features and Design: [Low-level]
- **Database Integration**: Setting up a Database system with MongoDB to store restaurant information like data, menu items, user accounts, user sessions, and reviews.
- **Api Integration**: Integrate with third-party APIs to gather restaurant informations like location data, menus, and reviews. Add complex feature support in addition expected account information retrieval APIs. Utilizing Google Maps API for map view and location pins, Yelp API for resturant information and menus, 
Stripe API for secure and easy payments.
- **User Authentication and Authorization**: Develop user authentication mechanisms, including user registration, login, and password reset features for the user. Add session support to maintain logged in/out status. Implement search algorithms that optimize query performance.
- **Data Validation and Sanitization**: Implement input validation and data sanitization to prevent security vulnerabilities like SQL injection and cross-site scripting (XSS). Validate and sanitize user-generated content like reviews and the user's information that they put when creating an account. Ensure users do not put invalid emails or passwords to prevent spam and protect accounts.
- **Error Handling**: Implement robust error handling to gracefully handle unexpected errors and provide meaningful error messages to users. Set up logging to track application events and monitor system health.
- **Data Security**: Continuously monitor and update security measures to protect user data and payment information. Implement encryption for sensitive data and comply with data protection regulations.
- **Automated Processes and Testing**: Utilize GitHub actions for CI/CD (Continuous Integration / Continuous Deployment/Delivery) to ensure that the application is stable and ready to deploy or deliver continously for stakeholders and users needing new features. Automated testing with a TDD approach to speed up development and ensure functionality in an Agile setting. Implement continuous updating of Food Finder's data through automation saving engineering hours and manual errors.

## LOGIN & REGISTRATION (Workflow)

![Food Finder Image](https://github.com/mukutchowdhury/Food-Finder/blob/master/assets/ff_image_1.jpg)

  
## CLIENT INTERFACE (Workflow)

![Food Finder Image](https://github.com/mukutchowdhury/Food-Finder/blob/master/assets/ff_client_workflow.jpeg)


## RESTAURANT OWNER INTERFACE (Workflow)

![Food Finder Image](https://github.com/mukutchowdhury/Food-Finder/blob/master/assets/ff_owner_workflow.jpeg)
