import json

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    payment_date = fields.Date(compute="_compute_payment_date", store=False)

    def _compute_payment_date(self):
        for record in self:
            dates = []
            for payment_info in json.loads(record.invoice_payments_widget).get(
                "content", []
            ):
                dates.append(payment_info.get("date", ""))
            if dates:
                dates.sort()
                record.payment_date = dates[0]

    def create_user(self, partner):
        user_obj = self.env["res.users"]
        vat = partner.vat

        user = user_obj.search([("login", "=", vat)])
        if not user:
            user = user_obj.search([("login", "=", vat), ("active", "=", False)])
            if user:
                user.sudo().write({"active": True})
            else:
                user_values = {
                    "partner_id": partner.id,
                    "login": vat,
                    "company_ids": [partner.company_id.id],
                    "company_id": partner.company_id.id,
                    "role_line_ids": [
                        (
                            0,
                            0,
                            {
                                "role_id": self.env.ref(
                                    "energy_communities.role_ce_member"
                                ).id,
                                "company_id": partner.company_id.id,
                            },
                        )
                    ],
                }
                user = user_obj.sudo()._signup_create_user(user_values)
                # We requiere the user to update the password in keycloak
                # user.sudo().with_context({"create_user": True}).action_reset_password()
                if partner.company_id.create_user_in_keycloak:
                    user.create_users_on_keycloak()
        return user
