# -*- coding: <encoding> -*-

from odoo import models, fields, api, _


class PayrollCustomConcept(models.Model):
    _name = "payroll.custom.concept"
    _description = "Payroll Custom Concept"

    @api.model
    def create(self, vals):
        default_account_ext_id = vals.get("default_account_ext_id", False)
        if default_account_ext_id:
            account = self.env.ref(default_account_ext_id, False)
            vals.update({"account_id": account.id if account else False})

        return super(PayrollCustomConcept, self).create(vals)

    name = fields.Char(
        string="Tag",
        required=True,
        help=_("Indicate the name of the custom concept.")
    )
    col_index = fields.Integer(
        string="Column Number",
        required=True,
        help=_("Indicate the position in the file.")
    )
    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account",
        required=True,
        help=_("Indicate the account to post the data.")
    )
    default_account_ext_id = fields.Char("Default Account External ID")
    payroll_import_setup_id = fields.Many2one(
        comodel_name="payroll.import.setup",
        string="Payroll Import Setup"
    )
