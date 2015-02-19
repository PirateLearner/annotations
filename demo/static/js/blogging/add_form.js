function updateElementIndex(el, prefix, ndx) {
	var id_regex = new RegExp('(' + prefix + '-\\d+)');
	var replacement = prefix + '-' + ndx;
	if ($(el).attr("for"))
	{
		$(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
		console.log($(el).attr("for"))
	}
	
	if (el.id)
	{
		el.id = el.id.replace(id_regex, replacement);
		console.log(el.id)
	}
		
	if (el.name)
	{
		el.name = el.name.replace(id_regex, replacement);
		console.log(el.name)
	}
		
}

function addForm(btn, prefix) {
	var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
	var row = $('.dynamic-form:first').clone(true).get(0);
	$(row).attr('id','form-'+formCount+'-row').insertAfter($('.dynamic-form:last')).children(
			'.hidden').removeClass('hidden');
	console.log($(row).find('[id*="_form-0-"]'));
	$(row).find('[id*="_form-0-"]').each(function (){
		 updateElementIndex(this,prefix,formCount);	
		});
	$(row).find('[for*="_form-0-"]').each(function (){
		 updateElementIndex(this,prefix,formCount);	
		});
	
	
//	$(row).children().not(':last').children().each(function() {
//		updateElementIndex(this, prefix, formCount);
//		$(this).val('');
//	});
	$(row).find('.delete-row').click(function() {
		deleteForm(this, prefix);
	});
	$('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
	return false;
}

function deleteForm(btn, prefix) {
	$(btn).parents('.dynamic-form').remove();
	var forms = $('.dynamic-form');
	$('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
	for (var i = 0, formCount = forms.length; i < formCount; i++) {
		$(forms.get(i)).children().not(':last').children().each(function() {
			updateElementIndex(this, prefix, i);
		});
	}
	return false;
}