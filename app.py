from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, FloatField, DateField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import os
# from model import Part,Region,Nation,Customer,Supplier,Orders,Lineite
from config import brand_choice,type_choice,container_choice
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
bootstrap = Bootstrap(app)
moment = Moment(app)
# app.config['SQLALCHEMY_DATABASE_URI'] =\
# 	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:###@localhost/dbhomework'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/tpc-h'
app.config["SQLALCHEMY_COMMENT_ON_TEARDOWN"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'ysy'
app.secret_key = 'ysy'

db = SQLAlchemy(app)

class Part(db.Model):
    __tablename__ = 'PART'
    P_PARTKEY = db.Column(db.Integer, primary_key=True)
    P_NAME = db.Column(db.String(55))
    P_MFGR = db.Column(db.String(25))
    P_BRAND = db.Column(db.String(10))
    P_TYPE = db.Column(db.String(25))
    P_SIZE = db.Column(db.Integer)
    P_CONTAINER = db.Column(db.String(10))
    P_RETAILPRICE = db.Column(db.Float)
    P_COMMENT = db.Column(db.String(23))


class Region(db.Model):
    __tablename__ = 'REGION'
    R_REGIONKEY = db.Column(db.Integer, primary_key=True)
    R_NAME = db.Column(db.String(25))
    R_COMMENT = db.Column(db.String(152))
    PS_SUPPLYCOST = db.Column(db.Float)
    PS_COMMENT = db.Column(db.String(199))


class Nation(db.Model):
    __tablename__ = 'NATION'
    N_NATIONKEY = db.Column(db.Integer, primary_key=True)
    N_NAME = db.Column(db.String(25))
    N_REGIONKEY = db.Column(db.Integer, db.ForeignKey('REGION.R_REGIONKEY'))
    N_COMMENT = db.Column(db.String(152))
    reg = db.relationship("Region", backref="find_name")


class Customer(db.Model):
    __tablename__ = 'CUSTOMER'
    C_CUSTKEY = db.Column(db.Integer, primary_key=True)
    C_NAME = db.Column(db.String(25))
    C_ADDRESS = db.Column(db.String(40))
    C_NATIONKEY = db.Column(db.Integer, db.ForeignKey('NATION.N_NATIONKEY'))
    C_PHONE = db.Column(db.String(16))
    C_ACCTBAL = db.Column(db.Float)
    C_MKTSEGMENT = db.Column(db.String(10))
    C_COMMENT = db.Column(db.String(117))
    NAT = db.relationship("Nation", backref="cfind_name")


class Supplier(db.Model):
    __tablename__ = 'SUPPLIER'
    S_SUPPKEY = db.Column(db.Integer, primary_key=True)
    S_NAME = db.Column(db.String(25))
    S_ADDRESS = db.Column(db.String(40))
    S_NATIONKEY = db.Column(db.Integer, db.ForeignKey('NATION.N_NATIONKEY'))
    S_PHONE = db.Column(db.String(15))
    S_ACCTBAL = db.Column(db.Float)
    S_COMMENT = db.Column(db.String(101))
    nati = db.relationship("Nation", backref="sfind_name")


class Partsupp(db.Model):
    __tablename__ = 'PARTSUPP'
    PS_PARTKEY = db.Column(db.Integer, db.ForeignKey('PART.P_PARTKEY'), primary_key=True)
    PS_SUPPKEY = db.Column(db.Integer, db.ForeignKey('SUPPLIER.S_SUPPKEY'), primary_key=True)
    PS_AVAILQTY = db.Column(db.Integer)
    PS_SUPPLYCOST = db.Column(db.Float)
    PS_COMMENT = db.Column(db.String(199))


class Orders(db.Model):
    __tablename__ = 'ORDERS'
    O_ORDERKEY = db.Column(db.Integer, primary_key=True)
    O_CUSTKEY = db.Column(db.Integer, db.ForeignKey('CUSTOMER.C_CUSTKEY'))
    O_ORDERSTATUS = db.Column(db.String(1))
    O_TOTALPRICE = db.Column(db.Float)
    O_ORDERDATE = db.Column(db.DateTime)
    O_ORDERPRIORITY = db.Column(db.String(15))
    O_CLERK = db.Column(db.String(15))
    O_SHIPPRIORITY = db.Column(db.Integer)
    O_COMMENT = db.Column(db.String(79))


class Lineitem(db.Model):
    L_ORDERKEY = db.Column(db.Integer, db.ForeignKey('ORDERS.O_ORDERKEY'), primary_key=True)
    L_PARTKEY = db.Column(db.Integer, db.ForeignKey('PARTSUPP.PS_PARTKEY'), db.ForeignKey('PARTSUPP.PS_SUPPKEY'))
    L_SUPPKEY = db.Column(db.Integer, db.ForeignKey('PARTSUPP.PS_PARTKEY'), db.ForeignKey('PARTSUPP.PS_SUPPKEY'))
    L_LINENUMBER = db.Column(db.Integer, primary_key=True)
    L_QUANTITY = db.Column(db.Float)
    L_EXTENDEDPRICE = db.Column(db.Float)
    L_DISCOUNT = db.Column(db.Float)
    L_TAX = db.Column(db.Float)
    L_RETURNFLAG = db.Column(db.String(1))
    L_LINESTATUS = db.Column(db.String(1))
    L_SHIPDATE = db.Column(db.DateTime)
    L_COMMITDATE = db.Column(db.DateTime)
    L_RECEIPTDATE = db.Column(db.DateTime)
    L_SHIPINSTRUCT = db.Column(db.String(25))
    L_SHIPMODE = db.Column(db.String(25))
    L_COMMENT = db.Column(db.String(44))

db.create_all()

class Select(SelectField):
    def pre_validate(self, form):
        pass


class EditFormPart(FlaskForm):
    part_key = IntegerField('零件编号', validators=[])
    name = StringField('零件名称', validators=[])
    MFGR = StringField('MFGR', validators=[])
    brand = SelectField('商标', validators=[], render_kw={'class': 'form-control'},
                        choices = brand_choice,
                        default='派大星', coerce=str)
    type = SelectField('型号', validators=[], render_kw={'class': 'form-control'},
                        choices = type_choice, default='齿轮零件', coerce=str)
    size = IntegerField('尺寸', validators=[])
    container = SelectField('包装容器', validators=[], render_kw={'class': 'form-control'},
                            choices = container_choice,
                            default='一次性包装', coerce=str)
    retailprice = FloatField('零售价', validators=[])
    comment = StringField('备注', validators=[])
    submit = SubmitField('提交')


class EditFormRegion(FlaskForm):
    regionkey = IntegerField('地区编号', validators=[])
    regionname = StringField('地区名称', validators=[])
    r_comment = StringField('备注', validators=[])
    supplycost = FloatField('供应价格', validators=[])
    ps_comment = StringField('备注(供应)', validators=[])
    submit = SubmitField('提交')


class EditFormNation(FlaskForm):
    nationkey = IntegerField('国家编号', validators=[])
    nationname = StringField('国家名称', validators=[])
    '''region = []
    regions = Region.query.order_by(Region.R_NAME).all()
    for i in regions:
        region.append((i.R_REGIONKEY, i.R_NAME))
    n_regionkey = SelectField('所属地区', validators=[], render_kw={'class': 'form-control'}, coerce=int)'''
    n_regionkey = Select('所属地区', validators=[], render_kw={'class': 'form-control'}, choices=[(0, '无')],
                              coerce=int)
    comment = StringField('备注', validators=[])
    submit = SubmitField('提交')


def UpdateFormNation():
    EditFormNation.nationkey = IntegerField('国家编码', validators=[])
    EditFormNation.nationname = StringField('国家名称', validators=[])
    region = []
    regions = Region.query.order_by(Region.R_NAME).all()
    for i in regions:
        region.append((i.R_REGIONKEY, '(%d)'%i.R_REGIONKEY + i.R_NAME))
    EditFormNation.n_regionkey = Select('所属地区', validators=[], render_kw={'class': 'form-control'},
                                           choices=region, coerce=int)
    EditFormNation.n_regionkey.choices += region
    EditFormNation.comment = StringField('备注', validators=[])
    EditFormNation.submit = SubmitField('提交')
    return


class EditFormCustomer(FlaskForm):
    custkey = IntegerField('顾客编号', validators=[])
    name = StringField('顾客名称', validators=[])
    address = StringField('顾客地址', validators=[])
    nation = []
    nations = Nation.query.all()
    for i in nations:
        nation.append((i.N_NATIONKEY, i.N_NAME))
    c_nationkey = Select('所属国家', validators=[], render_kw={'class':'form-control'}, choices=nation, coerce=int)
    phone = StringField('联系电话', validators=[])
    acctbal = FloatField('可用余额', validators=[])
    mktsegment = StringField('市场', validators=[])
    comment = StringField('备注', validators=[])
    submit = SubmitField('提交')


def UpdateFormCustomer():
    EditFormCustomer.custkey = IntegerField('顾客编号', validators=[])
    EditFormCustomer.name = StringField('顾客名称', validators=[])
    EditFormCustomer.address = StringField('顾客地址', validators=[])
    nation = []
    nations = Nation.query.all()
    for i in nations:
        nation.append((i.N_NATIONKEY, i.N_NAME))
    EditFormCustomer.c_nationkey = Select('所属国家', validators=[], render_kw={'class': 'form-control'}, choices=nation, coerce=int)
    EditFormCustomer.phone = StringField('联系电话', validators=[])
    EditFormCustomer.acctbal = FloatField('可用余额', validators=[])
    EditFormCustomer.mktsegment = StringField('市场', validators=[])
    EditFormCustomer.comment = StringField('备注', validators=[])
    EditFormCustomer.submit = SubmitField('提交')
    return


class EditFormSupplier(FlaskForm):
    suppkey = IntegerField('供应商编码', validators=[])
    name = StringField('供应商名称', validators=[])
    address = StringField('供应商地址', validators=[])
    nation = []
    nations = Nation.query.all()
    for i in nations:
        nation.append((i.N_NATIONKEY, '(%d)'%i.N_NATIONKEY + i.N_NAME))
    nationkey = Select('所属国家', validators=[], render_kw={'class': 'form-control'}, choices=nation, coerce=int)
    phone = StringField('电话', validators=[])
    acctbal = FloatField('账户余额', validators=[])
    comment = StringField('备注', validators=[])
    submit = SubmitField('提交')


def UpdateFormSupplier():
    EditFormSupplier.suppkey = IntegerField('供应商编码', validators=[])
    EditFormSupplier.name = StringField('供应商名称', validators=[])
    EditFormSupplier.address = StringField('供应商地址', validators=[])
    nation = []
    nations = Nation.query.all()
    for i in nations:
        nation.append((i.N_NATIONKEY, '(%d)'%i.N_NATIONKEY + i.N_NAME))
    EditFormSupplier.nationkey = Select('所属国家', validators=[], render_kw={'class': 'form-control'}, choices=nation, coerce=int)
    EditFormSupplier.phone = StringField('电话', validators=[])
    EditFormSupplier.acctbal = FloatField('账户余额', validators=[])
    EditFormSupplier.comment = StringField('备注', validators=[])
    EditFormSupplier.submit = SubmitField('提交')
    return


class EditFormPartsupp(FlaskForm):
    part = []
    parts = Part.query.all()
    for i in parts:
        part.append((i.P_PARTKEY, '(%d)'%i.P_PARTKEY + i.P_NAME))
    partkey = Select('零件编号', validators=[], render_kw={'class':'form-control'}, choices=part, coerce=int)
    supplier = []
    suppliers = Supplier.query.all()
    for i in suppliers:
        supplier.append((i.S_SUPPKEY, '(%d)'%i.S_SUPPKEY + i.S_NAME))
    suppkey = Select('供应商编号', validators=[], render_kw={'class':'form-control'}, choices=supplier, coerce=int)
    availqty = IntegerField('供应数量', validators=[])
    supplycost = FloatField('供应价格', validators=[])
    comment = StringField('备注', validators=[])
    submit = SubmitField('提交')


def UpdateFormPartsupp():
    part = []
    parts = Part.query.all()
    for i in parts:
        part.append((i.P_PARTKEY, '(%d)'%i.P_PARTKEY + i.P_NAME))
    EditFormPartsupp.partkey = Select('零件编号', validators=[], render_kw={'class': 'form-control'}, choices=part, coerce=int)
    supplier = []
    suppliers = Supplier.query.all()
    for i in suppliers:
        supplier.append((i.S_SUPPKEY, '(%d)'%i.S_SUPPKEY + i.S_NAME))
    EditFormPartsupp.suppkey = Select('供应商编号', validators=[], render_kw={'class': 'form-control'}, choices=supplier, coerce=int)
    EditFormPartsupp.availqty = IntegerField('供应数量', validators=[])
    EditFormPartsupp.supplycost = FloatField('供应价格', validators=[])
    EditFormPartsupp.comment = StringField('备注', validators=[])
    EditFormPartsupp.submit = SubmitField('提交')


class EditFormOrders(FlaskForm):
    orderkey = IntegerField('订单编号', validators=[])
    customer = []
    customers = Customer.query.all()
    for i in customers:
        customer.append((i.C_CUSTKEY, '(%d)'%i.C_CUSTKEY + i.C_NAME))
    custkey = SelectField('顾客编号', validators=[], render_kw={'class':'form-control'}, choices=customer, coerce=int)
    orderstatus = Select('订单状态', validators=[],
                         render_kw={'class':'form-control'},
                         choices={(1, "已送达"), (2, '运输中'), (3, "未送出")}, default=0, coerce=int)
    '''totalprice = FloatField('订单金额', validators=[])'''
    orderdate = DateField('订单日期', default='', render_kw={'id':'date'}, format='%Y-%m-%d')
    orderpriority = StringField('优先级', validators=[])
    clerk = StringField('制单员', validators=[])
    shippriority = IntegerField('运输优先级', validators=[])
    comment = StringField('备注', validators=[])
    submit = SubmitField('提交')


def UpdateFormOrders():
    EditFormOrders.orderkey = IntegerField('订单编号', validators=[])
    customer = []
    customers = Customer.query.all()
    for i in customers:
        customer.append((i.C_CUSTKEY, '(%d)'%i.C_CUSTKEY + i.C_NAME))
    EditFormOrders.custkey = Select('顾客编号', validators=[], render_kw={'class': 'form-control'}, choices=customer, coerce=int)
    EditFormOrders.orderstatus = Select('订单状态', validators=[],
                                        render_kw={'class':'form-control'},
                                        choices={(1, "已送达"), (2, '运输中'), (3, "未送出")}, default=0, coerce=int)
    '''EditFormOrders.totalprice = FloatField('订单金额', validators=[])'''
    EditFormOrders.orderdate = DateField('订单日期', default='', render_kw={'id':'date'}, format='%Y-%m-%d')
    EditFormOrders.orderpriority = StringField('优先级', validators=[])
    EditFormOrders.clerk = StringField('制单员', validators=[])
    EditFormOrders.shippriority = IntegerField('运输优先级', validators=[])
    EditFormOrders.comment = StringField('备注', validators=[])
    EditFormOrders.submit = SubmitField('提交')


class EditFormLineitem(FlaskForm):
    order = []
    orders = Orders.query.all()
    for i in orders:
        order.append((i.O_ORDERKEY, i.O_ORDERKEY))
    orderkey = Select('订单号', validators=[], render_kw={'class': 'form-control'}, choices=order, coerce=int)
    part = []
    parts = Part.query.all()
    for i in parts:
        part.append((i.P_PARTKEY, '(%d)'%i.P_PARTKEY + i.P_NAME))
    partkey = Select('零件', validators=[], render_kw={'class': 'form-control'}, choices=part, coerce=int)
    supplier = []
    suppliers = Supplier.query.all()
    for i in suppliers:
        supplier.append((i.S_SUPPKEY, '(%d)'%i.S_SUPPKEY + i.S_NAME))
    suppkey = Select('供应商', validators=[], render_kw={'class': 'form-control'}, choices=supplier, coerce=int)
    linenumber = IntegerField('明细编号', validators=[])
    quantity = FloatField('数量', validators=[])
    '''extendedprice = FloatField('总金额', validators=[])'''
    discount = FloatField('折扣', validators=[])
    tax = FloatField('税', validators=[])
    returnflag = StringField('是否退货', validators=[])
    linestatus = Select('订单明细状态', validators=[],
                        render_kw={'class':'form-control'},
                        choices={(1, "已送达"), (2, '运输中'), (3, "未送出")}, default=0, coerce=int)
    shipdate = DateField('运输日期', default='', validators=[], render_kw={'id':'date'}, format='%Y-%m-%d')
    commitdate = DateField('交付日期', default='', validators=[], render_kw={'id':'date1'}, format='%Y-%m-%d')
    receiptdate = DateField('收获日期', default='', validators=[], render_kw={'id':'date1'}, format='%Y-%m-%d')
    shipinstruct = StringField('运输单位', validators=[])
    shipmode = StringField('运送方式', validators=[])
    comment = StringField('备注', validators=[])
    submit = SubmitField('提交')


def UpdateFormLineitem():
    order = []
    orders = Orders.query.all()
    for i in orders:
        order.append((i.O_ORDERKEY, i.O_ORDERKEY))
    EditFormLineitem.orderkey = Select('订单号', validators=[], render_kw={'class': 'form-control'}, choices=order, coerce=int)
    part = []
    parts = Part.query.all()
    for i in parts:
        part.append((i.P_PARTKEY, '(%d)'%i.P_PARTKEY + i.P_NAME))
    EditFormLineitem.partkey = Select('零件编号', validators=[], render_kw={'class': 'form-control'}, choices=part, coerce=int)
    supplier = []
    suppliers = Supplier.query.all()
    for i in suppliers:
        supplier.append((i.S_SUPPKEY, '(%d)'%i.S_SUPPKEY + i.S_NAME))
    EditFormLineitem.suppkey = Select('供应商编号', validators=[], render_kw={'class': 'form-control'}, choices=supplier, coerce=int)
    EditFormLineitem.linenumber = IntegerField('明细编号', validators=[])
    EditFormLineitem.quantity = FloatField('数量', validators=[])
    '''EditFormLineitem.extendedprice = FloatField('总金额', validators=[])'''
    EditFormLineitem.discount = FloatField('折扣', validators=[])
    EditFormLineitem.tax = FloatField('税', validators=[])
    EditFormLineitem.returnflag = StringField('是否退货', validators=[])
    EditFormLineitem.linestatus = Select('订单明细状态', validators=[],
                                        render_kw={'class':'form-control'},
                                        choices={(1, "已送达"), (2, '运输中'), (3, "未送出")}, default=0, coerce=int)
    EditFormLineitem.shipdate = DateField('运输日期', default='', validators=[], render_kw={'id':'date'}, format='%Y-%m-%d')
    EditFormLineitem.commitdate = DateField('交付日期', default='', validators=[], render_kw={'id':'date1'}, format='%Y-%m-%d')
    EditFormLineitem.receiptdate = DateField('收货日期', default='', validators=[], render_kw={'id':'date2'}, format='%Y-%m-%d')
    EditFormLineitem.shipinstruct = StringField('运输单位', validators=[])
    EditFormLineitem.shipmode = StringField('运送方式', validators=[])
    EditFormLineitem.comment = StringField('备注', validators=[])
    EditFormLineitem.submit = SubmitField('提交')


class SearchForm(FlaskForm):
    part_key = IntegerField('信息', validators=[])
    submit = SubmitField('搜索')


class SearchFormforRegion(FlaskForm):
    regionkey = IntegerField('信息', validators=[])
    submit = SubmitField('搜索')


class SearchFormforNation(FlaskForm):
    nationkey = IntegerField('信息', validators=[])
    submit = SubmitField('搜索')


class SearchFormforCustomer(FlaskForm):
    c_custkey = IntegerField('信息', validators=[])
    submit = SubmitField('搜索')


class SearchFormforSupplier(FlaskForm):
    suppkey = IntegerField('信息', validators=[])
    submit = SubmitField('搜索')


class SearchFormforPartsupp(FlaskForm):
    partkey = IntegerField('零件信息', validators=[])
    suppkey = IntegerField('供应商信息', validators=[])
    submit = SubmitField('搜索')


class SearchFormforOrders(FlaskForm):
    orderkey = IntegerField('订单信息', validators=[])
    submit = SubmitField('搜索')


class SearchFormforLineitem(FlaskForm):
    orderkey = IntegerField('订单信息', validators=[])
    linenumber = IntegerField('明细编号信息', validators=[])
    submit = SubmitField('搜索')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        parts = Part.query.filter_by(P_PARTKEY=form.part_key.data).all()
    else:
        parts = Part.query.all()
    return render_template('part.html', title_name='welcome', parts=parts, form=form)


@app.route('/add_part', methods=['GET', 'POST'])
def add_part():
    form = EditFormPart()
    if form.validate_on_submit():
        try:
            part = Part(P_PARTKEY=form.part_key.data,
                        P_NAME=form.name.data, P_MFGR=form.MFGR.data, P_BRAND=form.brand.data,
                        P_TYPE=form.type.data, P_SIZE=form.size.data, P_CONTAINER=form.container.data,
                        P_RETAILPRICE=form.retailprice.data, P_COMMENT=form.comment.data)
            db.session.add(part)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
            return render_template('edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_part/<int:id>', methods=['GET', 'POST'])
def delete_part(id):
    part = Part.query.get(id)
    if part:
        try:
            db.session.delete(part)
            db.session.commit()
            flash("删除成功")
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
    else:
        flash("无零件记录")
    print(url_for('index'))
    return redirect(url_for('index'))


@app.route('/edit_part/<int:id>', methods=['GET', 'POST'])
def edit_part(id):
    part = Part.query.get(id)
    form = EditFormPart(part_key=part.P_PARTKEY, name=part.P_NAME, MFGR=part.P_MFGR,
                        brand=part.P_BRAND, type=part.P_TYPE, size=part.P_SIZE,
                        container=part.P_CONTAINER, retailprice=part.P_RETAILPRICE,
                        comment=part.P_COMMENT)
    if form.validate_on_submit():
        part.P_PARTKEY = form.part_key.data
        part.P_NAME = form.name.data
        part.P_MFGR = form.MFGR.data
        part.P_BRAND = form.brand.data
        part.P_TYPE = form.type.data
        part.P_SIZE = form.size.data
        part.P_CONTAINER = form.container.data
        part.P_RETAILPRICE = form.retailprice.data
        part.P_COMMENT = form.comment.data

        db.session.commit()
        flash("修改成功")
        return redirect(url_for('index'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/region', methods=['GET', 'POST'])
def region():
    form = SearchFormforRegion()
    if form.validate_on_submit():
        regions = Region.query.filter_by(R_REGIONKEY=form.regionkey.data).all()
    else:
        regions = Region.query.all()
    return render_template('region.html', title_name='地区', regions=regions, form=form)


@app.route('/add_region', methods=['GET', 'POST'])
def add_region():
    form = EditFormRegion()
    if form.validate_on_submit():
        try:
            region = Region(R_REGIONKEY=form.regionkey.data,
                        R_NAME=form.regionname.data, R_COMMENT=form.r_comment.data, PS_SUPPLYCOST=form.supplycost.data,
                        PS_COMMENT=form.ps_comment.data)
            db.session.add(region)
            db.session.commit()
            return redirect(url_for('region'))
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
            return render_template(u'edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/edit_region/<int:id>', methods=['GET', 'POST'])
def edit_region(id):
    region = Region.query.get(id)
    form = EditFormRegion(regionkey=region.R_REGIONKEY, regionname=region.R_NAME,
                          r_comment=region.R_COMMENT, supplycost=region.PS_SUPPLYCOST,
                          ps_comment=region.PS_COMMENT)
    if form.validate_on_submit():
        region.R_REGIONKEY = form.regionkey.data
        region.R_NAME = form.regionname.data
        region.R_COMMENT = form.r_comment.data
        region.PS_SUPPLYCOST = form.supplycost.data
        region.PS_COMMENT = form.ps_comment.data

        db.session.commit()
        flash("修改成功")
        return redirect(url_for('region'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_region/<int:id>', methods=['GET', 'POST'])
def delete_region(id):
    region = Region.query.get(id)
    if region:
        try:
            db.session.delete(region)
            db.session.commit()
            flash("删除成功")
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
    else:
        flash("无地区记录")
    print(url_for('region'))
    return redirect(url_for('region'))


@app.route('/nation', methods=['GET', 'POST'])
def nation():
    form = SearchFormforNation()
    if form.validate_on_submit():
        nations = Nation.query.filter_by(N_NATIONKEY=form.nationkey.data).all()
    else:
        nations = Nation.query.all()
    return render_template('nation.html', title_name='国家', nations=nations, Region=Region, form=form)


@app.route('/add_nation', methods=['GET', 'POST'])
def add_nation():
    form = EditFormNation()
    choices = [(a.R_REGIONKEY, '(%d)'%a.R_REGIONKEY + a.R_NAME) for a in Region.query.all()]
    form.n_regionkey.choices += choices
    if form.validate_on_submit():
        try:
            nation = Nation(N_NATIONKEY=form.nationkey.data, N_NAME=form.nationname.data,
                            N_REGIONKEY=form.n_regionkey.data, N_COMMENT=form.comment.data)
            db.session.add(nation)
            db.session.commit()
            return redirect(url_for('nation'))
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
            return render_template('edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/edit_nation/<int:id>', methods=['GET', 'POST'])
def edit_nation(id):
    nation = Nation.query.get(id)
    form = EditFormNation(nationkey=nation.N_NATIONKEY, nationname=nation.N_NAME,
                            n_regionkey=nation.N_REGIONKEY, comment=nation.N_COMMENT)
    if form.validate_on_submit():
        nation.N_NATIONKEY = form.nationkey.data
        nation.N_NAME = form.nationname.data
        nation.N_REGIONKEY = form.n_regionkey.data
        nation.N_COMMENT = form.comment.data

        db.session.commit()
        flash("修改成功")
        return redirect(url_for('nation'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_nation/<int:id>', methods=['GET', 'POST'])
def delete_nation(id):
    nation = Nation.query.get(id)
    if nation:
        try:
            db.session.delete(nation)
            db.session.commit()
            flash("删除成功")
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
    else:
        flash("无国家记录")
    print(url_for('nation'))
    return redirect(url_for('nation'))


@app.route('/customer', methods=['GET', 'POST'])
def customer():
    form = SearchFormforCustomer()
    UpdateFormCustomer()
    if form.validate_on_submit():
        customers = Customer.query.filter_by(C_CUSTKEY=form.c_custkey.data).all()
    else:
        customers = Customer.query.all()
    return render_template('customer.html', title_name='顾客', customers=customers, Nation=Nation, form=form)


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    form = EditFormCustomer()
    if form.validate_on_submit():
        try:
            customer = Customer(C_CUSTKEY=form.custkey.data, C_NAME=form.name.data,
                                C_ADDRESS=form.address.data, C_NATIONKEY=form.c_nationkey.data,
                                C_PHONE=form.phone.data, C_ACCTBAL=form.acctbal.data,
                                C_MKTSEGMENT=form.mktsegment.data, C_COMMENT=form.comment.data)
            for i in form.phone.data:
                if i>'9':
                    flash("不能输入字母")
                    return render_template('edit_part.html', form=form)
                if i<'0':
                    flash("不能输入字母")
                    return render_template('edit_part.html', form=form)
            if (len(form.phone.data) != 11):
                flash("非法号码")
                return render_template('edit_part.html', form=form)
            db.session.add(customer)
            db.session.commit()
            return redirect(url_for('customer'))
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
            return render_template('edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = Customer.query.get(id)
    form = EditFormCustomer(custkey=customer.C_CUSTKEY, name=customer.C_NAME, address=customer.C_ADDRESS,
                            c_nationkey=customer.C_NATIONKEY, phone=customer.C_PHONE, acctbal=customer.C_ACCTBAL,
                            mktsegment=customer.C_MKTSEGMENT, comment=customer.C_COMMENT)
    if form.validate_on_submit():
        customer.C_CUSTKEY = form.custkey.data
        customer.C_NAME = form.name.data
        customer.C_ADDRESS = form.address.data
        customer.C_NATIONKEY = form.c_nationkey.data
        customer.C_PHONE = form.phone.data
        customer.C_ACCTBAL = form.acctbal.data
        customer.C_MKTSEGMENT = form.mktsegment.data
        customer.C_COMMENT = form.comment.data

        db.session.commit()
        flash("修改成功")
        return redirect(url_for('customer'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_customer/<int:id>', methods=['GET', 'POST'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if customer:
        try:
            db.session.delete(customer)
            db.session.commit()
            flash("删除成功")
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
    else:
        flash("无顾客记录")
    print(url_for('customer'))
    return redirect(url_for('customer'))


@app.route('/supplier', methods=['GET', 'POST'])
def supplier():
    form = SearchFormforSupplier()
    UpdateFormSupplier()
    if form.validate_on_submit():
        suppliers = Supplier.query.filter_by(S_SUPPKEY=form.suppkey.data).all()
    else:
        suppliers = Supplier.query.all()
    return render_template('supplier.html', title_name='顾客', suppliers=suppliers, Nation=Nation, form=form)


@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    form = EditFormSupplier()
    if form.validate_on_submit():
        try:
            supplier = Supplier(S_SUPPKEY=form.suppkey.data, S_NAME=form.name.data,
                                S_ADDRESS=form.address.data, S_NATIONKEY=form.nationkey.data,
                                S_PHONE=form.phone.data, S_ACCTBAL=form.acctbal.data,
                                S_COMMENT=form.comment.data)
            for i in form.phone.data:
                if i>'9':
                    flash("不能输入字母")
                    return render_template('edit_part.html', form=form)
                if i<'0':
                    flash("不能输入字母")
                    return render_template('edit_part.html', form=form)
            if (len(form.phone.data) != 11):
                flash("非法号码")
                return render_template('edit_part.html', form=form)
            db.session.add(supplier)
            db.session.commit()
            return redirect(url_for('supplier'))
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
            return render_template('edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/edit_supplier/<int:id>', methods=['GET', 'POST'])
def edit_supplier(id):
    supplier = Supplier.query.get(id)
    form = EditFormSupplier(suppkey=supplier.S_SUPPKEY, name=supplier.S_NAME, address=supplier.S_ADDRESS,
                            nationkey=supplier.S_NATIONKEY, phone=supplier.S_PHONE, acctbal=supplier.S_ACCTBAL,
                            comment=supplier.S_COMMENT)
    if form.validate_on_submit():
        supplier.S_SUPPKEY = form.suppkey.data
        supplier.S_NAME = form.name.data
        supplier.S_ADDRESS = form.address.data
        supplier.S_NATIONKEY = form.nationkey.data
        supplier.S_PHONE = form.phone.data
        supplier.S_ACCTBAL = form.acctbal.data
        supplier.S_COMMENT = form.comment.data

        db.session.commit()
        flash("修改成功")
        return redirect(url_for('supplier'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_supplier/<int:id>', methods=['GET', 'POST'])
def delete_supplier(id):
    supplier = Supplier.query.get(id)
    if supplier:
        try:
            db.session.delete(supplier)
            db.session.commit()
            flash("删除成功")
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
    else:
        flash("无供应商记录")
    print(url_for('supplier'))
    return redirect(url_for('supplier'))


@app.route('/partsupp', methods=['GET', 'POST'])
def partsupp():
    form = SearchFormforPartsupp()
    UpdateFormPartsupp()
    if form.validate_on_submit():
        partsupps = Partsupp.query.filter_by(PS_PARTKEY=form.partkey.data, PS_SUPPKEY=form.suppkey.data).all()
    else:
        partsupps = Partsupp.query.all()
    return render_template('partsupp.html', title_name='零件供应', partsupps=partsupps,
                           Part=Part, Supplier=Supplier, form=form)


@app.route('/add_partsupp', methods=['GET', 'POST'])
def add_partsupp():
    form = EditFormPartsupp()
    if form.validate_on_submit():
        try:
            partsupp = Partsupp(PS_PARTKEY=form.partkey.data,PS_SUPPKEY=form.suppkey.data,
                                PS_AVAILQTY=form.availqty.data, PS_SUPPLYCOST=form.supplycost.data,
                                PS_COMMENT=form.comment.data)
            db.session.add(partsupp)
            db.session.commit()
            return redirect(url_for('partsupp'))
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
            return render_template(u'edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/edit_partsupp/<int:id1>/<int:id2>', methods=['GET', 'POST'])
def edit_partsupp(id1, id2):
    partsupp = Partsupp.query.filter_by(PS_SUPPKEY=id2, PS_PARTKEY=id1).first()
    form = EditFormPartsupp(partkey=partsupp.PS_PARTKEY, suppkey=partsupp.PS_SUPPKEY, availqty=partsupp.PS_AVAILQTY,
                            supplycost=partsupp.PS_SUPPLYCOST, comment=partsupp.PS_COMMENT)
    if form.validate_on_submit():
        partsupp.PS_PARTKEY = form.partkey.data
        partsupp.PS_SUPPKEY = form.suppkey.data
        partsupp.PS_AVAILQTY = form.availqty.data
        partsupp.PS_SUPPLYCOST = form.supplycost.data
        partsupp.PS_COMMENT = form.comment.data

        db.session.commit()
        flash("修改成功")
        return redirect(url_for('partsupp'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_partsupp/<int:id1>/<int:id2>', methods=['GET', 'POST'])
def delete_partsupp(id1, id2):
    partsupp = Partsupp.query.filter_by(PS_SUPPKEY=id2, PS_PARTKEY=id1).first()
    if Partsupp:
        try:
            db.session.delete(partsupp)
            db.session.commit()
            flash("删除成功")
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
    else:
        flash("无零件供应记录")
    print(url_for('partsupp'))
    return redirect(url_for('partsupp'))


@app.route('/order', methods=['GET', 'POST'])
def order():
    form = SearchFormforOrders()
    UpdateFormOrders()
    if form.validate_on_submit():
        orders = Orders.query.filter_by(O_ORDERKEY=form.orderkey.data).all()
    else:
        orders = Orders.query.all()
    return render_template('order.html', title_name='订单', orders=orders, Customer=Customer, form=form)


@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    form = EditFormOrders()
    if form.validate_on_submit():
        try:
            order = Orders(O_ORDERKEY=form.orderkey.data, O_CUSTKEY=form.custkey.data, O_ORDERSTATUS=form.orderstatus.data,
                           O_TOTALPRICE=0, O_ORDERDATE=form.orderdate.data.strftime('%Y-%m-%d'), O_ORDERPRIORITY=form.orderpriority.data,
                           O_CLERK=form.clerk.data, O_SHIPPRIORITY=form.shippriority.data, O_COMMENT=form.comment.data)
            '''totals = Lineitem.query.filter_by(L_ORDERKEY=order.O_ORDERKEY).all()
            for i in totals:
                total = i.L_EXTENDEDPRICE
                order.O_TOTALPRICE += total'''
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('order'))
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
            return render_template('edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_order/<int:id>', methods=['GET', 'POST'])
def delete_order(id):
    order = Orders.query.get(id)
    if order:
        try:
            db.session.delete(order)
            db.session.commit()
            flash("删除成功")
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
    else:
        flash("无零件记录")
    print(url_for('order'))
    return redirect(url_for('order'))


@app.route('/edit_order/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    order = Orders.query.get(id)
    form = EditFormPart(orderkey=order.O_ORDERKEY, custkey=order.O_CUSTKEY, orderstatus=order.O_ORDERSTATUS,
                        orderdate=order.O_ORDERDATE, orderpriority=order.O_ORDERPRIORITY, clerk=order.O_CLERK, shippriority=order.O_SHIPPRIORITY,
                        comment=order.O_COMMENT)
    if form.validate_on_submit():
        order.O_ORDERKEY = form.orderkey.data
        order.O_CUSTKEY = form.custkey.data
        order.O_ORDERSTATUS = form.orderstatus.data
        order.O_ORDERDATE = form.orderdate.data.strftime('%Y-%m-%d')
        order.O_ORDERPRIORITY = form.orderpriority.data
        order.O_CLERK = form.clerk.data
        order.O_SHIPPRIORITY = form.shippriority.data
        order.O_COMMENT = form.comment.data
        '''totals = Lineitem.query.filter_by(L_ORDERKEY=order.O_ORDERKEY).all()
        for i in totals:
            total = i.L_EXTENDEDPRICE
            order.O_TOTALPRICE += total'''

        db.session.commit()
        flash("修改成功")
        return redirect(url_for('order'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/lineitem', methods=['GET', 'POST'])
def lineitem():
    form = SearchFormforLineitem()
    UpdateFormLineitem()
    if form.validate_on_submit():
        lineitems = Lineitem.query.filter_by(L_ORDERKEY=form.orderkey.data, L_LINENUMBER=form.linenumber.data).all()
    else:
        lineitems = Lineitem.query.all()
    return render_template('lineitem.html', title_name='零件供应', lineitems=lineitems,
                           Part=Part, Supplier=Supplier, form=form)


@app.route('/add_lineitem', methods=['GET', 'POST'])
def add_lineitem():
    form = EditFormLineitem()
    if form.validate_on_submit():
        try:
            lineitem = Lineitem(L_ORDERKEY=form.orderkey.data, L_PARTKEY=form.partkey.data,
                                L_SUPPKEY=form.suppkey.data, L_LINENUMBER=form.linenumber.data,
                                L_QUANTITY=form.quantity.data,
                                L_EXTENDEDPRICE=form.quantity.data * Part.query.filter_by(P_PARTKEY=form.partkey.data).first().P_RETAILPRICE * form.discount.data,
                                L_DISCOUNT=form.discount.data, L_TAX=form.tax.data,
                                L_RETURNFLAG=form.returnflag.data, L_LINESTATUS=form.linestatus.data,
                                L_SHIPDATE=form.shipdate.data.strftime('%Y-%m-%d'), L_COMMITDATE=form.commitdate.data.strftime('%Y-%m-%d'),
                                L_RECEIPTDATE=form.receiptdate.data.strftime('%Y-%m-%d'), L_SHIPINSTRUCT=form.shipinstruct.data,
                                L_SHIPMODE=form.shipmode.data, L_COMMENT=form.comment.data)
            order = Orders.query.filter_by(O_ORDERKEY=form.orderkey.data).first()
            order.O_TOTALPRICE += lineitem.L_EXTENDEDPRICE

            db.session.add(lineitem)
            db.session.commit()
            return redirect(url_for('lineitem'))
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
            return render_template(u'edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/edit_lineitem/<int:id1>/<int:id2>', methods=['GET', 'POST'])
def edit_lineitem(id1, id2):
    lineitem = Lineitem.query.filter_by(L_ORDERKEY=id1, L_LINENUMBER=id2).first()
    form = EditFormLineitem(orderkey=lineitem.L_ORDERKEY, partkey=lineitem.L_PARTKEY, suppkey=lineitem.L_SUPPKEY,
                            linenumber=lineitem.L_LINENUMBER, quantity=lineitem.L_QUANTITY,
                            discount=lineitem.L_DISCOUNT, tax=lineitem.L_TAX, returnflag=lineitem.L_RETURNFLAG,
                            linestatus=lineitem.L_LINESTATUS, shipdate=lineitem.L_SHIPDATE, commitdate=lineitem.L_COMMITDATE,
                            receiptdate=lineitem.L_RECEIPTDATE, shipinstruct=lineitem.L_SHIPINSTRUCT, shipmode=lineitem.L_SHIPMODE,
                            comment=lineitem.L_COMMENT)
    if form.validate_on_submit():
        order = Orders.query.filter_by(O_ORDERKEY=id1).first()
        order.O_TOTALPRICE -= lineitem.L_EXTENDEDPRICE
        lineitem.L_ORDERKEY = form.orderkey.data
        lineitem.L_PARTKEY = form.partkey.data
        lineitem.L_SUPPKEY = form.suppkey.data
        lineitem.L_LINENUMBER = form.linenumber.data
        lineitem.L_QUANTITY = form.quantity.data
        lineitem.L_EXTENDEDPRICE = form.quantity.data * Part.query.filter_by(P_PARTKEY=form.partkey.data).first().P_RETAILPRICE * form.discount.data
        lineitem.L_DISCOUNT = form.discount.data
        lineitem.L_TAX = form.tax.data
        lineitem.L_RETURNFLAG = form.returnflag.data
        lineitem.L_LINESTATUS = form.linestatus.data
        lineitem.L_SHIPDATE = form.shipdate.data.strftime('%Y-%m-%d')
        lineitem.L_COMMITDATE = form.commitdate.data.strftime('%Y-%m-%d')
        lineitem.L_RECEIPTDATE = form.receiptdate.data.strftime('%Y-%m-%d')
        lineitem.L_SHIPINSTRUCT = form.shipinstruct.data
        lineitem.L_SHIPMODE = form.shipmode.data
        lineitem.L_COMMENT = form.comment.data
        order.O_TOTALPRICE += form.quantity.data * Part.query.filter_by(P_PARTKEY=form.partkey.data).first().P_RETAILPRICE * form.discount.data

        db.session.commit()
        flash("修改成功")
        return redirect(url_for('lineitem'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_lineitem/<int:id1>/<int:id2>', methods=['GET', 'POST'])
def delete_lineitem(id1, id2):
    lineitem = Lineitem.query.filter_by(L_ORDERKEY=id1, L_LINENUMBER=id2).first()
    if Partsupp:
        try:
            db.session.delete(lineitem)
            db.session.commit()
            flash("删除成功")
        except Exception as e:
            print(e)
            flash("操作错误")
            db.session.rollback()
    else:
        flash("无订单明细记录")
    print(url_for('lineitem'))
    return redirect(url_for('lineitem'))


if __name__ == '__main__':
    app.run(debug=True)
