# models.py

from banjo.models import Model, StringField, IntegerField, FloatField, BooleanField

class TOD(Model):
    statement = StringField()
    truth = BooleanField()
    dare = BooleanField()
    check_complete = BooleanField()
    archive = BooleanField()

    def json_response(self):

        return{
            'id': self.id,
            'statement': self.statement,
            'truth': self.truth,
            'dare': self.dare,
            'check_complete': self.check_complete,
            'archive': self.archive
        }

    def change_statement(self, new_statement):
        self.statement = new_statement
        self.save()

    def change_complete(self):
        self.check_complete = True
        self.save()

    def change_archive(self):
        self.archive = True
        self.save()
        