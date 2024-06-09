#  Copyright (c) 2020. Codustry Pte. Ltd., Codustry (Thailand) Co., Ltd.


from datetime import datetime, timedelta
from decimal import Decimal
from enum import auto
from json import JSONDecodeError
from typing import Optional

from sqlmodel import SQLModel

import arrow
from gebwai.db.models.__base__ import TimestampModel
import omise
from autoname import AutoName
from beanie import Document, Link
from loguru import logger
from pydantic import BaseModel, Field, conint
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)




class NGebByFileType(BaseModel):
    image: int = 0
    audio: int = 0
    file: int = 0
    video: int = 0
    slip: int = 0

    link: int = 0
    chat: int = 0


class MonthlyStats(BaseModel):
    """
    easy and quick access of stats,
    recal at 00.00+7, at the first day of each month
    """

    n_geb_all: int = 0
    n_process_slip: int = 0

    n_geb_by_file_type: NGebByFileType = Field(default_factory=NGebByFileType)

    updated: datetime = Field(default_factory=datetime.now)


class UserPayment(BaseModel):
    omise_customer_id: str | None = None
    omise_schedule_id: str | None = None
    end_subscription_on: datetime | None = None
    start_trial_on: datetime | None = None
    billing_day: conint(ge=1, le=31) | None = None

    pending_charges: list[dict] = Field(default_factory=list)

    @property
    @retry(
        reraise=True,
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(7),
        retry=retry_if_exception_type(JSONDecodeError),
    )
    def charges(self):
        """
        Note.
        Omise has no retry mechanic #216
        """
        return [omise.Charge.retrieve(charge["id"]) for charge in self.pending_charges]

    @property
    def omise_customer_obj(self):
        if self.omise_customer_id:
            return omise.Customer.retrieve(self.omise_customer_id)

    @property
    def omise_schedule_obj(self):
        if self.omise_schedule_id:
            return omise.Schedule.retrieve(self.omise_schedule_id)

    def get_next_occurrences(self):
        return self.omise_schedule_obj.next_occurrences_on

    @property
    def end_trial_on(self):
        return (
            (self.start_trial_on + timedelta(days=30)) if self.start_trial_on else None
        )

    @property
    def is_on_trial(self):
        return (datetime.now() <= self.end_trial_on) if self.end_trial_on else False

    @property
    def once_paid(self):
        if self.end_trial_on and self.end_subscription_on:
            return self.end_trial_on < self.end_subscription_on
        else:
            return False

    @property
    def is_subscribed(self):
        now = datetime.now()
        if self.end_trial_on and self.end_subscription_on:
            return (
                self.end_trial_on < self.end_subscription_on
                and now <= self.end_subscription_on
            )
        else:
            return False

    # @property
    # def is_monthly_subscribed(self):
    #     if self.omise_schedule_id:
    #         return omise.Schedule.retrieve(self.omise_schedule_id).status == "running"
    #     else:
    #         return False

    def unsubscribe(self):
        self.omise_schedule_obj.destroy()
        assert self.omise_schedule_obj.destroyed

    def remove_card(self, card_token: str):
        card = self.omise_customer_obj.cards.retrieve(card_token)
        card.destroy()

    def subscribe(self):
        """
        subscribe a customer with his default card

        post: update user_payment to db
        """
        now = arrow.now(tz="GMT+7")

        self.billing_day = now.date().day
        charge_schedule = {
            "customer": self.omise_customer_id,
            "amount": 5900,
            "currency": "thb",
            "description": "Gebwai.com Subscription",
            "default_card": True,
            "metadata": {"isSchedule": True},
            "return_uri": "https://liff.line.me/1655710486-zPk1dAjy",
        }
        if self.billing_day <= 28:
            charge = omise.Charge.create(**charge_schedule)
            self.pending_charges.append(charge._attributes)

            schedule = omise.Schedule.create(
                every=1,
                period="month",
                start_date=now.shift(months=1).isoformat(),
                on={"days_of_month": [self.billing_day]},
                end_date=now.shift(years=1).isoformat(),
                charge=charge_schedule,
            )
        else:
            self.billing_day = 1

            charge = omise.Charge.create(**charge_schedule)
            self.pending_charges.append(charge._attributes)

            schedule = omise.Schedule.create(
                every=1,
                period="month",
                start_date=now.shift(
                    months=1
                ).isoformat(),  # we might start a bit early but, will charge on 1st day
                on={"days_of_month": [1]},
                end_date=now.shift(years=1).isoformat(),
                charge=charge_schedule,
            )

        self.omise_schedule_id = schedule.id

        return charge.authorize_uri

    def charge(self, token, amount):
        """
        subscribe a customer with his default card

        post: update user_payment to db
        """
        # ensure min charge amount
        assert amount >= 2000

        # ensure charge
        assert amount in (5900, 58800)

        now = arrow.now(tz="GMT+7")

        self.billing_day = now.date().day
        if self.billing_day > 28:
            self.billing_day = 1

        charge_schedule = {
            "amount": amount,
            "currency": "thb",
            "description": "Gebwai.com Subscription",
            "return_uri": settings.liff_payment.url,
        }

        token_type, *_ = token.split("_")
        if token_type == "tokn":  # noqa: S105
            charge_schedule["customer"] = self.omise_customer_id
            customer = self.omise_customer_obj
            customer.update(card=token)
        elif token_type == "src":  # noqa: S105
            charge_schedule["source"] = token
        else:
            raise NotImplementedError

        charge = omise.Charge.create(**charge_schedule)
        self.pending_charges.append(charge._attributes)

        return charge.authorize_uri

    def add_omise_customer(self, user_id, description, email=None):
        customer = omise.Customer.create(
            metadata={"line_user_id": user_id},
            email=email,
            description=description,
        )
        self.omise_customer_id = customer.id
        return self

    def make_onetime_payment(
        self,
        amount: Decimal,
        source_token: str = None,
        callback_url: str = "https://4365ce20-7532-47b5-a553-ee9aff24d256.mock.pstmn.io/get",
    ):
        """
        pay a customer with his default card

        ref. https://www.omise.co/charging-cards#charging-the-card-directly
        """
        if source_token:
            return omise.Charge.create(
                amount=amount * 100,
                currency="thb",
                card=source_token,
                return_uri=callback_url,
            )
        else:
            return omise.Charge.create(
                amount=amount * 100,
                currency="thb",
                customer=self.omise_customer_id,
                return_uri=callback_url,
            )

    def add_card(self, card_token: str):
        return self.omise_customer_obj.update(card=card_token)

    def list_cards(self):
        """
        Object.keys(response.data).forEach(index =>  {
          cards.push({
            name: response.data[index].name,
            expiration_date: `EXP ${response.data[index].expiration_month}/${response.data[index].expiration_year}`,
            brand_type: response.data[index].brand,
            last_digits: response.data[index].last_digits

        """
        return self.omise_customer_obj.list_cards()

    def get_schedule(self):
        """
             const shallowPromise = new Promise((res, rej) => {
          omise.schedules.retrieve(payload.omise_user_schedule_id).then((response) => {
            if (Object.keys(response).length) {
             res({
               stamp: +new Date(),
               payload: response,
               extra: {
                 code: 200,
                 status: true
               }
             });
           }
          }).catch((err) => {
            rej(err);
          }).done();
         });

        return await shallowPromise;
        """


