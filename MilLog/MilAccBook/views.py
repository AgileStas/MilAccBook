"""
Definition of views.
"""

#import os

from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.urls import reverse_lazy

from .models import ComplexQuantity, Document, JournalLine, OperationSubline, Peer, Product, ProductVariant, ProductGroup, UOM_STR
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

class DocumentCreateView(CreateView):
    model = Document
    fields = ['name', 'number', 'date', 'operation', 'peer', 'base_document_str']
    success_url = reverse_lazy('documents')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The document was created successfully.")
        return super(DocumentCreateView, self).form_valid(form) 

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

class remains_line():
    def __init__(self):
        self.pg_name = ''
        #public string Name;
        self.name = ''
        self.uom = ''
        #public decimal Price;
        self.price = 0.0
        #public ComplexQuantity Total;
        self.total = ComplexQuantity()
        #public Dictionary<string, ComplexQuantity> Partitial;
        self.partitial = {}

class AssetView(TemplateView):
    def asset_page(self):
        main_peer = Peer.objects.get(name__exact=settings.MILACCBOOK_MAIN_PEER_NAME)
        main_name = main_peer.name

        divisions = [] 
        divisions.append(main_name)

        #List<RemainsLine> remainsLines = new List<RemainsLine>();
        remains_lines = []

        for product_variant in ProductVariant.objects.all().order_by('product_id'):
            # Needed info before JournalLine generation:
            # - Quantity of product in the main warehouse
            # - Quantity of product in each internal peer involved in previous product transfers
            # - Total quantity of product = sum of the previous two items

            # Select all journal lines for specified product variant
            #var ql = new Dictionary<string, ComplexQuantity>();
            ql = {}
            ql[main_name] = ComplexQuantity()
            for jli in JournalLine.objects.filter(document_product__product_variant=product_variant):
                change_quantity = ComplexQuantity(jli.document_product.total_q, jli.document_product.sort1_q, jli.document_product.sort2_q, jli.document_product.sort3_q, jli.document_product.sort4_q, jli.document_product.sort5_q)
                peer_name = jli.document_product.document.peer.name

                if jli.document_product.document.operation == EXTERNAL_TRANSFER:
                    #main_q = copy.copy(ql[mainName])
                    main_q = ql[main_name]
                    main_q.increase(change_quantity)
                    ql[main_name] = main_q
                elif jli.document_product.document.operation == INTERNAL_TRANSFER:
                    cur_q = ComplexQuantity()
                    if not peer_name in ql:
                        pass
                    else:
                        cur_q = ql[peer_name]
                    main_q = ql[main_name]
                    main_q.increase(change_quantity)
                    ql[main_name] = main_q
                    cur_q.decrease(change_quantity)
                    ql[peer_name] = cur_q
                elif jli.document_product.document.operation == CATEGORY_CHANGE:
                    cur_q = ComplexQuantity()
                    if not peer_name in ql:
                        pass
                    else:
                        cur_q = ql[peer_name]
                    cur_q.increase(change_quantity)
                    ql[peer_name] = cur_q
                elif jli.document_product.document.operation == COMPLEX_OPERATION:
                    sublines = OperationSubline.objects.filter(document_product=jli.document_product)
                    for subline in sublines:
                        change_quantity = subline.operation_q
                        peer_name = subline.peer.name
                        if subline.operation == EXTERNAL_TRANSFER:
                            main_q = ql[main_name]
                            main_q.increase(change_quantity)
                            ql[main_name] = main_q
                        elif subline.operation == INTERNAL_TRANSFER:
                            cur_q = ComplexQuantity()
                            if not peer_name in ql:
                                pass
                            else:
                                cur_q = ql[peer_name]
                            main_q = ql[main_name]
                            main_q.increase(change_quantity)
                            ql[main_name] = main_q
                            cur_q.decrease(change_quantity)
                            ql[peer_name] = cur_q
                        elif subline.operation == CATEGORY_CHANGE:
                            cur_q = ComplexQuantity()
                            if not peer_name in ql:
                                pass
                            else:
                                cur_q = ql[peer_name]
                            cur_q.increase(change_quantity)
                            ql[peer_name] = cur_q

            total_q = ComplexQuantity()
            for cur_item in ql:
                if not cur_item in divisions:
                    divisions.append(cur_item)

                total_q.increase(ql[cur_item])

            rl = remains_line()
            rl.name = product_variant.product.name
            rl.price = product_variant.price
            rl.total = total_q
            rl.partitial = copy.copy(ql)
            remains_lines.append(rl)

        report_builder = ''
        report_builder += '<html>\n<body>\n<table>\n'
        # Product remains report Header
        report_builder += '<tr>\n'
        report_builder += '<th rowspan="4">Найменування військового майна, індекс, номер креслення</th>\n'
        report_builder += '<th rowspan="4">Ціна за одиницю</th>\n'
        report_builder += '<th rowspan="2" colspan="6">Перебуває згідно з документами</th>\n'
        report_builder += '<th colspan="100%">У тому числі на складі (у підрозділах, військових частинах)</th>\n'
        report_builder += '</tr><tr>\n'
        for item in divisions:
            if item == main_name:
                report_builder += '<th colspan="6">На складі</th>\n'
            else:
                report_builder += '<th colspan="6">' + item + '</th>\n'
        report_builder += '</tr><tr>\n'
        report_builder += '<th rowspan="2">Усього</th>\n'
        report_builder += '<th colspan="5">З них за категоріями (сортами)</th>\n'
        for item in divisions:
            report_builder += '<th rowspan="2">Усього</th>\n'
            report_builder += '<th colspan="5">З них за категоріями (сортами)</th>\n'
        report_builder += '</tr><tr>\n'
        report_builder += '<th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>\n'
        for item in divisions:
            report_builder += '<th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>\n'
        report_builder += '</tr>\n'

        for rl in remains_lines:
            report_builder += '<tr>\n'
            report_builder += '<td>' + rl.name + '</td>\n'
            report_builder += '<td>' + str(rl.price) + '</td>\n'
            report_builder += '<td>' + FormatTableZeroes(rl.total.total_q) + '</td>\n'
            report_builder += '<td>' + FormatTableZeroes(rl.total.sort1_q) + '</td>\n'
            report_builder += '<td>' + FormatTableZeroes(rl.total.sort2_q) + '</td>\n'
            report_builder += '<td>' + FormatTableZeroes(rl.total.sort3_q) + '</td>\n'
            report_builder += '<td>' + FormatTableZeroes(rl.total.sort4_q) + '</td>\n'
            report_builder += '<td>' + FormatTableZeroes(rl.total.sort5_q) + '</td>\n'

            for item in divisions:
                if not item in rl.partitial:
                    report_builder += '<td></td><td></td><td></td><td></td><td></td><td></td>\n'
                else:
                    report_builder += '<td>' + FormatTableZeroes(rl.partitial[item].total_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(rl.partitial[item].sort1_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(rl.partitial[item].sort2_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(rl.partitial[item].sort3_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(rl.partitial[item].sort4_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(rl.partitial[item].sort5_q) + '</td>\n'

            report_builder += '</tr>'
        report_builder += '</table>\n</body>\n</html>\n'

        return HttpResponse(report_builder)

class AssetGroupView(TemplateView):

    def asset_page(self):
        def recurse_product_group(pg):
            d = {}
            for product_group in ProductGroup.objects.filter(parent=pg):
                p = []
                for product in Product.objects.filter(group=product_group):
                    p.append(product)
                d[product_group] = p
                d.update(recurse_product_group(product_group))
            return d

        main_peer = Peer.objects.get(name__exact=settings.MILACCBOOK_MAIN_PEER_NAME)
        main_name = main_peer.name

        divisions = [] 
        divisions.append(main_name)

        #List<RemainsLine> remainsLines = new List<RemainsLine>();
        remains_lines = []

        data = recurse_product_group(None)
        #report_builder = ''
        #report_builder += '<html>\n<body>\n<table>\n'
        #for pg in data:
        #    for product in data[pg]:
        #        for product_variant in ProductVariant.objects.filter(product=product):
        #            pass
        #        report_builder += '<tr>\n<td>' + pg.name + '</td>\n<td>' + product.name + '</td>\n</tr>\n'
        #report_builder += '</table>\n</body>\n</html>\n'

        for pg in data:
            for product in data[pg]:
                for product_variant in ProductVariant.objects.filter(product=product):
                    # Needed info before JournalLine generation:
                    # - Quantity of product in the main warehouse
                    # - Quantity of product in each internal peer involved in previous product transfers
                    # - Total quantity of product = sum of the previous two items

                    # Select all journal lines for specified product variant
                    #var ql = new Dictionary<string, ComplexQuantity>();
                    ql = {}
                    ql[main_name] = ComplexQuantity()
                    for jli in JournalLine.objects.filter(document_product__product_variant=product_variant):
                        change_quantity = ComplexQuantity(jli.document_product.total_q, jli.document_product.sort1_q, jli.document_product.sort2_q, jli.document_product.sort3_q, jli.document_product.sort4_q, jli.document_product.sort5_q)
                        peer_name = jli.document_product.document.peer.name

                        if jli.document_product.document.operation == EXTERNAL_TRANSFER:
                            #main_q = copy.copy(ql[mainName])
                            main_q = ql[main_name]
                            main_q.increase(change_quantity)
                            ql[main_name] = main_q
                        elif jli.document_product.document.operation == INTERNAL_TRANSFER:
                            cur_q = ComplexQuantity()
                            if not peer_name in ql:
                                pass
                            else:
                                cur_q = ql[peer_name]
                            main_q = ql[main_name]
                            main_q.increase(change_quantity)
                            ql[main_name] = main_q
                            cur_q.decrease(change_quantity)
                            ql[peer_name] = cur_q
                        elif jli.document_product.document.operation == CATEGORY_CHANGE:
                            cur_q = ComplexQuantity()
                            if not peer_name in ql:
                                pass
                            else:
                                cur_q = ql[peer_name]
                            cur_q.increase(change_quantity)
                            ql[peer_name] = cur_q
                        elif jli.document_product.document.operation == COMPLEX_OPERATION:
                            sublines = OperationSubline.objects.filter(document_product=jli.document_product)
                            for subline in sublines:
                                change_quantity = subline.operation_q
                                peer_name = subline.peer.name
                                if subline.operation == EXTERNAL_TRANSFER:
                                    main_q = ql[main_name]
                                    main_q.increase(change_quantity)
                                    ql[main_name] = main_q
                                elif subline.operation == INTERNAL_TRANSFER:
                                    cur_q = ComplexQuantity()
                                    if not peer_name in ql:
                                        pass
                                    else:
                                        cur_q = ql[peer_name]
                                    main_q = ql[main_name]
                                    main_q.increase(change_quantity)
                                    ql[main_name] = main_q
                                    cur_q.decrease(change_quantity)
                                    ql[peer_name] = cur_q
                                elif subline.operation == CATEGORY_CHANGE:
                                    cur_q = ComplexQuantity()
                                    if not peer_name in ql:
                                        pass
                                    else:
                                        cur_q = ql[peer_name]
                                    cur_q.increase(change_quantity)
                                    ql[peer_name] = cur_q

                    total_q = ComplexQuantity()
                    for cur_item in ql:
                        if not cur_item in divisions:
                            divisions.append(cur_item)

                        total_q.increase(ql[cur_item])

                    rl = remains_line()
                    rl.pg_name = product_variant.product.group.name
                    rl.name = product_variant.product.name
                    rl.uom = product_variant.product.uom
                    rl.price = product_variant.price
                    rl.total = total_q
                    rl.partitial = copy.copy(ql)
                    remains_lines.append(rl)

        report_builder = ''
        report_builder += '<html>\n<body>\n<table>\n'
        # Product remains report Header
        report_builder += '<tr>\n'
        report_builder += '<th rowspan="4">Група майна</th>\n'
        report_builder += '<th rowspan="4">Найменування військового майна, індекс, номер креслення</th>\n'
        report_builder += '<th rowspan="4">Одиниця виміру</th>\n'
        report_builder += '<th rowspan="4">Ціна за одиницю</th>\n'
        report_builder += '<th rowspan="2" colspan="6">Перебуває згідно з документами</th>\n'
        report_builder += '<th colspan="100%">У тому числі на складі (у підрозділах, військових частинах)</th>\n'
        report_builder += '</tr><tr>\n'
        for item in divisions:
            if item == main_name:
                report_builder += '<th colspan="6">На складі</th>\n'
            else:
                report_builder += '<th colspan="6">' + item + '</th>\n'
        report_builder += '</tr><tr>\n'
        report_builder += '<th rowspan="2">Усього</th>\n'
        report_builder += '<th colspan="5">З них за категоріями (сортами)</th>\n'
        for item in divisions:
            report_builder += '<th rowspan="2">Усього</th>\n'
            report_builder += '<th colspan="5">З них за категоріями (сортами)</th>\n'
        report_builder += '</tr><tr>\n'
        report_builder += '<th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>\n'
        for item in divisions:
            report_builder += '<th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>\n'
        report_builder += '</tr>\n'

        for rl in remains_lines:
            report_builder += '<tr>\n'
            report_builder += '<td>' + rl.pg_name + '</td>\n'
            report_builder += '<td>' + rl.name + '</td>\n'
            report_builder += '<td>' + UOM_STR(rl.uom) + '</td>\n'
            report_builder += '<td>' + str(rl.price) + '</td>\n'
            report_builder += '<td>' + FormatTableZeroes(rl.total.total_q) + '</td>\n'
            report_builder += '<td>' + FormatTableZeroes(rl.total.sort1_q) + '</td>\n'
            report_builder += '<td>' + FormatTableZeroes(rl.total.sort2_q) + '</td>\n'
            report_builder += '<td>' + FormatTableZeroes(rl.total.sort3_q) + '</td>\n'
            report_builder += '<td>' + FormatTableZeroes(rl.total.sort4_q) + '</td>\n'
            report_builder += '<td>' + FormatTableZeroes(rl.total.sort5_q) + '</td>\n'

            for item in divisions:
                if not item in rl.partitial:
                    report_builder += '<td></td><td></td><td></td><td></td><td></td><td></td>\n'
                else:
                    report_builder += '<td>' + FormatTableZeroes(rl.partitial[item].total_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(rl.partitial[item].sort1_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(rl.partitial[item].sort2_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(rl.partitial[item].sort3_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(rl.partitial[item].sort4_q) + '</td>'
                    report_builder += '<td>' + FormatTableZeroes(rl.partitial[item].sort5_q) + '</td>\n'

            report_builder += '</tr>'
        report_builder += '</table>\n</body>\n</html>\n'

        return HttpResponse(report_builder)
