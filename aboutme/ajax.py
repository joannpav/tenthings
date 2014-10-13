from dajax.core import Dajax
from dajaxice.core import dajaxice_functions
   
def flickr_save(request, new_title):
	dajax = Dajax()
	dajax.script('cancel_edit();')
	dajax.assign('#title','value',new_title)
	dajax.alert('Save complete using "%s"!' % new_title )
	return dajax.json()

dajaxice_functions.register(flickr_save)
