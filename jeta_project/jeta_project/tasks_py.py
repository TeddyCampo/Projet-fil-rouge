from invoke import task
import os
import sys
import django


def django_setup():
    sys.path.append(os.path.join(os.curdir, 'Pack2Go'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pack2Go.settings")
    django.setup()


@task
def importtable(ctx, file_name):
    '''
    Import table data from json file providing the file name, it will fill respectively item and category table
    Ex: $invoke importtable file_name
    '''
    django_setup()

    from check.models import Items, Category

    import json
    i = 0
    with open(os.path.join('data', file_name + '.json'), 'r') as json_data:
        file = json.load(json_data)
    for key, value in file.items():
        for obj_list in value:
            for key, value in obj_list.items():
                if key == 'key':
                    category = value
                    category = Category(name=value)
                    category.save()
                    print('\nNEW CATEGORY ->', category)
                elif key == 'data':
                    for raw_data in value:
                        for key, value in raw_data.items():
                            if key == 'key':
                                item=Items(name=value, category=category)
                                item.save()
                                i = i + 1
                                print(i,'- NEW ITEM ->', item)