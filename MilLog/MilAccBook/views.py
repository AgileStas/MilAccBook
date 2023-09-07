"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import ListView, TemplateView

from .models import Product

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

"""
        var mainName = dbContext.Peers.Single(p => p.Name == "А7047").Name;

        // .........
        
        List<string> divisions1 = new List<string>();
        divisions1.Add(mainName);

        var product = dbContext.Products.Single(p => p.Name == "Термос ТН-36");
        var productVariant1 = dbContext.ProductVariants.Single(pv => pv.Product == product && pv.Price == 336);
        // var product = dbContext.Products.Single(p => p.Name == "Коробка картонна");
        // var productVariant1 = dbContext.ProductVariants.Single(pv => pv.Product == product && pv.Price == 0.5m);
        // var product = dbContext.Products.Single(p => p.Name == "Сірники запалювальні б/к");
        // var productVariant1 = dbContext.ProductVariants.Single(pv => pv.Product == product);
        // var product = dbContext.Products.Single(p => p.Name == "Раціон ДПНП-Р10");
        // var productVariant1 = dbContext.ProductVariants.Single(pv => pv.Product == product && pv.Price == 264);
        // var productVariant1 = dbContext.ProductVariants.Single(pv => pv.Product == product && pv.Price == 387);
        // var product = dbContext.Products.Single(p => p.Name == "Раціон ДПНП-Р11");
        // var productVariant1 = dbContext.ProductVariants.Single(pv => pv.Product == product && pv.Price == 264);
        // var productVariant1 = dbContext.ProductVariants.Single(pv => pv.Product == product && pv.Price == 387);
        // var product = dbContext.Products.Single(p => p.Name == "Раціон ДПНП-Р12");
        // var productVariant1 = dbContext.ProductVariants.Single(pv => pv.Product == product && pv.Price == 264);
        // var productVariant1 = dbContext.ProductVariants.Single(pv => pv.Product == product && pv.Price == 387);

        var pvJournal = new List<pvJournalLine>();
        var jql = new Dictionary<string, ComplexQuantity>();
        jql.Add(mainName, new ComplexQuantity());
        // Select all journal lines for specified product variant
        foreach (var jli in dbContext.JournalLines.Where(l => l.DocumentProduct.ProductVariant == productVariant1)) //.OrderBy()
        {
            var currentLine = new pvJournalLine();
            currentLine.RecordDate = jli.RecordDate;
            currentLine.DocumentName = jli.DocumentProduct.Document.Name;
            currentLine.DocumentNumber = jli.DocumentProduct.Document.Number;
            currentLine.DocumentDate = jli.DocumentProduct.Document.Date;
            currentLine.PeerName = jli.DocumentProduct.Document.Peer.Name;
            //currentLine.Income = 0;
            //currentLine.Outcome = 0;
            //currentLine.TotalQuantity = new ComplexQuantity();

            var changeQuantity = jli.DocumentProduct.OperationQuantity;
            var peerName = jli.DocumentProduct.Document.Peer.Name;
            if (jli.DocumentProduct.Document.Operation == Document.OperationType.ExternalTransfer)
            {
                ComplexQuantity mainQ = jql[mainName];
                mainQ.Increase(changeQuantity);
                jql[mainName] = mainQ;
                if (changeQuantity.TotalQuantity > 0)
                {
                    currentLine.Income += changeQuantity.TotalQuantity;
                }
                else
                {
                    currentLine.Outcome += (-1) * changeQuantity.TotalQuantity;
                }
            }
            else if (jli.DocumentProduct.Document.Operation == Document.OperationType.InternalTransfer)
            {
                ComplexQuantity curQ;
                if (!jql.ContainsKey(peerName))
                {
                    curQ = new ComplexQuantity();
                }
                else
                {
                    curQ = jql[peerName];
                }
                var mainQ = jql[mainName];
                mainQ.Increase(changeQuantity);
                jql[mainName] = mainQ;
                curQ.Decrease(changeQuantity);
                jql[peerName] = curQ;
            }
            else if (jli.DocumentProduct.Document.Operation == Document.OperationType.CategoryChange)
            {
                ComplexQuantity curQ;
                if (!jql.ContainsKey(peerName))
                {
                    curQ = new ComplexQuantity();
                }
                else
                {
                    curQ = jql[peerName];
                }
                curQ.Increase(changeQuantity);
                jql[peerName] = curQ;
            }
            else if (jli.DocumentProduct.Document.Operation == Document.OperationType.ComplexOperation)
            {
                var sublines = dbContext.OperationSublines.Where(l => l.DocumentProduct == jli.DocumentProduct);
                foreach (var subline in sublines)
                {
                    changeQuantity = subline.OperationQuantity;
                    peerName = subline.Peer.Name;
                    if (subline.Operation == Document.OperationType.ExternalTransfer)
                    {
                        ComplexQuantity mainQ = jql[mainName];
                        mainQ.Increase(changeQuantity);
                        jql[mainName] = mainQ;
                        if (changeQuantity.TotalQuantity > 0)
                        {
                            currentLine.Income += changeQuantity.TotalQuantity;
                        }
                        else
                        {
                            currentLine.Outcome += (-1) * changeQuantity.TotalQuantity;
                        }
                    }
                    else if (subline.Operation == Document.OperationType.InternalTransfer)
                    {
                        ComplexQuantity curQ;
                        if (!jql.ContainsKey(peerName))
                        {
                            curQ = new ComplexQuantity();
                        }
                        else
                        {
                            curQ = jql[peerName];
                        }
                        var mainQ = jql[mainName];
                        mainQ.Increase(changeQuantity);
                        jql[mainName] = mainQ;
                        curQ.Decrease(changeQuantity);
                        jql[peerName] = curQ;
                    }
                    else if (subline.Operation == Document.OperationType.CategoryChange)
                    {
                        ComplexQuantity curQ;
                        if (!jql.ContainsKey(peerName))
                        {
                            curQ = new ComplexQuantity();
                        }
                        else
                        {
                            curQ = jql[peerName];
                        }
                        curQ.Increase(changeQuantity);
                        jql[peerName] = curQ;
                    }
                }
            }

            foreach (var curItem in jql)
            {
                if (!divisions1.Contains(curItem.Key))
                {
                    divisions1.Add(curItem.Key);
                }
                currentLine.Total.Increase(curItem.Value);
            }
            currentLine.Partitial = new Dictionary<string, ComplexQuantity>(jql);

            pvJournal.Add(currentLine);
        }

        var reportBuilder1 = new StringBuilder();
        reportBuilder1.AppendLine("<html>\n<body>\n<table>\n");
        // Product Variant Journal report Header
        reportBuilder1.AppendLine("<tr>");
        reportBuilder1.AppendLine("<th rowspan=\"4\">Дата запису</th>");
        reportBuilder1.AppendLine("<th rowspan=\"4\">Найменування документа</th>");
        reportBuilder1.AppendLine("<th rowspan=\"4\">Номер документа</th>");
        reportBuilder1.AppendLine("<th rowspan=\"4\">Дата документа</th>");
        reportBuilder1.AppendLine("<th rowspan=\"4\">Постачальник (одержувач)</th>");
        reportBuilder1.AppendLine("<th rowspan=\"4\">Надійшло</th>");
        reportBuilder1.AppendLine("<th rowspan=\"4\">Вибуло</th>");
        reportBuilder1.AppendLine("<th rowspan=\"2\" colspan=\"6\">Перебуває згідно з документами</th>");
        reportBuilder1.AppendLine("<th colspan=\"100%\">У тому числі на складі (у підрозділах, військових частинах)</th>");
        reportBuilder1.AppendLine("</tr><tr>");
        foreach (var item in divisions1)
        {
            if (item == mainName)
            {
                reportBuilder1.AppendLine("<th colspan=\"6\">На складі</th>");
            }
            else
            {
                reportBuilder1.AppendLine("<th colspan=\"6\">" + item + "</th>");
            }
        }
        reportBuilder1.AppendLine("</tr><tr>");
        reportBuilder1.AppendLine("<th rowspan=\"2\">Усього</th>");
        reportBuilder1.AppendLine("<th colspan=\"5\">З них за категоріями (сортами)</th>");
        foreach (var item in divisions1)
        {
            reportBuilder1.AppendLine("<th rowspan=\"2\">Усього</th>");
            reportBuilder1.AppendLine("<th colspan=\"5\">З них за категоріями (сортами)</th>");
        }
        reportBuilder1.AppendLine("</tr><tr>");
        reportBuilder1.AppendLine("<th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>");
        foreach (var item in divisions1)
        {
            reportBuilder1.AppendLine("<th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>");
        }
        reportBuilder1.AppendLine("</tr>");

        foreach (var pvjItem in pvJournal)
        {
            reportBuilder1.AppendLine("<tr>");
            reportBuilder1.AppendLine("<td>" + pvjItem.RecordDate.ToShortDateString() + "</td>");
            reportBuilder1.AppendLine("<td>" + pvjItem.DocumentName + "</td>");
            reportBuilder1.AppendLine("<td>" + pvjItem.DocumentNumber + "</td>");
            reportBuilder1.AppendLine("<td>" + pvjItem.DocumentDate.ToShortDateString() + "</td>");
            reportBuilder1.AppendLine("<td>" + pvjItem.PeerName + "</td>");
            reportBuilder1.AppendLine("<td>" + pvjItem.Income + "</td>");
            reportBuilder1.AppendLine("<td>" + pvjItem.Outcome + "</td>");
            reportBuilder1.AppendLine("<td>" + FormatTableZeroes(pvjItem.Total.TotalQuantity) + "</td>");
            reportBuilder1.AppendLine("<td>" + FormatTableZeroes(pvjItem.Total.Sort1Quantity) + "</td>");
            reportBuilder1.AppendLine("<td>" + FormatTableZeroes(pvjItem.Total.Sort2Quantity) + "</td>");
            reportBuilder1.AppendLine("<td>" + FormatTableZeroes(pvjItem.Total.Sort3Quantity) + "</td>");
            reportBuilder1.AppendLine("<td>" + FormatTableZeroes(pvjItem.Total.Sort4Quantity) + "</td>");
            reportBuilder1.AppendLine("<td>" + FormatTableZeroes(pvjItem.Total.Sort5Quantity) + "</td>");
            foreach (var item in divisions1)
            {
                if (!pvjItem.Partitial.ContainsKey(item))
                {
                    reportBuilder1.AppendLine("<td></td><td></td><td></td><td></td><td></td><td></td>");
                }
                else
                {
                    reportBuilder1.Append("<td>" + FormatTableZeroes(pvjItem.Partitial[item].TotalQuantity) + "</td>");
                    reportBuilder1.Append("<td>" + FormatTableZeroes(pvjItem.Partitial[item].Sort1Quantity) + "</td>");
                    reportBuilder1.Append("<td>" + FormatTableZeroes(pvjItem.Partitial[item].Sort2Quantity) + "</td>");
                    reportBuilder1.Append("<td>" + FormatTableZeroes(pvjItem.Partitial[item].Sort3Quantity) + "</td>");
                    reportBuilder1.Append("<td>" + FormatTableZeroes(pvjItem.Partitial[item].Sort4Quantity) + "</td>");
                    reportBuilder1.AppendLine("<td>" + FormatTableZeroes(pvjItem.Partitial[item].Sort5Quantity) + "</td>");
                }
            }
            reportBuilder1.AppendLine("</tr>");
        }
        reportBuilder1.AppendLine("</table>\n</body>\n</html>\n");
        //Console.WriteLine(reportBuilder1.ToString());
        File.WriteAllText(@"C:\Users\xXx\source\repos\report1.html", reportBuilder1.ToString());

"""

class ProductVariantView(View):
    def get(self, request, *args, **kwargs):
        
        context = {'message': 'Hello Django!'}
        return render(request, "index.html", context=context)
