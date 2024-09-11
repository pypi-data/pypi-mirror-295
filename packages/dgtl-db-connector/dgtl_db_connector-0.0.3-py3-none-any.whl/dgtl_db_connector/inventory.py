from client import Client
from model import Model


class Inventory(Model):
    table_name = "inventory"
    primary_key = "PID"
    client = Client(table_name=table_name, index_name=primary_key)

    def __init__(self, **kwargs):
        super().__init__()
        self.PID = kwargs.get('PID')
        self.date_received = kwargs.get('date_received')
        self.holter_name = kwargs.get('holter_name')
        self.birthDate = kwargs.get('birthDate')
        self.sex = kwargs.get('sex')
        self.customerID = kwargs.get('customerID')
        self.dagboek_name = kwargs.get('dagboek_name')
        self.reference = kwargs.get('reference')
        self.selected_for_audit = kwargs.get('selected_for_audit')
        self.audit_status = kwargs.get('audit_status')
        self.audit_notes = kwargs.get('audit_notes')
        self.analyst_audit = kwargs.get('analyst_audit')
        self.notes = kwargs.get('notes')
        self.date_opened = kwargs.get('date_opened')
        self.analyst = kwargs.get('analyst')
        self.date_done = kwargs.get('date_done')
        self.comment = kwargs.get('comment')
        self.date_sent = kwargs.get('date_sent')
        self.status = kwargs.get('status')
        self.hasPacemaker = kwargs.get('hasPacemaker')
        self.indicatie = kwargs.get('indicatie')
        self.medicatie = kwargs.get('medicatie')
        self.secret = kwargs.get('secret')
        self.ecg_id = kwargs.get('ecg_id')
        self.urgent = kwargs.get('urgent')
        self.emergent = kwargs.get('emergent')
        self.graderPool = kwargs.get('graderPool')
        self.date_processed_by_dgtl = kwargs.get('date_processed_by_dgtl')
        self.SLABusinessDays = kwargs.get('SLABusinessDays')
        self.SLATargetDate = kwargs.get('SLATargetDate')
        self.customerPID = kwargs.get('customerPID')
        self.ecg_status = kwargs.get('ecg_status')
        self.source = kwargs.get('source')
        self.urgent_notification = kwargs.get('urgent_notification')
        self.date_marked_sent = kwargs.get('date_marked_sent')
        self.folder = kwargs.get('folder')



    