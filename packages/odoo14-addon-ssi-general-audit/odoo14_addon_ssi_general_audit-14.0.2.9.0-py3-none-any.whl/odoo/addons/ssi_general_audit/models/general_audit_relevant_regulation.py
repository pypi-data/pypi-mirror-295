# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditRelevantRegulation(models.Model):
    _name = "general_audit_relevant_regulation"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Relevant Regulation"

    item_ids = fields.One2many(
        string="Regulation Items",
        comodel_name="general_audit_relevant_regulation.item",
        inverse_name="regulation_id",
    )
