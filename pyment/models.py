from django.db import models

from abstarct_model.base_model import BaseModel
from authentication.models import User


STATUS_CHOICES = (
    (1, 'Pending'),
    (2, 'Approved'),
    (3, 'Rejected'),
)


class Subscription(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription')
    amount = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    pyment_date = models.DateField()
#
#
# class CreateTransaction(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     payme_id = models.CharField(max_length=100)
#     amount = models.IntegerField()
#     transaction = models.ForeignKey(Subscription, on_delete=models.CASCADE)
#     state = models.IntegerField(default=0)
#     time = models.DateTimeField()
#
#     def __str__(self):
#         return self.payme_id


class Transaction(BaseModel):
    STATES = [
        (1, "Pending"),
        (2, "Completed"),
        (-1, "Cancelled"),
        (-2, "Timeout Cancelled"),
    ]

    payme_id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    time= models.DateTimeField(null=True, blank=True)
    transaction = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    perform_time = models.DateTimeField(null=True, blank=True)
    cancel_time = models.DateTimeField(null=True, blank=True)
    state = models.IntegerField(choices=STATES, default=1)
    reason = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.id} - State {self.state}"
