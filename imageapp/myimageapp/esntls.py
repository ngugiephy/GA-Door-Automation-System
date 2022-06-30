from myimageapp.modelhelper import *

user1 = ["Donatus", "brEad"]
user2 = ["Don", "heAvy"]

user_list = [user1, user2]

image_list = []
custom_table_list = ["Users"]
record_list_of_lists = [user_list]

if __name__ == "__main__":
    initialize_all()
    # add_record_list_of_lists(record_list_of_lists, table_list=custom_table_list)
    # exec(f'[{adder_dict["Admins"]}(*record) for record in {admin_list}]')