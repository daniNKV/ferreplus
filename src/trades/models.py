from datetime import datetime
from django.db import models
from transitions import Machine
from django.utils.translation import gettext_lazy as _
from user.models import User, Employee
from item.models import Item
from owners.models import Branch


class ProposalState(models.TextChoices):
    PENDING = "PENDING", _("Pending")
    ACCEPTED = "ACCEPTED", _("Acepted")
    DECLINED = "DECLINED", _("Declined")
    COUNTEROFFERED = "COUNTEROFFERED", _("Counteroffered")
    EXPIRED = "EXPIRED", _("Expired")


class ProposalStateMachine:
    states = [state for state, _ in ProposalState.choices]
    proposal_transitions = [
        {
            "trigger": "accept",
            "source": [ProposalState.PENDING, ProposalState.COUNTEROFFERED],
            "dest": ProposalState.ACCEPTED,
            "before": "create_trade",
            "after": "save_state",
        },
        {
            "trigger": "decline",
            "source": [ProposalState.PENDING, ProposalState.COUNTEROFFERED],
            "dest": ProposalState.DECLINED,
            "after": ["save_state"],
        },
        {
            "trigger": "counteroffer",
            "source": ProposalState.PENDING,
            "dest": ProposalState.COUNTEROFFERED,
            "before": "new_offer",
            "after": "save_state",
        },
        {
            "trigger": "expire",
            "source": [ProposalState.PENDING, ProposalState.COUNTEROFFERED],
            "dest": ProposalState.EXPIRED,
            "after": "save_state",
        },
    ]

    def __init__(self, proposal):
        self.proposal = proposal
        self.machine = Machine(
            model=self,
            states=ProposalStateMachine.states,
            transitions=self.proposal_transitions,
            initial=self.states.PENDING,
            send_event=True,
        )

    def save_state(self, event):
        self.proposal.state = event.model.state
        self.proposal.save()

    def create_trade(self, event):
        trade = Trade(
            proposal=self.proposal,
            agreed_date=event.kwargs.get("settled_date"),
            branch=self.proposal.branch,
        )
        trade.save()

    def new_offer(self, event):
        counter_item = event.kwargs.get("item")
        last_offer = self.proposal
        counteroffer = Proposal(
            replied_at=datetime.now,
            counteroffer_to=last_offer,
            requested_item=counter_item,
            requested_user=last_offer.offering_user,
            offering_user=last_offer.requested_user,
            offered_item=last_offer.requested_item,
            possible_branch=last_offer.possible_branch,
            possible_dates=last_offer.possible_dates,
        )
        counteroffer.save()


class TradeState(models.TextChoices):
    PENDING = "PENDING", _("Pending")
    CONFIRMED = "ACCEPTED", _("Acepted")
    CANCELED = "CANCELED", _("Canceled")
    EXPIRED = "EXPIRED", _("Expired")


class TradeStateMachine:
    state = [state for state, _ in TradeState.choices]
    trade_transitions = [
        {
            "trigger": "confirm",
            "source": TradeState.PENDING,
            "dest": TradeState.CONFIRMED,
            "after": "save_state",
        },
        {
            "trigger": "cancel",
            "source": TradeState.PENDING,
            "dest": TradeState.CANCELED,
            "after": "save_state",
        },
        {
            "trigger": "expire",
            "source": TradeState.PENDING,
            "dest": TradeState.EXPIRED,
            "after": "save_state",
        },
    ]

    def __init__(self, trade):
        self.trade = trade
        self.machine = Machine(
            model=self,
            states=TradeStateMachine.states,
            transitions=self.trade_transitions,
            initial="pending",
            send_event=True,
        )

    def save_state(self, event):
        self.proposal.state = event.model.state
        self.proposal.save()


class DateSelection(models.Model):
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()

    def __str__(self):
        return str(self.date) + str(self.from_time)


class Proposal(models.Model):
    state = models.CharField(
        max_length=20, choices=ProposalState.choices, default=ProposalState.PENDING
    )

    requested_user = models.ForeignKey(
        User,
        verbose_name="Usuario solicitado",
        related_name="requested_user",
        on_delete=models.PROTECT,
    )
    offering_user = models.ForeignKey(
        User,
        verbose_name="Usuario solicitante",
        related_name="requesting_user",
        on_delete=models.PROTECT,
    )
    requested_item = models.ForeignKey(
        Item,
        verbose_name="Articulo solicitado",
        related_name="requested_item",
        on_delete=models.PROTECT,
    )
    offered_item = models.ForeignKey(
        Item,
        verbose_name="Articulo ofrecido",
        related_name="offered_item",
        on_delete=models.PROTECT,
    )
    possible_dates = models.ManyToManyField(
        DateSelection,
        verbose_name="Fechas posibles para el encuentro",
    )
    possible_branch = models.ForeignKey(
        Branch, verbose_name="Sucursal elegida", on_delete=models.PROTECT
    )
    counteroffer_to = models.OneToOneField(
        "self",
        verbose_name="Propuesta previa",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    replied_at = models.DateTimeField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Trade(models.Model):
    state = models.CharField(
        max_length=20, choices=TradeState.choices, default=TradeState.PENDING
    )
    proposal = models.OneToOneField(
        Proposal,
        verbose_name="Propuesta",
        on_delete=models.PROTECT,
    )
    agreed_date = models.DateTimeField(verbose_name="Fecha acordada")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField()
