"""
Definition of views.
"""

#import os

from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, TemplateView

from .models import ComplexQuantity, JournalLine, OperationSubline, Peer, Product, ProductVariant
from .models import CATEGORY_CHANGE, COMPLEX_OPERATION, INTERNAL_TRANSFER, EXTERNAL_TRANSFER

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

class ProductsView(ListView):
    model = Product
    
# class ProductView(TemplateView):
#     template_name = 'product_page.html'

#     def get_context_data(self, *args, **kwargs):
#         context = super(Home. self).get_context_data(*args, **kwargs)
#         context['message'] = 'Hello World!'
#         return context

class pv_journal_line():
    def __init__(self):
        #DateTime RecordDate;
        self.record_date = None
        #string DocumentName;
        self.document_name = ''
        #string DocumentNumber;
        self.document_number = ''
        #DateTime DocumentDate;
        self.document_date = None
        #string PeerName;
        self.peer_name = ''
        #decimal Income;
        self.income = 0.0
        #decimal Outcome;
        self.outcome = 0.0
        #ComplexQuantity Total;
        self.total = ComplexQuantity()
        #Dictionary<string, ComplexQuantity> Partitial;
        self.partitial = dict()


def FormatTableZeroes(val):
    return str(val) if val != 0 else ''
import copy
class ProductVariantView(TemplateView):
    def pv_page(self, pv_id):
        
        main_peer = Peer.objects.get(name__exact=settings.MILACCBOOK_MAIN_PEER_NAME)
        main_name = main_peer.name

        divisions = [] 
        divisions.append(main_name)

        product_variant = ProductVariant.objects.get(pk=pv_id)

        pv_journal = []
        jql = dict() # string, ComplexQuantity
        jql[main_name] = ComplexQuantity()

        jli_date = ''
        # Select all journal lines for specified product variant
        for jli in JournalLine.objects.filter(document_product__product_variant=product_variant):
            current_line = pv_journal_line()
            current_line.record_date = jli.record_date
            current_line.document_name = jli.document_product.document.name
            current_line.document_number = jli.document_product.document.number
            current_line.document_date = jli.document_product.document.date
            current_line.peer_name = jli.document_product.document.peer.name

            change_quantity = jli.document_product.operation_q
            #print('!!! ' + str(change_quantity.total_q) + '=' + str(change_quantity.sort1_q) + '+' + str(change_quantity.sort2_q) + '+' + str(change_quantity.sort3_q) + '+' + str(change_quantity.sort4_q) + '+' + str(change_quantity.sort5_q)) 
            peer_name = jli.document_product.document.peer.name
            
            if jli.document_product.document.operation == EXTERNAL_TRANSFER:
                main_q = copy.copy(jql[main_name])
                main_q.increase(change_quantity)
                jql[main_name] = main_q
                if (change_quantity.total_q > 0):
                    current_line.income += change_quantity.total_q;
                else:
                    current_line.outcome += (-1) * change_quantity.total_q;
            elif jli.document_product.document.operation == INTERNAL_TRANSFER:
                cur_q = None #ComplexQuantity
                if not peer_name in jql:
                    cur_q = ComplexQuantity()
                else:
                    cur_q = copy.copy(jql[peer_name])
                main_q = copy.copy(jql[main_name])
                main_q.increase(change_quantity)
                jql[main_name] = main_q
                cur_q.decrease(change_quantity)
                jql[peer_name] = cur_q
            elif jli.document_product.document.operation == CATEGORY_CHANGE:
                cur_q = None #ComplexQuantity
                if not peer_name in jql:
                    cur_q = ComplexQuantity()
                else:
                    cur_q = copy.copy(jql[peer_name])
                cur_q.increase(change_quantity)
                jql[peer_name] = cur_q
            elif jli.document_product.document.operation == COMPLEX_OPERATION:
                sublines = OperationSubline.objects.filter(document_product=jli.document_product)
                for subline in sublines:
                    change_quantity = subline.operation_q
                    peer_name = subline.peer.name
                    if subline.operation == EXTERNAL_TRANSFER:
                        main_q = copy.copy(jql[main_name])
                        main_q.increase(change_quantity)
                        jql[main_name] = main_q;
                        if change_quantity.total_q > 0:
                            current_line.income += change_quantity.total_q
                        else:
                            current_line.outcome += (-1) * change_quantity.total_q
                    elif subline.operation == INTERNAL_TRANSFER:
                        cur_q = None #ComplexQuantity
                        if not peer_name in jql:
                            cur_q = ComplexQuantity()
                        else:
                            cur_q = copy.copy(jql[peer_name])
                        main_q = copy.copy(jql[main_name])
                        main_q.increase(change_quantity)
                        jql[main_name] = main_q
                        cur_q.decrease(change_quantity)
                        jql[peer_name] = cur_q
                    elif subline.operation == CATEGORY_CHANGE:
                        cur_q = None #ComplexQuantity
                        if not peer_name in jql:
                            cur_q = ComplexQuantity()
                        else:
                            cur_q = copy.copy(jql[peer_name])
                        cur_q.increase(change_quantity)
                        jql[peer_name] = cur_q

            for cur_item in jql:
                if not cur_item in divisions:
                    divisions.append(cur_item)
                current_line.total.increase(jql[cur_item])
            current_line.partitial = jql.copy()

            pv_journal.append(current_line)

        report_builder = ''
        report_builder += '<html>\n<body>\n'
        report_builder += '<h1>' + product_variant.product.name + ' (' + str(product_variant.price) + ')' + '</h1>\n'
        report_builder += '<table>\n'
        # Product Variant Journal report Header
        report_builder += '<tr>'
        report_builder += '<th rowspan="4">Дата запису</th>'
        report_builder += '<th rowspan="4">Найменування документа</th>'
        report_builder += '<th rowspan="4">Номер документа</th>'
        report_builder += '<th rowspan="4">Дата документа</th>'
        report_builder += '<th rowspan="4">Постачальник (одержувач)</th>'
        report_builder += '<th rowspan="4">Надійшло</th>'
        report_builder += '<th rowspan="4">Вибуло</th>'
        report_builder += '<th rowspan="2" colspan="6">Перебуває згідно з документами</th>'
        report_builder += '<th colspan="100%">У тому числі на складі (у підрозділах, військових частинах)</th>'
        report_builder += '</tr><tr>'
        for item in divisions:
            if item == main_name:
                report_builder += '<th colspan="6">На складі</th>'
            else:
                report_builder += '<th colspan="6">' + item + '</th>'
        report_builder += '</tr><tr>'
        report_builder += '<th rowspan="2">Усього</th>'
        report_builder += '<th colspan="5">З них за категоріями (сортами)</th>'
        for item in divisions:
            report_builder += '<th rowspan="2">Усього</th>'
            report_builder += '<th colspan="5">З них за категоріями (сортами)</th>'
        report_builder += '</tr><tr>'
        report_builder += '<th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>'
        for item in divisions:
            report_builder += '<th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>'
        report_builder += '</tr>'

        for pvj_item in pv_journal:
            report_builder += '<tr>'
            report_builder += '<td>' + str(pvj_item.record_date) + '</td>'
            report_builder += '<td>' + pvj_item.document_name + '</td>'
            report_builder += '<td>' + pvj_item.document_number + '</td>'
            report_builder += '<td>' + str(pvj_item.document_date) + '</td>'
            report_builder += '<td>' + pvj_item.peer_name + '</td>'
            report_builder += '<td>' + str(pvj_item.income) + '</td>'
            report_builder += '<td>' + str(pvj_item.outcome) + '</td>'
            report_builder += '<td>' + FormatTableZeroes(pvj_item.total.total_q) + '</td>'
            report_builder += '<td>' + FormatTableZeroes(pvj_item.total.sort1_q) + '</td>'
            report_builder += '<td>' + FormatTableZeroes(pvj_item.total.sort2_q) + '</td>'
            report_builder += '<td>' + FormatTableZeroes(pvj_item.total.sort3_q) + '</td>'
            report_builder += '<td>' + FormatTableZeroes(pvj_item.total.sort4_q) + '</td>'
            report_builder += '<td>' + FormatTableZeroes(pvj_item.total.sort5_q) + '</td>'
            for item in divisions:
                if not item in pvj_item.partitial:
                    report_builder += '<td></td><td></td><td></td><td></td><td></td><td></td>'
                else:
                    report_builder += '<td>' + FormatTableZeroes(pvj_item.partitial[item].total_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(pvj_item.partitial[item].sort1_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(pvj_item.partitial[item].sort2_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(pvj_item.partitial[item].sort3_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(pvj_item.partitial[item].sort4_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(pvj_item.partitial[item].sort5_q) + '</td>'
            report_builder += '</tr>'
        report_builder += '</table>\n</body>\n</html>\n'

        return HttpResponse(report_builder)
