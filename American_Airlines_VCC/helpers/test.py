import random
import string
import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0000",
    database="flight_application"
)

# Generate random user IDs ranging from 1 to 9
def generate_random_user_id():
    return random.randint(1, 6)

# Generate random feedback messages
def generate_random_feedback():
    reviews = [
    "Great experience! Booking process was smooth and hassle-free.",
    "Terrible service! The flight was delayed and customer support was unhelpful.",
    "Excellent app! Easy to use and find the best deals on flights.",
    "Worst experience ever! The app crashed multiple times and I lost my booking.",
    "Highly recommended! The prices are competitive and the app is user-friendly.",
    "Disappointed with the service. My flight got canceled without any prior notice.",
    "Amazing app! It saved me a lot of time and effort in booking my flights.",
    "Awful experience! The seats were uncomfortable and the in-flight service was poor.",
    "Efficient booking process. I found the perfect flight in just a few clicks.",
    "Horrific customer support! They were rude and unresponsive to my queries.",
    "Smooth transaction. The app made it easy to manage my bookings and check-in.",
    "Unreliable app! It showed incorrect flight details and caused a lot of confusion.",
    "Satisfactory experience overall. The app could use some improvements in terms of speed.",
    "Never using this app again! It overcharged me for the flight tickets.",
    "Fast and convenient booking. I got my e-ticket instantly without any issues.",
    "Extremely dissatisfied! The app kept crashing and I had to start the booking process again.",
    "Good deals on flights. I was able to find affordable options for my trip.",
    "The worst app I've used for flight bookings! It constantly froze and crashed.",
    "Efficient customer support. They promptly resolved my issues with flight rescheduling.",
    "Unacceptable delays! My flight was delayed by several hours without any explanation.",
    "Highly efficient app! It helped me find the best deals and save money on flights.",
    "App needs improvement. It lacks some essential features like seat selection during booking.",
    "Great customer service! They assisted me in changing my flight dates without any hassle.",
    "Nightmare experience! The app charged me twice for the same flight booking.",
    "User-friendly interface. I could easily navigate through the app and complete my booking.",
    "Unprofessional staff! The airline mishandled my baggage and offered no compensation.",
    "Impressed with the app's features. I could track my flight status and get timely updates.",
    "The app needs work. It crashed multiple times during the payment process.",
    "Smooth check-in process. I scanned the barcode from the app and boarded without any issues.",
    "Disorganized boarding process! It was chaotic and lacked proper instructions.",
    "Efficient app. I could book my flights quickly and receive e-tickets instantly.",
    "Pathetic customer support! They ignored my refund request and never responded.",
    "Reasonable prices for flights. I found good deals within my budget.",
    "Inconsistent app performance. It worked fine sometimes but froze at other times.",
    "Good customer assistance. They helped me find alternative flights when mine got canceled.",
    "Avoid this app! It redirected me to a different flight without my consent.",
    "Effortless booking experience. I completed my reservation within minutes.",
    "Unreliable flight schedules! My flight was rescheduled twice without any prior notice.",
    "Impressive app functionality. I could easily manage my bookings and make changes.",
    "The app crashed at the payment stage, and I had to restart the booking process.",
    "Prompt customer support. They quickly resolved my issue with incorrect flight details.",
    "Overpriced flights. I found cheaper options on other platforms"
    ]

   
    return random.choice(reviews)


# Insert random feedback messages into the 'feedbacks' table
cursor = db.cursor()
for _ in range(100):
    user_id = generate_random_user_id()
    message = generate_random_feedback()

    # Insert the feedback into the 'feedbacks' table
    cursor.execute("INSERT INTO feedback (user_id, message) VALUES (%s, %s)", (user_id, message))

# Commit the changes to the database
db.commit()

# Close the database connection
db.close()
