
# =====================
# Base Import
# =====================

from rest_framework import serializers

# from support_generic import common_methods
from DbUtils import common_methods


def group_model_set(model_dict):

    model_dict_final = model_dict
    group_dic_ind = common_methods.dict_01()
    group_dic_arr = common_methods.dict_01()

    for key in model_dict:
        if key.isnumeric():
            group_dic_arr[key] = model_dict[key]
        else:
            group_dic_ind[key] = model_dict[key]

    if len(group_dic_arr) >0:
        if len(group_dic_ind) >0:
            for key_group_dic_arr in group_dic_arr:
                val_each = group_dic_arr[key_group_dic_arr]
                val_each.update(group_dic_ind)
                val_m = val_each
                group_dic_arr[key_group_dic_arr] = val_each
            return group_dic_arr
        else:
            return group_dic_arr
    else:
        return group_dic_ind


def getSerializerCleanData(form_data):

    parent_dic = common_methods.dict_01()

    for key in form_data:


        field_value = form_data[key]

        print("field_value testt001")

        print(key)
        print(field_value)

        key_child_index = "-1"

        # checkinf if multiple value set with eg "___1, etc., is there"
        # and if exist making value set as array of values

        key_root = key.split("___");

        print(key_root)

        if len(key_root) > 1:
            key = key_root[0]
            key_child_index = key_root[1]

        split = key.split("__");

        model_name = split[0]
        field_name = split[1]

        parent_dic = get_create_dict(parent_dic, model_name, field_name, field_value, key_child_index)

    for model_key in parent_dic:
        # print("model_key")
        # print(model_key)
        parent_dic[model_key] = group_model_set(parent_dic[model_key])

    return parent_dic;

def get_create_dict(parent_dic, key, child_key, child_value, data_array_index):

    # print("ccc")
    # print(parent_dic)
    # print(key)
    # print(child_key)
    # print(child_value)
    # print(data_array_index)
    # print("===========\n=========")

    if key in parent_dic.keys():
        # print("key exist"+key)
        field_dic =  parent_dic[key]
    else:
        field_dic = common_methods.dict_01()

    if data_array_index == "-1":
        field_dic.add(child_key, child_value)
        parent_dic.add(key, field_dic)
    else:

        if data_array_index in field_dic.keys():
            # print("key exist"+key)
            field_dic_item =  field_dic[data_array_index]
        else:
            field_dic_item = common_methods.dict_01()

        field_dic_item.add(child_key, child_value)
        field_dic.add(data_array_index, field_dic_item)
        parent_dic.add(key, field_dic)
    # for model_key in parent_dic:
    #     print("model_key")
    #     print(model_key)
    #     model_dic[model_key] = group_model_set(model_dic[model_key])
    return parent_dic


def getSerilalierField(serializer_obj,field_arr, model ,form_fields ):

    for field_name, field_obj in serializer_obj.get_fields().items():

        # print(field_name)
        if 'Serializer' in field_obj.__class__.__name__ and field_obj.__class__.__name__ != 'SerializerMethodField':
            field_arr=getSerilalierField(field_obj, field_arr, field_obj.__class__.__name__, form_fields)
        else:
            # print("camesssa")
            name_final = model.replace("ModelSerializer", "Model")+"__"+field_name
            # name_final = name_final.replace("SerializerModel__", "Model__")
            print(name_final)
            if name_final in form_fields:
                each_obj ={}
                # each_obj['model'] = model
                each_obj['cn'] = name_final
                each_obj['dt'] = field_obj.help_text
                each_obj['dt_r'] = field_obj.__class__.__name__
                each_obj['required'] = field_obj.required
                if hasattr(field_obj, 'verbose_name'):
                    each_obj['lb'] = field_obj.verbose_name
                else:
                    v_name = field_name.replace("_"," ")
                    each_obj['lb'] = v_name

                if hasattr(field_obj, 'choices'):
                   each_obj['choices'] = field_obj.choices
                   # each_obj['dt'] = 'MOD_DT_CHOICES'
                # if hasattr(field_obj, 'label'):
                #    each_obj['lb'] = field_obj.label
                field_arr.append(each_obj)
    return field_arr;



# Get serializer using model dynamically
def getGenericSerializer(model_arg):
    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_arg
            fields = '__all__'

    return GenericSerializer


def getGenericSerializerFieldSet(model_arg, field_set):
    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_arg
            fields = field_set

    return GenericSerializer


def getGenericSerializerFieldSet2(model_arg, field_set):

    class GenericSerializer(serializers.ModelSerializer):

        dataset = serializers.SerializerMethodField()

        class Meta:
            model = model_arg
            fields = ["dataset"]

        def get_dataset(self, obj):
            dataset = {}
            dataset["slug"] = obj.slug
            for e_key in field_set:
                e_key_splits = e_key.split(".")
                key_l = len(e_key_splits)

                temp_obj = obj
                for i in range(key_l):
                    e_key_spl = e_key_splits[i]
                    temp_obj = getattr(temp_obj, e_key_spl)
                dataset[e_key] = temp_obj
            return dataset


    return GenericSerializer


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
