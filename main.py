from flask import Flask, render_template, request, redirect
from model.Client import Client
from model.Sale import Sale
from model.Product import Product
from model.ItemSale import SaleItem
from dao.ControllerDefault import Controller
from datetime import datetime

app = Flask(__name__)
controller = Controller()
clients = []
products = []
sales = []

@app.route('/sales')
def sale_list():
    sales = controller.search_all(Sale())
    for sale in sales:
        cli = controller.search(query=f"select * from cliente where codcliente = {sale.client.idclient}")
        if cli:
            sale.client = Client(cli[0][0], cli[0][1], cli[0][2])

        data = str(sale.date).split('-')
        sale.date = f"{data[2]}/{data[1]}/{data[0]}"
    return render_template('sales/list.html', sales=sales, active_page='sales')

@app.route('/sales/create', methods=['GET', 'POST'])
def sale_create():
    if request.method == 'POST':
        sale = Sale()
        sale.date = datetime.today().strftime('%Y-%m-%d')
        sale.client.idclient = int(request.form['client_id'])

        total = 0
        items = []
        products = controller.search_all(Product())
        for product in products:
            qtd_str = request.form.get(f'quantities_{product.idproduct}', '0')
            qtd = int(qtd_str) if qtd_str.isdigit() else 0
            if qtd > 0:
                item = SaleItem()
                item.product = product
                item.quantity = qtd
                item.value = qtd * product.price
                total += item.value
                items.append(item)

        sale.total_value = total
        controller.insert(sale)
        sale.idsale = controller.max_code(sale)[0][0]

        for item in items:
            item.idsale = sale.idsale
            controller.insert(item)

        return redirect('/sales')

    clients = controller.search_all(Client())
    products = controller.search_all(Product())
    return render_template('sales/create.html', clients=clients, products=products, active_page='sales')

@app.route('/sales/edit/<int:idsale>', methods=['GET', 'POST'])
def sale_edit(idsale):
    if request.method == 'POST':
        sale = Sale()
        sale.idsale = idsale
        sale.client.idclient = int(request.form['client_id'])
        sale.date = datetime.today().strftime('%Y-%m-%d')

        total = 0
        products = controller.search_all(Product())
        items = []
        for product in products:
            qtd_str = request.form.get(f'quantities_{product.idproduct}', '0')
            qtd = int(qtd_str) if qtd_str.isdigit() else 0
            if qtd > 0:
                item = SaleItem()
                item.idsale = idsale
                item.product = product
                item.quantity = qtd
                item.value = qtd * product.price
                total += item.value
                items.append(item)

        sale.total_value = total
        controller.update(sale, idsale)

        controller.db.execute(f"DELETE FROM item_venda WHERE codvenda = {idsale}")
        controller.db.save()

        for item in items:
            controller.insert(item)

        return redirect('/sales')

    result = controller.search(query=f"SELECT * FROM venda WHERE codvenda = {idsale}")
    if not result:
        return "Venda não encontrada", 404

    sale_data = result[0]
    sale = Sale(sale_data[0], sale_data[1], sale_data[2], Client(sale_data[3]))

    products = controller.search_all(Product())
    clients = controller.search_all(Client())
    item_data = controller.search(query=f"SELECT * FROM item_venda WHERE codvenda = {idsale}")

    sale_items = {}
    for i in item_data:
        sale_items[i[1]] = i[2]  # codproduto : qtde

    return render_template('sales/edit.html',
                           sale=sale,
                           clients=clients,
                           products=products,
                           sale_items=sale_items,
                           active_page='sales')

@app.route('/sales/delete/<int:idsale>')
def sale_delete(idsale):
    controller.db.execute(f"DELETE FROM item_venda WHERE codvenda = {idsale}")
    controller.db.save()

    controller.db.execute(f"DELETE FROM venda WHERE codvenda = {idsale}")
    controller.db.save()

    return redirect('/sales')

@app.route('/products')
def product_list():
    products = controller.search_all(Product())
    return render_template('products/list.html', products=products, active_page='products')

@app.route('/products/create', methods=['GET', 'POST'])
def product_create():
    if request.method == 'POST':
        prod = Product()
        prod.name = request.form['name']
        prod.price = float(request.form['price'])
        controller.insert(prod)
        return redirect('/products')
    return render_template('products/create.html', active_page='products')

@app.route('/products/edit/<int:idproduct>', methods=['GET', 'POST'])
def product_edit(idproduct):
    if request.method == 'POST':
        prod = Product()
        prod.idproduct = idproduct
        prod.name = request.form['name']
        prod.price = float(request.form['price'])
        controller.update(prod, idproduct)
        return redirect('/products')

    result = controller.search(query=f"SELECT * FROM produto WHERE codproduto = {idproduct}")
    if not result:
        return "Produto não encontrado", 404

    data = result[0]
    prod = Product(data[0], data[1], data[2])
    return render_template('products/edit.html', product=prod, active_page='products')

@app.route('/products/delete/<int:idproduct>')
def product_delete(idproduct):
    result = controller.search(query=f"SELECT * FROM produto WHERE codproduto = {idproduct}")
    if not result:
        return "Produto não encontrado", 404
    prod = Product.convert(result[0])
    controller.delete(prod)
    return redirect('/products')


@app.route('/clients')
def client_list():
    clients = controller.search_all(Client())
    return render_template('clients/list.html',
                           clients=clients,
                           active_page='clients')

@app.route('/clients/create', methods=['GET', 'POST'])
def client_create():
    if request.method == 'POST':
        cli = Client()
        cli.name = request.form['name']
        cli.address = request.form['address']
        controller.insert(cli)
        return redirect('/clients')
    return render_template('clients/create.html', active_page='clients')

@app.route('/clients/edit/<int:idclient>', methods=['GET', 'POST'])
def client_edit(idclient):
    if request.method == 'POST':
        cli = Client()
        cli.idclient = idclient
        cli.name = request.form['name']
        cli.address = request.form['address']
        controller.update(cli, idclient)
        return redirect('/clients')

    result = controller.search(query=f"SELECT * FROM cliente WHERE codcliente = {idclient}")
    if not result:
        return "Cliente não encontrado", 404

    cli = Client(result[0][0], result[0][1], result[0][2])
    return render_template('clients/edit.html', client=cli, active_page='clients')

@app.route('/clients/delete/<idclient>')
def client_delete(idclient):
    clis = controller.search(query=("select * from cliente where codcliente = " + str(idclient)))
    cli = Client.convert(clis[0])
    controller.delete(cli)
    return redirect('/clients')

@app.route("/")
def index():
    clients = controller.search_all(Client())
    products = controller.search_all(Product())
    sales = controller.search_all(Sale())
    dashboard_data = {
        "total_clientes": len(clients),
        "total_produtos": len(products),
        "total_vendas": len(sales)
    }
    return render_template('home.html', data=dashboard_data)

if __name__ == '__main__':
    app.run(debug=True)