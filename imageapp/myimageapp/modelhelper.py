# here all useful helper functions will be added

from myimageapp.models import *
# from myimageapp.modelhelper2 import *

def initialize_all():
    db.drop_all()
    db.create_all()


def add_record(record):
    db.session.add(record)
    db.session.commit()


def add_many_records(record_list):
    [add_record(record) for record in record_list]


adder_dict = {
    "Users": "add_user", "Images": "add_image"
}

table_list = ["Users", "Images" ]

the_table_names_list = ["users", "images" ]

def add_record_list_of_lists(record_list_of_lists, **kwargs):
    final_table_list = kwargs.get("table_list", table_list)

    for table, record_list in zip(final_table_list, record_list_of_lists):
        exec(f'[{adder_dict[table]}(*record) for record in {record_list}]')


def add_user(user_name, password):
    add_record(Users(user_name=user_name, password=password))


def add_image(user_id, image_name):
    add_record(Images(user_id=user_id, image_name=image_name))
