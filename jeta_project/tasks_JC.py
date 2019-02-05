from invoke import task
import os
import sys
import django


def django_setup():
   sys.path.append(os.path.join(os.curdir, 'server'))
   os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
   django.setup()


@task
def importtable(ctx, table_name):
   '''
   Import table data from csv file
   Ex: $ inv importtable nutrition_source
   '''
   django_setup()

   from nutrition.models import Source, Food, FoodPortion, Nutrient, NutData

   models = {
       "nutrition_source": Source,
       "nutrition_food": Food,
       "nutrition_foodportion": FoodPortion,
       "nutrition_nutrient": Nutrient,
       "nutrition_nutdata": NutData,
   }
   model = models[table_name]
   with open(os.path.join('server/data', table_name + '.csv'), 'r') as file:
      is_header = True
      for line in file:
         fields = [field.strip(' \n "') for field in line.split('|')]
         if is_header:
            # first line contains headers - that is attribute names
            field_names = fields
            is_header = False
         else:
            # create default model instance, with the id given in .csv file to maintain relationships between models
            object = model(pk=fields[0])
            # populate object attributes one by one with the attribute names collected before
            for field_index, field_name in enumerate(field_names):
               if field_index > 0:
                  # skip id field, which is already provided
                  value = fields[field_index]
                  if type(model._meta.local_fields[field_index]).__name__ == 'BooleanField':
                     if value == 'false':
                        # some boolean values need to be normalized
                        value = False
                  setattr(object, field_name, value)
            object.save()
            print(object)
