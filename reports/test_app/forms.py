from django import forms

class InputForm(forms.Form):
    """ 
    Fund file form for the admin importer
    """
    sc = forms.CharField()

class IntegerInputForm(forms.Form):
    """ 
    Fund file form for the admin importer
    """
    school_code = forms.IntegerField()
