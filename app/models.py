# models.py

from banjo.models import Model, StringField, IntegerField, FloatField, BooleanField

class TOD(Model):
    statement = StringField()
    truth = BooleanField()
    dare = BooleanField()

    def json_response(self):

        return{
            'id': self.id,
            'statement': self.statement,
            'truth': self.truth,
            'dare': self.dare
        }

    def change_statement(self, new_statement):
        self.statement = new_statement
        self.save()
        