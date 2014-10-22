from app import db
from sqlalchemy.dialects.postgresql import JSONB

# Check http://docs.sqlalchemy.org/en/rel_0_8/core/sqlelement.html
# to see what can you use


class Record(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True)
    jsonb = db.Column(JSONB)

    def __init__(self, jsonb):
        self.jsonb = jsonb


class Query():

    def _filter(self, *criterion):
        return Record.query.filter(*criterion)

    def filter(self, *criterion):
        return self._filter(*criterion)

    def filter_by(self, **kwargs):
        criterion = []
        for (k, v) in kwargs.iteritems():
            criterion.append(BinaryExpression(k).like(v))
        return self._filter(*criterion)

    def get(self, id):
        return Record.query.get(id)


class Mangler(object):

    def __init__(self):
        self.query = Query()

    def __getitem__(self, key):
        return BinaryExpression(key)

    def any_(self, key):
        return BinaryExpression(key, type='any')


class BinaryExpression(object):

    def __init__(self, key, type='getitem'):
        self.prefix = ''
        self.suffix = ''
        if type == 'getitem':
            self.__getitem__(key)
        else:
            self._any(key)

    def any_(self, key):
        self.prefix += '[{"' + key + '": '
        self.suffix = '}]' + self.suffix
        return self

    def all_(self, key):
        raise NotImplementedError

    def __getitem__(self, key):
        self.prefix += '{"' + key + '": '
        self.suffix += '}'
        return self

    def __eq__(self, other):
        if isinstance(other, basestring):
            return self.like(other)
        raise TypeError

    def __ne__(self, other):
        raise NotImplementedError

    def like(self, key):
        # Here we create sqlalchemy binaryexpression
        print self.prefix + '"' + key + '"' + self.suffix
        return Record.jsonb.contains(self.prefix + '"' + key +
                                     '"' + self.suffix)
