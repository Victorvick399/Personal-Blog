from flask import render_template 
from . import main

@main.errorhandler(404)
def four_Ow_four(error):
    '''
    Function to show the 404 error page.
    '''
    return render_template('four_Ow_four.html'),404
    