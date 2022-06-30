from .models import *
from flask_dt import get_class_by_tablename
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


def fetch_drop_down_data(column_list_dict_given):
    column_list = list(column_list_dict_given.keys())        
    final_dict = {}

    for column in column_list:
        table_class = None

        if not column_list_dict_given[column][-1]:
            exec(f"final_dict['{column}'] = []")
            continue
        
        if column_list_dict_given[column][0][1] == "provided":
            exec(f"final_dict['{column}'] = column_list_dict_given[column][0][2]")

        if column_list_dict_given[column][-1]:
            table_class = get_class_by_tablename(column_list_dict_given[column][0][1], db)

        if table_class:
            exec(f"final_dict['{column}'] = [the_data[0] for the_data in db.session.query(table_class.{column_list_dict_given[column][0][2]}).all()]")
            # exec(f"final_dict[{column}'] = db.session.query({table_class}.{column_list_dict_given[column][0][2]}).all()")
        
        if column_list_dict_given[column][0][1] == "date_time":
            exec(f"final_dict['{column}'] = [(datetime.datetime.now().replace(microsecond=0) - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]")                
    
    return final_dict


