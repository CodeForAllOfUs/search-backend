def fill_auxiliary(manager, field, json, json_key):
    """
    gather all categories/tags, then fill the database with any new ones
    """
    saved = set(getattr(o, field) for o in manager.objects.all())
    unsaved = set()

    for obj in json:
        unsaved.update(obj[json_key])

    # get a set of all models not yet saved
    unsaved = unsaved - saved

    # create new models and save them
    for name in unsaved:
        model = manager()
        setattr(model, field, name)
        model.save()

def fill_models(manager, pk, json, attrs):
    """
    create/update all models with the appropriate fields
    """
    for obj in json:
        try:
            model = manager.objects.get(pk=obj[pk])
        except:
            model = manager()

        normal_attrs = []
        default_attrs = []
        foreign_key_attrs = []
        many_to_many_attrs = []

        # update properties
        for attr in attrs:
            if isinstance(attr, str):
                normal_attrs.append(attr)

            if isinstance(attr, dict):
                if 'default' in attr:
                    default_attrs.append(attr)
                elif 'foreign_key' in attr:
                    foreign_key_attrs.append(attr)
                elif 'many_to_many' in attr:
                    many_to_many_attrs.append(attr)

        for attr in normal_attrs:
            setattr(model, attr, obj[attr])

        for attr in default_attrs:
            setattr(model, attr['name'], obj.get(attr['name'], attr['default']))

        for attr in foreign_key_attrs:
            name = attr['name']
            json_key = attr['json_key']
            foreign_manager = attr['manager']
            if obj[json_key]:
                setattr(model, name, foreign_manager.objects.get(pk=obj[json_key]))

        # save model before we start modifying its ManyToManyFields
        # ref: https://docs.djangoproject.com/en/1.8/topics/db/examples/many_to_many/
        model.save()

        # map the foreign table by the given field
        for attr in many_to_many_attrs:
            name = attr['name']
            foreign_manager = attr['manager']
            field = attr['map_field']
            foreign_set = getattr(model, name)
            # set up reverse lookup for foreign objects so that
            # we can get the foreign object by its key in the json array
            foreign_objs = {getattr(o, field): o for o in foreign_manager.objects.all()}
            foreign_set.add(*(foreign_objs[key] for key in obj[name]))
