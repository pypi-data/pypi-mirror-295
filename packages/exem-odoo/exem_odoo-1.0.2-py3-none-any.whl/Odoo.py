import base64
import json
import os
import re
import xmlrpc.client


class Odoo:
    URL = "url"
    DB_NAME = "dbname"
    USER = "user"
    PASSWORD = "pwd"

    def __init__(self):
        self.odoo = None
        self.uid = None
        self.url = ""
        self.dbname = ""
        self.user = ""
        self.pwd = ""
        self.date_format = "%Y-%m-%d %H:%M:%S"
        self.max_ids_count = 1000

    def connect(self, credentials):
        self.url = credentials[self.URL]
        self.dbname = credentials[self.DB_NAME]
        self.user = credentials[self.USER]
        self.pwd = credentials[self.PASSWORD]
        self.odoo = xmlrpc.client.ServerProxy(self.url + '/xmlrpc/2/common', verbose=False, use_datetime=True)
        self.uid = self.odoo.login(self.dbname, self.user, self.pwd)
        self.odoo = xmlrpc.client.ServerProxy(self.url + '/xmlrpc/2/object', verbose=False, use_datetime=True)

    def execute(self, module, method, ids=None, data=None, **args):
        parameters = [self.dbname, self.uid, self.pwd, module, method]

        if ids is not None:
            parameters.append(ids)
        if data is not None:
            parameters.append(data)
        if args:
            parameters.append(**args)

        return self.odoo.execute(*parameters)

    def get_ids(self, module, filters=None, **args):
        return self.execute(module, 'search', data=filters if filters else [], **args)

    def get_ids_count(self, module, filters=None):
        return self.execute(module, 'search_count', data=filters if filters else [])

    def get_fields(self, module, ids, fields=None, **args):
        return self.execute(module, 'read', ids=ids, data=fields if fields else [], **args)

    def get_fields_by_conditions(self, module, filters=None, fields=None, **args):
        ids = self.get_ids(module, filters if filters else [], **args)
        return self.get_fields(module, ids, fields if fields else [])

    def get_fields_name(self, module):
        return self.execute(module, 'fields_get')

    def set_fields(self, module, ids, values):
        return self.execute(module, 'write', ids=ids, data=values)

    def create(self, module, values):
        return self.execute(module, 'create', data=values)

    def delete_field(self, module, ids):
        return self.execute(module, 'unlink', ids=ids)

    def create_attachment(self, attachment):
        return self.execute('ir.attachment', 'create', data=attachment)

    def create_attachment_file(self, module, obj_id, file_name, file_path):
        file_data = open(file_path, 'rb').read()

        base64_bytes = base64.b64encode(file_data)
        base64_string = base64_bytes.decode('UTF-8')

        _, file_extension = os.path.splitext(file_name)

        return self.create_attachment(self.Attachment(
            name=file_name,
            res_id=obj_id,
            res_model=module,
            datas=json.dumps(base64_string),
            datas_fname=file_name,
            mimetype="application/" + file_extension[1:]
        ))

    class Attachment:
        NAME = "name"
        TYPE = "type"
        DATAS_FNAME = "datas_fname"
        RES_ID = "res_id"
        RES_MODEL = "res_model"
        DATAS = "datas"
        MIMETYPE = "mimetype"

        DEFAULT_DATATYPE = "binary"
        DEFAULT_MIMETYPE = "application/pdf"

        def __init__(self, name, datas, datas_fname, res_model, res_id, data_type=DEFAULT_DATATYPE,
                     mimetype=DEFAULT_MIMETYPE):
            self.name = name
            self.datas = datas
            self.datas_fname = datas_fname
            self.res_model = res_model
            self.res_id = res_id
            self.type = data_type
            self.mimetype = mimetype

        def __str__(self):
            return {
                self.NAME: self.name,
                self.TYPE: self.type,
                self.DATAS_FNAME: self.datas_fname,
                self.RES_ID: self.res_id,
                self.RES_MODEL: self.res_model,
                self.DATAS: self.datas,
                self.MIMETYPE: self.mimetype,
            }

        @staticmethod
        def from_json(_json):
            return Odoo.Attachment(
                _json[Odoo.Attachment.NAME],
                _json[Odoo.Attachment.DATAS],
                _json[Odoo.Attachment.DATAS_FNAME],
                _json[Odoo.Attachment.RES_MODEL],
                _json[Odoo.Attachment.RES_ID],
                _json[Odoo.Attachment.TYPE] if Odoo.Attachment.TYPE in _json else Odoo.Attachment.DEFAULT_DATATYPE,
                _json[
                    Odoo.Attachment.MIMETYPE] if Odoo.Attachment.MIMETYPE in _json else Odoo.Attachment.DEFAULT_MIMETYPE
            )
