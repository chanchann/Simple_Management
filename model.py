from app import db
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
