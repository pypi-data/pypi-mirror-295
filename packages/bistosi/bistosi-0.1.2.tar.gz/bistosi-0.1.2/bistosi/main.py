from .celery_app import app


def send_email(sender, recipients, subject, html_content, group_uuid, send_at):
    app.send_task(
        "buzzbell.tasks.create_email_object_task",
        kwargs={
            "sender": sender,
            "recipients": recipients,
            "subject": subject,
            "html_content": html_content,
            "group_uuid": group_uuid,
            "send_at": send_at
        }
    )


def cancel_notification_by_group_uuid(group_uuid):
    app.send_task(
        "buzzbell.tasks.cancel_notification_by_group_uuid_task",
        kwargs={"group_uuid": group_uuid}
    )


def send_notice(sender, recipients, subject, linked_to, html_content, group_uuid, send_at):
    app.send_task(
        "buzzbell.tasks.create_notice_object_task",
        kwargs={
            "sender": sender,
            "recipients": recipients,
            "linked_to": linked_to,
            "subject": subject,
            "html_content": html_content,
            "group_uuid": group_uuid,
            "send_at": send_at
        }
    )


def send_sms(sender, recipients, content, group_uuid, send_at):
    app.send_task(
        "buzzbell.tasks.create_sms_object_task",
        kwargs={
            "sender": sender,
            "recipients": recipients,
            "content": content,
            "group_uuid": group_uuid,
            "send_at": send_at
        }
    )


# sample_group_uuid = uuid.uuid4()
# send_notice(
#     "maktab",
#     [
#         {
#             "user_uuid": uuid.UUID("bc47a842-d6d3-4b2f-ae88-30ece57370ec")  # User amirreza
#         },
#         {
#             "user_uuid": uuid.UUID("c1c889a2-bca9-430c-844a-ec6541edf122")  # User maryam
#         },
#         {
#             "user_uuid": uuid.UUID("4e7b55b7-b2a3-415b-900a-e4503d83bd84")  # User ali
#         }
#     ],
#     "TEST SUBJECT",
#     "www.google.com",
#     "این یک پیام تست است.",
#     sample_group_uuid,
#     # datetime.datetime.utcnow()
#     datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
# )

# time.sleep(3)
# cancel_notification_by_message_id(sample_group_uuid)

# send_sms(
#     "maktab",
#     [
#         {
#             "phone_number": "09300629575",
#             "user_uuid": uuid.UUID("bc47a842-d6d3-4b2f-ae88-30ece57370ec")  # User amirreza
#         },
#         {
#             "phone_number": "0933",
#             "user_uuid": uuid.UUID("c1c889a2-bca9-430c-844a-ec6541edf122")  # User maryam
#         },
#         {
#             "phone_number": "",
#             "user_uuid": uuid.UUID("4e7b55b7-b2a3-415b-900a-e4503d83bd84")  # User ali
#         }
#     ],
#     "این یک پیام تست است.",
#     uuid.uuid4(),
#     datetime.datetime.utcnow()
#     # datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
# )

# send_email(
#     "maktab",
#     [
#         {
#             "email": "artaher404@gmail.com",
#             "user_uuid": uuid.UUID("bc47a842-d6d3-4b2f-ae88-30ece57370ec")  # User amirreza
#         },
#         {
#             "email": "artaher403@gmail.com",
#             "user_uuid": uuid.UUID("c1c889a2-bca9-430c-844a-ec6541edf122")  # User maryam
#         },
#         {
#             "email": "visapick.it8@gmail.com",
#             "user_uuid": uuid.UUID("4e7b55b7-b2a3-415b-900a-e4503d83bd84")  # User ali
#         }
#     ],
#     "Hello test 5 min message",
#     f'<h1>Hello</h1><h2>this is an</h2><hr>example email from MailerSend',
#     uuid.uuid4(),
#     datetime.datetime.utcnow()
#     # datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
# )
