# models.py

from banjo.models import Model, StringField, IntegerField, FloatField, BooleanField

class TOD(Model):
    statement = StringField()
    truth = BooleanField()
    dare = BooleanField()
    must_complete = BooleanField()
    check_complete = BooleanField()
    reject = BooleanField()

    def json_response(self):

        return{
            'id': self.id,
            'statement': self.statement,
            'truth': self.truth,
            'dare': self.dare,
            'must_complete': self.must_complete,
            'check_complete': self.check_complete,
            'reject': self.reject
        }

    def change_statement(self, new_statement):
        self.statement = new_statement
        self.save()

    def change_must_complete(self):
        self.must_complete = True
        self.save()

    def reset_must_complete(self):
        self.must_complete = False
        self.save()

    def change_complete(self):
        self.check_complete = True
        self.save()

    def reset_change_complete(self):
        self.check_complete = False
        self.save()

    def change_reject(self):
        self.reject = True
        self.save()
        
    def reset_change_reject(self):
        self.reject = False
        self.save()