class GebSettings(BaseModel):
    image: bool = True
    slip: bool = True
    audio: bool = True
    file: bool = True
    video: bool = True
    chat: bool = False
    link: bool = True


class TemplateSourceSettings(BaseModel):
    """
    for templating
    """

    geb_settings: GebSettings = GebSettings()
    verify_slip: bool | None = None
    # integration: Optional[Link["Integration"]] = None
    enabled: bool = True


class SourceSettings(TemplateSourceSettings):
    starting_source_name: str
    source_id: str
    created: datetime = Field(default_factory=datetime.now)
    before_follow_gebwai: bool = False

    @classmethod
    def create_from_template(
        cls, starting_source_name, source_id, template: TemplateSourceSettings
    ):
        return cls(
            starting_source_name=starting_source_name,
            source_id=source_id,
            geb_settings=template.geb_settings,
            verify_slip=template.verify_slip,
            integration=template.integration,
        )


class UserSettings(SQLModel):
    automatic_geb_for_newly_added_group: bool = True
    geb_my_own_files: bool = True
    report_geb_stats: bool = True

    default_source_settings: TemplateSourceSettings = TemplateSourceSettings()
    source_settings: dict[str, SourceSettings] = Field(default_factory=dict)

    async def get_or_create_source_settings(
        self, source_id: SourceIdStr, before_follow_gebwai: bool = False
    ):
        """please save after call this"""
        did_create = False
        source_setting = self.source_settings.get(source_id)
        if source_setting is None:
            source_setting = SourceSettings.create_from_template(
                starting_source_name=await source_id.get_starting_name(),
                source_id=source_id,
                template=self.default_source_settings,
            )
            if not self.automatic_geb_for_newly_added_group:
                source_setting.enabled = False

            source_setting.before_follow_gebwai = before_follow_gebwai
            self.source_settings[source_id] = source_setting
            did_create = True
        return did_create, source_setting


