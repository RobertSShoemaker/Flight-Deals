from twilio.rest import Client
import smtplib

FROM_EMAIL = ""
PASSWORD = ""

ACCOUNT_SID = ""
AUTH_TOKEN = ""
FROM_NUM = ""
TO_NUM = ""


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def send_text(self, flight):
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message_body = f"Low price alert!\n" \
                       f"Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to " \
                       f"{flight.destination_city}-{flight.destination_airport}, from {flight.out_date}" \
                       f" to {flight.return_date}.\n" \
                       f""

        if flight.stop_overs > 0:
            message_body += f"Flight has 1 stop over, via {flight.via_city}."

        message1 = client.messages \
            .create(
                body=message_body,
                from_=FROM_NUM,
                to=TO_NUM
            )
        print(message1.status)
        return message_body

    def send_emails(self, message, email_data):
        with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
            # encrypts email
            connection.starttls()
            # login to email
            connection.login(user=FROM_EMAIL, password=PASSWORD)
            # send email
            print(message)
            for email in email_data:
                to_email = email["email"]
                connection.sendmail(from_addr=FROM_EMAIL,
                                    to_addrs=to_email,
                                    msg=f"Subject:New Low Price Flight!\n\n{message}\n"
                                    )
