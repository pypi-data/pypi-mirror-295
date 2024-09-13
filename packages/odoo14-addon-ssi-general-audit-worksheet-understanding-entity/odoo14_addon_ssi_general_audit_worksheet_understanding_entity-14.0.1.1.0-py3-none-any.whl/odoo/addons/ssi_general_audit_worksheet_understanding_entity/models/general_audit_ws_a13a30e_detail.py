# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditWSa13a30eOrganizationStructure(models.Model):
    _name = "general_audit_ws_a13a30e.detail"
    _description = "Worksheet a13a30e - Detail"
    _order = "worksheet_id, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="general_audit_ws_a13a30e",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    regulation_id = fields.Many2one(
        string="Regulation",
        comodel_name="general_audit_relevant_regulation",
        required=True,
    )
    item_id = fields.Many2one(
        string="Item",
        comodel_name="general_audit_relevant_regulation.item",
        required=True,
    )
    related_account_type_ids = fields.Many2many(
        string="Related Standard Accounts",
        comodel_name="client_account_type",
        relation="rel_general_audit_ws_a13a30e_detail_2_account_type",
        column1="detail_id",
        column2="type_id",
        required=True,
    )
    significant_impact = fields.Boolean(
        string="Significant Impact",
        default=False,
    )
