# Flight-Deals-Finder-Project
A flight deals finder application that searches and sends deals to a flight club of users.

APIs used and their purpose:
Kiwi - Searches for IATA codes and flights
Sheety - Reads from and writes data in the google sheet.
Twilio - Send an SMS to each user in the flight club

If the IATA codes column in a google sheet isn't populated, Kiwi is used to search for IATA codes for each city in the sheet, which are thereafter written into the 
empty column using the Sheety API. The IATA codes are then read from the sheet and used to search for available flights. The flight club file contains code which allows users to register for the flight club. Notifications (SMSes and emails) are sent to users if a particular flight is found which costs a lower price than the price listed in the sheet for that specific destination. SMTPLIB is used to send the emails. 
