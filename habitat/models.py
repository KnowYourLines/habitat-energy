from django.db import models


class Record(models.Model):
    unique_bid_number = models.CharField(max_length=255, unique=True)
    accepted_or_rejected = models.CharField(max_length=255)
    delivery_date = models.DateField()


#             "Market Name":"DC LF",
#             "Delivery Date":"2021-02-01",
#             "Unique bid number":"20210201 AG-HEL00G",
#             "Response Unit":"AG-HEL00G",
#             "Unit type":"BM",
#             "Agent/Applicant":"Habitat Energy Limited",
#             "Related Entity":"N/A",
#             "Volume offered":49,
#             "Volume Accepted":49,
#             "Delivery Start":"2021-01-31T23:00:00",
#             "Delivery End":"2021-02-01T23:00:00",
#             "Service Duration":24,
#             "Availability Fee":16.99,
#             "Total Cost":19980.24,
#             "RTM/no RTM":"RTM",
#             "Accepted/Rejected":"Accepted",
#             "Rejection code":null,
#             "Technology Type":"Battery"
