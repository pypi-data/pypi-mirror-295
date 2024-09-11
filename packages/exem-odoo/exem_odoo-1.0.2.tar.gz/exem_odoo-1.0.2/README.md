# Odoo

Query and send data on a Odoo server.

## Getting started

Create your Odoo instance with:

    odoo = Odoo()

Connect to your Odoo with your *url*, *database name*, *user*, *password* with:

    odoo.connect({ 
        Odoo.URL: "your url", 
        Odoo.DB_NAME: "your db", 
        Odoo.USER: "your user", 
        Odoo.PASSWORD: "your password" 
    })

And query your data with:

    get_ids(module, filters, *args)
    get_ids_count(module, filters)
    get_fields(module, ids, fields, *args)
    get_fields_name(module)
    set_fields(module, ids, values)
    create(module, values)
    delete_field(module, ids)
    create_attachment(self,attachment)
    create_attachment_file(module, obj_id, file_name, file_path)
    get_fields_by_conditions(module, filters, fields, **args)

 _A **module** is in format "my.module"_

_A **field** is in format ["field_name",]_

_A **filter** is in format [("fields", "condition", "value"),]_

 _An **Attachment** is an inner object of the Odoo class_

More details in [Odoo.py](Odoo.py)

## Set fields

There are many ways to set_fields:

### one2many

    (0, 0,  { values })    link to a new record that needs to be created with the given values dictionary
    (1, ID, { values })    update the linked record with id = ID (write *values* on it)
    (2, ID)                remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)
    (3, ID)                cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)
    (4, ID)                link to existing record with id = ID (adds a relationship)
    (5)                    unlink all (like using (3,ID) for all linked records)
    (6, 0, [IDs])          replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)

Example:

    odoo.set_fields("module", ids, {"the_one2many_field": [(0, 0, {'field_name':field_value_record1, ...}), (6, 0, [78, 3])]})

### many2one

Set the id of the many2one field.

Example:

    odoo.set_fields("module", ids, {"the_many2one_field": 78})

## Attachment

You can use The Odoo.Attachment object to transform your file into an Odoo Attachment.

Example:
    
    my_file = open("my_file_path", "rb")

    attachment = odoo.Attachment()
    attachment.name = "my_file_name"
    attachment.datas = base64.b64encode(my_file.read())
    attachment.datas_fname = "my_file_name"
    attachment.res_model = "module"
    attachment.res_id = module_id_to_attach_to
    attachment.mimetype = "application/pdf"

    odoo.create_attachment(attachment)

## Search conditions

When you query ids or fields by conditions, you can use the following conditions:

    like : [('name', 'like', 'John%')]
    ilike : [('name', 'ilike', 'John%')]
    = : [('product_id', '=', 122)]
    in : [('state', 'in', ('draft', 'done'))]
    < : [('price_unit', '<', 14.50)]
    <= : >[('price_unit', '<=', 14.50)]
    > : [('price_unit', '>', 14.50)]
    >= : [('price_unit', '>=', 14.50)]
    != : [('product_id', '!=', 122)]

Example:

    odoo.get_ids("type.commentaire", [("name", "ilike", ("2023"))])
