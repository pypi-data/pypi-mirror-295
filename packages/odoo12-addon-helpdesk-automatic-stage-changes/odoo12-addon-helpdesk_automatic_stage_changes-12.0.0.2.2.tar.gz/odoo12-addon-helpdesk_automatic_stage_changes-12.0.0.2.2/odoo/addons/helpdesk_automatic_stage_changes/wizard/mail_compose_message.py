# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    when_odoo_responds_change_stage_to_id = fields.Many2one(
        "helpdesk.ticket.stage", string="Change stage to (When Odoo responds)"
    )

    @api.model
    def default_get(self, fields):
        result = super(MailComposeMessage, self).default_get(fields)
        if result.get("composition_mode") and result["composition_mode"] == "comment":
            result["subject"] = self._context.get("default_subject", result["subject"])
        return result

    @api.multi
    def action_send_mail(self):
        if (
            self.model == "helpdesk.ticket"
            and self.when_odoo_responds_change_stage_to_id
            and self.composition_mode == "mass_mail"
        ):
            ticket = self.env[self.model].browse(self.res_id)
            vals = {
                "when_odoo_responds_change_stage_to_id": self.when_odoo_responds_change_stage_to_id.id,  # noqa: E501
                "stage_id": self.when_odoo_responds_change_stage_to_id.id,
            }
            ticket.write(vals)
        return super(MailComposeMessage, self).action_send_mail()

    @api.multi
    @api.onchange('template_id')
    def onchange_template_id_wrapper(self):
        # Prevent onchange from messing with defaults when the template is set from
        # the mass mailing wizard in the helpdesk ticket form view
        if self._context and self._context.get('skip_onchange_template_id'):
            return
        super(MailComposeMessage, self).onchange_template_id_wrapper()

    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields=None):
        """
        Override (for helpdesk tickets only) to avoid the email composer to suggest
        addresses based on ticket partners, since it was causing duplicates for gmail
        accounts. (See also helpdesk_automatic_stage_changes/models/helpdesk_ticket.py)
        """
        template_values = super(MailComposeMessage, self).generate_email_for_composer(
            template_id, res_ids, fields
        )

        # Remove partner_ids from template_values for helpdesk tickets
        if self._context.get("active_model") == "helpdesk.ticket":
            [template_values[res_id].update({"partner_ids": []}) for res_id in res_ids]

        return template_values