class Affiliate(BaseModel):
    suffix_url: str
    payment_details: dict


class UserTier(AutoName):
    iron = auto()
    silver = auto()
    gold = auto()


class TutorialExperience(BaseModel):
    invited_to_group: bool = False
    collected_first_file_on: datetime | None = None


class User(SQLModel, TimestampModel, table=True):

    # settings: UserSettings = Field(default_factory=UserSettings)
    # integrations: list[Link[Integration]] = Field(default_factory=list)
    # proposed_default_integration: Link[Integration] | None = None

    # stats: MonthlyStats = Field(default_factory=MonthlyStats)

    # is_blocked: bool = False
    # tier: UserTier = UserTier.iron
    # payment: UserPayment = Field(default_factory=UserPayment)

    # tutorial_experience: TutorialExperience = Field(default_factory=TutorialExperience)

    # affiliate: Affiliate | None = None
    # refer_by_user: str | None = None
    # refer_time: datetime | None = None

    line_user_id: str = Field(foreign_key="LINEUser.user_id")


    @property
    def user_id(self):
        return self.profile.user_id

    @property
    def n_club(self):
        n = len(self.settings.source_settings)
        if self.user_id in self.settings.source_settings:
            n -= 1
        return n

    @property
    def n_club_before_follow_gebwai(self):
        return sum(
            c.before_follow_gebwai for c in self.settings.source_settings.values()
        )

    def get_default_integration_id(self):
        if self.proposed_default_integration:
            return self.proposed_default_integration
        elif self.integrations:
            return self.integrations[-1]
        else:
            return None

    # affiliate: Optional[Affiliate] = None
    # refer_by_user: Optional[str] = None
    # refer_time: Optional[datetime] = None

    def start_trial(self):
        """
        post: save changes to db
        """
        if self.payment.start_trial_on is None:
            self.payment.start_trial_on = datetime.now()
            self.payment.end_subscription_on = self.payment.end_trial_on
            self.tier = UserTier.silver
            return True

        return False

    @classmethod
    async def get_it_done(
        cls,
        line_id: str,
        *,
        create_or_unblock_if_not_exists=False,
        with_working_token=False,
    ) -> Optional["User"]:
        if with_working_token:
            logger.warning("Removing `with_working_token`")

        # majority of cases

        user = await cls.find_one(User.profile.user_id == line_id)

        if user:
            if create_or_unblock_if_not_exists:
                user.is_blocked = False
                await user.save()
            return user
        else:
            # minority of cases
            if create_or_unblock_if_not_exists:
                new = await cls.init_from_line_id(user_id=line_id)
                await new.save()
                return new
            else:
                return None

    # # @staticmethod
    # # def exists(db: Database, line_id: str) -> bool:
    # #     n = (
    # #         db[settings.MONGODB_USER_COLLECTION]
    # #         .find({"profile.user_id": line_id})
    # #         .count()
    # #     )
    # #     return n == 1

    @classmethod
    async def init_from_line_id(cls, user_id, group_id=None):
        user_profile = await UserProfile.from_line_id(
            user_id=user_id, group_id=group_id
        )
        return cls(profile=user_profile)

    async def get_or_create_source_settings(
        self,
        source_id: SourceIdStr,
        before_follow_gebwai: bool = False,
    ):
        if not isinstance(source_id, SourceIdStr):
            source_id = SourceIdStr(source_id)

        did_create, source_setting = await self.settings.get_or_create_source_settings(
            source_id, before_follow_gebwai=before_follow_gebwai
        )
        if did_create:
            await self.save()
        return source_setting
