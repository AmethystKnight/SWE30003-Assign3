class Invoice:
    """based on: https://business.gov.au/finance/payments-and-invoicing/how-to-invoice
    The template for invoice should eventually be moved to a table"""
    def __init__(self, invoice_number):
        from helper_functions import get_current_date, get_current_time_in_melbourne
        self._header = 'TAX INVOICE'
        self._company_name = 'Kozy Koala'
        self._ABN = '11156A'
        self.invoice_number = invoice_number
        self.date = get_current_date()
        self.time = get_current_time_in_melbourne()
        self.total_order = {}
        # Has to include gst
        self.total_price = 0
        self.GST = 0.11

    def add_to_order(self, order: dict):
        """Add items to the order.
        SCHEMA: {item_name: {'item': item_name, 'allergy': allergy_info, 'cost': cost}}
        """
        for item_name, item_details in order.items():
            if item_name in self.total_order:
                self.total_order[item_name]['quantity'] += 1
            else:
                self.total_order[item_name] = {
                    'item': item_details['item'],
                    'allergy': item_details['allergy'],
                    'cost': item_details['cost'],
                    'quantity': 1
                }
            self.total_price += item_details['cost']

    def calculate_total(self):
        self.total_price = 0.0
        for item_name, details in self.total_order.items():
            self.total_price += details['cost'] * details['quantity']
        self.total_price += self.total_price * self.GST

    def get_printable_invoice(self) -> dict:
        self.calculate_total()
        invoice_details = {
            'header': self._header,
            'company_name': self._company_name,
            'ABN': self._ABN,
            'invoice_number': self.invoice_number,
            'date': self.date,
            'time': self.time.strftime('%H:%M'),
            'total_order': self.total_order,
            'total_price': f"{self.total_price:.2f}"
        }
        return invoice_details


from singleton import Singleton


class Invoice_Manager(Singleton):
    """factory pattern, the manager is responsible for
       creating and tracking invoices"""

    def __init__(self):
        self._invoices = []

    def get_next_invoice(self) -> Invoice:
        invoice = Invoice(len(self._invoices))
        self._invoices.append(invoice)
        return invoice

    def retrieve_invoice(self, invoice_number) -> Invoice:
        return self._invoices[invoice_number]

    def process_invoice(self, invoice: Invoice):
        # TODO: add functionality
        pass
